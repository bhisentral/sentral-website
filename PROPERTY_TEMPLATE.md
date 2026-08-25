# STAY Property Template — Phase 2

**File:** `property-template.html` · **Demo property:** Sol Modern, Phoenix
**Status:** design proposal, branch `feat/stay-property-template`, preview-deployed
**Companion to:** `STYLE_GUIDE.md` (v4 Slate), `WP_HANDOFF.md`, `ADA_BRIEF.md`

One template, every STAY property. Drop in the fields listed in §3 and the page
is done — no per-property layout work.

---

## 1. What's wrong with the property pages today

Measured against `sentral.com/chicago/michigan-avenue` and
`sentral.com/phoenix/sol-modern`:

| Problem | Today | Here |
|---|---|---|
| Amenity dump | 28 items listed inline, flat, unranked | 7 icons in a glance strip; all 28 behind one disclosure |
| Amenity essays | 4 paragraph blocks before anything actionable | 3 story blocks, one CTA each, further down |
| Booking | No booking widget on the page at all | Booking card in the hero + a booking band + a sticky bar |
| Room types | Not shown anywhere | 4-card suite grid with sleeps / sq ft / bed |
| Practical info | Missing (check-in, parking, pets, fees, accessibility) | Collapsed accordion at the bottom |
| Neighborhood | Generic city-guide paragraph | 6 named places with walk times |
| Page identity | Reads like a leasing page | Reads like an aparthotel — which is what STAY sells |

The reference set is 1 Hotels and Ace: photography carries the page, copy is
short, and the guest can book from anywhere on it.

---

## 2. Section order — fixed for every property

| # | Section | Surface | Purpose |
|---|---|---|---|
| 1 | Hero | off-black photo/video | Name, city, one sentence, address, booking card |
| 2 | Sticky book bar | ink | Appears past the hero. Name + jump links + CHECK RATES |
| 3 | At a glance | cream-light | 7 attributes, then `ALL N AMENITIES +` disclosure |
| 4 | Intro | cream | Two paragraphs and three stats. Nothing else |
| 5 | Suites | off-black | Full-bleed grid, 3–6 cards |
| 6 | Story block 01 — Stay | cream | Inside the suites. One CTA |
| 6b | Amenity showcase 02 — Gather | cream-warm | 4–6 photo tiles: pool, fitness, coworking, lounges |
| 6c | Story block 03 — Neighborhood | cream | One CTA |
| 7 | Booking band | slate | Mews widget + direct-book perks |
| 8 | Neighborhood | cream-warm | Map + 5–7 places with walk times |
| 9 | Longer stays | ink | Business Travel · Group Travel · Live With Us |
| 10 | Practical info | cream-light | Collapsed accordion + property contact card |

This follows the STYLE_GUIDE §4 section rhythm: dark hero → cream body →
full-slate CTA band → ink → off-black footer. Nav and footer are the global
components, unchanged.

**Three sections do not vary.** Order, surface alternation, and the position of
the booking band are the same on every property page. Only the content changes.

---

## 3. Content model — what each property supplies

Every `[FIELD]` marker in the HTML maps to one of these.

### Identity
| Field | Example | Notes |
|---|---|---|
| `name` | Sol Modern | Hero H1, sticky bar, booking band, contact card |
| `city`, `state` | Phoenix, Arizona | Hero eyebrow, breadcrumb, sticky bar |
| `address` | 50 E. Fillmore Street, Phoenix, AZ 85004 | Hero, booking band, contact card |
| `phone` | (833) 370-4161 | Contact card |
| `maps_url` | Google Maps link | Get Directions |
| `mews_config_id` | — | Booking widget |

### Copy — the hard cap is the point
| Field | Cap | Where |
|---|---|---|
| `positioning` | 2 sentences | Hero subtitle |
| `intro` | 2 paragraphs, ≤ 60 words each | Intro |
| `intro_stats` | 3 stats | Intro right column |
| `story[1..3].head` + `.body` | 1 line + 2 sentences | Story blocks |

Copy longer than the cap gets cut, not shrunk. If a property "needs" a fourth
story block, the answer is that one of the three is not earning its place.

### Suites — 3 to 6 cards
`photo` · `name` · `sleeps` · `sq_ft` · `bed_config` · `mews_room_category_id` · `link`

There is no `from_rate` field — the rate badge is live. See §5.

Clicking a suite card pre-selects that suite in **both** booking forms, scrolls
to the booking band, and focuses Check-in. The two forms carry the same `Suite`
field for exactly this reason — a guest who picks Two Bedroom should not have to
pick it again.

### Amenities — shown three ways, deliberately
- `glance[7]` — the seven that decide a booking. Icon + label, up top.
- `spaces[4..6]` — **photo tiles** in the §6b showcase. Lead with pool and
  fitness; these are what sell an extended stay, so they get shown rather than
  listed. Photo 1200×900 + a short chip label.
- `all` — the full list behind the disclosure, grouped **In your suite** /
  **Around the building** / **Building & access**. Any length.

### Neighborhood
- `map` — static image, or a Leaflet mount matching `live-with-us.html`
- `poi[5..7]` — `name` · `kind` · `distance` ("4 min walk", "12 min drive")

