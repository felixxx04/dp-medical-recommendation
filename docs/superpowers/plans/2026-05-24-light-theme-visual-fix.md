# Light Theme Visual Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix three-layer visual hierarchy: page background (darker) → cards (lighter, floating) → inset areas (deepest). Deepen neumorphic shadows by ~25% and increase chart contrast.

**Architecture:** Update CSS variable and Tailwind token values only. No logic changes, no new components. Foundation layer (2 files) first, then page-component fixes (5 files).

**Tech Stack:** React 18 + TypeScript + Tailwind CSS

---

## Phase 1: Foundation Tokens

### Task 1: Update tailwind.config.ts color & shadow tokens

**Files:**
- Modify: `tailwind.config.ts:19,22,50,62,66-69,80-82,106-114`

- [ ] **Step 1: Replace border, background, and surface token values**

```typescript
// Line 19: border
border: 'rgba(140,160,180,0.22)',

// Line 22: background
background: '#dde6f0',

// Line 50-52: muted.DEFAULT
muted: {
  DEFAULT: '#d2deea',
  foreground: '#5e7f92',
},

// Line 62-65: card.DEFAULT
card: {
  DEFAULT: '#e8eff7',
  foreground: '#0a2f2f',
},

// Line 66-71: surface
surface: {
  base: '#dde6f0',
  DEFAULT: '#dde6f0',
  elevated: '#edf3fa',
  inset: '#d2deea',
},
```

- [ ] **Step 2: Replace neu shadow colors**

```typescript
// Lines 80-82: neu
neu: {
  light: 'rgba(255,255,255,0.72)',
  dark: 'rgba(135,155,178,0.48)',
  'dark-hover': 'rgba(130,148,170,0.38)',
  'dark-subtle': 'rgba(125,142,165,0.28)',
},
```

- [ ] **Step 3: Replace boxShadow definitions using old shadow values**

Replace all occurrences of `rgba(148,168,195,0.38)` with `rgba(135,155,178,0.48)`, `rgba(138,160,188,0.28)` with `rgba(130,148,170,0.38)`, and `rgba(128,152,180,0.18)` with `rgba(125,142,165,0.28)` in lines 106-114.

```typescript
// Lines 106-114 (replace old rgba values with new ones)
'neu-raised': '5px 5px 12px rgba(135,155,178,0.48), -5px -5px 12px rgba(255,255,255,0.72)',
'neu-raised-hover': '7px 7px 16px rgba(130,148,170,0.38), -7px -7px 16px rgba(255,255,255,0.72)',
'neu-inset': 'inset 1.5px 1.5px 4px rgba(135,155,178,0.48), inset -1px -1px 3px rgba(255,255,255,0.72)',
'neu-inset-soft': 'inset 1px 1px 3px rgba(135,155,178,0.48), inset -0.5px -0.5px 2px rgba(255,255,255,0.72)',
'neu-pressed': 'inset 2px 2px 4px rgba(0,0,0,0.15)',
'btn-primary': '3px 3px 7px rgba(135,155,178,0.48), -2px -2px 5px rgba(255,255,255,0.72), 0 2px 6px rgba(8,145,178,0.2)',
'btn-primary-hover': '5px 5px 10px rgba(130,148,170,0.38), -3px -3px 7px rgba(255,255,255,0.72), 0 4px 12px rgba(8,145,178,0.3)',
'btn-glass': '3px 3px 7px rgba(135,155,178,0.48), -3px -3px 7px rgba(255,255,255,0.72)',
'btn-glass-hover': '4px 4px 9px rgba(130,148,170,0.38), -4px -4px 9px rgba(255,255,255,0.72)',
```

- [ ] **Step 4: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 5: Commit**

```bash
git add tailwind.config.ts
git commit -m "refactor: update color and shadow tokens for three-layer separation"
```

---

### Task 2: Update src/index.css CSS variables

**Files:**
- Modify: `src/index.css:14-17,19-21,28-29`

- [ ] **Step 1: Replace CSS variable values**

