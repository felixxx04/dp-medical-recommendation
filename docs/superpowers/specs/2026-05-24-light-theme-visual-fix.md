---
name: Light Theme Visual Fix — Layer Separation & Contrast Enhancement
date: 2026-05-24
status: approved
---

# Light Theme Visual Fix — 层次分离 & 对比度增强

## Problem

After the initial neumorphic light theme migration (2026-05-24), three issues emerged:

1. **Homepage hero section is invisible** — `background`, `card`, and `surface.base` all equal `#e4ecf4`. The hero section's gradient (`from-background via-surface to-surface-elevated`) uses three nearly-identical colors, making it indistinguishable from the page background.

2. **Cards blend into the page** — `--bg-card` = `--bg` = `#e4ecf4`. Neumorphic cards rely solely on subtle shadows for differentiation. On light backgrounds, the `box-shadow: 5px 5px 12px rgba(148,168,195,0.38)` is too faint to create clear visual hierarchy.

3. **Chart components are unreadable** — Grid lines (`rgba(155,175,200,0.12)`) are nearly invisible, axis tick labels (`#5e7f92`) lack contrast, and dark tooltip backgrounds (`#0f2744`) clash with the light theme.

## Root Cause

The design spec explicitly set `--bg-card: #e4ecf4` equal to `--bg: #e4ecf4` (line 31 of the spec: "Card surface (same as bg — neumorphic cards differentiate via shadow, not color)"). While correct in theory, the shadow intensity was calibrated for dark backgrounds and is too faint on light backgrounds.

## Decision

**Keep the blue-gray color direction.** Adjust tokens to create a three-layer visual hierarchy, deepen neumorphic shadows by ~25%, and fix chart contrast globally. **Palette J (original improved)** is selected.

## Design System

### Color Tokens — Three-Layer Separation

| Token | Old | New | Purpose |
|-------|-----|-----|---------|
| `--bg` / `background` | `#e4ecf4` | `#dde6f0` | Page background (darkest layer) |
| `--bg-card` / `card.DEFAULT` | `#e4ecf4` | `#e8eff7` | Card surface (middle — floats above bg) |
| `--bg-inset` / `surface.inset` | `#dae4ef` | `#d2deea` | Input fields, progress tracks (deepest inset) |
| `--bg-elevated` / `surface.elevated` | `#edf3fa` | No change | Hover/active states |
| `muted.DEFAULT` | `#dae4ef` | `#d2deea` | Match inline with inset |
| `surface.base` | `#e4ecf4` | `#dde6f0` | Match background |
| `surface.DEFAULT` | `#e4ecf4` | `#dde6f0` | Match background |

### Shadow Tokens — Deepen ~25%

| Token | Old | New |
|-------|-----|-----|
| `--sh-d` | `rgba(148,168,195,0.38)` | `rgba(135,155,178,0.48)` |
| `--sh-d2` (hover) | `rgba(138,160,188,0.28)` | `rgba(130,148,170,0.38)` |
| `--sh-d3` (subtle) | `rgba(128,152,180,0.18)` | `rgba(125,142,165,0.28)` |
| `neu-dark` (Tailwind) | `rgba(148,168,195,0.38)` | `rgba(135,155,178,0.48)` |
| `neu-dark-hover` | `rgba(138,160,188,0.28)` | `rgba(130,148,170,0.38)` |
| `neu-dark-subtle` | `rgba(128,152,180,0.18)` | `rgba(125,142,165,0.28)` |

### Border Tokens

| Token | Old | New |
|-------|-----|-----|
| `border` (Tailwind) | `rgba(155,175,200,0.18)` | `rgba(140,160,180,0.22)` |
| `--border-subtle` | `rgba(155,175,200,0.12)` | `rgba(140,160,180,0.16)` |
| `--border-default` | `rgba(155,175,200,0.18)` | `rgba(140,160,180,0.22)` |

### Unchanged Tokens

All brand colors, text colors, typography, and radius tokens remain unchanged:
- `primary`: `#0891b2`, `accent`: `#14b8a6`
- `foreground` / `--text-heading`: `#0a2f2f`
- `--text-body`: `#1a3244`
- `--text-secondary`: `#3d5f73`
- `--text-muted`: `#5e7f92`
- Light shadow (`--sh-l`): `rgba(255,255,255,0.72)` — unchanged

### Homepage Hero Section Fix

Replace the hero section background in `HomePage.tsx` (line 41):

```
Old: from-background via-surface to-surface-elevated border border-border
New: from-[#d2deea] to-[#dde6f0] border border-border
```

This gives the hero a distinct gradient background (slightly bluer and darker at the top) that clearly separates it from the page background.

### Chart System Fix

Update all hardcoded chart colors across `AdminDashboard.tsx`, `RecommendationStats.tsx`, `AgeDistributionChart.tsx`, and `DiseaseDistributionChart.tsx`:

| Element | Old | New |
|---------|-----|-----|
| Grid lines | `rgba(155,175,200,0.12)` | `rgba(140,160,180,0.25)` |
| Axis tick text | `#5e7f92` | `#4a6578` |
| Axis stroke | `#5e7f92` | `#4a6578` |
| Tooltip background | `#0f2744` / `#0f1d32` | `#edf3fa` |
| Tooltip text | `#f8fafc` | `#1a3244` |
| Tooltip border | `rgba(255,255,255,0.12)` / `#334155` | `rgba(140,160,180,0.22)` |
| Legend text | `#cbd5e1` | `#3d5f73` |

## Files to Modify

### Foundation (Phase 1)
1. **`tailwind.config.ts`** — 6 color tokens, 3 shadow tokens, 1 border token
2. **`src/index.css`** — 6 CSS variables, 3 shadow variables, 2 border variables

### Page Fixes (Phase 2)
3. **`src/pages/HomePage.tsx`** — Hero section background gradient (1 line)
4. **`src/pages/AdminDashboard.tsx`** — Chart tooltip/grid/axis colors
5. **`src/pages/RecommendationStats.tsx`** — Chart tooltip/grid/axis colors + PIE_COLORS
6. **`src/components/charts/AgeDistributionChart.tsx`** — Chart tooltip/legend colors
7. **`src/components/charts/DiseaseDistributionChart.tsx`** — Chart grid/axis/tooltip colors

## Migration Strategy

1. Update `tailwind.config.ts` token values
2. Update `src/index.css` CSS variables
3. Fix HomePage hero background
4. Fix all chart components
5. Build & visually verify

## Visual Quality Checks

- [ ] Homepage hero section has visible boundary against page background
- [ ] Cards clearly "float" above the page background
- [ ] Chart grid lines are visible at normal viewing distance
- [ ] Chart axis labels are readable
- [ ] Chart tooltips display correctly on light backgrounds
- [ ] Print output remains clear (shadows → borders in print)
