/**
 * GET /api/rates?property=sol-modern
 *
 * Returns the lowest nightly rate per Mews room category for one property, so
 * the STAY property template can show a live "FROM $189/NIGHT" badge on each
 * suite card instead of a hardcoded number.
 *
 * Source: Mews Booking Engine (Distributor) API
 *   POST {base}/api/distributor/v1/hotels/getAvailability
 *   docs.mews.com/booking-engine-guide/booking-engine-api/operations/hotels
 *
 * The Distributor API is the guest-facing surface — Client and ConfigurationId
 * are the same values the public booking widget uses, so there is no secret
 * here. It still runs server-side so we control caching and are not exposed to
 * the Distributor's allowed-origin rules from the browser.
 *
 * ── Configuration ────────────────────────────────────────────────────────────
 * Environment variables on the Vercel project:
 *
 *   MEWS_PROPERTIES   JSON map, slug → { configurationId, hotelId }
 *                     {"sol-modern":{"configurationId":"…","hotelId":"…"}}
 *   MEWS_CLIENT       optional, defaults to "Sentral Website 1.0.0"
 *   MEWS_API_BASE     optional, defaults to https://api.mews.com
 *                     (use https://api.mews-demo.com against the demo estate)
 *
 * Adding a property is an env change, not a code change.
 *
 * ── "From" price heuristic ───────────────────────────────────────────────────
 * A true lowest-available-rate would mean one call per night across the booking
 * window. Instead we probe four representative one-night stays (+7, +14, +30 and
 * +60 days) and take the minimum per category. That is what the badge claims —
 * an indicative starting rate, not a quote — and it costs four upstream calls
 * per hour per property rather than sixty.
 *
 * If the number needs to be exact, this is the function to change; nothing on
 * the page assumes the heuristic.
 */

const PROBE_OFFSETS_DAYS = [7, 14, 30, 60];
// Extended-stay probe: Sentral's differentiator is that rates drop past 30
// nights, so we ask Mews what a 30-night stay actually costs per night rather
// than asserting a discount the page cannot back up.
const EXTENDED_STAY_NIGHTS = 30;
const EXTENDED_STAY_OFFSET_DAYS = 14;
const DEFAULT_CLIENT = 'Sentral Website 1.0.0';
const DEFAULT_BASE = 'https://api.mews.com';

function isoDay(offsetDays) {
  const d = new Date();
  d.setUTCHours(0, 0, 0, 0);
  d.setUTCDate(d.getUTCDate() + offsetDays);
  return d.toISOString();
}

function loadProperties() {
  const raw = process.env.MEWS_PROPERTIES;
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/**
 * Pull the per-night amount out of one Pricing entry. Mews returns multi-currency
 * amounts; we take the requested currency if present, otherwise the first one.
 */
function nightlyAmount(pricing, currencyCode) {
  const avg = pricing?.Price?.AverageAmountPerTimeUnit;
  if (!avg) return null;

  // Multi-currency shape: { Currency, GrossValue, NetValue, ... } or
  // { Currencies: [{ Currency, GrossValue }, …] } depending on estate config.
  const candidates = Array.isArray(avg.Currencies) ? avg.Currencies : [avg];
  const match =
    candidates.find((c) => c && c.Currency === currencyCode) || candidates[0];
  if (!match) return null;

  const value = match.GrossValue ?? match.Value ?? match.NetValue;
  return typeof value === 'number' && value > 0
    ? { amount: value, currency: match.Currency || currencyCode || null }
    : null;
}

async function probe({ base, client, configurationId, hotelId, currencyCode, offset, nights = 1 }) {
  const res = await fetch(`${base}/api/distributor/v1/hotels/getAvailability`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      Client: client,
      ConfigurationId: configurationId,
      HotelId: hotelId,
      StartUtc: isoDay(offset),
      EndUtc: isoDay(offset + nights),
      ...(currencyCode ? { CurrencyCode: currencyCode } : {}),
    }),
  });

  if (!res.ok) {
    throw new Error(`mews ${res.status} on +${offset}d/${nights}n`);
  }
  return res.json();
}

