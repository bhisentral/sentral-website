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
| Room types | Not shown anywhere | Suite grid with sleeps / sq ft / bed |
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
| 5 | Suites | off-black | Full-bleed grid, 3–6 cards; per-card photo carousel; specs incl. beds + baths; gold CHECK RATES CTA |
| 5b | Offers | cream-light | **The CMS promo slot** — 3 offer cards, marketing-owned copy (Laurie 9-25) |
| 6 | Story block 01 — Stay | cream | Inside the suites. One CTA |
| 6b | Amenity showcase 02 — Gather | cream-warm | 4–6 photo tiles: pool, fitness, coworking, lounges |
| 6c | Story block 03 — Neighborhood | cream | One CTA |
| 7 | Booking band | slate | StayNTouch booking engine + direct-book perks |
| 8 | Neighborhood | cream-warm | Map + 5–7 places with walk times |
| 8b | Food + Drink | cream | 3 in-building/nearby venues per property — sells the location, matters to owners (Laurie 9-25) |
| 8c | Gather | ink | The group/events offer from the current stay pages, verbatim; INQUIRE → Group Travel RFP (Laurie 9-25) |
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
| `snt_booking_url` | — | StayNTouch booking-engine link for this property |

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
`photo` · `name` · `sleeps` · `sq_ft` · `bed_config` · `snt_room_type_id`

There is no `from_rate` field — the rate badge is live. See §5.

Each card carries two explicit actions:

- **BOOK THIS SUITE** pre-selects that suite in *both* booking forms, scrolls to
  the booking band, and focuses Check-in. The two forms share a `Suite` field for
  exactly this reason — a guest who picks Two Bedroom should not pick it twice.
  The card photo is a shortcut to the same thing.
- **FLOOR PLAN** opens the plan in the lightbox. Until a plan is uploaded it says
  so plainly rather than rendering a broken image.

Cards are `<article>`, not `<a>` — two jobs, and a link inside a link is invalid.

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
| Gallery photo | 1600×1067 | **20+ per property**, split across Suites / Amenities / Neighborhood |
| Floor plan | SVG preferred, else 1600×1200 PNG | One per suite type |
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

**Booking/rates platform decision (2026-09-10): Sentral is staying on its
current RMS, StayNTouch. The earlier Mews rates adapter (`api/rates.mjs`) has
been removed** — the Mews integration is not moving forward.

The page-side contract is unchanged and platform-agnostic:

```
suite card  →  /api/rates?property=<slug>  →  StayNTouch RMS (adapter to build)
```

The adapter should return `{currency, categories:{<snt_room_type_id>:{from}},
extended:{from,nights,savingsPercent}}`; the page fills each
`.pt-suite-badge[data-rate-category]` and unhides it. Each suite card carries
its `snt_room_type_id` — the badge is keyed on it.

**Failure behaviour — deliberate.** No rate, sold out, upstream down, or not yet
built all produce the same result: the badge stays hidden and the card renders
without it. There is no hardcoded fallback anywhere in the path, because a stale
price on a booking page is worse than no price.

**Extended stay.** The `extended` value drives the Longer Stays band: *"$139 a
night on stays of 30 nights or more — about 26% below the nightly rate."* If the
RMS shows no discount, the line stays hidden — the page never claims a saving it
cannot show.

**`?demoRates=1`** renders sample numbers labelled `SAMPLE — FROM $189/NIGHT`,
plus a sample extended-stay line, for design review. Opt-in per URL, never on a
normal load.

Because the Distributor API is the same guest-facing surface the booking widget
uses, `Client` and `ConfigurationId` are not secrets. The call still runs
server-side so we own the caching and are not subject to allowed-origin rules
from the browser.

---

## 5b. Gallery and floor plans

One lightbox serves both, so neither costs the page a section:

- **Gallery** opens from a `View gallery` button in the hero, or from any amenity
  tile (which opens it pre-filtered to Amenities). Filters are All / Suites /
  Amenities / Neighborhood, driven by the `#ptGalleryData` JSON manifest — at
  build that comes from the CMS instead of being inlined.
- **Floor plans** open from each suite card.

Focus is trapped while open, Escape closes, and focus returns to whatever opened
it. Missing photography or an un-uploaded plan produces an honest message, never
a broken image.

**This is the template's biggest remaining dependency.** Twenty-plus photos and a
plan per suite type, per property. The demo reuses the same handful of `/assets/`
images across all three groups.

---

## 6. One deliberate difference from the other pages

On every other page, nav **BOOK A STAY** opens the cross-property booking strip
(`overrides.css` §9e). On a property page the property is already known, so it
scrolls to that property's own booking band instead. The nav looks identical.

**This needs an owner decision** — the alternative is keeping the strip and
pre-selecting the property in its "Where" field.

---

## 6b. SEO — anchors + structured data (marketing request, 2026-09-10)

Every section carries a stable, human-readable anchor id — `#the-property`,
`#suites`, `#inside-the-suites`, `#amenity-spaces`, `#roosevelt-row`,
`#book-stay`, `#amenities`, `#neighborhood`, `#longer-stays`, `#info` — usable
in campaign links, sitelinks, and on-page search. `section[id]` gets
`scroll-margin-top` so targets clear the sticky bar. The head carries a
schema.org **Hotel** JSON-LD block (name, address, phone, check-in/out,
amenityFeature, HotelRoom entries with real occupancy and sq ft) — facts only,
no rates. Per property, the JSON-LD is generated from the same §3 fields.
Copy facts (suite mix/specs, 19-amenity list, PHX Arena naming) reconciled
against the live sentral.com/phoenix/sol-modern/stay page 2026-09-10.

## 6c. Laurie review round (2026-09-25) — applied

Suite-card photo carousels (arrows + dots, [FIELD] photo sets); suite CTA is a
gold CHECK RATES button; "Pick your footprint" → **"Choose your apartment-sized
room."**; story block 02 eyebrow → **Notable Amenities**; Offers, Food + Drink,
and Gather sections restored (copy verbatim from live pages — all
marketing-editable in Storyblok at build); intro section carries two photos;
suite specs show beds + baths. Pending from Laurie: one cross-sell comment.

## 7. Open items

1. **Rates.** StayNTouch adapter for `/api/rates` to build (see §5 — the Mews
   version was removed 2026-09-10). Until then rate badges stay hidden;
   `?demoRates=1` shows labelled sample numbers for review.
2. **Suite detail pages.** Cards book directly; floor-plan buttons were removed
   2026-09-25 (several plans per suite type — a single drawing set a false
   expectation). Spec-only cards may be enough. Phase 2b question: does each suite type still need its own page?
3. **Booking hand-off.** Even wired, Check Rates passes the guest to the
   StayNTouch booking engine without ever showing availability or a total. "No hidden fees" is
   promised but no total is displayed. Worth deciding whether an inline
   availability/total step is in scope.
4. **Reviews.** The current Michigan Avenue page has "PEOPLE LIKE IT HERE"; this
   template has no social proof at all.
5. **URL shape.** Demo is at `/property-template`. Live pages are
   `/{city}/{property}` today. `vercel.json` adds `/stay/sol-modern` as a
   demonstration of the intended shape — confirm before the build.
6. **Which properties get this.** All STAY properties, or STAY-only ones
   first? Mixed-use buildings (Live + Stay) may need a variant.
7. **Photography.** The template is only as good as the assets — see §5b. Per
   property: a hero, 2 story images, 4–6 amenity tiles, one photo and one floor
   plan per suite type, and 20+ gallery photos.
