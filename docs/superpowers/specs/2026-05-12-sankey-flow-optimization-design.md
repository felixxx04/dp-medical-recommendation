# Sankey Flow Chart Optimization Design

## Problem

The admin stats page's Sankey flow chart (`SankeyFlowChart.tsx`) has a fixed 240px height. When selecting more than 2-3 diseases, flow lines and drug labels overlap and become unreadable. The right-side drug nodes crowd together with no way to inspect details.

## Solution Overview

Two-layer interaction model: card thumbnail + fullscreen modal with dynamic-height Sankey and detail panel.

## Layout

### Card View (existing, minimal change)

- Keep current 240px Sankey as-is
- Add "展开全屏 ↗" button to the card header
- Default disease selection stays Top 3
- Card state is independent from modal state

### Fullscreen Modal

- Overlay: 85vh × 90vw, centered, dark background
- Three sections from top to bottom:
  1. **Header bar** — title + close button (✕)
  2. **Disease tag selector** — 全选/全清 + individual disease tags, default: all selected
  3. **Main content** — left-right split:
     - **Left: Sankey chart** (flex: 1, min-width: 0)
     - **Right: Detail panel** (fixed 280px width)

## Sankey Chart Improvements

### Dynamic Height

- Chart height = `max(400px, nodeCount × 35px)`
- Container max-height = 85vh - header/tags height
- If content exceeds container, vertical scrollbar appears

### Zoom & Pan (roam)

- Enable ECharts `roam: true` for wheel zoom + drag pan
- Solves readability when all diseases selected — zoom into a region

### Disease-Colored Flow Lines

- Each disease gets a distinct color from a preset palette
- All flow lines originating from that disease use the same color
- Implementation: `lineStyle.color` as a function returning color based on source node name
- Color palette: `['#38bdf8', '#22d3ee', '#818cf8', '#f472b6', '#4ade80', '#fbbf24', '#fb923c', '#a78bfa', '#f87171', '#34d399']`

### Drug Label Truncation

- Drug names exceeding 6 characters are truncated with "…"
- Full name shown in tooltip on hover
- Full details always available in right panel on click

### ECharts Config Changes

```
roam: true
nodeAlign: 'left'
nodeWidth: 16
nodeGap: 14
label: { color: '#cbd5e1', fontSize: 11, formatter: truncate function }
lineStyle: { color: function(params) based on source disease, curveness: 0.5, opacity: 0.35 }
emphasis: { focus: 'adjacency' }
```

## Detail Panel

### Empty State

When no node is selected, show a placeholder: "点击 Sankey 中的节点查看关联详情"

### Content by Node Type

**Disease node clicked:**
- Header: disease name (colored)
- Section: recommended categories with counts
- Under each category: drug list with recommendation counts

**Category node clicked:**
- Header: category name
- Section: source diseases with percentage breakdown
- Section: drugs under this category with counts

**Drug node clicked:**
- Header: full drug name
- Section: parent category
- Section: source diseases with percentage breakdown
- Section: total recommendation count

### Data Source

The detail panel data is derived from the existing `FlowData` (nodes + links). No new backend API needed:

- From `links` array, find all links where `source` or `target` matches the clicked node index
- For disease→category links: group by category, then find category→drug links for drug details
- For category→drug links: group by drug, then trace back to source diseases
- For drug nodes: trace back via category to disease

### Panel Styling

- Fixed 280px width, flex column layout
- Drug/category list items: flex row, name left-aligned, count right-aligned
- Scrollable if content exceeds panel height
- Dark theme consistent with existing UI

## Interaction Flow

1. User opens admin stats page → sees card with current Sankey (Top 3 diseases)
2. User clicks "展开全屏 ↗" → modal opens, all diseases selected by default
3. Sankey renders with dynamic height, colored flow lines, zoom enabled
4. User can:
   - Toggle disease tags to filter the Sankey
   - Scroll/zoom the Sankey to explore dense areas
   - Click any Sankey node → right panel updates with details
   - Hover nodes → tooltip shows full info
5. User clicks ✕ or outside modal → closes, returns to card view

## Files to Modify

| File | Change |
|------|--------|
| `src/components/SankeyFlowChart.tsx` | Add modal toggle, extract Sankey into reusable render, add detail panel |
| `src/pages/RecommendationStats.tsx` | Pass expand button into card header |

## No Backend Changes

All data comes from the existing `/api/stats/recommendation-flow` endpoint. The detail panel derives its content from the same `FlowData` structure by traversing the links array.
