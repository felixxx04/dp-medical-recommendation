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
- **Glass**: Translucent white + backdrop-blur for buttons and overlays. The `rgba(255,255,255,0.38)` glass background is semitransparent over `#e4ecf4` — it produces a lighter surface, not a "pure white" fill, so it does not violate the no-pure-white rule.
- **Base color**: `#e4ecf4` (not pure white — a soft gray-blue with texture).

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg` | `#e4ecf4` | Page background |
| `--bg-card` | `#e4ecf4` | Card surface (same as bg — neumorphic cards differentiate via shadow, not color) |
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

- Font stack: `'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif` (unchanged from current)
- Heading color: `#0a2f2f` (deep teal-black)
- Body color: `#1a3244` (dark navy)
- Muted color: `#5e7f92` (visible gray-blue, NOT too light)

### Component Styles

#### Buttons (5 variants)

Old → New variant mapping:

| Old variant | New variant | Notes |
|-------------|-------------|-------|
| `default` | `primary` | Solid gradient, brand color |
| `destructive` | `danger-glass` | Glass with red tint |
| `outline` | `glass` | Glass effect with blur |
| `secondary` | `ghost` | Raised neumorphic bg |
| `ghost` | `ghost` | Same, raised neumorphic bg |
| `link` | removed | Use text + color instead |

| Variant | Background | Color | Shadow |
|---------|-----------|-------|--------|
| `btn-primary` | `linear-gradient(145deg, #0a9dc4, #077f9f)` | `#fff` | raised + brand glow |
| `btn-glass` | `rgba(255,255,255,0.35)` + blur(10px) | `var(--primary)` | raised + glass border `1px solid rgba(255,255,255,0.5)` |
| `btn-ghost` | `var(--bg-card)` | `var(--secondary)` | raised |
| `btn-success` | `linear-gradient(145deg, #06a873, #048a5e)` | `#fff` | raised + green glow |
| `btn-danger-glass` | `rgba(185,28,28,0.07)` + blur(8px) | `var(--danger)` | raised + border `1px solid rgba(185,28,28,0.1)` |

All buttons have:
- `::after` top highlight line: `position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent)`
- `:hover` — deeper shadow + translateY(-1px)
- `:active` — inset shadow (pressed effect)

#### Badges (5 variants)

All use light background + deep text color + border `1px solid` at matching low opacity:
- `badge-primary`: `rgba(8,145,178,0.08)` bg + `#0e7490` text + `rgba(8,145,178,0.1)` border
- `badge-success`: `rgba(5,150,105,0.07)` bg + `#059669` text + `rgba(5,150,105,0.1)` border
- `badge-warning`: `rgba(180,83,9,0.07)` bg + `#b45309` text + `rgba(180,83,9,0.1)` border
- `badge-danger`: `rgba(185,28,28,0.06)` bg + `#b91c1c` text + `rgba(185,28,28,0.08)` border
- `badge-info`: `rgba(3,105,161,0.06)` bg + `#0369a1` text + `rgba(3,105,161,0.08)` border

SafetyBadge.tsx maps its 4 semantic levels as:
- `safe` → `badge-success`
- `relative_contraindication` → `badge-warning`
- `off_label` → `badge-info`
- `unverified` → `badge-danger`

#### Cards

- Raised neumorphic: `background: var(--bg-card)` + dual shadow
- Hover: deeper shadow + translateY(-1px)
- Drug items (elements with class `drug-item` or in recommendation result lists): inset (recessed into the card)
- Drug items hover: emerge (raised shadow)

#### Input Fields

- Inset neumorphic: `background: var(--bg-inset)` + inset shadow
- Focus: stronger inset + `0 0 0 2px rgba(8,145,178,0.12)` ring
- Placeholder: `var(--muted)` = `#5e7f92`

#### Navigation

Structure change: wrap nav items in an inset container:
```html
<nav class="nav-wrap">  <!-- inset container: bg-card, inset shadow, border-radius, padding:3px -->
  <div class="nav-item active">...</div>  <!-- raised pill: bg, raised shadow -->
  <div class="nav-item">...</div>  <!-- flat: transparent bg, var(--secondary) -->
</nav>
```

#### Table

- Header: `background: var(--bg-inset)` + `inset 1px 1px 2.5px var(--sh-d), inset -0.5px -0.5px 2px var(--sh-l)`
- Rows: `border-bottom: 1px solid rgba(155,175,200,0.1)`, hover `background: rgba(8,145,178,0.03)`
- Text: body `var(--body)`, headers `var(--muted)`

