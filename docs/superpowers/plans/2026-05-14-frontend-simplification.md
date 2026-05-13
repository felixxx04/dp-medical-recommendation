# Frontend Page Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce visual clutter on 4 frontend pages (DrugRecommendation, PatientRecords, AdminDashboard, PrivacyConfig) by moving non-essential info into expandable sections, merging redundant displays, and simplifying card headers — with zero information loss.

**Architecture:** All changes are purely presentational (JSX restructuring, CSS adjustments, adding collapse/expand state). No backend changes. No new components needed — reuse existing `TextExpander`, `Accordion`, and simple `useState` toggles already in the codebase.

**Tech Stack:** React 18, TypeScript, Tailwind CSS, existing UI primitives (Card, Button, Accordion, TextExpander)

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `src/pages/DrugRecommendation.tsx` | Modify | Simplify drug cards, collapse excluded drugs, merge stats |
| `src/pages/PatientRecords.tsx` | Modify | Merge stat cards, collapse charts, simplify card header, add form steps |
| `src/pages/AdminDashboard.tsx` | Modify | Add tab navigation, merge admin+stats row, simplify ledger |
| `src/pages/PrivacyConfig.tsx` | Modify | Collapse algorithm/research, restructure sliders, merge metrics |

---

## Task 1: DrugRecommendation — Simplify Drug Card Badges

**Files:**
- Modify: `src/pages/DrugRecommendation.tsx` (lines ~851-950, drug card header area)

- [ ] **Step 1: Remove non-essential badges from drug card header**

In the drug card JSX (around line 851-950), remove the inline badge rendering for:
- `evidenceLevel` badge (lines ~857-870)
- `reviewStatus` badge (lines ~871-893)
- `mode` badge (lines ~897-904)
- `qualityWarning` badge (lines ~910-914)

Keep these 4 badges in the card header:
- `SafetyBadge` (already rendered, line 856)
- Category badge (lines ~922-924)
- `requiresReview` badge (lines ~905-909)
- `dpAnomaly` badge (lines ~915-919)

The removed badges will be re-added in Task 2 inside the detail panel.

- [ ] **Step 2: Remove score breakdown, routing path, and safety warning from card**

From the drug card body (lines ~962-1031), remove:
- Score breakdown section (lines ~969-1006) — the `rawScore → DP score → noise → confidence interval` block
- DP anomaly inline warning (lines ~1008-1014) — already shown as a badge
- Routing path box (lines ~932-947) — the "推荐路径：疾病匹配→..." box
- Warnings list (lines ~1017-1022)

Also remove the standalone "⚠ 需医生审核" text (lines ~963-967) since `requiresReview` badge already conveys this.

The card body should now contain only: drug name + badges, english name, dosage/frequency, confidence %, and progress bar.

- [ ] **Step 3: Verify DrugRecommendation page renders in browser**

Run: `npm run dev`
Open http://localhost:5173/recommendation, log in, generate recommendations, confirm:
- Drug cards show only 4 badges max (safety, category, requiresReview, dpAnomaly)
- No score breakdown, routing path, or warnings visible on card
- Cards are visually cleaner with less vertical space

- [ ] **Step 4: Commit**

```bash
git add src/pages/DrugRecommendation.tsx
git commit -m "refactor: simplify drug card badges — keep only safety, category, requiresReview, dpAnomaly"
```

---

## Task 2: DrugRecommendation — Move Details to Detail Panel + Collapse Excluded Drugs

**Files:**
- Modify: `src/pages/DrugRecommendation.tsx` (lines ~1130-1310, detail panel area)

- [ ] **Step 1: Move DP comparison table into detail panel**

Cut the DP comparison block (lines ~762-801, the `comparison && (...)` section) from the results area. Paste it as the first section inside the `selectedDrug && (...)` detail panel (after line ~1133, before the existing grid). Wrap it in a collapsible toggle:

```tsx
<div className="mb-4">
  <button
    onClick={() => setShowComparison(!showComparison)}
    className="flex items-center gap-2 text-ia-caption font-heading font-semibold text-brand-sky hover:underline cursor-pointer mb-2"
  >
    <GitCompare className="h-3.5 w-3.5" />
    有/无 DP 结果对比
    {showComparison ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
  </button>
  {showComparison && comparison && (
    // ... existing comparison JSX ...
  )}
</div>
```

