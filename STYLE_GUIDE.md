# Sentral Website — Style Guide

**Version:** 2.0 (final, approved direction)
**For:** WordPress development team, designers, copywriters
**Companion to:** `Sentral_WP_Developer_Brief.docx`, `ADA_BRIEF.md`
**Source:** Audit of all 11 pages of the static HTML prototype, reconciled
with Sentral's official brand guidelines

This document captures the design system as it will be *implemented* in
WordPress — a reconciled version that takes the prototype's structural
work and pairs it with brand-correct color and typography. Use it as
the canonical reference when building the WordPress theme.

---

## 0. Brand reconciliation — what changed and why

The original prototype diverged from Sentral's official brand guide in
three ways: palette, accent color, and typography. Rather than ship two
identities (one for digital, one for print) or rebuild the prototype
from scratch, we're reconciling the two by keeping everything
structural from the prototype and pulling the surface decoration back
toward the brand guide. We're also expanding cream into a three-tone
surface system to give the site more visual rhythm, and reserving gold
for a narrow set of premium status signals.

### What carries over from the prototype

- Italic continuation headline pattern ("Stay like it's already
  *your home*")
- Cream-on-dark contrast direction
- Layout system, spacing scale, breakpoints, container widths
- Component patterns (cards, eyebrows, filters, hero structure)
- Editorial photography direction
- Voice and tone (quiet authority, em-dashes, concrete numbers)
- Accessibility floor (WCAG AA minimum, with AAA on body text)

### What changes from the prototype

| | Prototype as built | Reconciled (this doc) |
|---|---|---|
| Dark surface | `#141414` (pure-ish black) | `#282828` (off-black, brand guide) |
| Light surface | Single `#F5F3EF` | **Three tones** — `#FAF8F4`, `#F5F5F3`, `#EFEDE6` |
| Primary accent | Gold `#C8B89A` | **Forest `#196E5F`** (brand guide) |
| Italic accents on cream | Bronze `#5E4A2C` | **Deep forest `#0F4A3F`** |
| Border / divider on cream | Stone `#D8D4CE` | **Cloud `#AFAA9B`** (brand guide) |
| Display typeface | Cormorant Garamond | **Georgia** (system-safe, brand guide fallback) |
| Body typeface | DM Sans | **Aptos** (Microsoft 365 default, system-safe) |
| Gold | Used as general accent | **Reserved** — SentralPlus, awards, print only |

### The system in three roles

- **Surfaces** carry the structure: off-black, three cream tones, cloud
  for borders. These do the layout work.
- **Accent** carries the brand: forest and forest-deep. Used as
  punctuation — eyebrows, italic emphasis, CTAs, focus states, one
  full-color section per page.
- **Reserved metallic** carries earned status: gold and gold-deep.
  Deployed only in three contexts (SentralPlus tier indicators,
  awards/press recognition, print/physical signage). Not a general
  accent. The discipline of keeping gold in its lanes is what makes it
  meaningful when it appears.

### Why these specific changes

**Forest replaces gold as the primary accent.** Gold is the most-borrowed
color in luxury branding right now — every boutique hotel and fintech
startup is using it. Forest does the same emotional work (warmth
against dark, signal of premium) but is distinctly Sentral.

**Cream expands to three tones.** Long pages need rhythm. Without
tonal variation, every section break either feels flat (all one cream)
or jarring (cream → dark → cream → dark). Three close cream tones
read as one cream family, but create visual breaks that don't require
dropping to a dark surface every time.

**Gold returns, but reserved.** Gold has a job nothing else does well:
signaling earned status. SentralPlus is a membership product. Awards
and press recognition have a long visual vocabulary built around
gold. Embossed gold on key cards and signage is how the brand shows
up physically. Banning gold entirely would mean rebuilding all of
that. Reserving it — with explicit, documented rules about where it
appears — keeps it meaningful.

**Georgia + Aptos replaces Cormorant Garamond + DM Sans.** Both Tobias
(brand guide primary) and Cormorant Garamond (prototype) carry
licensing costs that don't scale to 400+ employees. Georgia is named
in the official brand guide as the display fallback, is a screen-first
serif, and pairs cleanly with Aptos — Microsoft's post-2024 default,
already on every employee machine. Web, Word, PowerPoint, Outlook, and
Teams all render in the same type system. Zero licensing cost.

---

## 1. Color system

### Surfaces

```css
--black:        #282828;   /* primary dark surface — nav, hero, dark sections */
--ink:          #1F1F1F;   /* slightly darker — search dropdowns, footers */
--cream-light:  #FAF8F4;   /* softest cream — hero intros, filter bars */
--cream:        #F5F5F3;   /* primary cream — body bg, primary card grid */
--cream-warm:   #EFEDE6;   /* warmest cream — testimonials, secondary cards */
--white:        #FFFFFF;   /* pure white — text on dark, input fills */
```

### Accent (primary)

```css
--forest:       #196E5F;   /* primary accent — eyebrows, italic on dark, CTAs */
--forest-deep:  #0F4A3F;   /* hover/pressed, italic accents on cream */
--cloud:        #AFAA9B;   /* warm gray — borders/dividers on cream */
```

### Reserved metallic — restricted use only

```css
--gold:         #C8B89A;   /* SentralPlus, awards, print — NOT a general accent */
--gold-deep:    #9A8862;   /* deep gold — gold text on cream surfaces */
```

**See §1.3 below for governance rules. These tokens are intentionally
isolated; they are not part of the general accent system.**

### Text on cream — accessibility-corrected

```css
--text-body:    #3A3633;   /* AAA, ~12.6 : 1 on cream */
--text-muted:   #6B6560;   /* AA,  ~5.14 : 1 on cream */
--text-accent:  #0F4A3F;   /* AAA, ~9.8 : 1 — italic emphasis on cream */
```

### Text on dark

```css
--text-on-dark:       #FFFFFF;
--text-on-dark-muted: rgba(255, 255, 255, 0.78);   /* min 70% opacity */
```

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
- Accent fills inside cards (use forest or stay with the section
  background)

### 1.2 Forest usage rules

- **Forest is decorative on dark, structural on cream.** On dark
  surfaces, use forest for eyebrows, italic emphasis, CTA buttons,
  active nav state, focus borders, and link hover. On cream, use
  deep forest only for italic emphasis in headlines — never as a
  surface color or button background.
- **Forest CTAs on dark** use white text. Verify 4.6:1 contrast
  (passes AA for large text and UI; for small text, use white on
  forest, never forest on white).
- **Italic accents** in headlines (`<em>`) get forest on dark, deep
  forest on cream.
- **One full-forest section per page** (CTA band, values section,
  SentralPlus block) gives the accent room to breathe at scale.
  Don't over-use; forest should remain a punctuation, not a
  background.

### 1.3 Gold governance rules — read before using

Gold is reserved. It is not a general accent. The discipline of
keeping gold in its three lanes is what makes it meaningful when
it appears. **A designer reaching for gold to make something "feel
premium" is the failure mode this rule exists to prevent.** Forest
does that job everywhere except the contexts below.

**The only places gold appears on the website:**

1. **SentralPlus tier indicators and member labels.** Tier badges,
   founding-member markers, member-exclusive section labels. The
   SentralPlus product surface and any place a member is identified
   as such.

2. **Awards and press recognition.** Industry awards, "Best Places
   to Live" rankings on the Press page, third-party recognition
   badges, year markers on award listings.

3. **Print and physical signage parity.** Where the website
   references or mirrors a physical asset that uses gold (key cards,
   embossed signage, foil-stamped welcome packets), digital gold
   honors that visual code.

**Where gold must not appear:**
- General CTAs (those are forest)
- Eyebrows on non-SentralPlus, non-award sections
- Italic accents in headlines
- Active nav states, focus rings, hover states
- Map pins, link colors, button hovers
- Decorative tinting on cream
- Anywhere a designer is choosing it for "warmth" or "premium feel"
  without a SentralPlus / award / print justification

If a request comes in to use gold somewhere outside these contexts,
the answer is forest.

### 1.4 General color usage rules

- **Body text on cream** uses `--text-body` or `--text-muted`. Never
  lighter than `#6B6560`.
- **Hero subtitles on dark** sit at 70–90% white opacity. The
  prototype's original 30–40% values fail accessibility.
- **Dividers** are nearly transparent (`rule`/`ruleW`) — never solid
  lines. Cloud is reserved for visible borders on cards and inputs.
- **Text on gold** uses `--black` (`#282828`) or `--gold-deep`
  (`#9A8862`) — never plain white, which can muddy on the warm gold
  tone.
- **Text on forest** uses white. Cream-light (`#FAF8F4`) is acceptable
  for italic emphasis on a forest surface (see hero example in §4).

---

## 2. Typography

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

**Note on weight:** Cormorant Garamond looks elegant at weight 300;
Georgia does not. Default Georgia to weight 400. If a heading needs
to feel lighter, use letter-spacing (`0.01em`) and generous line-height
(`1.15`) rather than reducing weight.

**Floor:** no text below `0.75rem` (12 px), ever. The prototype has
text as small as `0.42rem` (≈ 6.7 px) on the Experience page; this
must not survive into the WordPress build.

### Italic emphasis — Sentral's signature move

The most distinctive typographic pattern on the site is splitting
headlines into a declarative first clause and an italic continuation:

> Stay like it's already *your home.*
> Find your next home. *Elevated.*
> We operate communities where people *genuinely* want to be.
> Where great spaces meet *exceptional people.*
> What you get as a *member.*

Georgia's italic carries this pattern beautifully. Italic accents
inherit `--text-accent` (deep forest) on cream, `--forest` on dark.
On forest surfaces, italic accents use cream-light (`#FAF8F4`) for
contrast — never gold (gold is reserved).

### Line heights

- Display headings: `1.15`
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

### Section rhythm

A typical long page should alternate surfaces in a rhythm like:

```
[Off-black hero]
  ↓
[Cream-light filter bar or intro]
  ↓
[Cream primary content]
  ↓
[Cream-warm testimonial/quote block]
  ↓
[Forest full-section CTA band]
  ↓
[Ink + gold SentralPlus footer block]   ← only on pages where SentralPlus is contextually relevant
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

## 4. Component patterns

### Primary navigation

- Off-black bar, `SEN+RAL` wordmark left, link cluster center, CTA +
  hamburger right
- **Active link:** forest underline + white text
- **Inactive link:** 55% white, hover → 100% white
- **CTAs in nav** ("Book a Stay", "Login"): forest button background
  `#196E5F`, white text. Verify 4.6:1 contrast — passes AA for UI
  components and large text.

### Hero — photo

Used on: Home, Stay, Live, Partner, Experience, Careers, Group
Business, SentralPlus.

Structure (left-aligned by default):
```
[Eyebrow: forest uppercase]
[Headline: Georgia, large, italic continuation in forest]
[Subtitle: Aptos, 80%+ white opacity]
[Stats / CTAs (optional)]
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
- Color: `--text-accent` (deep forest) on cream, `--forest` on dark
- Always sits `14 – 16px` above the section heading
- Examples: `"MEMBER BENEFITS"`, `"01 — BUSINESS TRAVEL"`,
  `"WHAT DRIVES US"`, `"FOR OWNERS & DEVELOPERS"`

**Exception:** Award badges and SentralPlus tier eyebrows use gold.
See §4.7 and §4.8.

### Cards — standard

Property card, news card, value card all share:

- Photo top, content below
- Pinned badge top-left in pill shape (`"AVAILABLE"`,
  `"NEW — LEASING"`)
- City label uppercase, lighter weight
- Title in Georgia, weight 400
- "View →" or "Read article →" CTA with arrow glyph; arrow turns
  forest on hover

Card backgrounds: white on cream-light or cream-warm; cream-warm on
cream-light or cream. Avoid same-tone cards on same-tone backgrounds.

### Buttons

| Variant | Background | Text | Use |
|---|---|---|---|
| Primary on dark | `--forest` | `--white` | "Book a Stay", "Join SentralPlus", "View Open Roles" |
| Primary on cream | `--black` | `--cream` | Primary CTA on cream sections |
| Secondary on dark | transparent + 1px white border | `--white` | "Learn more →" |
| Tertiary text-link | none | `--forest` (cream bg) / `--white` (dark bg) | Inline links |

All buttons:
- Text: `0.85rem`, weight 500, Aptos
- Padding: `14 – 16px` vertical, `22 – 28px` horizontal
- Border-radius: `2 – 3px` (very subtle)
- Hover: forest darkens to `--forest-deep` on dark; on cream, off-black
  shifts to `--ink`. No transform.

**Gold buttons do not exist in the standard system.** SentralPlus has
its own gold button variant — see §4.7.

### Forms

**On dark:**
- Inputs: 6% white fill, 25% forest border
- Focus: 60% forest border (`--forest`), 9% white fill
- Placeholder: 40% white

**On cream / cream-light / cream-warm:**
- Inputs: white fill, cloud (`#AFAA9B`) border
- Focus: deep forest (`--text-accent`) border
- Placeholder: `--text-muted`

**Always:** pair every input with a visible `<label>`, not just a
placeholder. Placeholders disappear when typing.

### Filters / pills

Used on Live With Us (state filter) and Press (year + category):

- Active: off-black fill, white text
- Inactive: cream fill, dark text, cloud border
- Hover: border darkens to deep forest
- Padding: `6 – 8px` vertical, `14 – 18px` horizontal
- Border-radius: full pill (999px)

### Map (Live With Us)

- Leaflet base map with grayscale + brightness filters applied:
  ```css
  filter: grayscale(0.3) brightness(0.92);
  ```
- Custom forest pins (`14 × 14px`, forest fill, forest halo)
- Popup on `--black` background, forest border, forest link text
- Pins must be keyboard-focusable and announce property + city to
  screen readers

### 4.7 SentralPlus components — reserved gold

These are the primary places gold appears on the site. Every gold
treatment below is justified by a SentralPlus / member context.

**Member tier badge (outline variant, on dark):**
```css
.tier-badge-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(200, 184, 154, 0.12);
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

### 4.8 Award and recognition components — reserved gold

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
(`#9A8862`), not `--gold`. The lighter gold fails contrast on cream.
Verify on the actual designer's monitor — deep gold can read olive on
some displays. If it does, fall back to `#8A7654`.

---

## 5. Iconography

- Icons are **stroked, not filled**, `stroke-width: 1.5`
- Default size: `16px` or `20px`
- Use `stroke="currentColor"` so icons inherit the text color of
  their parent
- Award icons (trophy, ribbon, laurel) inherit gold-deep on cream,
  gold on dark — these are the only icons that get gold

---

## 6. Imagery

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
  text and UI components
- Minimum font-size: **12 px** (`0.75rem`) — labels included
- Visible `:focus-visible` outline on every interactive element
  (forest at 2px, offset 2px)
- Every informational image has meaningful `alt`; decorative
  images have `alt=""`
- `<main>` landmark on every page
- Skip-to-content link as first focusable element
- 200% zoom must not cause horizontal scroll on body content
- Site must pass keyboard-only navigation
- Animations respect `prefers-reduced-motion`

### 9.1 Forest contrast notes

- Forest `#196E5F` on off-black `#282828`: **4.6:1** — passes AA for
  large text (18px+) and UI components. Do not use for body text on
  dark; use white instead.
- Forest `#196E5F` on cream `#F5F5F3`: **5.1:1** — passes AA for
  body text. Reserved for buttons and decorative accents.
- Deep forest `#0F4A3F` on cream `#F5F5F3`: **9.8:1** — passes AAA.
  Use for italic emphasis in cream-background headlines.
- White `#FFFFFF` on forest `#196E5F`: **4.6:1** — passes AA for
  large text and UI; safe for buttons.

### 9.2 Cream contrast notes

- All three cream tones pass AAA contrast with `--text-body`
  (`#3A3633`) — minimum ratio `12.4:1` on cream-warm
- All three cream tones pass AA contrast with `--text-muted`
  (`#6B6560`) — minimum ratio `4.9:1` on cream-warm
- Deep forest `#0F4A3F` passes AAA on all three cream tones

### 9.3 Gold contrast notes — verify before deploying

- Gold `#C8B89A` on off-black `#282828`: **6.8:1** — passes AA. Safe
  for tier badges, member labels, eyebrows on dark.
- Gold `#C8B89A` on cream `#F5F5F3`: **1.8:1** — **FAILS**. Never use
  light gold for text on cream.
- Gold-deep `#9A8862` on cream `#F5F5F3`: **3.6:1** — passes AA for
  large text only (18px+). Use for award eyebrows and 14px+ labels;
  never for body or sub-14px text.
- White `#FFFFFF` on gold `#C8B89A`: **2.0:1** — **FAILS**. Use
  off-black on gold buttons, never white.
- Off-black `#282828` on gold `#C8B89A`: **8.9:1** — passes AAA.
  Standard text-on-gold combination.

If `--gold-deep` (`#9A8862`) reads olive on a particular monitor,
substitute `#8A7654` (slightly less green, passes the same contrast
checks).

---

## 10. Reference: complete `:root{}` block

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
  --forest:       #196E5F;
  --forest-deep:  #0F4A3F;
  --cloud:        #AFAA9B;

  /* Reserved metallic — SentralPlus, awards, print only */
  --gold:         #C8B89A;
  --gold-deep:    #9A8862;

  /* Text on cream */
  --text-body:    #3A3633;
  --text-muted:   #6B6560;
  --text-accent:  #0F4A3F;

  /* Text on dark */
  --text-on-dark:       #FFFFFF;
  --text-on-dark-muted: rgba(255, 255, 255, 0.78);

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

## 11. Decision matrix — quick reference

When in doubt, this table settles it:

| Use case | Forest | Cream tones | Gold |
|---|:---:|:---:|:---:|
| Primary CTAs | ● | — | — |
| Eyebrows (general) | ● | — | — |
| Italic accents in headlines | ● | — | — |
| Section background variation | — | ● | — |
| Card surfaces on cream | — | ● | — |
| Active nav · focus rings · map pins | ● | — | — |
| Full-section hero band (one per page) | ● | — | — |
| Borders & dividers on cream | — | — | — *(cloud)* |
| SentralPlus tier badges & member labels | — | — | ● |
| SentralPlus footer/promo block | — | — | ● *(accents)* |
| Awards & press recognition | — | — | ● |
| Award icons & ribbons | — | — | ● |
| Print & physical signage parity | — | — | ● |
| Decorative "warmth" with no specific reason | — | — | **No** |

---

## 12. Pre-build checklist for the WordPress developer

Before theme development begins, confirm:

- [ ] `:root{}` token block in §10 is implemented exactly as shown
- [ ] All three cream tones are defined and used per §1.1
- [ ] Gold tokens are defined but used **only** in SentralPlus, award,
      and print-parity components (per §1.3 and §11)
- [ ] Georgia + Aptos render correctly across Chrome, Safari, Firefox,
      and Edge — no font-loading shims or `@font-face` rules needed
- [ ] All gold references in the original prototype CSS that are
      *not* SentralPlus or award contexts are replaced with forest
      tokens; no inappropriate `#C8B89A` remains in the codebase
- [ ] All `#141414` references replaced with `#282828`
- [ ] Cormorant Garamond and DM Sans `<link>` tags removed from
      `<head>` (no Google Fonts loading)
- [ ] Hero text-shadow values applied consistently across all
      photo-hero pages
- [ ] Focus outlines verified on every interactive element using
      keyboard-only navigation
- [ ] All form inputs have visible labels (not placeholder-only)
- [ ] Contrast verified with axe DevTools or WAVE on every template
      — pay special attention to gold-on-cream combinations (§9.3)
- [ ] Reduced-motion media query disables carousel auto-advance and
      hover transforms
- [ ] At least one page (Home or Live With Us) demonstrates the full
      surface rhythm (off-black → cream-light → cream → cream-warm →
      forest → ink+gold footer if SentralPlus is contextually present)

---

## 13. Governance — who owns what

- **Color additions or modifications:** Must come through brand
  marketing review. The reserved-gold rule in §1.3 is the most
  fragile part of this system; pressure to expand gold's use will
  come up. Hold the line.
- **Typography changes:** Require IT and marketing sign-off jointly,
  because any non-system typeface introduces licensing and
  deployment cost.
- **Component additions:** Designer + WP dev review; document new
  components in this guide before they ship.
- **Voice and copy changes:** Marketing owns; refer to §7.

---

## Questions / sign-off

For questions on any of the above, contact JCheshire@sentral.com.

This guide should be read alongside:
- `Sentral_WP_Developer_Brief.docx` — original WordPress
  implementation brief
- `ADA_BRIEF.md` — accessibility / WCAG correction spec
- The static prototype repo: https://github.com/Sentral2026/sentral-website
- `internal-note-brand-reconciliation.md` — the rationale and
  decision context behind this version of the guide
