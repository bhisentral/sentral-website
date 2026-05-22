# Sentral Website — Style Guide

**Version:** 4.0 (Slate system — supersedes v3 Racing Green)
**For:** WordPress development team, designers, copywriters, brand owners
**Companion to:** `Sentral_WP_Developer_Brief.docx`, `ADA_BRIEF.md`,
`Sentral_Brand_System_v2.pptx` (canonical brand book), `Sentral_Brand_Standards_Brief.docx`
**Source:** Audit of all 11 pages of the static HTML prototype, reconciled
with Sentral Brand System v2 (May 2026) — the locked, leadership-approved
identity that moves Sentral from a green-anchored palette to a blue
slate-and-neutral system.

This document captures the design system as it will be *implemented* in
WordPress and applied across all Sentral surfaces. v4 swaps the v3
Racing Green primary accent for **Slate (`#2D4A5C`)**, replaces sage
with **Slate Light (`#5C8CA0`)**, updates oat to the v2 value
(`#F2E8D5`), and re-anchors the reserved metallic to **Gold
(`#B8924A`)** / **Gold deep (`#8C6A2E`)**. Surfaces, typography
(Georgia + Aptos), the italic continuation pattern, and the
reserved-gold governance all carry over unchanged.

> **Prose-update status:** PR 1 (this PR) updates the canonical token
> blocks in §2 and the §0 changelog. Prose elsewhere in this guide
> (§1.2 "Racing Green usage rules," §1.3 "Sage and oat usage rules,"
> §3 photography & motif language, etc.) still uses v3 terminology
> and will be rewritten in a follow-up PR. **If §2 disagrees with
> prose below, §2 wins.**

---

## 0. What changed in v4 — the accent direction

The brand moves from a green-anchored system (v3 Racing Green) to a
blue slate-and-neutral system. The change is sourced from
`Sentral_Brand_System_v2.pptx` (May 2026), approved by VP Marketing
with full ET endorsement. The rationale per the brand book: legacy
REIT operators own navy and Bozzuto owns green-and-sage; the
Slate-and-cream combination occupies defensible whitespace in the
multifamily peer set while reading as premium, contemporary, and
tenure-neutral.

### Key changes from v3 → v4

| | v3 (Racing Green) | v4 (Slate) |
|---|---|---|
| Primary accent | Racing Green `#1F3D2E` | **Slate `#2D4A5C`** |
| Hover / pressed, italic on cream | Racing Green deep `#0F2418` | **Slate deep `#3D6478`** |
| Italic on dark surfaces | Sage `#9CAE92` | **Slate light `#5C8CA0`** |
| Eyebrows on dark surfaces | Oat `#E8E0CC` | **Oat `#F2E8D5`** (value updated) |
| SentralPlus / awards gold | Metallic `#C8B89A` | **Gold `#B8924A`** |
| Award eyebrow gold deep | `#9A8862` | **Gold deep `#8C6A2E`** |

Surfaces (`#282828`, `#1F1F1F`, `#F5F5F3`, `#FAF8F4`, `#EFEDE6`),
cloud `#AFAA9B`, typography (Georgia + Aptos), the italic
continuation pattern, the wordmark, the reserved-gold governance,
the accessibility floor, and the overall structure of the system
all carry over unchanged.

### Why Slate

Per the Brand Standards Brief: the v4 palette anchors on Slate
because legacy REIT operators own navy, Bozzuto owns green-and-sage,
and warm-earth tones are cluttered in the multifamily peer set.
Slate reads as institutional, contemporary, and tenure-neutral
without crowding any existing competitor's identity.

Slate also pairs cleanly with the existing cream surfaces and
off-black structural colors, so v3 surface decisions stay intact
— this is a single-axis palette change, not a redesign.

### Accessibility note — slate light on dark

Slate light (`#5C8CA0`) on off-black (`#282828`) measures ~4.15:1
contrast — passes WCAG AA Large (3:1) and the 3:1 non-text contrast
requirement for focus indicators, but falls short of AA Normal
(4.5:1). v3 sage measured ~6.2:1 on off-black, so this is a
deliberate accessibility trade-off the brand book accepts because
slate-light is used only for italic emphasis in headlines (always
Large) and never for body text. Eyebrow text on dark continues to
use oat (`#F2E8D5`), which has very high contrast on off-black.

---

## 1. The system in four roles

Every color in the Sentral system has one of four roles. Confusing the
roles is what creates drift. The brand owner's job is to enforce the
boundaries between them.

### Surfaces

Carry the structure. Backgrounds, sections, dividers. Never decorative
on their own. Off-black, three cream tones, cloud for borders.

### Primary accent

Carries the brand. Used as punctuation throughout the system — CTAs,
eyebrows on cream, italic emphasis on cream, focus rings, active
states, one full-color section per page. Slate and Slate deep.

