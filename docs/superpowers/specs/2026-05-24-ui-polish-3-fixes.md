---
name: UI Polish — Homepage Hero + SafetyChart + ReviewDashboard
date: 2026-05-24
status: approved
---

# UI Polish — 首页 Hero 重构 + 安全分层图颜色修复 + 审核页美化

## Problem

Three visual issues identified after the initial light theme migration and contrast fix:

1. **Homepage hero text position is too low** — `lg:p-16` padding plus `justify-center` pushes the headline "精准用药推荐 守护患者隐私" into the lower half of the hero section, leaving excessive blank space at the top.

2. **SafetyLayerChart has dark-theme leftovers** — `bg-slate-800/50` background on summary stat cards, `text-sky-400`/`text-amber-400`/`text-purple-400` text colors, `#1e293b` grid lines, and `#0f1d32` tooltip backgrounds are all dark-theme artifacts that clash with the light theme.

3. **ReviewDashboard UI lacks visual polish** — The pending review list is flat with minimal visual distinction between items. The ReviewPanel's three-layer cards lack depth. The confirm/modify/reject action buttons have weak visual differentiation.

## Decision

Three independent fixes targeting specific components. No design-system changes. Each fix is self-contained.

### Fix 1: Homepage Hero — Classic Two-Column Layout (方案 A)

Replace the current `flex-col justify-center` layout with a **left-text + right-visual** two-column arrangement.

**Before:**
```tsx
// HomePage.tsx line 48-101
<div className="relative z-10 grid lg:grid-cols-2 gap-8 p-8 md:p-12 lg:p-16">
  <div className="flex flex-col justify-center">
    <h1>...</h1>
    <p>...</p>
    <div className="flex flex-wrap gap-3">...</div>
  </div>
  <div className="flex items-center justify-center">
    <!-- small epsilon card -->
  </div>
</div>
```

**After:**
```tsx
<div className="relative z-10 flex flex-col lg:flex-row items-center gap-8 p-6 md:p-10 lg:p-12">
  {/* Left: Text block */}
  <div className="flex-1 lg:pr-8">
    <h1 className="text-3xl md:text-4xl lg:text-[2.5rem] font-extrabold text-foreground leading-[1.15] tracking-[-0.03em] mb-3">
      精准用药推荐<br />
      <span className="gradient-text">守护患者隐私</span>
    </h1>
    <p className="text-sm md:text-base text-muted-foreground max-w-lg mb-6 leading-relaxed">
      融合差分隐私技术与深度学习算法，在严格保护患者隐私的前提下，
      提供精准、安全、个性化的医疗用药推荐服务
    </p>
    <div className="flex flex-wrap gap-3 mb-6 lg:mb-0">
      {/* buttons */}
    </div>
  </div>

  {/* Right: Visual column — epsilon card + mini stats */}
  <div className="flex-shrink-0 flex flex-col items-center gap-4">
    <div className="w-44 h-52 rounded-xl bg-card shadow-neu-raised flex flex-col items-center justify-center gap-2">
      <div className="text-5xl font-extrabold text-primary">ε</div>
      <div className="text-[10px] text-accent tracking-[0.12em] uppercase font-semibold">Differential Privacy</div>
      <div className="w-16 h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />
      <div className="text-2xl font-bold text-foreground">≤ 1.0</div>
      <div className="text-xs text-muted-foreground">PRIVACY BUDGET</div>
    </div>
    {/* Mini stats under epsilon card */}
    <div className="grid grid-cols-2 gap-3 w-full">
      <div className="rounded-lg bg-card shadow-neu-raised px-4 py-2.5 text-center">
        <div className="text-lg font-bold text-primary">92%+</div>
        <div className="text-[10px] text-muted-foreground">推荐准确率</div>
      </div>
      <div className="rounded-lg bg-card shadow-neu-raised px-4 py-2.5 text-center">
        <div className="text-lg font-bold text-accent">5K+</div>
        <div className="text-[10px] text-muted-foreground">药物种类</div>
      </div>
    </div>
  </div>
</div>
```

Key changes:
- Remove `grid lg:grid-cols-2`, use `flex flex-col lg:flex-row`
- Reduce padding from `p-16` to `p-12`
- Add mini stat cards below the epsilon card to fill the right column visually
- Left text gets `lg:pr-8` for breathing room

