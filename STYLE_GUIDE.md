# Sentral Website — Style Guide

**For:** WordPress development team, designers, copywriters
**Companion to:** `Sentral_WP_Developer_Brief.docx`, `ADA_BRIEF.md`
**Source:** Audit of all 11 pages of the static HTML prototype

This document captures the design system as it is *implemented* in the
prototype, not just as it was specified. Use it as the canonical
reference when building the WordPress theme. Where the prototype
diverges from official Sentral brand guidelines, that divergence is
flagged in §0 below.

---

## 0. Brand divergence — read this first

The prototype does **not** match Sentral's official brand guidelines.
Before any WordPress work begins, the team needs to decide which
identity is the source of truth.

|  | Official Sentral brand | Prototype as built |
|---|---|---|
| **Palette** | Forest `#196E5F`, Coral `#F57D73`, Cloud `#AFAA9B`, Off-black `#282828`, Cream `#F5F5F3` | Black `#141414`, Cream `#F5F3EF`, Gold `#C8B89A` |
| **Typography** | Tobias (display) + Matter (body); Georgia / Open Sans fallbacks | Cormorant Garamond (display) + DM Sans (body) |
| **Wordmark** | "Sen+ral" with stylized + | "SEN+RAL" — same |

The prototype is essentially a different visual identity that shares
only the wordmark and the cream-on-dark contrast direction. The rest
of this document describes the prototype's identity. If the team
elects to revert to the official brand, the typographic scale, layout
system, component patterns, voice, and accessibility floor all carry
over; only the color and font tokens change.

---

## 1. Color system

### Surfaces

```css
--black:   #141414;   /* primary dark surface — nav, hero, dark sections */
--ink:     #1a1a1a;   /* slightly lighter dark — search dropdowns, popups */
--cream:   #f5f3ef;   /* primary light surface — body bg */
--white:   #ffffff;   /* pure white — text on dark */
```

### Accents

```css
--gold:    #c8b89a;   /* eyebrows, italic emphasis, CTA on dark */
--gold-d:  #2a1f10;   /* deep bronze — used sparingly */
--stone:   #d8d4ce;   /* warm gray — borders/dividers on cream */
```

### Text on cream — accessibility-corrected

The prototype's original light-gray and gold-on-cream values failed
WCAG AA. Use these instead:

```css
--text-body:    #3a3633;   /* AAA, ~12.6 : 1 on cream */
--text-muted:   #6b6560;   /* AA,  ~5.14 : 1 on cream */
--text-accent:  #5e4a2c;   /* AAA, ~7.10 : 1 — replaces gold-on-cream */
```

### Text on dark

```css
--text-on-dark:        #ffffff;
--text-on-dark-muted:  rgba(255, 255, 255, 0.78);   /* min 70% opacity */
```

### Rules / dividers

```css
--rule:    rgba(255, 255, 255, 0.08);   /* on dark */
--ruleW:   rgba(0, 0, 0, 0.08);         /* on cream */
```

### Color usage rules

- **Gold is decorative on dark only.** Never use as text on cream.
- **Italic accents** in headings (`<em>`) get gold on dark, bronze
  (`--text-accent`) on cream.
- **Body text on cream** uses `--text-body` or `--text-muted`. Never
  lighter than `#6b6560`.
- **Hero subtitles on dark** sit at 70–90% white opacity. The
  prototype's original 30–40% values fail accessibility.
- **Dividers** are nearly transparent (`rule`/`ruleW`) — never solid
  lines.

---

## 2. Typography

### Type families

- **Display:** `Cormorant Garamond` — serif, weights 300 + italic.
  Fallback: Georgia, serif.
- **Body:** `DM Sans` — sans-serif, weights 300 / 400 / 500.
  Fallback: system-ui, sans-serif.

