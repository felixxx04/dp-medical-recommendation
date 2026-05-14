# Review Dashboard Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Optimize the review dashboard with sticky layout, modern styling, and auto-select next item after submit.

**Architecture:** Left-right split layout with sticky right panel. Left column has pending list with color bars and collapsible reviewed section. Right column has three-layer card structure (patient info, drug list, review actions). Auto-select next item after submission for fluent batch review.

**Tech Stack:** React 18, TypeScript, Tailwind CSS, existing UI components (Card), CSS variables from index.css

---

## File Structure

| File | Purpose |
|------|---------|
| `src/pages/ReviewDashboard.tsx` | Main page: layout restructure, stats bar, sticky right, collapsible reviewed, auto-select |
| `src/components/ReviewPanel.tsx` | Review form: Tailwind styles, three-layer cards, drug list with safety labels |

---

### Task 1: Update ReviewDashboard Layout Structure

**Files:**
- Modify: `src/pages/ReviewDashboard.tsx`

**Goal:** Restructure the page layout with stats bar, sticky right panel, and collapsible reviewed section.

- [ ] **Step 1: Add stats bar component at top**

Add a stats bar between the header section and the grid. This shows pending/done counts with badge styling.

```tsx
// After the header section (line 133), add:

      {/* Stats Bar */}
      <div className="flex items-center gap-4 px-1 mb-4">
        <span className="text-sm font-semibold text-foreground">推荐审核</span>
        <span className="ia-badge ia-badge-warning">
          <span className="w-1.5 h-1.5 rounded-full bg-orange-500"></span>
          待审核 {pendingReviews.filter(r => r.reviewStatus === 'pending').length}
        </span>
        <span className="ia-badge ia-badge-success">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
          已审核 {pendingReviews.filter(r => r.reviewStatus !== 'pending').length}
        </span>
      </div>
```

- [ ] **Step 2: Restructure grid to support sticky right panel**

Replace the existing grid structure (lines 137-188) with a new layout that supports sticky positioning.