#### Progress Bars

- Track: inset shadow (recessed channel)
- Primary fill: `linear-gradient(90deg, var(--primary), var(--accent))` + `box-shadow: 0 0 4px rgba(8,145,178,0.15)`
- Success fill: `linear-gradient(90deg, var(--success), #34d399)`
- Warning fill: `linear-gradient(90deg, var(--warning), #fbbf24)`

### Dark-theme CSS Cleanup

Remove or replace these dark-theme-specific classes from `index.css`:
- `section-dark` / `section-light` / `section-base` → replace with neumorphic `n-raised` / `n-flat`
- `ia-card-dark` → remove (use `n-raised` instead)
- `gradient-text` → keep but restyle for light bg
- `hero-circle-lg` / `hero-circle-md` / `hero-dot` → restyle borders/colors for light theme

### Tailwind `darkMode` Config

Remove `darkMode: ['class']` from `tailwind.config.ts` — no dark mode support needed.

### Print CSS Update

Update `@media print` in `index.css`:
```css
@media print {
  .no-print { display: none !important; }
  .print-area { break-inside: avoid; }
  body { background: #e4ecf4 !important; color: #1a3244 !important; }
  .n-raised { background: #e4ecf4 !important; box-shadow: none !important; border: 1px solid #c8d5e0 !important; }
  .n-inset { background: #dae4ef !important; box-shadow: none !important; border: 1px solid #c8d5e0 !important; }
  h1, h2, h3, h4 { color: #0a2f2f !important; }
  .gradient-text { background: none !important; -webkit-text-fill-color: #0891b2 !important; }
}
```

### Print Considerations

- Light background `#e4ecf4` prints as very light gray — readable
- Deep text colors print clearly as dark text
- Neumorphic shadows simplified to subtle borders in print
- Badges print as light-tinted rectangles with dark text — fully legible
- No pure-white or pure-black areas that cause printing issues

## Files to Modify

### Foundation (Phase 1)
1. **`tailwind.config.ts`** — Replace all colors, shadows, remove `darkMode`, add neumorphic utilities
2. **`src/index.css`** — CSS variables, neumorphic classes, replace dark-theme components, update print CSS

### UI Primitives (Phase 2)
3. **`src/components/ui/button.tsx`** — Remap variants: default→primary, destructive→danger-glass, outline→glass, secondary→ghost, remove link
4. **`src/components/ui/card.tsx`** — Neumorphic card with raised/inset variants
5. **`src/components/ui/input.tsx`** — Inset shadow style
6. **`src/components/SafetyBadge.tsx`** — Remap semantic levels to 5 badge variants

### Layout (Phase 3)
7. **`src/components/Layout.tsx`** — Header/footer/navigation with neumorphic nav-wrap

### Pages (Phase 4)
8. **`src/pages/HomePage.tsx`**
9. **`src/pages/DrugRecommendation.tsx`**
10. **`src/pages/PatientRecords.tsx`**
11. **`src/pages/PrivacyConfig.tsx`**
12. **`src/pages/AdminDashboard.tsx`**
13. **`src/pages/LoginPage.tsx`**
14. **`src/pages/DrugDatabase.tsx`**
15. **`src/pages/MyRecords.tsx`**
16. **`src/pages/ReviewDashboard.tsx`**
17. **`src/pages/RecommendationStats.tsx`**
18. **`src/pages/ForbiddenPage.tsx`**
19. **`src/components/ReviewPanel.tsx`**
20. **`src/components/ConsentDialog.tsx`**
21. **`src/components/Charts/*.tsx`**

## Migration Strategy

1. Update `tailwind.config.ts` and `src/index.css` first (foundation)
2. Update UI primitives (button, card, input, SafetyBadge)
3. Update Layout (header, nav, footer)
4. Update each page component (replace hardcoded dark colors with light theme tokens)
5. Test each page visually
6. Verify print output

## Anti-patterns to Avoid

- No colored edge strips on cards or stats
- No pure-white `#ffffff` backgrounds (use `#e4ecf4` or `#edf3fa`; glass `rgba(255,255,255,0.38)` is acceptable as it overlays the base color)
- No `rgba(255,255,255,0.1)` borders (invisible on light bg)
- No light-colored text on light backgrounds (minimum 4.5:1 contrast)
- No neon or bright colors as primary fills
