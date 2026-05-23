import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/lib/api'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, Legend,
} from 'recharts'
import SafetyLayerChart from '../components/SafetyLayerChart'
import { BarChart3, TrendingUp, Activity, Shield, Pill, Settings } from 'lucide-react'

interface StatsData {
  totalRecommendations: number
  statusDistribution: Record<string, number>
  approvalRate: number
  uniqueDrugCount: number
  trend: { day: string; count: number }[]
  topDrugs: { name: string; count: number }[]
  categoryDistribution: { name: string; value: number }[]
}
export default function RecommendationStats() {
  const [stats, setStats] = useState<StatsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [showCategoryPicker, setShowCategoryPicker] = useState(false)

  // 默认选中 Top 8 分类
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(new Set())

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.get<StatsData>('/api/stats/recommendations')
        setStats(data)
        // 默认选中 Top 8
        const top8 = (data.categoryDistribution || []).slice(0, 8).map(c => c.name)
        setSelectedCategories(new Set(top8))
      } catch { /* silent */ }
      finally { setLoading(false) }
    }
    fetchStats()
  }, [])

  // 根据用户选择生成饼图数据：所选分类 + 其余汇总为"其他"
  const allCategories = stats?.categoryDistribution || []
  const pieData = (() => {
    const selected: { name: string; value: number }[] = []
    let otherValue = 0
    for (const c of allCategories) {
      if (selectedCategories.has(c.name)) {
        selected.push({ name: c.name, value: c.value })
      } else {
        otherValue += c.value
      }
    }
    if (otherValue > 0) selected.push({ name: '其他', value: otherValue })
    return selected
  })()

  const toggleCategory = (name: string) => {
    setSelectedCategories(prev => {
      const next = new Set(prev)
      if (next.has(name)) next.delete(name)
      else next.add(name)
      return next
    })
  }

  const PIE_COLORS = ['#0891b2', '#059669', '#b45309', '#b91c1c', '#7c3aed', '#db2777', '#0d9488', '#ea580c', '#0369a1', '#9333ea', '#0891b2', '#65a30d']
  const OTHER_COLOR = '#5e7f92'

  if (loading) return <div className="p-8 text-center text-muted-foreground">加载统计数据...</div>

  return (
    <div className="space-y-6">
      <section className="border-l-4 border-l-primary bg-background px-6 py-8">
        <div className="flex items-center gap-3">
          <BarChart3 className="h-5 w-5 text-primary" />
          <div>
            <h1 className="text-ia-tile font-display font-bold text-foreground">推荐统计</h1>
            <p className="text-ia-body text-muted-foreground mt-1">推荐分布统计 · 药物分析 · 审核概览</p>
          </div>
        </div>
      </section>

      {/* 指标卡片 */}
      <div className="grid grid-cols-4 gap-4">
        <Card hover="none"><CardContent className="p-5 text-center">
          <TrendingUp className="h-5 w-5 text-primary mx-auto mb-2" />
          <div className="text-2xl font-heading font-bold text-primary">{stats?.totalRecommendations || 0}</div>
          <div className="text-sm text-muted-foreground">总推荐次数</div>
        </CardContent></Card>
        <Card hover="none"><CardContent className="p-5 text-center">
          <Activity className="h-5 w-5 text-amber-400 mx-auto mb-2" />
          <div className="text-2xl font-heading font-bold text-amber-400">{stats?.statusDistribution?.pending || 0}</div>
          <div className="text-sm text-muted-foreground">待审核</div>
        </CardContent></Card>
        <Card hover="none"><CardContent className="p-5 text-center">
          <Shield className="h-5 w-5 text-green-500 mx-auto mb-2" />
          <div className="text-2xl font-heading font-bold text-green-500">{stats?.approvalRate || 0}%</div>
          <div className="text-sm text-muted-foreground">审核通过率</div>
        </CardContent></Card>
        <Card hover="none"><CardContent className="p-5 text-center">
          <Pill className="h-5 w-5 text-purple-400 mx-auto mb-2" />
          <div className="text-2xl font-heading font-bold text-purple-400">{stats?.uniqueDrugCount || 0}</div>
          <div className="text-sm text-muted-foreground">涉及药物数</div>
        </CardContent></Card>
      </div>

      {/* 2x2 图表 */}
      <div className="grid grid-cols-2 gap-5">
        {/* 推荐趋势 */}
        <Card hover="none">
          <CardHeader><CardTitle className="text-base">推荐趋势</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stats?.trend || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(155,175,200,0.12)" />
                <XAxis dataKey="day" stroke="#5e7f92" tick={{ fontSize: 11 }} />
                <YAxis stroke="#5e7f92" tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip contentStyle={{ background: '#edf3fa', border: '1px solid rgba(155,175,200,0.18)', borderRadius: 4, fontSize: 12, color: '#1a3244' }} itemStyle={{ color: '#1a3244' }} labelStyle={{ color: '#5e7f92', fontSize: 11 }} />
                <Line type="monotone" dataKey="count" stroke="#0891b2" strokeWidth={2} dot={{ fill: '#0891b2', r: 3 }} name="推荐数" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* 药物频次 Top 10 */}
        <Card hover="none">
          <CardHeader><CardTitle className="text-base">药物推荐频次 Top 10</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats?.topDrugs || []} layout="vertical" margin={{ left: 0, top: 5, right: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(155,175,200,0.12)" />
                <XAxis type="number" stroke="#5e7f92" tick={{ fontSize: 11 }} allowDecimals={false} />
                <YAxis dataKey="name" type="category" stroke="#5e7f92" tick={{ fontSize: 11, fill: '#3d5f73' }} width={160} interval={0} />
                <Tooltip contentStyle={{ background: '#edf3fa', border: '1px solid rgba(155,175,200,0.18)', borderRadius: 4, fontSize: 12, color: '#1a3244' }} itemStyle={{ color: '#1a3244' }} labelStyle={{ color: '#5e7f92', fontSize: 11 }} />
                <Bar dataKey="count" fill="#0891b2" radius={[0, 3, 3, 0]} name="次数" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* 药物分类占比 — 饼图 + 分类选择 */}
        <Card hover="none">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">药物分类分布</CardTitle>
              <button
                onClick={() => setShowCategoryPicker(!showCategoryPicker)}
                className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors"
              >
                <Settings className="h-3.5 w-3.5" />
                选择分类
              </button>
            </div>
            {showCategoryPicker && (
              <div className="mt-2 flex flex-wrap gap-1 max-h-24 overflow-y-auto">
                {allCategories.map((c, i) => (
                  <button
                    key={c.name}
                    onClick={() => toggleCategory(c.name)}
                    className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs transition-colors"
                    style={{
                      background: selectedCategories.has(c.name) ? PIE_COLORS[i % PIE_COLORS.length] : '#edf3fa',
                      color: selectedCategories.has(c.name) ? '#fff' : '#3d5f73',
                      border: `1px solid ${selectedCategories.has(c.name) ? PIE_COLORS[i % PIE_COLORS.length] : 'rgba(155,175,200,0.18)'}`,
                    }}
                  >
                    {c.name} ({c.value})
                  </button>
                ))}
              </div>
            )}
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={95}
                  paddingAngle={1}
                  dataKey="value"
                >
                  {pieData.map((entry) => (
                    <Cell
                      key={entry.name}
                      fill={entry.name === '其他' ? OTHER_COLOR : PIE_COLORS[allCategories.findIndex(c => c.name === entry.name) % PIE_COLORS.length]}
                      stroke="transparent"
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#edf3fa', border: '1px solid rgba(155,175,200,0.18)', borderRadius: 4, fontSize: 12, color: '#1a3244' }}
                  itemStyle={{ color: '#1a3244' }}
                  labelStyle={{ color: '#5e7f92', fontSize: 11 }}
                  formatter={(value: number, name: string) => [`${value} 次`, name]}
                />
                <Legend
                  layout="vertical"
                  align="right"
                  verticalAlign="middle"
                  iconType="circle"
                  iconSize={6}
                  formatter={(value: string) => <span style={{ color: '#3d5f73', fontSize: 11 }}>{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* 安全分层分析 */}
        <Card hover="none">
          <CardHeader><CardTitle className="text-base">安全分层分析 · 三层过滤架构</CardTitle></CardHeader>
          <CardContent className="p-3 pt-0">
            <SafetyLayerChart />
          </CardContent>
        </Card>
      </div>

    </div>
  )
}