```tsx
      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-[280px_1fr] gap-6" style={{ minHeight: 'calc(100vh - 280px)' }}>
        {/* Left Column: Pending List */}
        <div className="space-y-4">
          {/* Pending Section */}
          <div>
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-1">
              待审核
            </h3>
            <div className="space-y-1">
              {pendingReviews.filter(r => r.reviewStatus === 'pending').length === 0 && (
                <p className="text-sm text-muted-foreground text-center py-8">暂无待审核记录</p>
              )}
              {pendingReviews.filter(r => r.reviewStatus === 'pending').map(review => {
                const disease = parseInputDisease(review.inputData)
                const isSelected = selectedReview?.recommendationId === review.recommendationId
                return (
                  <div
                    key={review.recommendationId}
                    onClick={() => selectReview(review)}
                    className={`group flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-150 ${
                      isSelected
                        ? 'bg-white/[0.04] border-l-[3px] border-l-orange-500'
                        : 'border-l-[3px] border-l-transparent hover:bg-white/[0.02] hover:border-l-orange-500/50'
                    }`}
                  >
                    <div className={`w-[3px] h-8 rounded-full flex-shrink-0 ${
                      isSelected ? 'bg-orange-500' : 'bg-orange-500/60'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm text-foreground truncate">{disease || '未知疾病'}</div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        {new Date(review.createdAt).toLocaleDateString('zh-CN')}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Reviewed Section - Collapsible */}
          {pendingReviews.filter(r => r.reviewStatus !== 'pending').length > 0 && (
            <div className="border-t border-white/[0.06] pt-4">
              <button
                onClick={() => setReviewedExpanded(!reviewedExpanded)}
                className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors w-full px-1"
              >
                <span className={`transition-transform duration-200 ${reviewedExpanded ? 'rotate-90' : ''}`}>
                  ▶
                </span>
                已审核 ({pendingReviews.filter(r => r.reviewStatus !== 'pending').length})
              </button>
              {reviewedExpanded && (
                <div className="mt-2 space-y-1">
                  {pendingReviews.filter(r => r.reviewStatus !== 'pending').map(review => {
                    const disease = parseInputDisease(review.inputData)
                    return (
                      <div
                        key={review.recommendationId}
                        className="flex items-center gap-3 p-2.5 rounded-lg text-muted-foreground hover:bg-white/[0.02] transition-colors cursor-pointer"
                      >
                        <div className="w-[3px] h-6 rounded-full bg-slate-600 flex-shrink-0"></div>
                        <div className="flex-1 min-w-0">
                          <div className="text-xs truncate">{disease || '未知疾病'}</div>
                        </div>
                        <div className="text-xs text-muted-foreground/60">
                          {new Date(review.createdAt).toLocaleDateString('zh-CN')}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Sticky Detail Panel */}
        <div className="lg:sticky lg:top-4 lg:self-start">
          <div className="max-h-[calc(100vh-4rem)] overflow-y-auto">
            {detailLoading ? (
              <div className="p-8 text-center text-muted-foreground border border-dashed border-white/[0.06] rounded-xl">
                加载推荐详情...
              </div>
            ) : selectedReview ? (
              <ReviewPanel
                recommendationId={selectedReview.recommendationId}
                diseaseCn={diseaseCn}
                drugs={drugs}
                onSubmitReview={handleSubmitReview}
              />
            ) : (
              <div className="p-8 text-center text-muted-foreground border border-dashed border-white/[0.06] rounded-xl">
                选择左侧待审核记录查看详情
              </div>
            )}
          </div>
        </div>
      </div>
```

- [ ] **Step 3: Add reviewedExpanded state**

Add the state for collapsible reviewed section at the top of the component (after other useState hooks, around line 51):

```tsx
  const [reviewedExpanded, setReviewedExpanded] = useState(false)
```

- [ ] **Step 4: Implement auto-select next item after submit**

Update the `handleSubmitReview` function to auto-select the next pending item after submission:

```tsx
  const handleSubmitReview = async (
    decision: 'confirm' | 'modify' | 'reject',
    selectedDrug?: string,
    reason?: string,
    template?: string,
    advice?: string,
  ) => {
    if (!selectedReview) return
    try {
      await api.post('/api/review/log', {
        recommendationId: selectedReview.recommendationId,
        patientId: selectedReview.patientId,
        diseaseCn,
        diseaseStandardized: '',
        routingPath: '',
        systemDrugs: selectedReview.resultData,
        doctorDecision: decision,
        doctorSelectedDrug: selectedDrug || null,
        doctorReason: reason || null,
        treatmentTemplate: template || null,
        treatmentAdvice: advice || null,
      })
      
      // Refresh the list and auto-select next item
      const updatedList = await api.get<PendingReview[]>('/api/review/pending')
      setPendingReviews(updatedList)
      
      // Auto-select next pending item
      const pendingItems = updatedList.filter(r => r.reviewStatus === 'pending')
      if (pendingItems.length > 0) {
        const nextItem = pendingItems[0]
        selectReview(nextItem)
      } else {
        setSelectedReview(null)
      }
    } catch { setError('提交审核失败') }
  }
```

- [ ] **Step 5: Verify build succeeds**

Run: `npm run build`
Expected: Build completes without errors

- [ ] **Step 6: Commit Task 1 changes**

```bash
git add src/pages/ReviewDashboard.tsx
git commit -m "refactor: ReviewDashboard — sticky layout, stats bar, collapsible reviewed, auto-select next"
```

---

### Task 2: Update ReviewPanel with Three-Layer Cards and Tailwind Styles

**Files:**
- Modify: `src/components/ReviewPanel.tsx`

**Goal:** Convert inline styles to Tailwind, create three-layer card structure with patient info, drug list, and review actions.

- [ ] **Step 1: Rewrite ReviewPanel with Tailwind and three-layer structure**

Replace the entire content of `ReviewPanel.tsx`:

```tsx
import { useState } from 'react'

interface DrugOption {
  drugName: string
  englishName: string
  category: string
  safetyType: string
  score: number
}

interface ReviewPanelProps {
  recommendationId: number
  diseaseCn: string
  drugs: DrugOption[]
  onSubmitReview: (decision: 'confirm' | 'modify' | 'reject', selectedDrug?: string, reason?: string, template?: string, advice?: string) => void
}

const TREATMENT_TEMPLATES = [
  { name: '标准用法', text: '建议使用[药物名]，每日[N]次，每次[剂量]，连用[N]天。' },
  { name: '递增剂量', text: '起始剂量[小剂量]，根据耐受情况逐步调整至[目标剂量]。' },
  { name: '联合用药', text: '建议[药物A]联合[药物B]，注意监测[相互作用/不良反应]。' },
  { name: '对症治疗', text: '针对[症状]进行对症治疗，如症状持续或加重请及时复诊。' },
  { name: '自定义', text: '' },
]

export default function ReviewPanel({ 
  recommendationId: _recommendationId, 
  diseaseCn, 
  drugs, 
  onSubmitReview 
}: ReviewPanelProps) {
  const [decision, setDecision] = useState<'confirm' | 'modify' | 'reject' | null>(null)
  const [selectedDrug, setSelectedDrug] = useState('')
  const [reason, setReason] = useState('')
  const [selectedTemplate, setSelectedTemplate] = useState('')
  const [treatmentAdvice, setTreatmentAdvice] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = () => {
    if (!decision) return
    onSubmitReview(decision, selectedDrug || undefined, reason || undefined, selectedTemplate || undefined, treatmentAdvice || undefined)
    setSubmitted(true)
  }

  const handleTemplateChange = (name: string) => {
    setSelectedTemplate(name)
    if (name && name !== '自定义' && !treatmentAdvice.trim()) {
      setTreatmentAdvice(TREATMENT_TEMPLATES.find(t => t.name === name)?.text || '')
    }
  }

  const getSafetyColor = (safetyType: string) => {
    switch (safetyType) {
      case 'safe': return 'text-green-500'
      case 'warning': return 'text-amber-500'
      case 'danger': return 'text-red-500'
      default: return 'text-green-500'
    }
  }

  const getSafetyLabel = (safetyType: string) => {
    switch (safetyType) {
      case 'safe': return '安全'
      case 'warning': return '需关注'
      case 'danger': return '禁忌'
      default: return '安全'
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'bg-green-500/10 text-green-400'
    if (score >= 0.5) return 'bg-amber-500/10 text-amber-400'
    return 'bg-slate-500/10 text-slate-400'
  }

  if (submitted) {
    return (
      <div className="p-6 rounded-xl bg-green-500/10 border border-green-500/20 text-center">
        <span className="text-green-400 font-medium">审核已提交</span>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Layer 1: Patient Info Card */}
      <div className="p-4 rounded-xl bg-surface-elevated border border-white/[0.06]">
        <div className="text-lg font-semibold text-foreground mb-2">{diseaseCn || '未提供'}</div>
        <div className="text-sm text-muted-foreground mb-3">审核患者的用药推荐方案</div>
        {drugs.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {drugs.slice(0, 4).map((drug, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 text-xs rounded-md bg-brand-sky/10 text-brand-sky"
              >
                {drug.drugName}
              </span>
            ))}
            {drugs.length > 4 && (
              <span className="px-2 py-0.5 text-xs rounded-md bg-white/[0.04] text-muted-foreground">
                +{drugs.length - 4}种
              </span>
            )}
          </div>
        )}
      </div>

      {/* Layer 2: Drug List Card */}
      <div className="p-4 rounded-xl bg-surface-elevated border border-white/[0.06]">
        <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
          推荐药物
        </div>
        <div className="space-y-2">
          {drugs.map((drug, idx) => (
            <div
              key={idx}
              className="flex items-center gap-3 py-2 border-b border-white/[0.04] last:border-b-0"
            >
              <span className="flex-1 text-sm font-medium text-foreground">{drug.drugName}</span>
              <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${getScoreColor(drug.score)}`}>
                {drug.score.toFixed(2)}
              </span>
              <span className={`text-xs font-medium ${getSafetyColor(drug.safetyType)}`}>
                {getSafetyLabel(drug.safetyType)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Layer 3: Review Actions Card */}
      <div className="p-4 rounded-xl bg-surface-elevated border border-white/[0.06]">
        <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
          审核操作
        </div>

        {/* Decision Buttons */}
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setDecision('confirm')}
            className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-150 border ${
              decision === 'confirm'
                ? 'bg-green-500/15 text-green-400 border-green-500/40'
                : 'bg-transparent text-muted-foreground border-white/[0.08] hover:bg-green-500/5 hover:text-green-400 hover:border-green-500/20'
            }`}
          >
            确认
          </button>
          <button
            onClick={() => setDecision('modify')}
            className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-150 border ${
              decision === 'modify'
                ? 'bg-blue-500/15 text-blue-400 border-blue-500/40'
                : 'bg-transparent text-muted-foreground border-white/[0.08] hover:bg-blue-500/5 hover:text-blue-400 hover:border-blue-500/20'
            }`}
          >
            修改
          </button>
          <button
            onClick={() => setDecision('reject')}
            className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-150 border ${
              decision === 'reject'
                ? 'bg-red-500/15 text-red-400 border-red-500/40'
                : 'bg-transparent text-muted-foreground border-white/[0.08] hover:bg-red-500/5 hover:text-red-400 hover:border-red-500/20'
            }`}
          >
            拒绝
          </button>
        </div>

        {/* Modify: Drug Selector */}
        {decision === 'modify' && (
          <div className="mb-3">
            <label className="block text-xs text-muted-foreground mb-1.5">选择更合适的药物：</label>
            <select
              value={selectedDrug}
              onChange={e => setSelectedDrug(e.target.value)}
              className="w-full p-2.5 rounded-lg bg-surface border border-white/[0.08] text-sm text-foreground focus:outline-none focus:border-brand-sky/40"
            >
              <option value="">-- 选择药物 --</option>
              {drugs.map(d => (
                <option key={d.englishName} value={d.englishName}>
                  {d.drugName} ({d.category})
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Modify/Reject: Reason */}
        {(decision === 'modify' || decision === 'reject') && (
          <div className="mb-3">
            <label className="block text-xs text-muted-foreground mb-1.5">原因说明（可选）：</label>
            <textarea
              value={reason}
              onChange={e => setReason(e.target.value)}
              placeholder="请输入审核意见..."
              rows={2}
              className="w-full p-2.5 rounded-lg bg-surface border border-white/[0.08] text-sm text-foreground resize-none focus:outline-none focus:border-brand-sky/40 placeholder:text-muted-foreground/50"
            />
          </div>
        )}

        {/* Template + Advice */}
        {decision && (
          <div className="mb-4">
            <label className="block text-xs text-muted-foreground mb-1.5">诊疗建议模板（可选）：</label>
            <select
              value={selectedTemplate}
              onChange={e => handleTemplateChange(e.target.value)}
              className="w-full p-2.5 rounded-lg bg-surface border border-white/[0.08] text-sm text-foreground mb-2 focus:outline-none focus:border-brand-sky/40"
            >
              <option value="">-- 选择模板 --</option>
              {TREATMENT_TEMPLATES.map(t => (
                <option key={t.name} value={t.name}>{t.name}</option>
              ))}
            </select>
            <label className="block text-xs text-muted-foreground mb-1.5">诊疗建议（可编辑）：</label>
            <textarea
              value={treatmentAdvice}
              onChange={e => setTreatmentAdvice(e.target.value)}
              placeholder="请输入诊疗建议..."
              rows={3}
              className="w-full p-2.5 rounded-lg bg-surface border border-white/[0.08] text-sm text-foreground resize-none focus:outline-none focus:border-brand-sky/40 placeholder:text-muted-foreground/50"
            />
          </div>
        )}

        {/* Submit Button */}
        {decision && (
          <button
            onClick={handleSubmit}
            className="w-full py-2.5 rounded-lg bg-foreground text-background font-semibold text-sm transition-all duration-150 hover:bg-foreground/90"
          >
            提交审核
          </button>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Verify build succeeds**

Run: `npm run build`
Expected: Build completes without errors

- [ ] **Step 3: Verify TypeScript types are correct**

Run: `npx tsc --noEmit`
Expected: No type errors

- [ ] **Step 4: Commit Task 2 changes**

```bash
git add src/components/ReviewPanel.tsx
git commit -m "refactor: ReviewPanel — three-layer cards, Tailwind styles, drug list with safety labels"
```

---

### Task 3: Verify and Test the Complete Implementation

**Files:**
- None (verification only)

- [ ] **Step 1: Start development server**

Run: `npm run dev`

- [ ] **Step 2: Navigate to review page and verify layout**

1. Open http://localhost:5173/login
2. Login with `admin` / `admin123`
3. Navigate to /review
4. Verify:
   - Stats bar shows pending/done counts
   - Left column has pending list with orange color bars
   - Right column stays visible when scrolling left list
   - Clicking pending item updates right panel without scrolling
   - Reviewed section is collapsible

- [ ] **Step 3: Verify auto-select next item**

1. Select a pending item
2. Click "确认" and "提交审核"
3. Verify next pending item is auto-selected
4. If no more pending items, verify empty state is shown

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: verify review dashboard optimization — all features working"
```

---

## Self-Review Checklist

| Spec Requirement | Task | Status |
|------------------|------|--------|
| Stats bar with pending/done counts | Task 1, Step 1 | ✓ |
| Sticky right panel | Task 1, Step 2 | ✓ |
| Left column pending list with color bars | Task 1, Step 2 | ✓ |
| Collapsible reviewed section | Task 1, Steps 2-3 | ✓ |
| Auto-select next after submit | Task 1, Step 4 | ✓ |
| Three-layer card structure | Task 2, Step 1 | ✓ |
| Tailwind styles (no inline) | Task 2, Step 1 | ✓ |
| Drug list with safety labels | Task 2, Step 1 | ✓ |
| Modern button styles | Task 2, Step 1 | ✓ |