After this change, the four-stat row below the hero (lines 103-119) becomes redundant. Remove the `<section className="grid grid-cols-2 lg:grid-cols-4 gap-4">` stats section since stats are now integrated into the hero. The remaining sections (features grid, CTA) stay unchanged.

### Fix 2: SafetyLayerChart — Light Theme Color Migration

Replace all dark-theme hardcoded colors in `src/components/SafetyLayerChart.tsx`.

| Line | Element | Old (dark) | New (light) |
|------|---------|-----------|-------------|
| 29 | Funnel colors | `['#0284c7', '#f59e0b', '#a855f7', '#22c55e']` | Unchanged (semantic colors, use at 15% alpha) |
| 76 | Funnel bg alpha | `+ '33'` (20% opacity) | `+ '22'` (13% opacity, softer on light bg) |
| 83 | Stage label | `text-foreground/80` | `text-foreground/90` |
| 101 | Grid stroke | `#1e293b` | `rgba(140,160,180,0.25)` |
| 102-103 | Axis stroke | `#64748b` | `#4a6578` |
| 103 | Tick fill | `'#cbd5e1'` | `'#3d5f73'` |
| 105 | Tooltip bg | `'#0f1d32'` | `'#edf3fa'` |
| 105 | Tooltip border | `'1px solid #334155'` | `'1px solid rgba(140,160,180,0.22)'` |
| 105 | Tooltip color | `'#e2e8f0'` | `'#1a3244'` |
| 120,124,128 | Summary cards bg | `bg-slate-800/50` | `bg-surface-inset rounded-lg shadow-neu-inset-soft p-2` |
| 121 | Excluded count text | `text-sky-400` | `text-primary font-bold` |
| 125 | Review count text | `text-amber-400` | `text-warning font-bold` |
| 129 | Avg excluded text | `text-purple-400` | `text-purple-600 font-bold` |

### Fix 3: ReviewDashboard + ReviewPanel — Visual Polish

Three targeted changes to improve visual hierarchy and distinction.

**a) ReviewDashboard — Left pending list items**

Add neumorphic card styling to pending items for clear click affordance:

```tsx
// Selected item (line 188-192)
className={`group flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 ${
  isSelected
    ? 'bg-card shadow-neu-raised border-l-[4px] border-l-primary'
    : 'border-l-[4px] border-l-transparent hover:bg-card/60 hover:shadow-neu-raised'
}`}
```

Remove the redundant `w-[3px] h-8 rounded-full` color bar div (lines 194-196) — the left border already serves as the active indicator.

**b) ReviewDashboard — Reviewed section (collapsible)**

Add neumorphic card wrapper and improve the expand toggle:

```tsx
<div className="border-t border-border pt-4">
  <button className="flex items-center gap-2 text-xs font-medium text-muted-foreground hover:text-foreground transition-colors w-full px-1 py-1">
    <span className={`transition-transform duration-200 ${reviewedExpanded ? 'rotate-90' : ''}`}>▶</span>
    已审核 ({count})
  </button>
  ...
</div>
```

**c) ReviewPanel — Drug list items + Action buttons**

- Drug list items: Use the `drug-item` CSS class from index.css for consistent neumorphic inset styling
- Active decision buttons: add `shadow-neu-raised` for depth, and stronger border colors:
  - Confirm: `bg-success/8 text-success border-success/25`  
  - Modify: `bg-primary/8 text-primary border-primary/25`
  - Reject: `bg-destructive/6 text-destructive border-destructive/20`
- Submit button: Keep as primary gradient button

## Files to Modify

1. `src/pages/HomePage.tsx` — Hero section re-layout (lines 40-119)
2. `src/components/SafetyLayerChart.tsx` — 12 color replacements
3. `src/pages/ReviewDashboard.tsx` — Pending list item styling (lines 185-206)
4. `src/components/ReviewPanel.tsx` — Drug items + action buttons

## Verification

- [ ] Homepage hero: text at top, two-column balanced, no excessive whitespace
- [ ] Homepage: redundant stats section removed (stats now in hero)
- [ ] SafetyLayerChart: all cards have light background, text is readable
- [ ] SafetyLayerChart: chart grid and axis labels visible
- [ ] ReviewDashboard: pending items have neumorphic depth
- [ ] ReviewDashboard: active item clearly distinguished via left border
- [ ] ReviewPanel: drug items use proper neumorphic inset style
- [ ] ReviewPanel: action buttons have clear visual hierarchy