### Secondary accents (dark surfaces only)

Carry visual layering on dark backgrounds where the primary accent is
too dark to read. Slate light for italic emphasis in headlines on dark.
Oat for eyebrows on dark. **Used nowhere else.** These are visual
register shifts, not new primary colors.

### Reserved metallic

Carries earned status. Gold and gold-deep, deployed only for
SentralPlus tier indicators, awards and press recognition, and print
or physical signage parity. Never general accent. The discipline of
keeping gold restricted is what makes it meaningful when it appears.

---

## 2. Color system

### Surfaces

```css
--black:        #282828;   /* primary dark surface — nav, hero, dark sections */
--ink:          #1F1F1F;   /* slightly darker — search dropdowns, footers */
--cream-light:  #FAF8F4;   /* softest cream — hero intros, filter bars */
--cream:        #F5F5F3;   /* primary cream — body bg, card grids */
--cream-warm:   #EFEDE6;   /* warmest cream — testimonials, secondary cards */
--white:        #FFFFFF;   /* pure white — text on dark, input fills */
```

### Primary accent

```css
--slate:        #2D4A5C;   /* primary accent — CTAs, eyebrows on cream, italic on cream */
--slate-deep:   #3D6478;   /* hover/pressed, italic on cream, deepest accent moments */
--cloud:        #AFAA9B;   /* warm gray — borders/dividers on cream */
```

### Secondary accent — dark surfaces only

```css
--slate-light: #5C8CA0;   /* italic emphasis in headlines on dark — ONLY */
--oat:         #F2E8D5;   /* eyebrow text on dark — ONLY */
```

**See §1.4 governance rules. These tokens are intentionally narrow in
scope; treating them as general accents will dilute the system.**

### Reserved metallic — restricted use only

```css
--gold:         #B8924A;   /* SentralPlus, awards on dark — NOT a general accent */
--gold-deep:    #8C6A2E;   /* deep gold — gold text on cream surfaces (award eyebrows) */
```

### Text on cream — accessibility-corrected

```css
--text-body:    #3A3633;   /* AAA, ~12.6 : 1 on cream */
--text-muted:   #6B6560;   /* AA,  ~5.14 : 1 on cream */
--text-accent:  #3D6478;   /* slate-deep — italic emphasis on cream (AAA ~7.3:1) */
```

### Text on dark

```css
--text-on-dark:        #FFFFFF;
--text-on-dark-muted:  rgba(255, 255, 255, 0.78);   /* min 70% opacity */
--text-on-dark-accent: #5C8CA0;   /* slate-light — italic emphasis only */
--text-on-dark-eyebrow: #F2E8D5;  /* oat — eyebrow text only */
```

### Legacy v3 token aliases

For backward compatibility during the v3 → v4 migration, the following
aliases are defined in `overrides.css`. They will be removed in a
follow-up PR after the WP rebuild migrates off the v3 names:

```css
--racing-green:      var(--slate);
--racing-green-deep: var(--slate-deep);
--sage:              var(--slate-light);
```

**Do not introduce new uses of these aliases.** They exist only to keep
v3-named references resolving during the transition.

### Rules / dividers

```css
--rule:    rgba(255, 255, 255, 0.08);   /* on dark */
--ruleW:   rgba(0, 0, 0, 0.08);         /* on cream — subtle */
--ruleC:   #AFAA9B;                      /* cloud — visible card/input borders */
```

### 1.1 Cream surface usage rules

The three creams are close enough to read as one family, distinct
enough to create visual breaks. Use them deliberately to create page
rhythm:

| Tone | Hex | Use |
|---|---|---|
| Cream light | `#FAF8F4` | Hero intros on cream pages, sticky filter bars, the lightest touch — when a section needs to feel like air |
| Cream | `#F5F5F3` | Primary body background. Main card grids. The default cream for most page content |
| Cream warm | `#EFEDE6` | Testimonial blocks, quote callouts, secondary cards on a primary-cream page, "what's included" lists |

Pattern: A long cream page should typically use at least two of the
three tones to break up its rhythm. A short page can stay on one.
Never mix all three within a single section — alternate by section,
not within.

**Don't use cream tones for:**
- Borders or dividers (cloud `#AFAA9B` does that)
- Text (use `--text-body` or `--text-muted`)
- Accent fills inside cards (use Slate or stay with the section
  background)

### 1.2 Slate usage rules

- **Slate is the brand color.** It does the primary accent work
  everywhere except where it's too dark to read on dark backgrounds.
- **On dark surfaces:** Slate is dark enough that it cannot be used as
  italic emphasis, eyebrow text, hairline rules, or focus indicators
  *on* off-black — the contrast is too low. On dark surfaces, slate
  works only as a **background fill** with cream/white text on top
  (CTA buttons, full-section bands). For italic emphasis on dark use
  **slate light** (`#5C8CA0`); for eyebrows on dark use **oat**
  (`#F2E8D5`); for hairlines and focus rings on dark use **slate
  light** or oat depending on context.
