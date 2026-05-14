import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import ReviewPanel from '../components/ReviewPanel'
import { Shield } from 'lucide-react'

interface PendingReview {
  recommendationId: number
  patientId: number | null
  inputData: string
  resultData?: string
  reviewStatus: string
  createdAt: string
}

interface DrugOption {
  drugName: string
  englishName: string
  category: string
  safetyType: string
  score: number
}

function parseInputDisease(inputData: string): string {
  try {
    const parsed = JSON.parse(inputData)
    return parsed.diseases || parsed.disease || ''
  } catch { return '' }
}

function parseResultDrugs(resultData?: string): DrugOption[] {
  if (!resultData) return []
  try {
    const parsed = JSON.parse(resultData)
    const selected = parsed.selected || []
    return selected.map((item: any) => ({
      drugName: item.drugName || '',
      englishName: item.englishName || '',
      category: item.category || '',
      safetyType: item.safetyType || 'safe',
      score: item.score || 0,
    }))
  } catch { return [] }
}

export default function ReviewDashboard() {
  const [pendingReviews, setPendingReviews] = useState<PendingReview[]>([])
  const [selectedReview, setSelectedReview] = useState<PendingReview | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [reviewedExpanded, setReviewedExpanded] = useState(false)
  const [stats, setStats] = useState({ pending: 0, reviewed: 0 })

  const fetchData = async () => {
    setLoading(true)
    try {
      const [pendingData, statsData] = await Promise.all([
        api.get<PendingReview[]>('/api/review/pending'),
        api.get<{ pending: number; reviewed: number }>('/api/review/stats')
      ])
      setPendingReviews(pendingData)
      setStats(statsData)
      setError(null)
    } catch { setError('获取待审核列表失败') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const selectReview = async (review: PendingReview) => {
    if (review.resultData) {
      setSelectedReview(review)
      return
    }
    setDetailLoading(true)
    try {
      const detail = await api.get<{
        recommendationId: number
        patientId: number | null
        inputData: string
        resultData: string
        reviewStatus: string
        createdAt: string
      }>(`/api/review/recommendation/${review.recommendationId}`)
      setSelectedReview({
        ...review,
        resultData: detail.resultData,
      })
    } catch {
      setError('获取推荐详情失败')
    } finally {
      setDetailLoading(false)
    }
  }

  const diseaseCn = selectedReview ? parseInputDisease(selectedReview.inputData) : ''
  const drugs = selectedReview ? parseResultDrugs(selectedReview.resultData) : []

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

      // Refresh the list and stats
      const [updatedList, newStats] = await Promise.all([
        api.get<PendingReview[]>('/api/review/pending'),
        api.get<{ pending: number; reviewed: number }>('/api/review/stats')
      ])
      setPendingReviews(updatedList)
      setStats(newStats)

      // Auto-select next pending item
      if (updatedList.length > 0) {
        selectReview(updatedList[0])
      } else {
        setSelectedReview(null)
      }
    } catch { setError('提交审核失败') }
  }

  if (loading) return <div className="p-8 text-center text-muted-foreground">加载中...</div>

  return (
    <div className="space-y-6">
      <section className="border-l-4 border-l-primary bg-surface-elevated px-6 py-8">
        <div className="flex items-center gap-3">
          <Shield className="h-5 w-5 text-brand-sky" />
          <div>
            <h1 className="text-ia-tile font-display font-bold text-foreground">推荐审核</h1>
            <p className="text-ia-body text-muted-foreground mt-1">审核患者的用药推荐，出具诊疗建议</p>
          </div>
        </div>
      </section>

      {error && <div className="p-3 rounded-sm bg-destructive/6 border border-destructive/30 text-destructive text-sm">{error}</div>}

      {/* Stats Bar */}
      <div className="flex items-center gap-4 px-1 mb-4">
        <span className="text-sm font-semibold text-foreground">推荐审核</span>
        <span className="ia-badge ia-badge-warning">
          <span className="w-1.5 h-1.5 rounded-full bg-orange-500"></span>
          待审核 {stats.pending}
        </span>
        <span className="ia-badge ia-badge-success">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
          已审核 {stats.reviewed}
        </span>
      </div>

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
    </div>
  )
}