Both load from Google Fonts in production:
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap">
```

### Type scale

| Token | Size | Weight | Use |
|---|---|---|---|
| `h1-hero` | `clamp(2.2rem, 4vw, 3.6rem)` | 300 | Hero headline |
| `h1` | `2.4rem – 3rem` | 300 | Section heroes ("Our core values") |
| `h2` | `1.6rem – 2rem` | 300 / 400 | Subsection headings |
| `h3` | `1.2rem – 1.4rem` | 400 | Card titles ("Service First") |
| `body` | `1rem` (16 px) | 300 | Paragraphs |
| `body-sm` | `0.85rem` | 300 | Caption-adjacent body |
| `eyebrow` | `0.75rem` minimum | 500 uppercase, letter-spacing 0.18em | "MEMBER BENEFITS", "01 — BUSINESS TRAVEL" |
| `caption` | `0.75rem` minimum | 400 | Filter labels, badges, metadata |

**Floor:** no text below `0.75rem` (12 px), ever. The prototype has
text as small as `0.42rem` (≈ 6.7 px) on the Experience page; this
must not survive into the WordPress build.

### Italic emphasis — a Sentral signature

The prototype's most distinctive typographic move is splitting
headlines into a declarative first clause and an italic continuation:

> Stay like it's already *your home.*
> Find your next home. *Elevated.*
> We operate communities where people *genuinely* want to be.
> Where great spaces meet *exceptional people.*
> What you get as a *member.*

Preserve this pattern in WordPress. Italic accents inherit the
`--text-accent` color on cream, `--gold` on dark.

### Line heights

- Display headings: `1.1`
- Body paragraphs: `1.6 – 1.8`
- Captions / eyebrows: `1.4`

---

## 3. Layout system

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

### Fixed nav

- Height: `64px`
- Background: `--black`
- Always sticky-fixed at top of viewport
- Border-bottom: `--rule` (subtle, near-invisible)

---

## 4. Component patterns

### Primary navigation

- Black bar, `SEN+RAL` wordmark left, link cluster center, CTA +
  hamburger right
- **Active link:** gold underline + white text
- **Inactive link:** 55% white, hover → 100% white
- **CTAs in nav** ("Book a Stay", "Login"): gold-tinted button
  background `#c8b89a`, text `#141414`. Never dark-on-dark.

### Hero — photo

Used on: Home, Stay, Live, Partner, Experience, Careers, Group
Business, SentralPlus.

Structure (left-aligned by default):
```
[Eyebrow: gold uppercase]
[Headline: display, large, italic continuation]
[Subtitle: body, 80%+ white opacity]
[Stats / CTAs (optional)]
```

Required treatment for legibility on photo backgrounds:
```css
text-shadow:
  0 0 18px rgba(0, 0, 0, 0.65),
  0 2px  8px rgba(0, 0, 0, 0.55),
  0 1px  2px rgba(0, 0, 0, 0.50);
```

The text-shadow creates a soft dark glow around the typography that
remains readable on any photo without dimming the image itself.

### Hero — typographic (no photo)

Used on: Live With Us (after carousel), Press, Privacy Policy,
Terms of Use.

- Black background, no photo
- Same eyebrow → headline → subtitle structure
- Often paired with a sticky filter bar or table-of-contents below

### Section eyebrow

- `0.75rem` minimum, weight 500, uppercase, letter-spacing
  0.18 – 0.24em
- Color: `--text-accent` on cream, `--gold` on dark
- Always sits `14 – 16px` above the section heading
- Examples: `"MEMBER BENEFITS"`, `"01 — BUSINESS TRAVEL"`,
  `"WHAT DRIVES US"`, `"FOR OWNERS & DEVELOPERS"`

### Cards

Property card, news card, value card all share:

- Photo top, content below
- Pinned badge top-left in pill shape (`"AVAILABLE"`,
  `"NEW — LEASING"`, `"AWARDS"`)
- City label uppercase, lighter weight
- Title in display serif, weight 300 – 400
- "View →" or "Read article →" CTA with arrow glyph

### Buttons

| Variant | Background | Text | Use |
|---|---|---|---|
| Primary on dark | `--white` | `--black` | "Join SentralPlus", "View Open Roles" |
| Primary on cream | `--black` | `--cream` | "Book a Stay" on cream sections |
| Secondary on dark | transparent + 1px white border | `--white` | "Learn more →" |
| Gold CTA | `--gold` | `--black` | Nav CTAs, schedule actions |

All buttons:
- Text: `0.85rem`, weight 400 – 500
- Padding: `14 – 16px` vertical, `22 – 28px` horizontal
- Border-radius: `2 – 3px` (very subtle)
- Hover: subtle background shift, no transform

### Forms

**On dark:**
- Inputs: 6% white fill, 20% gold border
- Focus: 50% gold border, 9% white fill
- Placeholder: 25% white