Add `showComparison` state: `const [showComparison, setShowComparison] = useState(false)`

- [ ] **Step 2: Add moved badges + score breakdown + routing path to detail panel**

Inside the detail panel's 2-column grid (lines ~1139-1190), add a new section after "用法用量" that shows the previously-hidden info:

```tsx
<div className="space-y-3">
  {/* Moved badges */}
  <div className="flex flex-wrap gap-1.5">
    {selectedDrug.explanation?.evidenceLevel && (
      <span className="ia-badge text-[10px] px-1.5 py-0.5" style={{
        background: selectedDrug.explanation.evidenceLevel === 'on_label' ? '#052e16' : '#451a03',
        color: selectedDrug.explanation.evidenceLevel === 'on_label' ? '#22c55e' : '#f59e0b',
      }}>
        {selectedDrug.explanation.evidenceLevel === 'on_label' ? '说明书内' : '超说明书'}
      </span>
    )}
    {selectedDrug.reviewStatus && (
      <span className="ia-badge text-[10px] px-1.5 py-0.5">{
        selectedDrug.reviewStatus === 'pending' ? '待审核' :
        selectedDrug.reviewStatus === 'confirmed' ? '已确认' :
        selectedDrug.reviewStatus === 'modified' ? '已修改' : '已拒绝'
      }</span>
    )}
    <span className="ia-badge text-[10px] px-1.5 py-0.5">
      {selectedDrug.mode === 'model' ? '模型推理' : '演示模式'}
    </span>
    {selectedDrug.qualityWarning && (
      <span className="ia-badge text-[10px] px-1.5 py-0.5">{selectedDrug.qualityWarning}</span>
    )}
  </div>
  {/* Score breakdown */}
  {dpEnabled && selectedDrug.rawScore !== undefined && (
    <div className="p-2.5 rounded-sm bg-surface-elevated border border-white/[0.06] text-ia-label text-muted-foreground space-y-1.5">
      <div className="flex items-center gap-1.5">
        <span>原始评分: {selectedDrug.rawScore.toFixed(3)}</span>
        {typeof selectedDrug.dpNoise === 'number' && (
          <>
            <span>→</span>
            <span>DP评分: {selectedDrug.score.toFixed(3)}</span>
            <span className={`text-[10px] ${selectedDrug.dpNoise >= 0 ? 'text-brand-sky' : 'text-ia-data-4'}`}>
              (噪声 {selectedDrug.dpNoise >= 0 ? '+' : ''}{selectedDrug.dpNoise.toFixed(3)})
            </span>
          </>
        )}
      </div>
      {selectedDrug.dpConfidence && (
        <div className="flex items-center gap-2">
          <span className="text-[10px]">置信区间</span>
          <div className="relative h-2 w-24 bg-surface rounded-full overflow-hidden">
            <div className="absolute h-full bg-brand-sky/40 rounded-full" style={{
              left: `${Math.max(0, selectedDrug.dpConfidence.low) * 100}%`,
              width: `${(Math.min(1, selectedDrug.dpConfidence.high) - Math.max(0, selectedDrug.dpConfidence.low)) * 100}%`,
            }} />
            <div className="absolute h-full w-1 bg-gradient-to-br from-brand-sky to-sky-600 rounded" style={{ left: `${selectedDrug.score * 100}%` }} />
          </div>
          <span className="text-[10px]">[{selectedDrug.dpConfidence.low.toFixed(2)}–{selectedDrug.dpConfidence.high.toFixed(2)}]</span>
        </div>
      )}
    </div>
  )}
  {/* Routing path */}
  {selectedDrug.routingPath && (
    <div className="text-ia-label text-muted-foreground" style={{ fontSize: '11px', padding: '4px 8px', background: '#16213e', borderRadius: '4px' }}>
      <span style={{ color: '#00d4aa' }}>推荐路径：</span>{selectedDrug.routingPath}
    </div>
  )}
  {/* Safety warnings */}
  {selectedDrug.warnings && selectedDrug.warnings.length > 0 && (
    <div className="flex items-center gap-1.5 text-ia-caption text-secondary">
      <Info className="h-3 w-3" />
      <span>{selectedDrug.warnings.join('；')}</span>
    </div>
  )}
</div>
```

