# Guest Reservation Policies — Storyblok build notes

**Prototype:** `/policies` (policies.html) — a faithful, on-brand duplicate of
policies.staysentral.com (currently a Coassemble-style lesson portal). Content
is verbatim from the three lessons; the gold CTAs carry the portal's real
destinations.

| Portal lesson | Prototype section | CTA |
|---|---|---|
| Manage Reservation | `#manage` | LOOKUP NOW → https://reservations.sentral.com/login (new tab) |
| Cancellation and Payment Policy | `#cancellation` | — (three verbatim tiers: ≤29 nights · advance purchase · 30+ nights) |
| General Reservation Policies | `#general` | VIEW TERMS → /reservation-policies |

**Storyblok model**
- One `PolicyPage` story (`/policies`): `title`, `intro`, body = list of
  nestable **`PolicySection`** bloks: `{ anchor, title, rich_text, cta_label?,
  cta_url?, cta_new_tab? }`. Marketing owns all copy.
- The reservation-lookup URL belongs in the global `Config` story (it will
  change if the guest portal moves off reservations.sentral.com).
- `/reservation-policies` (the fuller operational page) shares the same
  `PolicySection` blok — one component serves both pages.

**Launch notes**
- Redirect `policies.staysentral.com/*` → `sentral.com/policies`. The old
  per-lesson links are hash routes (`#/lessons/<id>`) — fragments never reach
  the server, so individual lessons cannot be redirected; the single
  domain-level redirect is the ceiling.
- The payment/cancellation copy on `/reservation-policies` is synced verbatim
  from the portal (2026-10-08); the two pages must not drift — in Storyblok,
  reference the same section blok from both stories.
