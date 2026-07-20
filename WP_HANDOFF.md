# Sentral Website — WordPress Developer Handoff

**Date:** July 2026 · **Contact:** JCheshire@sentral.com
**Read alongside:** `STYLE_GUIDE.md` (canonical design system, v4 Slate), `ADA_BRIEF.md`
(accessibility spec), `README.txt` (file map), `Sentral_WP_Developer_Brief.docx` (original brief).

This document is the **entry point**: what the prototype source now guarantees, what the
WordPress theme must still do, and exactly where the remaining work lives.

---

## 1. What you're building from

Twelve self-contained HTML pages in the repo root — one per launch page, each with its
design tokens inline in `:root{}` — plus `overrides.css`, loaded last on every page.

| Page file | Final URL |
|---|---|
| `index.html` | `/` |
| `stay-with-us.html` | `/stay` |
| `live-with-us.html` | `/live` |
| `partner-with-us.html` | `/partner` |
| `the-experience.html` | `/experience` |
| `sentralplus.html` | `/sentralplus` |
| `group-business.html` | `/group-business` |
| `careers.html` | `/careers` |
| `press.html` | `/press` |
| `contact.html` | `/contact` |
| `privacy-policy.html` | `/privacy-policy` |
| `terms-of-use.html` | `/terms-of-use` |

Redirect map for legacy URLs is in `vercel.json` — replicate those 301s in WP.

**Integrations:** Stay booking widget = **Mews**; Live map = **Leaflet** (grayscale filter
+ slate pins, spec in STYLE_GUIDE §5); Press is CMS-fed; Careers listings are static in the
prototype (source of truth TBD — confirm ATS vs WP posts before building).

---

## 2. State of the source (as of the July 2026 v4 bake — commit `9a99d64`)

The pages' source now matches the v4 Slate system directly. Already done, verified page by page:

- ✅ **v4 tokens inline** — every page's `:root{}` carries the STYLE_GUIDE §11 values
  (`#282828` off-black, Slate `#2D4A5C` primary accent, cream trio, reserved gold split
  out as `--metallic`/`--metallic-deep`). The old prototype token *names* (`--gold`,
  `--accent`, `--gold-d`) intentionally resolve to Slate values — see §3 below.
- ✅ **No web fonts** — Google Fonts loads removed; Georgia + Aptos system stacks only (§3 of the guide)
- ✅ **Landmarks** — `<main id="main">` + skip-to-content link on all 12 pages
- ✅ **Internal links** — nav/footer hrefs point at the real files (work locally + in prod)
- ✅ **Partner value-creation dial** — v4 sequential ramp (`#777 → #5C8CA0 → #8FB6C9 → #FFF`),
  needle/captions/tags per §10.1/§1.3, 12px text floor
- ✅ **SentralPlus gold** — `--gold-mid` is v4 gold-deep `#8C6A2E` (sanctioned context, cream surface)

## 3. The one architectural decision you must understand

**`overrides.css` is a preview overlay that your theme replaces.** The prototype was
originally built on a different identity; `overrides.css` (loaded last, heavy `!important`)
reconciles it to v4 at runtime. The token layer is now ALSO baked into the pages (§2 above),
but **component-level rules still live only in the overlay** — active-nav treatment, hero
italic colors, dark-surface text-opacity floors, button text rules, per-component gold→slate
disambiguation.

**Do not port `overrides.css` as-is.** Build the theme from `STYLE_GUIDE.md` (§11 token
block + §5 component patterns); use `overrides.css` as the annotated worked-example of every
reconciliation decision — each rule has a comment saying what it fixes and why. When the
theme implements a rule natively, that rule is done; the overlay ships nowhere.

## 4. Remaining work — the theme must fix these (they are NOT fixed in source)

1. **~80 uses of the v3 gold tint `rgba(200,184,154,…)`** across all pages — borders,
   text at various alphas, focus glows, radial washes, and `<select>` arrow SVGs
   (`background-image` data-URIs). Each needs a per-surface call: slate tint on cream,
   slate-light tint on dark, per the guide's §1.2/§1.3. Find them:
   `grep -rn "200,184,154" *.html`
2. **`--lt: #9a9490` body text** — lighter than the `#6B6560` floor (§1.5). Anywhere
   `var(--lt)` styles body-size text on cream, use `--text-muted` instead.
3. **`contact.html` is orphaned** — no nav or footer link reaches it. Decide placement
   (footer "Company" column is the natural home) and wire it.
4. **Sub-floor text sweep** — the dial section was fixed, but other pages still have
   `0.56–0.72rem` labels. The floor is 12px (`0.75rem`), no exceptions (§10).
5. **Prototype token names** — pages still use v3 *names* (`--gold` etc.) resolving to v4
   values. The theme should use the §11 canonical names and drop the aliases.

## 5. Pre-build checklist

Work through **STYLE_GUIDE §13** line by line — it is the acceptance checklist for the
theme. Items already ✅ in source (fonts, `:root`, landmarks) still need to hold true in
the theme build. The accessibility floor in §10 and `ADA_BRIEF.md` is non-negotiable;
pay particular attention to the two named QA traps: slate-light-on-cream and oat-on-cream
(both FAIL contrast — they are dark-surface-only colors).

## 6. Voice, imagery, governance

- Copy follows §8 (short declaratives, italic continuation, "elevated", no exclamation points)
- Photography per §7; every informational image needs meaningful alt text
- Color governance per §1.4 and §12: **gold appears only in SentralPlus, awards, and
  print-parity contexts. Everywhere else the answer is Slate.**

---

*Questions on any of the above: JCheshire@sentral.com.*
