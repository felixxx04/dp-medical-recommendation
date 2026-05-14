import { useState, useEffect } from 'react'

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
  recommendationId,
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

  // Reset form state when recommendationId changes (fixes stale state bug)
  useEffect(() => {
    setSubmitted(false)
    setDecision(null)
    setSelectedDrug('')
    setReason('')
    setSelectedTemplate('')
    setTreatmentAdvice('')
  }, [recommendationId])

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
