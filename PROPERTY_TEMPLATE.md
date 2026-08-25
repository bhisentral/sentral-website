# STAY Property Template — Phase 2

**File:** `property-template.html` · **Demo property:** Sol Modern, Phoenix
**Status:** design proposal, branch `feat/stay-property-template`, not deployed
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
| 6 | Story blocks ×3 | cream / cream-warm alternating | Stay · Gather · Neighborhood. One CTA each |
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
`photo` · `name` · `sleeps` · `sq_ft` · `bed_config` · `from_rate` · `link`

### Amenities
- `glance[7]` — the seven that actually decide a booking. Icon + label.
- `all` — the full list, grouped: **In your suite** / **Around the building** /
  **Building & access**. Any length; it is behind the disclosure.

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
| Story block | 1600×1200 | 3 per property |
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

## 5. One deliberate difference from the other pages

On every other page, nav **BOOK A STAY** opens the cross-property booking strip
(`overrides.css` §9e). On a property page the property is already known, so it
scrolls to that property's own booking band instead. The nav looks identical.

**This needs an owner decision** — the alternative is keeping the strip and
pre-selecting the property in its "Where" field.

---

## 6. Open items

1. **Rates.** Suite cards show `FROM $189/NIGHT`. If Mews cannot feed a live
   from-rate, the badges come off — a stale price is worse than no price.
2. **Suite detail pages.** `VIEW SUITE →` currently jumps to the booking band.
   Phase 2b question: does each suite type get its own page?
3. **URL shape.** Demo is at `/property-template`. Live pages are
   `/{city}/{property}` today. `vercel.json` adds `/stay/sol-modern` as a
   demonstration of the intended shape — confirm before the build.
4. **Which properties get this.** All STAY properties, or STAY-only ones
   first? Mixed-use buildings (Live + Stay) may need a variant.
5. **Photography.** The template is only as good as the assets. Every property
   needs a hero, 3 story images, and one image per suite type.