- **On cream surfaces:** Slate and Slate deep do all the accent
  work. Italic emphasis in headlines uses Slate deep (`#3D6478`).
  Eyebrows on cream use Slate or Slate deep. CTAs on cream use Slate.
- **Text on Slate (any size, any context) is white or cream.** Never
  set body text, button labels, or eyebrows to a darker color on a
  Slate background — the contrast collapses. Default to `--white`
  (`#FFFFFF`) for buttons and body, `--cream-light` (`#FAF8F4`) for
  large display headlines where a softer warmth is wanted.
- **One full-Slate section per page** (CTA band, values section,
  property highlight) gives the accent room to breathe at scale. Use
  oat for the eyebrow text and slate-light or cream-light for italic
  emphasis within that section. Body text and buttons inside this
  section are white.

### 1.3 Slate-light and oat usage rules

These are the most fragile rules in the system. Hold them.

**Slate light `#5C8CA0` appears only as:**
- Italic emphasis in headlines on off-black and ink surfaces
- Italic emphasis in headlines on the full-Slate section
- Active nav underlines and focus rings on dark surfaces (the
  non-text 3:1 contrast minimum is met; do not use for text)

**Oat `#F2E8D5` appears only as:**
- Eyebrow text on dark surfaces
- Small caption labels on dark where slate would be too dark to read
- Subtle accent text on the full-Slate section

**Where slate-light and oat must not appear:**
- On cream surfaces of any tone (slate-light on cream measures
  ~3.2:1 — fails AA for text; oat on cream is even worse)
- As button backgrounds or button text
- As decorative tints, fills, or borders
- As icon colors on cream (use slate or slate-deep)
- Adjacent to gold (the oat-gold distinction is hard to hold visually
  and creates governance ambiguity — keep them on separate sections)
- In any new context not explicitly named in this guide

If a use case requires "a lighter blue" or "a warm cream that isn't
gold" outside the contexts above, the answer is to redesign the
component, not to expand slate-light or oat usage. These colors
exist to solve specific contrast problems on dark surfaces. They
are not secondary brand colors.

### 1.4 Gold governance rules — read before using

Gold is reserved. It is not a general accent. The discipline of
keeping it in its three lanes is what makes it meaningful when
it appears. **A designer reaching for gold to make something "feel
premium" is the failure mode this rule exists to prevent.** Slate
does that job everywhere except the contexts below.

**The only places gold appears on the website:**

1. **SentralPlus tier indicators and member labels.** Tier badges,
   founding-member markers, member-exclusive section labels, the
   SentralPlus product surface itself.

2. **Awards and press recognition.** Industry awards, "Best Places
   to Live" rankings, third-party recognition badges, year markers
   on award listings.

3. **Print and physical signage parity.** Where the website
   references or mirrors a physical asset that uses gold (key cards,
   embossed signage, foil-stamped welcome packets), digital gold
   honors that visual code.

**Where gold must not appear:**
- General CTAs (those are Slate)
- Eyebrows on non-SentralPlus, non-award sections (those are oat on
  dark, Slate or Slate deep on cream)
- Italic accents in general headlines (those are Slate deep on cream,
  Slate light on dark)
- Active nav states, focus rings, hover states
- Map pins, link colors, button hovers
- Decorative tinting on cream
- Anywhere a designer is choosing it for "warmth" or "premium feel"
  without a SentralPlus / award / print justification

If a request comes in to use gold somewhere outside these contexts,
the answer is Slate.

### 1.5 General color usage rules

- **Body text on cream** uses `--text-body` or `--text-muted`. Never
  lighter than `#6B6560`.
- **Hero subtitles on dark** sit at 70–90% white opacity. The
  prototype's original 30–40% values fail accessibility.
- **Dividers** are nearly transparent (`rule`/`ruleW`) — never solid
  lines. Cloud is reserved for visible borders on cards and inputs.
- **Text on gold** uses `--black` (`#282828`) or `--gold-deep`
  (`#8C6A2E`) — never plain white, which fails contrast on the
  warm gold tone (white on gold ≈ 2.9 : 1).
- **Text on Slate (governance)** uses **white or cream only.**
  Body text and button labels are `--white` (`#FFFFFF`). Eyebrows on
  Slate are oat (`#F2E8D5`). Italic emphasis in headlines on Slate
  is slate-light (`#5C8CA0`) or cream-light (`#FAF8F4`) depending on
  whether warmth or coolness is wanted. **Any darker text color on
  a Slate background is a brand violation — slate is dark enough
  that black or slate-deep text on it would fail contrast.** Never
  use gold on a Slate background (gold is reserved, and contrast is
  marginal anyway).