/** Lowest per-night amount across every category in one getAvailability payload. */
function lowestNightly(payload, currencyCode) {
  let low = null;
  for (const cat of payload?.RoomCategoryAvailabilities || []) {
    if (!(cat?.AvailableRoomCount > 0)) continue;
    for (const occ of cat.RoomOccupancyAvailabilities || []) {
      for (const pricing of occ?.Pricing || []) {
        const n = nightlyAmount(pricing, currencyCode);
        if (n && (!low || n.amount < low.amount)) low = n;
      }
    }
  }
  return low;
}

export default async function handler(req, res) {
  const slug = String(req.query?.property || '').trim();
  const currencyCode = (req.query?.currency || 'USD').toString().toUpperCase();

  if (!slug) {
    res.status(400).json({ error: 'missing_property' });
    return;
  }

  const properties = loadProperties();
  const config = properties?.[slug];

  // Not configured yet is a normal state, not a failure: the page hides its
  // rate badges rather than showing a stale or invented price.
  if (!config?.configurationId || !config?.hotelId) {
    res.setHeader('Cache-Control', 'public, s-maxage=60');
    res.status(200).json({ property: slug, configured: false, categories: {}, extended: null });
    return;
  }

  const base = (process.env.MEWS_API_BASE || DEFAULT_BASE).replace(/\/+$/, '');
  const client = process.env.MEWS_CLIENT || DEFAULT_CLIENT;

  try {
    const shared = {
      base,
      client,
      configurationId: config.configurationId,
      hotelId: config.hotelId,
      currencyCode,
    };

    const [results, extendedResult] = await Promise.all([
      Promise.allSettled(PROBE_OFFSETS_DAYS.map((offset) => probe({ ...shared, offset }))),
      Promise.allSettled([
        probe({ ...shared, offset: EXTENDED_STAY_OFFSET_DAYS, nights: EXTENDED_STAY_NIGHTS }),
      ]).then((r) => r[0]),
    ]);

    const ok = results.filter((r) => r.status === 'fulfilled').map((r) => r.value);
    if (!ok.length) {
      const why = results[0]?.reason?.message || 'all probes failed';
      throw new Error(why);
    }

    /** @type {Record<string, {from:number, currency:string|null}>} */
    const categories = {};

    for (const payload of ok) {
      for (const cat of payload?.RoomCategoryAvailabilities || []) {
        const id = cat?.RoomCategoryId;
        if (!id || !(cat.AvailableRoomCount > 0)) continue;

        for (const occ of cat.RoomOccupancyAvailabilities || []) {
          for (const pricing of occ?.Pricing || []) {
            const nightly = nightlyAmount(pricing, currencyCode);
            if (!nightly) continue;
            if (!categories[id] || nightly.amount < categories[id].from) {
              categories[id] = { from: nightly.amount, currency: nightly.currency };
            }
          }
        }
      }
    }

    // Extended stay. Only reported when it genuinely beats the nightly rate —
    // if Mews returns no discount, the page says nothing rather than claiming one.
    let extended = null;
    if (extendedResult?.status === 'fulfilled') {
      const low = lowestNightly(extendedResult.value, currencyCode);
      const nightlyFloor = Object.values(categories).reduce(
        (min, c) => (min === null || c.from < min ? c.from : min),
        null
      );
      if (low && nightlyFloor && low.amount < nightlyFloor) {
        extended = {
          nights: EXTENDED_STAY_NIGHTS,
          from: low.amount,
          currency: low.currency,
          savingsPercent: Math.round(((nightlyFloor - low.amount) / nightlyFloor) * 100),
        };
      }
    }

    // Rates move slowly enough that an hour of edge cache is invisible to a
    // guest and saves five upstream calls per request.
    res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
    res.status(200).json({
      property: slug,
      configured: true,
      currency: currencyCode,
      partial: ok.length < PROBE_OFFSETS_DAYS.length,
      updatedAt: new Date().toISOString(),
      categories,
      extended,
    });
  } catch (err) {
    // Never fall back to a hardcoded price — the page hides the badges instead.
    res.setHeader('Cache-Control', 'public, s-maxage=60');
    res.status(200).json({
      property: slug,
      configured: true,
      error: 'upstream_unavailable',
      detail: String(err.message || err),
      categories: {},
      extended: null,
    });
  }
}