**On cream:**
- Inputs: white fill, light stone border
- Focus: bronze (`--text-accent`) border
- Placeholder: `--text-muted`

**Always:** pair every input with a visible `<label>`, not just a
placeholder. Placeholders disappear when typing.

### Filters / pills

Used on Live With Us (state filter) and Press (year + category):

- Active: black fill, white text
- Inactive: cream fill, dark text, light stone border
- Hover: border darkens to bronze
- Padding: `6 – 8px` vertical, `14 – 18px` horizontal
- Border-radius: full pill (999px)

### Map (Live With Us)

- Leaflet base map with grayscale + brightness filters applied:
  ```css
  filter: grayscale(0.3) brightness(0.92);
  ```
- Custom gold pins (`14 × 14px`, gold fill, gold halo)
- Popup on dark `--black` background, gold border, gold link text
- Pins must be keyboard-focusable and announce property + city to
  screen readers

---

## 5. Iconography

- Icons are **stroked, not filled**, `stroke-width: 1.5`
- Default size: `16px` or `20px`
- Use `stroke="currentColor"` so icons inherit the text color of
  their parent
- Exception: the gold key icon used on SentralPlus is filled (it's
  the only branded glyph in the system)

---

## 6. Imagery

### Photography direction

- **Editorial, hospitality-luxury.** Sunset / golden-hour exteriors,
  bright minimal interiors, candid lifestyle moments.
- **Avoid:** stock photography, posed corporate shots, harsh flash,
  oversaturated color grades.
- City labels accompany every property image: `"WEST PALM BEACH, FL — NORA"`

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

## 7. Voice & tone

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

## 8. Motion & interaction

- **Transitions:** `0.15 – 0.25s`, easing
  `cubic-bezier(.22, .68, 0, 1.2)` (the prototype's `--ease`)
- **No parallax**, no auto-playing carousels longer than 6 seconds
- **Hover states are subtle** — opacity shifts, color shifts, never
  jumps or bounces
- **Respect `prefers-reduced-motion: reduce`** — disable all
  movement-based animations for users who request it
- Carousels and image transitions: 4 – 6 second dwell, `0.6s` cross-fade

---

## 9. Accessibility floor (non-negotiable)

These are not aspirational — they're requirements. Full spec in
`ADA_BRIEF.md`.

- Minimum contrast: **4.5 : 1** on body text, **3 : 1** on large
  text
- Minimum font-size: **12 px** (`0.75rem`) — labels included
- Visible `:focus-visible` outline on every interactive element
- Every informational image has meaningful `alt`; decorative
  images have `alt=""`
- `<main>` landmark on every page
- Skip-to-content link as first focusable element
- 200% zoom must not cause horizontal scroll on body content
- Site must pass keyboard-only navigation
- Animations respect `prefers-reduced-motion`

---

## 10. Reference: corrected `:root{}` block

For copy-paste into the WordPress theme stylesheet:

```css
:root {
  /* Surfaces */
  --black:   #141414;
  --ink:     #1a1a1a;
  --cream:   #f5f3ef;
  --white:   #ffffff;

  /* Accents (decorative, dark-bg only) */
  --gold:    #c8b89a;
  --gold-d:  #2a1f10;
  --stone:   #d8d4ce;

  /* Text on cream */
  --text-body:   #3a3633;
  --text-muted:  #6b6560;
  --text-accent: #5e4a2c;

  /* Text on dark */
  --text-on-dark:       #ffffff;
  --text-on-dark-muted: rgba(255, 255, 255, 0.78);

  /* Rules */
  --rule:    rgba(255, 255, 255, 0.08);
  --ruleW:   rgba(0, 0, 0, 0.08);

  /* Type */
  --serif: "Cormorant Garamond", Georgia, serif;
  --sans:  "DM Sans", system-ui, sans-serif;

  /* Type floors */
  --fs-min-body:    1rem;     /* 16px */
  --fs-min-caption: 0.75rem;  /* 12px */

  /* Motion */
  --ease: cubic-bezier(0.22, 0.68, 0, 1.2);
}
```

---

## Questions / sign-off

For questions on any of the above, contact JCheshire@sentral.com.

This guide should be read alongside:
- `Sentral_WP_Developer_Brief.docx` — original WordPress
  implementation brief
- `ADA_BRIEF.md` — accessibility / WCAG correction spec
- The static prototype repo: https://github.com/Sentral2026/sentral-website