---

## 3. Typography

### Type families

- **Display:** `Georgia` — screen-optimized serif, weights 400 + italic.
  Fallback: "Times New Roman", serif.
- **Body:** `Aptos` — Microsoft humanist sans-serif, weights 300 / 400 / 500.
  Fallbacks: "Segoe UI", system-ui, sans-serif.

No web font loading required. Both render natively on every modern
device. This eliminates font-swap flash on first paint and removes any
external font dependency.

### Type scale

| Token | Size | Weight | Use |
|---|---|---|---|
| `h1-hero` | `clamp(2.2rem, 4vw, 3.6rem)` | 400 | Hero headline |
| `h1` | `2.4rem – 3rem` | 400 | Section heroes ("Our core values") |
| `h2` | `1.6rem – 2rem` | 400 | Subsection headings |
| `h3` | `1.2rem – 1.4rem` | 400 | Card titles ("Service First") |
| `body` | `1rem` (16 px) | 400 | Paragraphs |
| `body-sm` | `0.85rem` | 400 | Caption-adjacent body |
| `eyebrow` | `0.75rem` minimum | 500 uppercase, letter-spacing 0.18em | "MEMBER BENEFITS", "01 — BUSINESS TRAVEL" |
| `caption` | `0.75rem` minimum | 400 | Filter labels, badges, metadata |

**Note on weight:** Default Georgia to weight 400. If a heading needs
to feel lighter, use letter-spacing (`0.01em`) and generous line-height
(`1.15`) rather than reducing weight.

**Floor:** no text below `0.75rem` (12 px), ever.

### Italic emphasis — Sentral's signature move

The most distinctive typographic pattern on the site is splitting
headlines into a declarative first clause and an italic continuation:

> Stay like it's already *your home.*
> Find your next home. *Elevated.*
> We operate communities where people *genuinely* want to be.
> Where great spaces meet *exceptional people.*
> What you get as a *member.*

Italic accents inherit color based on surface:

- **On cream surfaces:** Slate deep `#3D6478`
- **On off-black surfaces:** Slate light `#5C8CA0`
- **On the full-Slate section:** Slate light `#5C8CA0` or
  cream-light `#FAF8F4` depending on visual weight needed

Never gold (gold is reserved). Never the primary Slate on dark
surfaces (insufficient contrast at type sizes — use slate-light).

### Line heights

- Display headings: `1.15`
- Body paragraphs: `1.6 – 1.8`
- Captions / eyebrows: `1.4`

---

## 4. Layout system

### Container

- **Max content width:** `1400px` (`.hero-inner`, section inners,
  card grids)
- Always center-aligned with `margin: 0 auto`

### Spacing

- **Page side padding:** `64px` desktop, `20px` mobile (≤ 900 px)
- **Section vertical padding:** `64px` / `80px` / `100px` depending
  on content density
- **Grid gap:** `32 – 48px` between major columns; `12 – 24px`
  within cards

### Breakpoints

- `≤ 900px` — collapse nav links to hamburger; single-column grids
- `≤ 640px` — smaller display sizes; tighter side padding

### Section rhythm

A typical long page should alternate surfaces in a rhythm like:

```
[Off-black hero — oat eyebrow, slate-light italic, Slate CTA with white text]
  ↓
[Cream-light filter bar or intro — Slate deep eyebrow, Slate deep italic]
  ↓
[Cream primary content — Slate deep eyebrow, Slate deep italic]
  ↓
[Cream-warm testimonial/quote block]
  ↓
[Full-Slate CTA band — oat eyebrow, slate-light or cream-light italic, white body/buttons]
  ↓
[Ink + gold SentralPlus footer block — only where contextually relevant]
  ↓
[Off-black footer]
```

Not every page needs every surface. Short pages (Privacy, Terms) can
stay on one or two. The Live With Us, SentralPlus, and Home pages
benefit from the full rhythm.

### Fixed nav

- Height: `64px`
- Background: `--black`
- Always sticky-fixed at top of viewport
- Border-bottom: `--rule` (subtle, near-invisible)

---

## 5. Component patterns

### Primary navigation

- Off-black bar, `SEN+RAL` wordmark left, link cluster center, CTA +
  hamburger right
- **Active link:** slate-light underline + white text (slate-light is
  the visual cue; Slate on off-black would be invisible at 1px stroke)
- **Inactive link:** 55% white, hover → 100% white
- **CTAs in nav** ("Book a Stay", "Login"): Slate button background
  `#2D4A5C`, white text

### Hero — photo

Used on: Home, Stay, Live, Partner, Experience, Careers, Group
Business, SentralPlus.

Structure (left-aligned by default):
```
[Eyebrow: oat uppercase]
[Headline: Georgia, large, italic continuation in slate-light]
[Subtitle: Aptos, 80%+ white opacity]
[Stats / CTAs (optional) — primary CTA in Slate with white text]
```

