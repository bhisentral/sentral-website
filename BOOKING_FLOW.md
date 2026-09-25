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
`property, city, in, out, adults, children, rooms (slug:qty,slug:qty), plan, guest`.
No storage, no session; every page is shareable/refreshable mid-funnel.

**Sample data:** every rate, tax line, and availability flag comes from
`assets/booking-demo.js` and every page carries a "Design prototype — sample rates"
ribbon. Rate plans mirror the live site's offers (Direct / Advance Purchase −20% /
Seasonal Sale −15%). Tax lines: sample 12.5% occupancy + the $0 resort-fee line.

**Known simplifications for review:** one standard room set (Sol Modern's real
studio/1BR/2BR) stands in for every property until per-property room data loads;
a rate plan applies to the whole stay; 30+ night properties warn and block
checkout under 30 nights.

**Entry points wired:** home bookbar CHECK RATES → `/book/search` (property+dates);
property-page CHECK RATES (hero + booking band) → `/book/search` with suite
pre-selected; nav BOOK A STAY on funnel pages → `/book/search`.
