---
name: Light Theme Migration Design
date: 2026-05-24
status: approved
---

# Light Theme Migration — Neumorphic Medical Light

## Problem

Current dark theme (`#060f1e` base) prints poorly in academic papers — dark backgrounds become gray, light text becomes illegible, and card borders are nearly invisible in black-and-white print.

## Decision

Migrate the entire frontend from dark theme to a **Neumorphic Medical Light** theme. No dark/light toggle — single light theme for all pages.

## Design System

### Style: Neumorphism + Glass

- **Neumorphism**: Soft raised/inset effects via dual box-shadows (light + dark). No hard borders, no colored edge strips.
- **Glass**: Translucent white + backdrop-blur for buttons and overlays.
- **Base color**: `#e4ecf4` (not pure white — a soft gray-blue with texture).

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg` | `#e4ecf4` | Page background, card surface |
| `--bg-inset` | `#dae4ef` | Input fields, progress tracks, inset areas |
| `--bg-elevated` | `#edf3fa` | Hover states, elevated surfaces |
| `--primary` | `#0891b2` | Primary buttons, active nav, links |
| `--primary-hover` | `#0e7490` | Hover state for primary |
| `--primary-light` | `#22d3ee` | Light accent (gradients) |
| `--accent` | `#14b8a6` | Secondary brand, gradients |
| `--heading` | `#0a2f2f` | H1-H6 text |
| `--body` | `#1a3244` | Body text, table cells |
| `--secondary` | `#3d5f73` | Secondary text, labels |
| `--muted` | `#5e7f92` | Captions, disabled text |
| `--success` | `#059669` | Safe badges, success buttons |
| `--warning` | `#b45309` | Review-needed badges |
| `--danger` | `#b91c1c` | Contraindication badges |
| `--info` | `#0369a1` | Info badges |
| `--border` | `rgba(155,175,200,0.18)` | Subtle dividers |

### Shadow System

```css
/* Light shadow (top-left highlight) */
--sh-l: rgba(255,255,255,0.72);

/* Dark shadow (bottom-right depth) */
--sh-d: rgba(148,168,195,0.38);
--sh-d2: rgba(138,160,188,0.28);  /* hover */
--sh-d3: rgba(128,152,180,0.18);  /* subtle */
```

**Raised (cards, stat items):**
```css
box-shadow: 5px 5px 12px var(--sh-d), -5px -5px 12px var(--sh-l);
```

**Inset (inputs, progress tracks, drug items):**
```css
box-shadow: inset 1.5px 1.5px 4px var(--sh-d), inset -1px -1px 3px var(--sh-l);
```

**Pressed (button:active):**
```css
box-shadow: inset 2px 2px 4px rgba(0,0,0,0.15);
transform: translateY(0);
```

**Glass:**
```css
background: rgba(255,255,255,0.38);
backdrop-filter: blur(14px);
border: 1px solid rgba(255,255,255,0.55);
```

### Typography

- Font stack: `'Inter', 'Noto Sans SC', -apple-system, sans-serif` (unchanged)
- Heading color: `#0a2f2f` (deep teal-black)
- Body color: `#1a3244` (dark navy)
- Muted color: `#5e7f92` (visible gray-blue, NOT too light)

### Component Styles

#### Buttons (5 variants)

| Variant | Background | Color | Shadow |
|---------|-----------|-------|--------|
| `btn-primary` | `linear-gradient(145deg, #0a9dc4, #077f9f)` | `#fff` | raised + brand glow |
| `btn-glass` | `rgba(255,255,255,0.35)` + blur | `var(--primary)` | raised + glass border |
| `btn-ghost` | `var(--bg-card)` | `var(--secondary)` | raised |
| `btn-success` | `linear-gradient(145deg, #06a873, #048a5e)` | `#fff` | raised + green glow |
| `btn-danger-glass` | `rgba(185,28,28,0.07)` + blur | `var(--danger)` | raised + red border |

All buttons have:
- `::after` pseudo-element with top highlight line
- `:hover` — deeper shadow + translateY(-1px)
- `:active` — inset shadow (pressed effect)

#### Badges (5 variants)

All use light background + deep text color + thin border:
- `badge-primary`: `rgba(8,145,178,0.08)` bg + `#0e7490` text
- `badge-success`: `rgba(5,150,105,0.07)` bg + `#059669` text
- `badge-warning`: `rgba(180,83,9,0.07)` bg + `#b45309` text
- `badge-danger`: `rgba(185,28,28,0.06)` bg + `#b91c1c` text
- `badge-info`: `rgba(3,105,161,0.06)` bg + `#0369a1` text

#### Cards

- Raised neumorphic: `background: var(--bg-card)` + dual shadow
- Hover: deeper shadow + translateY(-1px)
- Drug items: inset (recessed into the card)
- Drug items hover: emerge (raised shadow)

#### Input Fields

- Inset neumorphic: `background: var(--bg-inset)` + inset shadow
- Focus: stronger inset + `0 0 0 2px rgba(8,145,178,0.12)` ring
- Placeholder: `var(--muted)` = `#5e7f92`

#### Navigation

- Wrapped in inset container (concave track)
- Active item: raised pill (convex, popping out)
- Inactive: flat, `var(--secondary)` color

#### Table

- Header: inset background with recessed effect
- Rows: subtle bottom border, hover highlight
- Text: body text `var(--body)`, headers `var(--muted)`

#### Progress Bars

- Track: inset shadow (recessed channel)
- Fill: gradient `var(--primary) → var(--accent)` + subtle glow
- Variants: success gradient, warning gradient

### Print Considerations

- Light background `#e4ecf4` prints as very light gray — readable
- Deep text colors print clearly as dark text
- Neumorphic shadows print as subtle gray gradients — add depth without obscuring content
- Badges print as light-tinted rectangles with dark text — fully legible
- No pure-white or pure-black areas that cause printing issues

## Files to Modify

1. **`tailwind.config.ts`** — Replace all colors, shadows, add neumorphic utilities
2. **`src/index.css`** — CSS variables, neumorphic classes, component overrides
3. **`src/components/ui/button.tsx`** — Add `glass` and `ghost` variants
4. **`src/components/ui/card.tsx`** — Neumorphic card variants
5. **`src/components/ui/input.tsx`** — Inset shadow style
6. **`src/components/Layout.tsx`** — Header/footer/navigation
7. **All page components** — Replace hardcoded dark colors with light theme tokens

## Migration Strategy

1. Update `tailwind.config.ts` and `src/index.css` first (foundation)
2. Update UI primitives (button, card, input, badge)
3. Update Layout (header, nav, footer)
4. Update each page component
5. Test each page visually
6. Verify print output

## Anti-patterns to Avoid

- No colored edge strips on cards or stats
- No pure-white `#ffffff` backgrounds (use `#e4ecf4` or `#edf3fa`)
- No `rgba(255,255,255,0.1)` borders (invisible on light bg)
- No light-colored text on light backgrounds (minimum 4.5:1 contrast)
- No neon or bright colors as primary fills