Required treatment for legibility on photo backgrounds:
```css
text-shadow:
  0 0 18px rgba(0, 0, 0, 0.65),
  0 2px  8px rgba(0, 0, 0, 0.55),
  0 1px  2px rgba(0, 0, 0, 0.50);
```

### Hero — typographic (no photo)

Used on: Live With Us (after carousel), Press, Privacy Policy,
Terms of Use.

- Off-black background, no photo
- Same eyebrow → headline → subtitle structure
- Often paired with a sticky filter bar (use cream-light) below

### Section eyebrow

- `0.75rem` minimum, weight 500, uppercase, letter-spacing
  0.18 – 0.24em
- Color: `--text-accent` (Slate deep) on cream, `--oat` on dark
- Always sits `14 – 16px` above the section heading
- Examples: `"MEMBER BENEFITS"`, `"01 — BUSINESS TRAVEL"`,
  `"WHAT DRIVES US"`, `"FOR OWNERS & DEVELOPERS"`

**Exception:** Award badges and SentralPlus tier eyebrows use gold.
See §5.7 and §5.8.

### Cards — standard

Property card, news card, value card all share:

- Photo top, content below
- Pinned badge top-left in pill shape (`"AVAILABLE"`,
  `"NEW — LEASING"`)
- City label uppercase, lighter weight
- Title in Georgia, weight 400
- "View →" or "Read article →" CTA with arrow glyph; arrow turns
  Slate on hover

Card backgrounds: white on cream-light or cream-warm; cream-warm on
cream-light or cream. Avoid same-tone cards on same-tone backgrounds.

### Buttons

| Variant | Background | Text | Use |
|---|---|---|---|
| Primary on dark | `--slate` | `--white` | "Book a Stay", "Join SentralPlus", "View Open Roles" |
| Primary on cream | `--black` | `--cream` | Primary CTA on cream sections |
| Secondary on dark | transparent + 1px white border | `--white` | "Learn more →" |
| Tertiary text-link | none | `--slate` (cream bg) / `--white` (dark bg) | Inline links |

All buttons:
- Text: `0.85rem`, weight 500, Aptos
- Padding: `14 – 16px` vertical, `22 – 28px` horizontal
- Border-radius: `2 – 3px` (very subtle)
- Hover: Slate darkens to `--slate-deep` on dark; on cream,
  off-black shifts to `--ink`. No transform.

**Slate-light and oat are never used as button backgrounds or
button text. Buttons with a Slate background ALWAYS use white
text — never gold, never slate-deep, never any darker color.**

### Forms

**On dark:**
- Inputs: 6% white fill, 25% Slate border
- Focus: 60% Slate border (`--slate`), 9% white fill
- Placeholder: 40% white

**On cream / cream-light / cream-warm:**
- Inputs: white fill, cloud (`#AFAA9B`) border
- Focus: Slate deep (`--text-accent`) border
- Placeholder: `--text-muted`

**Always:** pair every input with a visible `<label>`, not just a
placeholder. Placeholders disappear when typing.

### Filters / pills

Used on Live With Us (state filter) and Press (year + category):

- Active: off-black fill, white text
- Inactive: cream fill, dark text, cloud border
- Hover: border darkens to Slate deep
- Padding: `6 – 8px` vertical, `14 – 18px` horizontal
- Border-radius: full pill (999px)

### Map (Live With Us)

- Leaflet base map with grayscale + brightness filters applied:
  ```css
  filter: grayscale(0.3) brightness(0.92);
  ```
- Custom Slate pins (`14 × 14px`, Slate fill, Slate halo)
- Popup on `--black` background, Slate border, Slate link text
- Pins must be keyboard-focusable and announce property + city to
  screen readers

### 5.7 SentralPlus components — reserved gold

These are the primary places gold appears on the site. Every gold
treatment below is justified by a SentralPlus / member context.

**Member tier badge (outline variant, on dark):**
```css
.tier-badge-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(184, 146, 74, 0.12);
  border: 1px solid var(--gold);
  color: var(--gold);
  font-family: var(--sans);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  padding: 5px 11px;
  border-radius: 999px;
}
.tier-badge-outline::before {
  content: "";
  width: 6px; height: 6px;
  background: var(--gold);
  border-radius: 50%;
}
```

**Member tier badge (filled variant, on dark):**
```css
.tier-badge-filled {
  background: var(--gold);
  color: var(--black);
  /* same dimensions and typography as outline variant */
}
```

**SentralPlus footer block:**
- Background: `--ink` (`#1F1F1F`), one shade darker than `--black`
- Eyebrow: gold, "SENTRALPLUS MEMBER"
- Headline: Georgia, white, with italic continuation in gold
- The visual signal: this block is *for* members, hence the gold

