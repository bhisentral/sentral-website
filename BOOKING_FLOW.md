# STAY Booking Funnel — Phase 3 prototype

**Status:** design prototype, live for review · **Generator:** `scripts/build-booking.py`
(edit the generator + `assets/booking-demo.js`, re-run, commit — never hand-edit the
generated pages) · **Styles:** `booking-chrome.css` (site chrome, extracted at build
from property-template.html) + `booking.css` (funnel components)

Maps to the six-page booking plan (2026-09-25):

| # | Plan page | Prototype | URL | Priority | Data at build |
|---|---|---|---|---|---|
| 1 | Home & Location Selector | `index.html` bookbar reskin | `/` | P1 | Hands property/dates to search; **no PMS call** |
| 1a | City STAY Selector | `city-stay.html` | `/stay/austin` · `/stay/charlotte` · `/stay/los-angeles` · `/stay/miami` | P1 | Routes to the right property's search, dates passed through |
| 2 | Search Availability Results | `book-search.html` | `/book/search` | **P0** | **Live StayNTouch via SentralOS** (pull method TBC w/ Nathan); hosts the multi-room module |
| 3 | Property Page | `property-template.html` (Phase 2) | `/stay/sol-modern` | P2 | Static + CMS promo slot; no live PMS call |
| 4 | Room List & Room Detail | `book-room.html` | `/book/room` | P1 | Live StayNTouch rate plans (direct / advance / sale); map view seam |
| 5 | Booking Details (Checkout) | `book-checkout.html` | `/book/checkout` | P1 | Native guest form; **Shift4 embed unchanged** (prototype renders no card fields by design); property-driven tax lines |
| 6 | Booking Confirmation | `book-confirm.html` | `/book/confirmation` | P2 | Confirmation # + summary from StayNTouch via SentralOS; triggers email + SMS |

**State model:** everything passes in the query string —
`property, city, in, out, adults, children, promo, rooms (slug:qty:plan,…), guest`.
No storage, no session; every page is shareable/refreshable mid-funnel.

**Sample data:** every rate, tax line, and availability flag comes from
`assets/booking-demo.js` and every page carries a "Design prototype — sample rates"
ribbon. Rate plans mirror the live site's offers (Fall Sale −20% / Campus Bound −14% /
Book Direct −10%). Rates **include select fees** (transparent-pricing disclosure —
"Includes Select Fees" opens the Included Fees dialog, wording from the live engine);
tax lines are samples (city 6% + state 6.5%), property-driven at build.

**Known simplifications for review:** one standard room set (Sol Modern's real
studio/1BR/2BR) stands in for every property until per-property room data loads;
rate plans are chosen per suite (mixed-plan stays work); 30+/31+ night properties
warn and block booking under their minimum.

## Laurie round — 2026-10-08

- **Search (step 1):** right-hand stay rail removed. Each suite card carries avg/night,
  stay total ("Excludes taxes · Includes Select Fees") and its own BOOK — pick a rate
  radio, click BOOK once, land on checkout. Rate notes collapse behind "Rate details";
  per-plan avg rates sit at the right edge. Strike-through kept, muted (not red).
  Multi-room: per-card ROOMS stepper for several of one suite; "+ Add another suite" on
  checkout returns to search with the stay carried (strip at top), next BOOK adds to it.
- **Checkout (step 2):** guest form now matches what the live engine captures (name,
  email, phone + country code, address, country, city, state, zip). Shift4 captures
  card data only (number, expiry, CVV, card zip, cardholder) — address stays native.
  Booking details list suite(s) in text (no photo) + rate plan + Modify, check-in 4 PM /
  check-out 11 AM, nights, guests (adults/children); Total Price Details; **Deposit** and
  **Cancellation** policy links (→ /reservation-policies#payment / #cancellation).
- **City selector:** VIEW PROPERTY beside CHECK AVAILABILITY (→ Sol Modern template until
  each property page exists), neighborhood with pin (Inkwell = NoDa, Joinerys = Optimist
  Park; others [FIELD]), one-line suites/amenities [FIELD], Amenities expand/collapse.


**Entry points wired:** home bookbar CHECK RATES → `/book/search` (property+dates);
property-page CHECK RATES (hero + booking band) → `/book/search` with suite
pre-selected; nav BOOK A STAY on funnel pages → `/book/search`.