- [ ] **Step 3: Collapse excluded drugs list by default**

Add state: `const [showExcludedDrugs, setShowExcludedDrugs] = useState(false)`

Replace the excluded drugs section (lines ~1040-1064) with a collapsed version:

```tsx
{excludedDrugs.length > 0 && (
  <div className="mb-5 p-3 rounded-sm bg-destructive/4 border border-destructive/20">
    <div
      className="flex items-center justify-between cursor-pointer"
      onClick={() => setShowExcludedDrugs(!showExcludedDrugs)}
    >
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-3.5 w-3.5 text-destructive" />
        <span className="text-ia-caption font-heading font-semibold text-destructive">
          安全排除药物（{excludedDrugs.length} 项）
        </span>
      </div>
      <span className="text-ia-label text-muted-foreground">
        {showExcludedDrugs ? '收起 ▴' : '展开详情 ▾'}
      </span>
    </div>
    {showExcludedDrugs && (
      <div className="mt-2">
        <p className="text-ia-label text-muted-foreground mb-2">
          以下药物因安全原因被排除，不受差分隐私噪声影响
        </p>
        <div className="max-h-40 overflow-y-auto space-y-1">
          {/* ... existing excluded drug list items ... */}
        </div>
      </div>
    )}
  </div>
)}
```

- [ ] **Step 4: Merge candidate stats + budget info into one line**

Replace the 2-column grid of candidate stats + budget (lines ~1037-1128) with a single compact line:

```tsx
{(totalCandidateInfo || budgetInfo) && (
  <div className="mb-5 flex flex-wrap items-center justify-between gap-3 text-ia-label text-muted-foreground">
    <div className="flex items-center gap-3">
      {totalCandidateInfo && (
        <>
          <Shield className="h-3.5 w-3.5 text-brand-sky" />
          <span>安全候选 <strong className="text-foreground">{totalCandidateInfo.safe}</strong>/{totalCandidateInfo.total}</span>
          <span>· 已排除 <strong className="text-destructive">{totalCandidateInfo.excluded}</strong></span>
        </>
      )}
    </div>
    <div className="flex items-center gap-3">
      {budgetInfo && (
        <>
          <Lock className="h-3.5 w-3.5 text-secondary" />
          <span>ε <strong className="text-foreground">{budgetInfo.epsilonSpent.toFixed(4)}</strong>/{budgetInfo.epsilonBudget.toFixed(1)}</span>
          <span>· 剩余 <strong className={budgetInfo.remainingRatio < 0.2 ? 'text-destructive' : 'text-foreground'}>{(budgetInfo.remainingRatio * 100).toFixed(1)}%</strong></span>
        </>
      )}
    </div>
  </div>
)}
```

- [ ] **Step 5: Simplify privacy notice in detail panel**

Replace the privacy notice block (lines ~1277-1306) with:

```tsx
<div className="pt-4 border-t border-white/[0.06]">
  <div className="flex items-start gap-2 p-3 rounded-sm border border-brand-sky/20 bg-brand-sky/4">
    <Shield className="h-4 w-4 text-brand-sky flex-shrink-0 mt-0.5" />
    <p className="text-ia-caption text-muted-foreground">
      本推荐由<strong className="text-foreground">{selectedDrug.mode === 'model' ? 'DeepFM模型' : '规则匹配'}</strong>生成
      {dpEnabled && '，已施加差分隐私保护'}
      （ε = {config.epsilon.toFixed(3)}）。
      {selectedDrug.dpAnomaly && <span className="text-ia-data-4">注意：该药物原始评分极低，排名可能因DP噪声异常。</span>}
      结果仅供参考，请遵医嘱。
    </p>
  </div>
</div>
```

- [ ] **Step 6: Verify all changes render correctly**

Run: `npm run dev`
Test: generate recommendations, click a drug card, verify:
- DP comparison is in detail panel (collapsed)
- Moved badges + score breakdown + routing path appear in detail panel
- Excluded drugs default collapsed, click to expand
- Candidate stats + budget are a single line
- Privacy notice is one sentence
- No information is missing — everything is accessible

- [ ] **Step 7: Commit**