### 5.8 Award and recognition components — reserved gold

**Award badge card (on cream):**
```css
.award-card {
  background: var(--white);
  border: 0.5px solid var(--cloud);
  border-radius: var(--border-radius-md);
  padding: 14px 16px;
}
.award-card .eyebrow {
  font-family: var(--sans);
  font-size: 0.65rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold-deep);   /* deeper gold on cream — passes AA */
}
.award-card .icon { stroke: var(--gold-deep); }
.award-card h4 {
  font-family: var(--serif);
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--text-body);
}
```

**Important:** On cream surfaces, gold text uses `--gold-deep`
(`#8C6A2E`), not `--gold`. The lighter gold fails contrast on cream.

---

## 6. Iconography

- Icons are **stroked, not filled**, `stroke-width: 1.5`
- Default size: `16px` or `20px`
- Use `stroke="currentColor"` so icons inherit the text color of
  their parent
- On cream surfaces: Slate for active icons, cloud for muted
- On dark surfaces: white for active icons, slate-light for emphasized
- Award icons (trophy, ribbon, laurel) inherit gold-deep on cream,
  gold on dark — these are the only icons that get gold

---

## 7. Imagery

### Photography direction

- **Editorial, hospitality-luxury.** Sunset / golden-hour exteriors,
  bright minimal interiors, candid lifestyle moments.
- **Avoid:** stock photography, posed corporate shots, harsh flash,
  oversaturated color grades.
- City labels accompany every property image:
  `"WEST PALM BEACH, FL — NORA"`

### Treatment

- Full-bleed in heroes, no rounded corners
- Cards: square or 4:3 aspect, no rounding (or minimal `2–3px`)
- Hover state on cards: subtle scale `1.02` or brightness lift, never
  drop-shadow

### Alt text

- Every informational image needs meaningful alt text:
  `"Sentral Sol Modern, Phoenix, AZ — rooftop pool at sunset"`
- Decorative images: `alt=""` (empty, not absent)
- Property thumbnails should describe property name + city, not
  filename

---

## 8. Voice & tone

### Personality

Confident, restrained, hospitality-luxury. Short sentences.
Em-dashes for rhythm. Italics for emotional emphasis.

### Headline pattern

Declarative + italic continuation:
- "Stay like it's *already your home.*"
- "We operate communities where people *genuinely* want to be."
- "Find your next home. *Elevated.*"
- "Live at Sentral. Travel at 20% off."

### Body copy traits

- Specifics over abstractions: `"23 cities"`, `"13 states"`,
  `"11K+ residences"`, `"$7B AUM"`
- Em-dashes for asides, not parentheses
- One word that recurs deliberately: **"elevated"**
- Active voice, present tense

### Avoid

- Marketing jargon ("synergy", "solutions", "cutting-edge")
- Exclamation points
- "We're so excited to…", "We're thrilled to…"
- Buzzy startup tone, generic SaaS copy

### Embrace

- Quiet authority
- Concrete numbers
- Language of hospitality (not real estate, not tech)
- The pause that comes from a well-placed em-dash

---

## 9. Motion & interaction

- **Transitions:** `0.15 – 0.25s`, easing
  `cubic-bezier(.22, .68, 0, 1.2)`
- **No parallax**, no auto-playing carousels longer than 6 seconds
- **Hover states are subtle** — opacity shifts, color shifts, never
  jumps or bounces
- **Respect `prefers-reduced-motion: reduce`** — disable all
  movement-based animations for users who request it
- Carousels and image transitions: 4 – 6 second dwell, `0.6s` cross-fade

---

## 10. Accessibility floor (non-negotiable)

These are not aspirational — they're requirements. Full spec in
`ADA_BRIEF.md`.

- Minimum contrast: **4.5 : 1** on body text, **3 : 1** on large
  text and UI components
- Minimum font-size: **12 px** (`0.75rem`) — labels included
- Visible `:focus-visible` outline on every interactive element
  (Slate at 2px, offset 2px on cream; slate-light at 2px, offset 2px
  on dark — slate-light gives sufficient non-text contrast on
  off-black where Slate itself would be too dark to see)
- Every informational image has meaningful `alt`; decorative
  images have `alt=""`
- `<main>` landmark on every page
- Skip-to-content link as first focusable element
- 200% zoom must not cause horizontal scroll on body content
- Site must pass keyboard-only navigation
- Animations respect `prefers-reduced-motion`

### 10.1 Slate contrast notes

- Slate `#2D4A5C` on cream `#F5F5F3`: **~8.3 : 1** — passes AAA.
  Use freely for body-size eyebrows, italic emphasis, and CTAs.
- Slate `#2D4A5C` on off-black `#282828`: **~1.6 : 1** — **FAILS** for
  text and non-text use alike. Do not use Slate as text or stroke on
  off-black. Use Slate as a background fill on dark sections (with
  white text), use slate-light for italic emphasis and focus rings
  on dark instead.