### Practical info — six accordions, all six on every property
Check-in & check-out · Parking & getting here · Pets · Fees, deposits &
cancellation · Accessibility · House rules

Blank is not an option. A property with no parking says so.

### Assets
| Slot | Size | Notes |
|---|---|---|
| Hero | 1920×1080 mp4 (muted loop) or 2400×1350 still | Poster image required either way |
| Suite card | 1200×1500 | 4:5 |
| Story block | 1600×1200 | 2 per property (01 Stay, 03 Neighborhood) |
| Amenity tile | 1200×900 | 4–6 per property, §6b showcase |
| Map | 1200×900 | |

**The demo page uses stand-in photography** from `/assets/` — Sol Modern's
own hero film, plus other Sentral properties' images in the suite and story
slots. Real property photography replaces all of it.

---

## 4. Brand rules this template follows

- **Booking gold.** `CHECK RATES` on the hero card, the booking band, and the
  sticky bar all use reserved booking gold `#B8924A` with off-black text —
  the §9f rule (owner, Aug 4). `.pt-book-btn` and `.pt-sticky-book` are
  registered in `overrides.css` §9f, not styled locally, so there is one
  source of truth.
- **All caps.** Every interactive label is uppercase per the standing owner
  rule (Jul 2026). New classes are registered in the sitewide all-caps block
  in `overrides.css`, not overridden per page.
- **"Check Rates," never "Check Availability."** Per `CHANGES_2026-08-05.md` §1.
- **Slate is the accent, gold is reserved.** Slate for eyebrows on cream,
  italic emphasis, and the CTA band. Slate-light for italic on dark. Oat for
  eyebrows on dark. Gold appears only on booking CTAs and SentralPlus.
- **Dark `<select>` elements declare explicit `option` / `optgroup` colors** —
  required for Windows Chrome per `CHANGES_2026-08-05.md` §3. Both booking
  forms do.
- **Accessibility:** skip link, `scroll-margin-top` on every jump target so
  anchors clear the nav and sticky bar, labelled inputs, a pausable hero video
  that respects `prefers-reduced-motion`, and a native `<details>` accordion.

---

## 5. Live rates

Suite-card badges read live from Mews. Nothing about a price is hardcoded.

```
suite card  →  /api/rates?property=<slug>  →  Mews Booking Engine API
                                              POST /api/distributor/v1/hotels/getAvailability
```

`api/rates.mjs` returns the lowest nightly rate per Mews room category. The page
fills each `.pt-suite-badge[data-rate-category]` and unhides it.

**Configuration** — Vercel env vars, no code change to add a property:

| Var | Value |
|---|---|
| `MEWS_PROPERTIES` | `{"sol-modern":{"configurationId":"…","hotelId":"…"}}` |
| `MEWS_CLIENT` | optional, defaults to `Sentral Website 1.0.0` |
| `MEWS_API_BASE` | optional, defaults to `https://api.mews.com` |

Each suite card also needs its `mews_room_category_id` — the badge is keyed on it.

**The "from" price is a heuristic.** Four one-night probes (+7, +14, +30, +60
days), minimum per category, cached an hour at the edge. That is four upstream
calls per hour per property instead of one per night in the booking window. The
badge claims an indicative starting rate, not a quote. If it needs to be exact,
`PROBE_OFFSETS_DAYS` in `api/rates.mjs` is the only thing to change.

**Failure behaviour — deliberate.** No rate, sold out, upstream down, or not yet
configured all produce the same result: the badge stays hidden and the card
renders without it. There is no hardcoded fallback anywhere in the path, because
a stale price on a booking page is worse than no price. Verified against mocked
Mews responses for all four cases.

**`?demoRates=1`** renders sample numbers labelled `SAMPLE — FROM $189/NIGHT`
for design review. Opt-in per URL, never on a normal load.

Because the Distributor API is the same guest-facing surface the booking widget
uses, `Client` and `ConfigurationId` are not secrets. The call still runs
server-side so we own the caching and are not subject to allowed-origin rules
from the browser.

---

## 6. One deliberate difference from the other pages

On every other page, nav **BOOK A STAY** opens the cross-property booking strip
(`overrides.css` §9e). On a property page the property is already known, so it
scrolls to that property's own booking band instead. The nav looks identical.

**This needs an owner decision** — the alternative is keeping the strip and
pre-selecting the property in its "Where" field.

---

## 7. Open items

1. ~~Rates.~~ **Resolved** — Mews feeds them live. See §5. Still needed before
   the badges appear anywhere: the `MEWS_PROPERTIES` env var and each suite's
   `mews_room_category_id`.
2. **Suite detail pages.** `VIEW SUITE →` currently jumps to the booking band.
   Phase 2b question: does each suite type get its own page?
3. **URL shape.** Demo is at `/property-template`. Live pages are
   `/{city}/{property}` today. `vercel.json` adds `/stay/sol-modern` as a
   demonstration of the intended shape — confirm before the build.
4. **Which properties get this.** All STAY properties, or STAY-only ones
   first? Mixed-use buildings (Live + Stay) may need a variant.
5. **Photography.** The template is only as good as the assets. Every property
   needs a hero, 3 story images, and one image per suite type.
