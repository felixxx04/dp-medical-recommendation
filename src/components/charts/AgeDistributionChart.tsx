import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const CHART_TOOLTIP_STYLE = {
  backgroundColor: '#edf3fa',
  border: '1px solid rgba(155,175,200,0.18)',
  borderRadius: '8px',
  fontSize: '12px',
  color: '#1a3244',
  boxShadow: '0 4px 12px rgba(135,155,178,0.35)',
}

interface AgeDistributionChartProps {
  data: { name: string; value: number; color: string }[]
}

export function AgeDistributionChart({ data }: AgeDistributionChartProps) {
  return (
    <Card className="rounded-xl bg-card shadow-neu-raised">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-foreground">年龄分布</CardTitle>
        <CardDescription>患者年龄段统计</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={45}
                outerRadius={70}
                paddingAngle={2}
                dataKey="value"
                animationBegin={0}
                animationDuration={800}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} stroke="transparent" />
                ))}
              </Pie>
              <Tooltip
                contentStyle={CHART_TOOLTIP_STYLE}
                itemStyle={{ color: '#1a3244' }}
                formatter={(value: number) => [`${value}人`, '数量']}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                wrapperStyle={{ color: '#3d5f73', fontSize: '12px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