```bash
git add src/pages/DrugRecommendation.tsx
git commit -m "refactor: DrugRecommendation — collapse excluded drugs, merge stats, move details to panel"
```

---

## Task 3: PatientRecords — Merge Stats, Collapse Charts, Simplify Card Header

**Files:**
- Modify: `src/pages/PatientRecords.tsx` (lines ~258-445, stats/charts/card header)

- [ ] **Step 1: Replace 4 stat cards with a single compact row**

Replace the 4-card grid (lines ~258-280) with a single card:

```tsx
<div className="rounded-sm border border-white/[0.06] bg-surface-elevated px-5 py-3">
  <div className="flex items-center justify-around gap-4 text-center">
    {[
      { label: '患者总数', value: `${stats.total}` },
      { label: '平均年龄', value: `${stats.avgAge}` },
      { label: '慢病种类', value: `${stats.diseaseCount}` },
      { label: '平均BMI', value: stats.avgBMI.toFixed(1) },
    ].map((item) => (
      <div key={item.label}>
        <div className="text-xl font-semibold font-bold">{item.value}</div>
        <div className="text-xs text-muted-foreground">{item.label}</div>
      </div>
    ))}
  </div>
</div>
```

- [ ] **Step 2: Collapse charts by default**

Add state: `const [showCharts, setShowCharts] = useState(false)`

Replace the charts section (lines ~283-288) with:

```tsx
<div className="rounded-sm border border-white/[0.06] bg-surface-elevated px-5 py-3">
  <div
    className="flex items-center justify-between cursor-pointer"
    onClick={() => setShowCharts(!showCharts)}
  >
    <span className="text-sm text-muted-foreground">📊 年龄 / 疾病分布图</span>
    <span className="text-xs text-muted-foreground">{showCharts ? '收起 ▴' : '展开 ▾'}</span>
  </div>
  {showCharts && !isLoading && patients.length > 0 && (
    <div className="grid gap-5 md:grid-cols-2 mt-3">
      <AgeDistributionChart data={ageDistribution} />
      <DiseaseDistributionChart data={diseaseDistribution} />
    </div>
  )}
</div>
```

- [ ] **Step 3: Simplify patient card header**

In the patient card header (lines ~400-443), remove:
- BMI line (lines ~412-414)
- Allergy count line (lines ~416-419)
- Creation date line (lines ~420-423)
- Edit and Delete buttons (lines ~438-439)

The simplified header should show: avatar, name, gender/age badge, disease badges, and only the "推荐" + expand buttons:

```tsx
<div className="cursor-pointer p-4" onClick={() => setExpandedPatient(isExpanded ? null : patient.id)}>
  <div className="flex items-center justify-between">
    <div className="flex min-w-0 flex-1 items-center gap-3">
      <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-sm bg-gradient-to-br from-brand-sky to-sky-600">
        <User className="h-5 w-5 text-white" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="mb-1.5 flex flex-wrap items-center gap-2">
          <h3 className="font-semibold text-base">{patient.name}</h3>
          <span className="ia-badge ia-badge-primary">{patient.gender} · {patient.age} 岁</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {patient.chronicDiseases.slice(0, 3).map((disease) => (
            <span key={disease} className="ia-badge ia-badge-info">{disease}</span>
          ))}
        </div>
      </div>
    </div>
    <div className="ml-2 flex flex-shrink-0 items-center gap-0.5">
      <Button variant="ghost" size="sm" className="gap-1 text-xs text-brand-sky hover:text-brand-sky cursor-pointer" onClick={(event) => { event.stopPropagation(); handleGoToRecommendation(patient) }}>
        <Stethoscope className="h-3.5 w-3.5" />
        推荐
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 cursor-pointer">
        {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
      </Button>
    </div>
  </div>
</div>
```

- [ ] **Step 4: Add Edit/Delete buttons inside expanded tab area**

Inside the expanded content area, after the tab bar, add a row of action buttons:

```tsx
<div className="flex items-center gap-2 px-4 pt-3">
  <Button variant="ghost" size="sm" className="gap-1 text-xs cursor-pointer" onClick={() => handleEdit(patient)}>
    <Edit2 className="h-3.5 w-3.5" /> 编辑
  </Button>
  <Button variant="ghost" size="sm" className="gap-1 text-xs text-destructive cursor-pointer" onClick={() => void handleDelete(patient.id)}>
    <Trash2 className="h-3.5 w-3.5" /> 删除
  </Button>
</div>
```

