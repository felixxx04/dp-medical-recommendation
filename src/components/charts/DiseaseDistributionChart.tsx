import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const CHART_TOOLTIP_STYLE = {
  backgroundColor: '#edf3fa',
  border: '1px solid rgba(155,175,200,0.18)',
  borderRadius: '8px',
  fontSize: '12px',
  color: '#1a3244',
  boxShadow: '0 4px 12px rgba(135,155,178,0.35)',
}

const COLORS = [
  '#0891b2',
  '#14b8a6',
  '#059669',
  '#b45309',
  '#b91c1c',
  '#0369a1',
  '#8b5cf6',
  '#ec4899',
]

interface DiseaseDistributionChartProps {
  data: { name: string; count: number }[]
}

export function DiseaseDistributionChart({ data }: DiseaseDistributionChartProps) {
  return (
    <Card className="rounded-xl bg-card shadow-neu-raised">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-foreground">疾病分布</CardTitle>
        <CardDescription>常见慢性病统计 (Top 8)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ left: 10, right: 10 }}>
              <defs>
                <linearGradient id="diseaseBarGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#0891b2" />
                  <stop offset="100%" stopColor="#0891b2" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(140,160,180,0.25)" horizontal={false} />
              <XAxis type="number" stroke="#5e7f92" tick={{ fontSize: 11, fill: '#5e7f92' }} />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#5e7f92"
                tick={{ fontSize: 11, fill: '#5e7f92' }}
                width={80}
              />
              <Tooltip
                contentStyle={CHART_TOOLTIP_STYLE}
                itemStyle={{ color: '#1a3244' }}
                formatter={(value: number) => [`${value}人`, '患者数']}
              />
              <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={16}>
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} fillOpacity={0.9} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
