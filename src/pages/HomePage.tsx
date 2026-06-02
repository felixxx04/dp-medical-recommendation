import { Link } from 'react-router-dom'
import {
  Shield, Brain, Activity, Lock, ArrowRight,
  Users, Stethoscope, BarChart3, Settings,
} from 'lucide-react'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/authStore'
import { canAccessFeature } from '@/lib/permissions'

const features = [
  { icon: Shield, title: '差分隐私保护', description: '采用先进的差分隐私技术，为患者医疗数据提供可证明的隐私保障', color: 'sky' as const },
  { icon: Brain, title: '深度学习推荐', description: '基于深度因子分解机模型，精准捕捉药物-疾病-患者之间的复杂关系', color: 'teal' as const },
  { icon: Activity, title: '个性化用药', description: '综合考虑患者个体差异、疾病特征、药物相互作用，提供定制化建议', color: 'sky' as const },
  { icon: Lock, title: '安全可控', description: '隐私预算可调、噪声机制可选，在隐私保护与推荐性能间实现最佳平衡', color: 'teal' as const },
]

const iconBgMap: Record<string, string> = {
  sky: 'bg-primary/8',
  teal: 'bg-accent/8',
}

const iconColorMap: Record<string, string> = {
  sky: 'text-primary',
  teal: 'text-accent',
}

export default function HomePage() {
  const { user } = useAuth()

  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section — Two-column: text left, visual right */}
      <section className="relative overflow-hidden rounded-xl bg-gradient-to-br from-[#d2deea] to-[#dde6f0] border border-border">
        {/* Geometric decorations */}
        <div className="absolute -top-20 -right-10 w-80 h-80 rounded-full bg-primary/5 blur-2xl" />
        <div className="absolute -bottom-10 right-30 w-45 h-45 rounded-full bg-accent/5 blur-2xl" />
        <div className="absolute top-15 right-50 w-2 h-2 rounded-full bg-primary/20" />
        <div className="absolute bottom-25 right-20 w-1.5 h-1.5 rounded-full bg-accent/20" />

        <div className="relative z-10 flex flex-col lg:flex-row items-center gap-8 p-6 md:p-10 lg:p-12">
          {/* Left: Text block */}
          <div className="flex-1 lg:pr-8">
            <h1 className="text-3xl md:text-4xl lg:text-[2.75rem] font-extrabold text-foreground leading-[1.15] tracking-[-0.03em] mb-4">
              精准用药推荐<br />
              <span className="gradient-text">守护患者隐私</span>
            </h1>

            <p className="text-base md:text-lg text-muted-foreground max-w-lg mb-6 leading-relaxed">
              融合差分隐私技术与深度学习算法，在严格保护患者隐私的前提下，
              提供精准、安全、个性化的医疗用药推荐服务
            </p>

            <div className="flex flex-wrap gap-3">
              {canAccessFeature(user?.role, 'recommendation') && (
                <Link to="/recommendation">
                  <Button size="lg" className="gap-2">
                    开始用药推荐
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              )}
              {canAccessFeature(user?.role, 'recommendation_stats') && (
                <Link to="/recommendation-stats">
                  <Button variant="outline" size="lg" className="gap-2">
                    <BarChart3 className="h-4 w-4" />
                    推荐统计
                  </Button>
                </Link>
              )}
              {canAccessFeature(user?.role, 'admin') && (
                <Link to="/admin">
                  <Button variant="outline" size="lg" className="gap-2">
                    <Settings className="h-4 w-4" />
                    管理后台
                  </Button>
                </Link>
              )}
            </div>
          </div>

          {/* Right: Epsilon card + mini stats */}
          <div className="flex-shrink-0 flex flex-col items-center gap-4">
            <div className="w-52 h-60 rounded-xl bg-card shadow-neu-raised flex flex-col items-center justify-center gap-2">
              <div className="text-6xl font-extrabold text-primary">ε</div>
              <div className="text-xs text-accent tracking-[0.12em] uppercase font-semibold">Differential Privacy</div>
              <div className="w-16 h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />
              <div className="text-3xl font-bold text-foreground">≤ 1.0</div>
              <div className="text-sm text-muted-foreground">PRIVACY BUDGET</div>
            </div>
            <div className="grid grid-cols-2 gap-3 w-full">
              <div className="rounded-lg bg-card shadow-neu-raised px-4 py-2.5 text-center">
                <div className="text-xl font-bold text-primary">92%+</div>
                <div className="text-xs text-muted-foreground">推荐准确率</div>
              </div>
              <div className="rounded-lg bg-card shadow-neu-raised px-4 py-2.5 text-center">
                <div className="text-xl font-bold text-accent">5K+</div>
                <div className="text-xs text-muted-foreground">药物种类</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="space-y-8">
        <div className="max-w-2xl">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-3">核心功能</h2>
          <p className="text-base md:text-lg text-muted-foreground">
            本系统结合医疗用药场景的数据特点与隐私保护需求，打造全方位的智能用药推荐解决方案
          </p>
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Card key={feature.title} className="group">
                <CardHeader>
                  <div className={`mb-3 flex h-12 w-12 items-center justify-center rounded-sm ${iconBgMap[feature.color]}`}>
                    <Icon className={`h-6 w-6 ${iconColorMap[feature.color]}`} />
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription className="mt-1">{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            )
          })}
        </div>
      </section>

      {/* CTA Section */}
      <section className="rounded-xl bg-gradient-to-br from-surface-elevated to-surface-elevated border border-border px-8 py-14 md:px-14 md:py-16 text-center">
        <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-3">准备好开始了吗？</h2>
        <p className="text-base md:text-lg text-muted-foreground mb-8 max-w-lg mx-auto">
          体验隐私保护与智能推荐的完美结合，为医疗用药决策提供科学依据
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {canAccessFeature(user?.role, 'patients') && (
            <Link to="/patients">
              <Button size="lg" className="gap-2">
                <Users className="h-4 w-4" />
                管理患者档案
              </Button>
            </Link>
          )}
          {canAccessFeature(user?.role, 'recommendation') && (
            <Link to="/recommendation">
              <Button variant="outline" size="lg" className="gap-2">
                <Stethoscope className="h-4 w-4" />
                获取用药推荐
              </Button>
            </Link>
          )}
        </div>
      </section>
    </div>
  )
}