Also add BMI info to the "基本信息" tab's body info section (it already shows height/weight, add BMI row — the data is already computed).

- [ ] **Step 5: Verify PatientRecords page renders correctly**

Run: `npm run dev`
Test on /patients page:
- Stats show as single row
- Charts default collapsed, click to expand
- Patient card headers are clean (name + age + diseases + recommend button)
- Edit/delete available when card is expanded
- No information lost

- [ ] **Step 6: Commit**

```bash
git add src/pages/PatientRecords.tsx
git commit -m "refactor: PatientRecords — merge stats, collapse charts, simplify card header"
```

---

## Task 4: PatientRecords — Add Form Steps + Clinical Metric Groups

**Files:**
- Modify: `src/pages/PatientRecords.tsx` (lines ~308-376 add form, lines ~542-639 clinical tab)

- [ ] **Step 1: Add step state and split add/edit form into 2 steps**

Add state: `const [formStep, setFormStep] = useState<1 | 2>(1)`

In `resetForm`, add `setFormStep(1)`.

Replace the single form (lines ~324-372) with a 2-step form:

Step 1 (基本信息): name, age, gender, height/weight — show "下一步 →" button instead of submit
Step 2 (健康档案): phone, allergies, chronicDiseases, currentMedications, medicalHistory — show "← 上一步" and submit button

```tsx
<CardContent className="space-y-5">
  {/* Step indicator */}
  <div className="flex items-center gap-3 mb-2">
    <button className={`text-sm font-semibold ${formStep === 1 ? 'text-brand-sky border-b-2 border-brand-sky pb-1' : 'text-muted-foreground pb-1'}`}>① 基本信息</button>
    <span className="text-muted-foreground">→</span>
    <button className={`text-sm font-semibold ${formStep === 2 ? 'text-brand-sky border-b-2 border-brand-sky pb-1' : 'text-muted-foreground pb-1'}`}>② 健康档案</button>
  </div>

  {formStep === 1 ? (
    <div className="grid gap-4 md:grid-cols-2">
      {/* name, age, gender, height/weight fields — existing JSX */}
      <div className="flex justify-end pt-2">
        <Button type="button" className="gap-2 cursor-pointer" onClick={() => setFormStep(2)}>下一步 →</Button>
      </div>
    </div>
  ) : (
    <div className="space-y-4">
      {/* phone, allergies, chronicDiseases, currentMedications, medicalHistory fields — existing JSX */}
      <div className="flex gap-2 pt-3">
        <Button type="button" variant="outline" onClick={() => setFormStep(1)} className="cursor-pointer">← 上一步</Button>
        <Button type="submit" className="gap-2 cursor-pointer" disabled={submitting}>
          <Save className="h-4 w-4" />
          {submitting ? '提交中...' : editingId ? '保存修改' : '添加患者'}
        </Button>
      </div>
    </div>
  )}
</CardContent>
```

- [ ] **Step 2: Group clinical metrics into 3 sections with progress indicator**

Replace the flat 12-field grid (lines ~544-639) with grouped sections:

```tsx
<div className="mt-4 space-y-5">
  {/* Progress indicator */}
  {(() => {
    const filled = [
      clinicalForm.renalFunction, clinicalForm.hepaticFunction,
      clinicalForm.bloodPressureSystolic, clinicalForm.heartRate,
      clinicalForm.fastingGlucose, clinicalForm.hba1c,
    ].filter((v) => v !== '' && v !== null && v !== 0).length
    return <div className="text-xs text-muted-foreground mb-2">已填写 {filled}/6 核心指标</div>
  })()}

  {/* 器官功能 + 生活习惯 */}
  <div>
    <h5 className="text-xs font-semibold text-brand-sky mb-2">器官功能与生活习惯</h5>
    <div className="grid gap-3 md:grid-cols-2">
      {/* renalFunction, hepaticFunction, smokingStatus, drinkingStatus selects — existing JSX */}
    </div>
  </div>

  {/* 心血管指标 */}
  <div>
    <h5 className="text-xs font-semibold text-brand-sky mb-2">心血管指标</h5>
    <div className="grid gap-3 md:grid-cols-2">
      {/* bloodPressureSystolic, bloodPressureDiastolic, heartRate inputs — existing JSX */}
    </div>
  </div>

  {/* 代谢指标 */}
  <div>
    <h5 className="text-xs font-semibold text-brand-sky mb-2">代谢指标</h5>
    <div className="grid gap-3 md:grid-cols-2">
      {/* fastingGlucose, hba1c, cholesterolTotal, cholesterolLdl inputs — existing JSX */}
    </div>
  </div>

  <div className="flex gap-2 pt-2">
    <Button size="sm" className="gap-1.5 cursor-pointer" disabled={clinicalSaving} onClick={() => handleClinicalSave(patient.id)}>
      <Save className="h-3.5 w-3.5" />
      {clinicalSaving ? '保存中...' : '保存临床指标'}
    </Button>
  </div>
</div>
```