- Slate deep `#3D6478` on cream: **~5.9 : 1** — passes AA for all
  sizes, AAA for large text. Use for italic emphasis in headlines
  on cream and hover/pressed states.
- White on slate `#2D4A5C`: **~9.1 : 1** — passes AAA. Standard CTA
  text combination. Use white (or `--cream-light`) for any text
  placed on a Slate background, regardless of size.

### 10.2 Slate-light contrast notes

- Slate light `#5C8CA0` on off-black `#282828`: **~4.15 : 1** —
  passes AA Large (3:1) and the 3:1 non-text contrast requirement
  for focus indicators and active-state strokes. Falls short of
  AA Normal (4.5:1) — use for italic emphasis in headlines (which
  are always Large) and decorative strokes, never for body text.
- Slate light `#5C8CA0` on Slate `#2D4A5C`: **~2.6 : 1** —
  **FAILS**. Do not place slate-light text on a Slate background.
  Use cream-light or white instead.
- Slate light `#5C8CA0` on cream `#F5F5F3`: **~3.2 : 1** —
  **FAILS for text** (under AA Normal). Never use slate-light on
  cream surfaces. This is the most likely misuse and must be
  caught in QA.

### 10.3 Oat contrast notes

- Oat `#F2E8D5` on off-black `#282828`: **~12.1 : 1** — passes AAA.
  Safe for eyebrow text and small caption labels on dark.
- Oat `#F2E8D5` on slate `#2D4A5C`: **~8.0 : 1** — passes AAA. Safe
  for eyebrow text on the full-Slate section.
- Oat `#F2E8D5` on cream `#F5F5F3`: **~1.0 : 1** — **FAILS**. Never
  use oat on cream surfaces. The two colors are too close in value.

### 10.4 Cream contrast notes

- All three cream tones pass AAA contrast with `--text-body`
  (`#3A3633`) — minimum ratio `12.4 : 1` on cream-warm
- All three cream tones pass AA contrast with `--text-muted`
  (`#6B6560`) — minimum ratio `4.9 : 1` on cream-warm
- Slate deep `#3D6478` passes AA Normal (≥5.6 : 1) on all three
  cream tones; Slate `#2D4A5C` passes AAA (≥8.0 : 1) on all three.

### 10.5 Gold contrast notes — verify before deploying

- Gold `#B8924A` on off-black `#282828`: **~5.1 : 1** — passes AA
  for all sizes. Safe for tier badges, member labels, eyebrows on
  dark *in SentralPlus contexts only*.
- Gold `#B8924A` on cream `#F5F5F3`: **~2.7 : 1** — **FAILS**. Never
  use light gold for text on cream.
- Gold-deep `#8C6A2E` on cream `#F5F5F3`: **~4.5 : 1** — passes AA
  Normal at the threshold. Use for award eyebrows and 14px+ labels;
  for body or sub-14px text, use `--text-body` instead.
- White `#FFFFFF` on gold `#B8924A`: **~2.9 : 1** — **FAILS**. Use
  off-black on gold buttons, never white.
- Off-black `#282828` on gold `#B8924A`: **~5.1 : 1** — passes AA
  Normal. Standard text-on-gold combination.

---

## 11. Reference: complete `:root{}` block

For copy-paste into the WordPress theme stylesheet:

```css
:root {
  /* Surfaces */
  --black:        #282828;
  --ink:          #1F1F1F;
  --cream-light:  #FAF8F4;
  --cream:        #F5F5F3;
  --cream-warm:   #EFEDE6;
  --white:        #FFFFFF;

  /* Primary accent */
  --slate:        #2D4A5C;
  --slate-deep:   #3D6478;
  --slate-light:  #5C8CA0;
  --cloud:        #AFAA9B;

  /* Eyebrow on dark surfaces — Oat */
  --oat:          #F2E8D5;

  /* Reserved metallic — SentralPlus, awards, print only */
  --gold:         #B8924A;
  --gold-deep:    #8C6A2E;

  /* Text on cream */
  --text-body:    #3A3633;
  --text-muted:   #6B6560;
  --text-accent:  #3D6478;

  /* Text on dark */
  --text-on-dark:         #FFFFFF;
  --text-on-dark-muted:   rgba(255, 255, 255, 0.78);
  --text-on-dark-accent:  #5C8CA0;
  --text-on-dark-eyebrow: #F2E8D5;

  /* Rules */
  --rule:    rgba(255, 255, 255, 0.08);
  --ruleW:   rgba(0, 0, 0, 0.08);
  --ruleC:   #AFAA9B;

  /* Type — system-safe, zero licensing */
  --serif: Georgia, "Times New Roman", serif;
  --sans:  Aptos, "Segoe UI", system-ui, -apple-system, sans-serif;

  /* Type floors */
  --fs-min-body:    1rem;     /* 16px */
  --fs-min-caption: 0.75rem;  /* 12px */

  /* Motion */
  --ease: cubic-bezier(0.22, 0.68, 0, 1.2);
}
```