```css
/* Lines 14-17: Background tokens */
--bg: #dde6f0;
--bg-card: #e8eff7;
--bg-inset: #d2deea;
--bg-elevated: #edf3fa;

/* Lines 19-21: Shadow tokens */
--sh-l: rgba(255,255,255,0.72);
--sh-d: rgba(135,155,178,0.48);
--sh-d2: rgba(130,148,170,0.38);
--sh-d3: rgba(125,142,165,0.28);

/* Lines 28-29: Border tokens */
--border-subtle: rgba(140,160,180,0.16);
--border-default: rgba(140,160,180,0.22);
```

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/index.css
git commit -m "refactor: update CSS variables for three-layer separation"
```

---

## Phase 2: Page & Chart Fixes

### Task 3: Fix HomePage hero section background

**Files:**
- Modify: `src/pages/HomePage.tsx:41`

- [ ] **Step 1: Replace hero section className**

Old:
```tsx
<section className="relative overflow-hidden rounded-xl bg-gradient-to-br from-background via-surface to-surface-elevated border border-border">
```

New:
```tsx
<section className="relative overflow-hidden rounded-xl bg-gradient-to-br from-[#d2deea] to-[#dde6f0] border border-border">
```

- [ ] **Step 2: Verify compilation**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 3: Commit**

```bash
git add src/pages/HomePage.tsx
git commit -m "fix: give homepage hero section a distinct gradient background"
```

---

### Task 4: Fix chart component colors

**Files:**
- Modify: `src/pages/AdminDashboard.tsx` — CHART_TOOLTIP_STYLE object
- Modify: `src/pages/RecommendationStats.tsx` — chart tooltip/grid/axis colors + PIE_COLORS
- Modify: `src/components/charts/AgeDistributionChart.tsx` — CHART_TOOLTIP_STYLE + legend
- Modify: `src/components/charts/DiseaseDistributionChart.tsx` — CHART_TOOLTIP_STYLE + grid/axis

- [ ] **Step 1: Fix AdminDashboard.tsx chart colors**

Replace the `CHART_TOOLTIP_STYLE` object:
```typescript
const CHART_TOOLTIP_STYLE = {
  backgroundColor: '#edf3fa',
  border: '1px solid rgba(140,160,180,0.22)',
  borderRadius: '8px',
  fontSize: '12px',
  color: '#1a3244',
}
```

Also replace chart grid/axis colors:
- `stroke="rgba(255,255,255,0.08)"` → `stroke="rgba(140,160,180,0.25)"`
- `stroke="#64748b"` → `stroke="#4a6578"`
- `fill: '#94a3b8'` → `fill: '#4a6578'`
- `color: '#cbd5e1'` → `color: '#3d5f73'`

- [ ] **Step 2: Fix RecommendationStats.tsx chart colors**

Replace all chart tooltip `contentStyle` objects from dark `background: '#0f1d32'` to light `background: '#edf3fa'`:
```typescript
contentStyle={{ background: '#edf3fa', border: '1px solid rgba(140,160,180,0.22)', borderRadius: 4, fontSize: 12, color: '#1a3244' }}
```

Replace grid/axis strokes:
- `stroke="#1e293b"` → `stroke="rgba(140,160,180,0.25)"`
- `stroke="#64748b"` → `stroke="#4a6578"`
- `fill: '#cbd5e1'` → `fill: '#3d5f73'`

Replace line/bar fills:
- `stroke="#38bdf8"` → `stroke="#0891b2"`
- `fill="#38bdf8"` → `fill="#0891b2"`

Replace pie category picker colors:
- `background: '#1e293b'` → `background: '#edf3fa'`
- `color: '#94a3b8'` → `color: '#3d5f73'`
- `border: '1px solid #334155'` → `border: '1px solid rgba(140,160,180,0.22)'`

Replace legend formatter color:
- `color: '#cbd5e1'` → `color: '#3d5f73'`

Replace OTHER_COLOR: `'#475569'` → `'#5e7f92'`

- [ ] **Step 3: Fix AgeDistributionChart.tsx**

Replace `CHART_TOOLTIP_STYLE`:
```typescript
const CHART_TOOLTIP_STYLE = {
  backgroundColor: '#edf3fa',
  border: '1px solid rgba(140,160,180,0.22)',
  borderRadius: '8px',
  fontSize: '12px',
  color: '#1a3244',
}
```

Replace itemStyle: `color: '#f8fafc'` → `color: '#1a3244'`
Replace legend wrapperStyle: `color: '#cbd5e1'` → `color: '#3d5f73'`

- [ ] **Step 4: Fix DiseaseDistributionChart.tsx**

Same CHART_TOOLTIP_STYLE update, plus grid/axis color replacements:
- `stroke="rgba(155,175,200,0.12)"` → `stroke="rgba(140,160,180,0.25)"`
- `stroke="#5e7f92"` → `stroke="#4a6578"`
- ItemStyle: `color: '#f8fafc'` → `color: '#1a3244'`

- [ ] **Step 5: Final type check**

Run: `cd D:/grad_medical && npx tsc --noEmit 2>&1 | tail -5`
Expected: No type errors

- [ ] **Step 6: Commit**

```bash
git add src/pages/AdminDashboard.tsx src/pages/RecommendationStats.tsx src/components/charts/AgeDistributionChart.tsx src/components/charts/DiseaseDistributionChart.tsx
git commit -m "fix: update chart colors for light theme contrast"
```

---

## Phase 3: Verification

### Task 5: Build and visual verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run full build**

Run: `cd D:/grad_medical && npx vite build 2>&1 | tail -5`
Expected: Build succeeds

- [ ] **Step 2: Search for old token values**

Run: `cd D:/grad_medical && grep -rn "#e4ecf4" src/index.css src/pages/ src/components/ --include="*.tsx" --include="*.css" 2>/dev/null`
Expected: No matches in source (may appear in comments)

Run: `cd D:/grad_medical && grep -rn "rgba(148,168,195" src/ --include="*.tsx" --include="*.css" 2>/dev/null`
Expected: No matches

- [ ] **Step 3: Visual verification in browser**

Start dev server: `cd D:/grad_medical && npx vite --port 5173`

Check pages:
- `/` — Hero section has visible boundary, cards float above background
- `/review` — Components don't blend into background
- `/recommendation-stats` — Chart grid lines and labels are readable
- `/privacy` — SVG chart in trade-off section renders correctly

- [ ] **Step 4: Commit any final fixes**

```bash
git add -A
git commit -m "fix: light theme visual adjustments after verification"
```

---

## Self-Review Checklist

- [x] **Spec coverage:**
  - Color tokens (3 layers) → Task 1 + Task 2
  - Shadow tokens (deepen ~25%) → Task 1 + Task 2
  - Border tokens → Task 1 + Task 2
  - Hero section fix → Task 3
  - Chart system fix → Task 4
- [x] **No placeholders:** All steps contain exact hex/rgba values and precise line numbers
- [x] **Type consistency:** Token names match between tailwind.config.ts and index.css
- [x] **File paths:** All paths are exact and verified against the actual codebase