- [ ] **Step 3: Verify form steps and clinical groups work**

Run: `npm run dev`
Test: open add patient form, confirm 2 steps work, navigate between steps, submit works. Expand a patient's clinical tab, confirm 3 grouped sections with progress indicator.

- [ ] **Step 4: Commit**

```bash
git add src/pages/PatientRecords.tsx
git commit -m "refactor: PatientRecords — add 2-step form, group clinical metrics into 3 sections"
```

---

## Task 5: AdminDashboard — Add Tab Navigation + Merge Stats + Simplify Ledger

**Files:**
- Modify: `src/pages/AdminDashboard.tsx`

- [ ] **Step 1: Add tab state and tab navigation**

Add state: `const [activeTab, setActiveTab] = useState<'users' | 'training' | 'ledger'>('users')`

After the merged stats row (which we'll add in Step 2), add tab navigation:

```tsx
<div className="flex gap-0 border-b border-white/[0.06] mb-6">
  {([
    { key: 'users' as const, label: '用户管理', icon: Users },
    { key: 'training' as const, label: '模型训练', icon: Brain },
    { key: 'ledger' as const, label: '隐私账本', icon: Shield },
  ]).map((tab) => {
    const Icon = tab.icon
    return (
      <button
        key={tab.key}
        onClick={() => setActiveTab(tab.key)}
        className={`px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer flex items-center gap-2 ${
          activeTab === tab.key ? 'text-brand-sky border-b-2 border-brand-sky' : 'text-muted-foreground hover:text-foreground border-b-2 border-transparent'
        }`}
      >
        <Icon className="h-4 w-4" />
        {tab.label}
      </button>
    )
  })}
</div>
```

Wrap each section (users, training, ledger) in `{activeTab === 'xxx' && (...)}`.

- [ ] **Step 2: Merge admin identity card + 5 stat cards into one row**

Replace the admin identity card (lines ~269-285) + system overview section (lines ~293-324) with a single compact row:

```tsx
<div className="rounded-sm border border-white/[0.06] bg-surface-elevated px-5 py-3">
  <div className="flex flex-wrap items-center justify-between gap-4">
    <div className="flex items-center gap-3">
      <div className="flex h-9 w-9 items-center justify-center rounded-sm bg-gradient-to-br from-brand-sky to-sky-600">
        <UserIcon className="h-4 w-4 text-white" />
      </div>
      <div>
        <span className="font-heading font-semibold text-ia-body">{user?.username ?? '管理员'}</span>
        <span className="ia-badge ia-badge-primary ml-2">管理员</span>
      </div>
    </div>
    <div className="flex flex-wrap items-center gap-4 text-ia-label text-muted-foreground">
      <span>患者 <strong className="text-foreground">{dashboard?.patientCount ?? 0}</strong></span>
      <span>用户 <strong className="text-foreground">{dashboard?.userCount ?? 0}</strong></span>
      <span>今日推理 <strong className="text-foreground">{todayInferences}</strong></span>
      <span>推荐总数 <strong className="text-foreground">{dashboard?.recommendationCount ?? 0}</strong></span>
      <span>ε剩余 <strong className="text-secondary">{budget.remaining.toFixed(2)}</strong></span>
    </div>
  </div>
</div>
```

Delete the `ε摘要行` (the "已消耗 ε · 剩余 ε" line below the stats grid).

- [ ] **Step 3: Simplify user table — remove "最近登录" column**

Remove the `<th>最近登录</th>` header and the corresponding `<td>` for `lastLoginAt`. Instead, add a `title` attribute to the username cell so hovering shows the login time:

```tsx
<td className="font-heading font-semibold" title={item.lastLoginAt ? `最近登录: ${new Date(item.lastLoginAt).toLocaleString()}` : '暂无登录记录'}>
  {item.username}
</td>
```

- [ ] **Step 4: Simplify ledger — merge 3 budget cards into progress bar labels**

Replace the 3 budget summary cards (lines ~545-558) with inline labels on the progress bar:

```tsx
<div>
  <div className="flex justify-between text-ia-caption font-heading font-semibold mb-1.5">
    <span className="text-destructive">已消耗 ε = {budget.spent.toFixed(2)}</span>
    <span>总预算 ε = {config.privacyBudget.toFixed(1)}</span>
  </div>
  <div className="progress-bar">
    <div className="progress-bar-fill" style={{ width: `${config.privacyBudget <= 0 ? 0 : Math.min(100, (budget.spent / config.privacyBudget) * 100)}%` }} />
  </div>
  <div className="mt-1 flex justify-between text-ia-label text-muted-foreground">
    <span>已消耗 {config.privacyBudget > 0 ? ((budget.spent / config.privacyBudget) * 100).toFixed(1) : 0}%</span>
    <span>剩余 ε = {budget.remaining.toFixed(2)}</span>
  </div>
</div>
```

- [ ] **Step 5: Verify AdminDashboard renders correctly**

Run: `npm run dev`
Test on /admin page:
- Stats show as single row with admin identity
- Tab navigation works — switch between users/training/ledger
- User table has 4 columns (no "最近登录"), hover shows login time
- Ledger has progress bar with inline labels instead of 3 cards

- [ ] **Step 6: Commit**

```bash
git add src/pages/AdminDashboard.tsx
git commit -m "refactor: AdminDashboard — add tabs, merge stats row, simplify ledger"
```

---

## Task 6: PrivacyConfig — Collapse Sections + Restructure Sliders + Merge Metrics

**Files:**
- Modify: `src/pages/PrivacyConfig.tsx`

- [ ] **Step 1: Collapse algorithm explanation by default**

Add state: `const [showAlgorithm, setShowAlgorithm] = useState(false)`

Wrap the algorithm explanation Card (lines ~79-154) with a collapsible toggle:

```tsx
<div className="rounded-sm border border-brand-sky/20 bg-surface-elevated">
  <div
    className="flex items-center justify-between px-5 py-3 cursor-pointer"
    onClick={() => setShowAlgorithm(!showAlgorithm)}
  >
    <div className="flex items-center gap-2">
      <BookOpen className="h-4 w-4 text-brand-sky" />
      <span className="font-heading font-semibold text-ia-body">差分隐私算法原理</span>
    </div>
    <span className="text-ia-label text-muted-foreground">{showAlgorithm ? '收起 ▴' : '展开查看 ▾'}</span>
  </div>
  {showAlgorithm && (
    <div className="border-t border-white/[0.06] px-5 py-4 space-y-4">
      {/* ... existing algorithm card content (lines 88-152) ... */}
    </div>
  )}
</div>
```

- [ ] **Step 2: Collapse research content by default**

Add state: `const [showResearch, setShowResearch] = useState(false)`

Similarly wrap the research content Card (lines ~472-505) with a collapsible toggle.

- [ ] **Step 3: Restructure sliders — core 2 + advanced collapsible**

Add state: `const [showAdvancedParams, setShowAdvancedParams] = useState(false)`

In the privacy parameters Card (lines ~160-226), restructure:

Show by default: ε slider and ε_total slider
Collapse: δ slider, Δf slider, noise mechanism selection, application stage selection

After the 2 default sliders, add:

```tsx
<div className="mt-4">
  <button
    onClick={() => setShowAdvancedParams(!showAdvancedParams)}
    className="flex items-center gap-2 text-ia-caption font-heading font-semibold text-muted-foreground hover:text-foreground cursor-pointer"
  >
    <Settings className="h-3.5 w-3.5" />
    高级参数
    {showAdvancedParams ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
  </button>
</div>
{showAdvancedParams && (
  <div className="mt-4 space-y-6 pt-4 border-t border-white/[0.06]">
    {/* δ slider, Δf slider — existing JSX */}
  </div>
)}
```

Move the noise mechanism Card and application stage Card into the same collapsible block (after the δ and Δf sliders).

Remove the info tip boxes under ε slider and ε_total slider (the blue "当前ε=1.00属于中等保护" box and the grey "Demo采用串行组合" box). Add `title` attributes to the slider labels instead:

```tsx
<Label className="text-ia-caption font-heading font-semibold flex items-center gap-2" title="ε越小隐私保护越强，推荐范围0.1~10">
  <Key className="h-3.5 w-3.5" />隐私预算 ε (Epsilon)
</Label>
```

- [ ] **Step 4: Merge 4 real-time metric cards into one compact block**

Replace the 4 individual metric cards (lines ~315-381) with a single compact block:

```tsx
<div className="p-3 rounded-sm bg-surface-elevated border border-white/[0.06] space-y-3">
  <div className="flex items-center gap-2 mb-1">
    <Activity className="h-3.5 w-3.5 text-brand-sky" />
    <span className="text-ia-caption font-heading font-semibold">实时评估</span>
    <span className="text-ia-label text-muted-foreground ml-auto">
      ε={config.epsilon.toFixed(1)}时 · 保护强度 <strong className={parseFloat(privacyScore) >= 8 ? 'text-ia-data-3' : parseFloat(privacyScore) >= 6 ? 'text-secondary' : 'text-ia-data-4'}>{privacyScore}/10</strong>
    </span>
  </div>
  <div className="flex flex-wrap items-center gap-4 text-ia-label text-muted-foreground">
    <span>噪声 <strong className="text-foreground">{noiseScale === Infinity ? '∞' : noiseScale.toFixed(4)}</strong></span>
    <span>效用损失 <strong className="text-ia-data-4">{utilityLoss}%</strong></span>
    <span>预算剩余 <strong className="text-secondary">ε = {budget.remaining.toFixed(2)}</strong></span>
  </div>
  <div>
    <div className="progress-bar">
      <div className="progress-bar-fill" style={{ width: `${config.privacyBudget <= 0 ? 0 : Math.min(100, (budget.spent / config.privacyBudget) * 100)}%` }} />
    </div>
    <div className="flex justify-between text-ia-label text-muted-foreground mt-1">
      <span>已消耗 ε = {budget.spent.toFixed(2)}</span>
      <span>ε_total = {config.privacyBudget.toFixed(1)}</span>
    </div>
  </div>
</div>
```

- [ ] **Step 5: Verify PrivacyConfig page renders correctly**

Run: `npm run dev`
Test on /privacy page:
- Algorithm explanation default collapsed, click to expand
- Only ε and ε_total sliders visible; "高级参数 ▾" reveals δ, Δf, mechanism, stage
- Metrics show as single compact block with progress bar
- Research content default collapsed
- No info tip boxes under sliders
- All functionality preserved

- [ ] **Step 6: Commit**

```bash
git add src/pages/PrivacyConfig.tsx
git commit -m "refactor: PrivacyConfig — collapse algorithm/research, restructure sliders, merge metrics"
```

---

## Task 7: Final Verification

**Files:** All 4 modified pages

- [ ] **Step 1: Run TypeScript type check**

Run: `npx tsc --noEmit`
Expected: No type errors

- [ ] **Step 2: Run production build**

Run: `npm run build`
Expected: Build succeeds

- [ ] **Step 3: Manual smoke test all 4 pages**

For each page, verify:
1. **DrugRecommendation** — generate recommendations → cards show 4 badges → click card → detail panel shows moved info → excluded drugs collapsed → stats in one line
2. **PatientRecords** — stats in one row → charts collapsed → card header clean → expand shows edit/delete → add form has 2 steps → clinical tab has 3 groups
3. **AdminDashboard** — stats/admin in one row → tabs switch content → user table 4 cols with hover → ledger has inline labels
4. **PrivacyConfig** — algorithm collapsed → 2 sliders default + advanced ▾ → metrics merged → research collapsed

- [ ] **Step 4: Commit final verification**

```bash
git add -A
git commit -m "chore: verify all 4 simplified pages build and render correctly"
```