---

## 12. Decision matrix — quick reference

When in doubt, this table settles it:

| Use case | Slate | Slate-light | Oat | Cream tones | Gold |
|---|:---:|:---:|:---:|:---:|:---:|
| Primary CTAs and buttons | ● | — | — | — | — |
| Eyebrows on cream | ● | — | — | — | — |
| Eyebrows on dark | — | — | ● | — | — |
| Italic accents on cream | ● | — | — | — | — |
| Italic accents on dark | — | ● | — | — | — |
| Active nav on dark · focus rings on dark | — | ● | — | — | — |
| Active states on cream · focus rings on cream | ● | — | — | — | — |
| Map pins | ● | — | — | — | — |
| Full-section hero band (one per page) | ● | — | — | — | — |
| Section background variation | — | — | — | ● | — |
| Card surfaces and quote blocks | — | — | — | ● | — |
| Borders and dividers on cream | — | — | — | — *(cloud)* | — |
| SentralPlus tier badges and member labels | — | — | — | — | ● |
| SentralPlus footer/promo block | — | — | — | — | ● |
| Awards and press recognition | — | — | — | — | ● |
| Award icons and ribbons | — | — | — | — | ● |
| Print and physical signage parity | — | — | — | — | ● |
| Decorative accent without specific reason | — | **No** | **No** | — | **No** |

---

## 13. Pre-build checklist for the WordPress developer

Before theme development begins, confirm:

- [ ] `:root{}` token block in §11 is implemented exactly as shown
- [ ] All three cream tones are defined and used per §1.1
- [ ] Slate-light and oat tokens are defined but used **only** in the
      contexts named in §1.3 (italic on dark, eyebrow on dark)
- [ ] Gold tokens are defined but used **only** in SentralPlus,
      award, and print-parity components (per §1.4 and §12)
- [ ] Georgia + Aptos render correctly across Chrome, Safari, Firefox,
      and Edge — no font-loading shims or `@font-face` rules needed
- [ ] All v3 Racing Green (`#1F3D2E`) and Racing Green deep (`#0F2418`)
      hex references replaced with Slate (`#2D4A5C`) and Slate deep
      (`#3D6478`); no stale racing-green / sage / forest values remain
      in the codebase (including SVG fills, gradient stops, JS color
      arrays, inline `style=""` attributes)
- [ ] All v3 gold hex values (`#C8B89A`, `#9A8862`) replaced with v4
      (`#B8924A`, `#8C6A2E`)
- [ ] All `#141414` references replaced with `#282828`
- [ ] Cormorant Garamond and DM Sans `<link>` tags removed from
      `<head>` (no Google Fonts loading)
- [ ] Hero text-shadow values applied consistently across all
      photo-hero pages
- [ ] Focus outlines verified on every interactive element using
      keyboard-only navigation (Slate on cream, slate-light on dark)
- [ ] All form inputs have visible labels (not placeholder-only)
- [ ] Contrast verified with axe DevTools or WAVE on every template
      — pay special attention to slate-light-on-cream (FAILS) and
      oat-on-cream (FAILS) misuses
- [ ] Every Slate background fill has white or cream text only
      (no slate-deep, no gold, no dark text) — per §1.5
- [ ] Reduced-motion media query disables carousel auto-advance and
      hover transforms
- [ ] At least one page (Home or Live With Us) demonstrates the full
      surface rhythm

---

## 14. Governance — who owns what

- **Color additions or modifications:** Must come through brand
  marketing review. The most fragile rules in this system, in order
  of fragility, are: (1) sage-and-oat boundaries — they will be
  treated as general accents if not actively governed; (2) the
  reserved-gold rule; (3) the cream tonal alternation. Pressure to
  expand all three will come up. Hold the line.
- **Typography changes:** Require IT and marketing sign-off jointly,
  because any non-system typeface introduces licensing and
  deployment cost.
- **Component additions:** Designer + WP dev review; document new
  components in this guide before they ship.
- **Voice and copy changes:** Marketing owns; refer to §8.

---

## Questions / sign-off

For questions on any of the above, contact JCheshire@sentral.com.

This guide should be read alongside:
- `Sentral_WP_Developer_Brief.docx` — original WordPress
  implementation brief
- `ADA_BRIEF.md` — accessibility / WCAG correction spec
- The static prototype repo: https://github.com/Sentral2026/sentral-website
- `internal-note-brand-reconciliation.md` — the rationale and
  decision context behind earlier versions of this guide
- `Sentral_Brand_Style_Guide_v3.pptx` — the visual companion to
  this document
