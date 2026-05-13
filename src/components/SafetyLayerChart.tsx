import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'

interface FunnelStage {
  stage: string
  count: number
  desc: string
}

interface ExclusionReason {
  reason: string
  count: number
}

interface SafetyLayersData {
  funnel: FunnelStage[]
  exclusionReasons: ExclusionReason[]
  summary: {
    recordCount: number
    totalExcludedSum: number
    avgExcludedPerRecommendation: number
    requiresReviewSum: number
  }
}

const FUNNEL_COLORS = ['#0284c7', '#f59e0b', '#a855f7', '#22c55e']
const EXCLUSION_COLORS: Record<string, string> = {
  '绝对禁忌': '#ef4444',
  '过敏冲突': '#f97316',
  '严重交互': '#eab308',
  '妊娠禁忌': '#ec4899',
  '儿科禁忌': '#8b5cf6',
  '其他': '#64748b',
}

export default function SafetyLayerChart() {
  const [data, setData] = useState<SafetyLayersData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get<SafetyLayersData>('/api/stats/safety-layers')
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="h-[300px] flex items-center justify-center text-muted-foreground text-sm">加载安全层数据...</div>
  }

  if (!data || data.summary.recordCount === 0) {
    return (
      <div className="h-[300px] flex flex-col items-center justify-center text-muted-foreground">
        <div className="text-lg mb-2">暂无数据</div>
        <div className="text-xs">推荐记录数为 0，无法展示安全分层分析</div>
      </div>
    )
  }

  const { funnel, exclusionReasons, summary } = data

  return (
    <div className="space-y-4">
      {/* Funnel visualization */}
      <div>
        <div className="text-xs text-muted-foreground mb-2">三层过滤漏斗</div>
        <div className="flex items-stretch gap-1">
          {funnel.map((stage, i) => (
            <div
              key={stage.stage}
              className="flex-1 py-3 px-2 text-center relative"
              style={{
                backgroundColor: FUNNEL_COLORS[i] + '33',
                borderLeft: `3px solid ${FUNNEL_COLORS[i]}`,
              }}
            >
              <div className="text-lg font-bold" style={{ color: FUNNEL_COLORS[i] }}>
                {stage.count.toLocaleString()}
              </div>
              <div className="text-xs text-foreground/80">{stage.stage}</div>
              <div className="text-[10px] text-muted-foreground mt-0.5">{stage.desc}</div>
            </div>
          ))}
        </div>
        <div className="flex justify-between text-[10px] text-muted-foreground mt-1 px-1">
          <span>Layer 1: SafetyFilter</span>
          <span>Layer 2: RuleMarker</span>
          <span>Layer 3: DeepFM</span>
        </div>
      </div>

      {/* Exclusion reasons bar chart */}
      {exclusionReasons.length > 0 && (
        <div>
          <div className="text-xs text-muted-foreground mb-2">Layer 1 排除原因分布</div>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={exclusionReasons} layout="vertical" margin={{ left: 10, right: 10, top: 5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
              <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
              <YAxis dataKey="reason" type="category" stroke="#64748b" tick={{ fontSize: 10, fill: '#cbd5e1' }} width={70} />
              <Tooltip
                contentStyle={{ background: '#0f1d32', border: '1px solid #334155', borderRadius: 4, fontSize: 11, color: '#e2e8f0' }}
                formatter={(value: number) => [`${value} 次`, '排除']}
              />
              <Bar dataKey="count" radius={[0, 2, 2, 0]}>
                {exclusionReasons.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={EXCLUSION_COLORS[entry.reason] || '#64748b'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Summary stats */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-800/50 rounded p-2">
          <div className="text-sm font-bold text-sky-400">{summary.totalExcludedSum}</div>
          <div className="text-[10px] text-muted-foreground">累计排除药物</div>
        </div>
        <div className="bg-slate-800/50 rounded p-2">
          <div className="text-sm font-bold text-amber-400">{summary.requiresReviewSum}</div>
          <div className="text-[10px] text-muted-foreground">需审核标记</div>
        </div>
        <div className="bg-slate-800/50 rounded p-2">
          <div className="text-sm font-bold text-purple-400">{summary.avgExcludedPerRecommendation}</div>
          <div className="text-[10px] text-muted-foreground">平均排除数/次</div>
        </div>
      </div>
    </div>
  )
}
