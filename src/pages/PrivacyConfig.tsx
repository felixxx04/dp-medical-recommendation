import { useState } from 'react'
import {
  Shield,
  Lock,
  Settings,
  CheckCircle2,
  TrendingDown,
  Eye,
  Key,
  Sliders,
  BookOpen,
  BarChart3,
  Activity,
  ChevronUp,
  ChevronDown,
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Label } from '@/components/ui/label'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { usePrivacyStore } from '@/lib/privacyStore'
import type { PrivacyConfig as GlobalPrivacyConfig } from '@/lib/privacy'
import { gaussianSigma, laplaceScale } from '@/lib/privacy'

export default function PrivacyConfig() {
  const { config: globalConfig, setConfig: setGlobalConfig, budget, clearEvents } = usePrivacyStore()
  const [config, setConfig] = useState<GlobalPrivacyConfig>(globalConfig)
  const [savedConfig, setSavedConfig] = useState<GlobalPrivacyConfig | null>(null)
  const [showAlgorithm, setShowAlgorithm] = useState(false)
  const [showResearch, setShowResearch] = useState(false)
  const [showAdvancedParams, setShowAdvancedParams] = useState(false)

  const calculateNoiseScale = () => {
    if (config.noiseMechanism === 'gaussian') return gaussianSigma(config)
    return laplaceScale(config)
  }

  const calculatePrivacyScore = () => {
    const epsilonScore = Math.max(0, 10 - config.epsilon * 5)
    const deltaScore = config.delta < 0.0001 ? 10 : Math.max(0, 10 - config.delta * 10000)
    return ((epsilonScore + deltaScore) / 2).toFixed(1)
  }

  const estimateUtilityLoss = () => {
    const noiseScale = calculateNoiseScale()
    if (noiseScale === Infinity) return '100.0'
    const loss = Math.min(100, noiseScale * 30)
    return loss.toFixed(1)
  }

  const handleSave = () => {
    setSavedConfig({ ...config })
    setGlobalConfig({ ...config })
  }

  const noiseScale = calculateNoiseScale()
  const privacyScore = calculatePrivacyScore()
  const utilityLoss = estimateUtilityLoss()

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section className="border-l-4 border-l-primary bg-background px-6 py-8">
        <div className="flex items-start gap-4">
          <div className="hidden md:flex h-10 w-10 items-center justify-center rounded-sm bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] flex-shrink-0">
            <Shield className="h-5 w-5 text-white" />
          </div>
          <div className="flex-1">
            <h1 className="text-ia-tile font-display font-bold text-foreground mb-2">差分隐私配置</h1>
            <p className="text-ia-body text-muted-foreground max-w-2xl">配置隐私保护参数，在数据安全与模型性能之间寻找最佳平衡点</p>
          </div>
        </div>
      </section>

      {/* Algorithm Explanation — collapsed by default */}
      <div className="rounded-xl bg-background shadow-neu-raised">
        <div
          className="flex items-center justify-between px-5 py-3 cursor-pointer"
          onClick={() => setShowAlgorithm(!showAlgorithm)}
        >
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-primary" />
            <span className="font-heading font-semibold text-ia-body">差分隐私算法原理</span>
          </div>
          <span className="text-ia-label text-muted-foreground">{showAlgorithm ? '收起 ▴' : '展开查看 ▾'}</span>
        </div>
        {showAlgorithm && (
          <div className="border-t border-border px-5 py-4 space-y-4">
            <div className="grid md:grid-cols-2 gap-3">
              <div className="p-3 rounded-sm bg-background border border-border">
                <h4 className="font-heading font-semibold text-ia-caption mb-1.5 flex items-center gap-2">
                  <Shield className="h-3.5 w-3.5 text-primary" />
                  ε-差分隐私定义
                </h4>
                <p className="text-ia-label text-muted-foreground leading-relaxed">
                  对于任意两个相邻数据集 D₁ 和 D₂，以及任意输出 S：
                  <code className="block mt-1.5 p-1.5 bg-surface-inset rounded-xs text-ia-data overflow-x-auto">
                    Pr[M(D₁) ∈ S] ≤ e^ε × Pr[M(D₂) ∈ S] + δ
                  </code>
                </p>
              </div>
              <div className="p-3 rounded-sm bg-background border border-border">
                <h4 className="font-heading font-semibold text-ia-caption mb-1.5 flex items-center gap-2">
                  <Lock className="h-3.5 w-3.5 text-secondary" />
                  隐私预算 ε
                </h4>
                <p className="text-ia-label text-muted-foreground leading-relaxed">
                  ε 越小，隐私保护越强，但数据效用越低。推荐范围：0.1 ~ 10
                  <span className="block mt-1">本系统默认 ε = 1.0，提供强隐私保护</span>
                </p>
              </div>
            </div>

            <Accordion type="single" collapsible className="w-full">
              <AccordionItem value="mechanism">
                <AccordionTrigger>噪声机制详解</AccordionTrigger>
                <AccordionContent>
                  <div className="grid md:grid-cols-3 gap-2 pt-3">
                    <div className="p-2.5 rounded-sm border border-primary/12 bg-primary/8">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1">Laplace 机制</h5>
                      <p className="text-ia-label text-muted-foreground">添加 Laplace 噪声：Noise ~ Lap(Δf/ε)。适用于数值型查询，提供纯ε-DP 保证</p>
                    </div>
                    <div className="p-2.5 rounded-sm border border-secondary/20 bg-secondary/8">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1">Gaussian 机制</h5>
                      <p className="text-ia-label text-muted-foreground">添加高斯噪声：Noise ~ N(0, σ²)。适用于高维数据，提供 (ε,δ)-DP 保证</p>
                    </div>
                    <div className="p-2.5 rounded-sm border border-primary/12 bg-primary/8">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1">Geometric 机制</h5>
                      <p className="text-ia-label text-muted-foreground">离散版本的 Laplace 机制。适用于计数查询和离散数据</p>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="application">
                <AccordionTrigger>应用场景说明</AccordionTrigger>
                <AccordionContent>
                  <div className="grid md:grid-cols-3 gap-2 pt-3">
                    <div className="p-2.5 rounded-sm bg-background border border-border">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1 flex items-center gap-1.5"><Eye className="h-3.5 w-3.5" />数据层扰动</h5>
                      <p className="text-ia-label text-muted-foreground">在原始数据发布前添加噪声，适用于数据共享场景</p>
                    </div>
                    <div className="p-2.5 rounded-sm bg-background border border-border">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1 flex items-center gap-1.5"><Sliders className="h-3.5 w-3.5" />梯度扰动</h5>
                      <p className="text-ia-label text-muted-foreground">在深度学习训练过程中对梯度添加噪声，适用于联邦学习</p>
                    </div>
                    <div className="p-2.5 rounded-sm bg-background border border-border">
                      <h5 className="font-heading font-semibold text-ia-caption mb-1 flex items-center gap-1.5"><Settings className="h-3.5 w-3.5" />模型层扰动</h5>
                      <p className="text-ia-label text-muted-foreground">对训练完成的模型参数添加噪声，适用于模型发布</p>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        )}
      </div>

      {/* Configuration Panel */}
      <div className="grid lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2 space-y-5">
          {/* Privacy Parameters — core 2 + advanced collapsible */}
          <Card hover="none">
            <CardHeader>
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-gradient-to-br from-[#0a9dc4] to-[#077f9f]">
                  <Shield className="h-4 w-4 text-white" />
                </div>
                <div>
                  <CardTitle>核心参数</CardTitle>
                  <CardDescription>设置差分隐私核心参数</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* ε slider */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2" title="ε越小隐私保护越强，推荐范围0.1~10"><Key className="h-3.5 w-3.5" />隐私预算 ε (Epsilon)</Label>
                  <span className="text-xl font-heading font-bold text-primary">{config.epsilon.toFixed(3)}</span>
                </div>
                <Slider value={config.epsilon} min={0.1} max={10} step={0.1} onChange={(value) => setConfig({ ...config, epsilon: value })} showTooltip={false} />
                <div className="flex justify-between text-ia-label text-muted-foreground">
                  <span>强保护 (0.1)</span>
                  <span>平衡 (1.0)</span>
                  <span>高效用 (10.0)</span>
                </div>
              </div>

              {/* ε_total slider */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2" title="串行组合记账，累计不超过总预算"><BarChart3 className="h-3.5 w-3.5" />总隐私预算 (会话级 ε_total)</Label>
                  <span className="text-xl font-heading font-bold text-primary">{config.privacyBudget.toFixed(1)}</span>
                </div>
                <Slider value={config.privacyBudget} min={0} max={50} step={0.5} onChange={(value) => setConfig({ ...config, privacyBudget: value })} showTooltip={false} />
              </div>

              {/* Advanced params toggle */}
              <div className="pt-2">
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
                <div className="space-y-6 pt-4 border-t border-border">
                  {/* δ slider */}
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2"><Lock className="h-3.5 w-3.5" />松弛参数 δ (Delta)</Label>
                      <span className="text-xl font-heading font-bold text-primary">{config.delta.toExponential(2)}</span>
                    </div>
                    <Slider value={config.delta} min={0.000001} max={0.001} step={0.000001} onChange={(value) => setConfig({ ...config, delta: value })} showTooltip={false} />
                    <p className="text-ia-label text-muted-foreground">δ 表示隐私保护失败的概率，应远小于 1/数据库大小</p>
                  </div>

                  {/* Δf slider */}
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2"><TrendingDown className="h-3.5 w-3.5" />全局敏感度 Δf</Label>
                      <span className="text-xl font-heading font-bold text-primary">{config.sensitivity.toFixed(2)}</span>
                    </div>
                    <Slider value={config.sensitivity} min={0.01} max={1.0} step={0.01} onChange={(value) => setConfig({ ...config, sensitivity: value })} showTooltip={false} />
                    <p className="text-ia-label text-muted-foreground">敏感度衡量单个记录变化对查询结果的最大影响（sigmoid输出范围[0,1]，上限1.0）</p>
                  </div>

                  {/* Noise Mechanism Selection */}
                  <div className="space-y-3">
                    <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2"><Settings className="h-3.5 w-3.5" />噪声机制</Label>
                    <div className="grid md:grid-cols-3 gap-3">
                      {[
                        { id: 'laplace', name: 'Laplace', desc: '数值查询，纯ε-DP', icon: TrendingDown },
                        { id: 'gaussian', name: 'Gaussian', desc: '高维数据，(ε,δ)-DP', icon: Sliders },
                        { id: 'geometric', name: 'Geometric', desc: '离散数据，计数查询', icon: BarChart3 },
                      ].map((mechanism) => {
                        const Icon = mechanism.icon
                        const isActive = config.noiseMechanism === mechanism.id
                        return (
                          <button
                            key={mechanism.id}
                            onClick={() => setConfig({ ...config, noiseMechanism: mechanism.id as any })}
                            className={`p-3 rounded-sm border transition-colors duration-150 text-left cursor-pointer ${
                              isActive ? 'border-primary bg-primary/8' : 'border-border hover:border-primary/30'
                            }`}
                          >
                            <Icon className={`h-5 w-5 mb-1.5 ${isActive ? 'text-primary' : 'text-foreground'}`} />
                            <div className={`font-heading font-semibold text-ia-caption ${isActive ? 'text-primary' : 'text-foreground'}`}>{mechanism.name}</div>
                            <div className="text-ia-label text-muted-foreground mt-0.5">{mechanism.desc}</div>
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  {/* Application Stage */}
                  <div className="space-y-3">
                    <Label className="text-ia-caption font-heading font-semibold flex items-center gap-2"><Eye className="h-3.5 w-3.5" />应用阶段</Label>
                    <div className="grid md:grid-cols-3 gap-3">
                      {[
                        { id: 'data', name: '数据层', desc: '原始数据扰动' },
                        { id: 'gradient', name: '梯度层', desc: '训练过程扰动' },
                        { id: 'model', name: '模型层', desc: '模型参数扰动' },
                      ].map((stage) => (
                        <button
                          key={stage.id}
                          onClick={() => setConfig({ ...config, applicationStage: stage.id as any })}
                          className={`p-3 rounded-sm border transition-colors duration-150 text-left cursor-pointer ${
                            config.applicationStage === stage.id ? 'border-primary bg-primary/8' : 'border-border hover:border-primary/30'
                          }`}
                        >
                          <div className="font-heading font-semibold text-ia-caption">{stage.name}</div>
                          <div className="text-ia-label text-muted-foreground mt-0.5">{stage.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Real-time Metrics */}
        <div className="space-y-5">
          <Card hover="none" className="sticky top-20 border-primary/12">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-base">
                <Activity className="h-4 w-4 text-primary" />
                实时指标分析
              </CardTitle>
              <CardDescription>基于当前配置的评估结果</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Real-time metrics — merged compact block */}
              <div className="p-3 rounded-sm bg-background border border-border space-y-3">
                <div className="flex items-center gap-2 mb-1">
                  <Activity className="h-3.5 w-3.5 text-primary" />
                  <span className="text-ia-caption font-heading font-semibold">实时评估</span>
                  <span className="text-ia-label text-muted-foreground ml-auto">
                    ε={config.epsilon.toFixed(1)}时 · 保护强度 <strong className={parseFloat(privacyScore) >= 8 ? 'text-success' : parseFloat(privacyScore) >= 6 ? 'text-secondary' : 'text-ia-data-4'}>{privacyScore}/10</strong>
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
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="text-ia-label cursor-pointer" onClick={() => { clearEvents() }}>重置消耗</Button>
                </div>
              </div>

              {/* Trade-off Visualization */}
              <div className="p-4 rounded-sm bg-surface-inset border border-border">
                <div className="text-ia-caption font-heading font-semibold mb-1">隐私 - 效用权衡</div>
                <p className="text-ia-label text-muted-foreground mb-3">隐私保护越强（ε 越小），模型效用越低</p>
                <div className="relative h-48">
                  <svg viewBox="0 0 240 130" className="w-full h-full">
                    {/* Grid lines */}
                    <line x1="55" y1="15" x2="55" y2="105" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="100" y1="15" x2="100" y2="105" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="145" y1="15" x2="145" y2="105" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="190" y1="15" x2="190" y2="105" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="55" y1="40" x2="225" y2="40" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="55" y1="65" x2="225" y2="65" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    <line x1="55" y1="85" x2="225" y2="85" stroke="rgba(155,175,200,0.12)" strokeWidth="0.5" />
                    {/* Axes */}
                    <line x1="55" y1="105" x2="225" y2="105" stroke="rgba(155,175,200,0.25)" strokeWidth="1.5" />
                    <line x1="55" y1="105" x2="55" y2="15" stroke="rgba(155,175,200,0.25)" strokeWidth="1.5" />
                    {/* Y-axis ticks */}
                    <text x="50" y="19" fontSize="8" fill="#5e7f92" textAnchor="end">100%</text>
                    <text x="50" y="43" fontSize="8" fill="#5e7f92" textAnchor="end">75%</text>
                    <text x="50" y="68" fontSize="8" fill="#5e7f92" textAnchor="end">50%</text>
                    <text x="50" y="93" fontSize="8" fill="#5e7f92" textAnchor="end">25%</text>
                    <text x="50" y="109" fontSize="8" fill="#5e7f92" textAnchor="end">0%</text>
                    {/* Axis labels */}
                    <text x="140" y="125" fontSize="9" fill="#3d5f73" textAnchor="middle">隐私预算 ε（越小越强）</text>
                    <text x="26" y="60" fontSize="9" fill="#3d5f73" textAnchor="middle" transform="rotate(-90, 26, 60)">模型效用</text>
                    {/* Area fill under curve */}
                    <path d="M 55 105 L 55 25 Q 90 35, 140 58 T 225 100 L 225 105 Z" fill="rgba(8,145,178,0.08)" />
                    {/* Curve */}
                    <path d="M 55 25 Q 90 35, 140 58 T 225 100" fill="none" stroke="#0891b2" strokeWidth="2.5" strokeLinecap="round" />
                    {/* Corner annotations */}
                    <text x="62" y="16" fontSize="8" fill="rgba(94,127,146,0.6)">效用最高</text>
                    <text x="58" y="100" fontSize="8" fill="rgba(94,127,146,0.6)">强隐私</text>
                    <text x="175" y="100" fontSize="8" fill="rgba(94,127,146,0.6)">弱隐私</text>
                    {/* Current point on bezier curve */}
                    {(() => {
                      // Bezier: M(55,25) Q(90,35)→(140,58) T(225,100) with implied ctrl=(190,81)
                      const eps = config.epsilon
                      let cx: number, cy: number
                      if (eps <= 5) {
                        const t = eps / 5  // segment 1: epsilon [0,5] → t [0,1]
                        const t1 = 1 - t
                        cx = t1*t1*55 + 2*t1*t*90 + t*t*140
                        cy = t1*t1*25 + 2*t1*t*35 + t*t*58
                      } else {
                        const t = (eps - 5) / 5  // segment 2: epsilon [5,10] → t [0,1]
                        const t1 = 1 - t
                        cx = t1*t1*140 + 2*t1*t*190 + t*t*225
                        cy = t1*t1*58 + 2*t1*t*81 + t*t*100
                      }
                      return (
                        <g>
                          <line x1={cx} y1={cy} x2={cx} y2="105" stroke="rgba(20,184,166,0.2)" strokeWidth="1" strokeDasharray="3,3" />
                          <line x1="55" y1={cy} x2={cx} y2={cy} stroke="rgba(20,184,166,0.2)" strokeWidth="1" strokeDasharray="3,3" />
                          <circle cx={cx} cy={cy} r="6" fill="#14b8a6" stroke="#dde6f0" strokeWidth="2" />
                          <circle cx={cx} cy={cy} r="2.5" fill="white" opacity="0.9" />
                          <text x="220" y="20" fontSize="9" fill="#14b8a6" fontWeight="bold" textAnchor="end">
                            当前 ε={eps.toFixed(1)}
                          </text>
                        </g>
                      )
                    })()}
                  </svg>
                </div>
                <div className="flex justify-between text-ia-label text-muted-foreground mt-2 px-2">
                  <span>ε = 0.1 · 强隐私保护</span>
                  <span>ε = 10 · 弱隐私 · 高精度</span>
                </div>
              </div>

              <Button onClick={handleSave} className="w-full gap-2 cursor-pointer" size="lg">
                <CheckCircle2 className="h-4 w-4" />
                保存配置
              </Button>

              {savedConfig && (
                <div className="p-2.5 rounded-sm border border-success/30 bg-success/6">
                  <div className="flex items-center gap-2 text-success text-ia-caption">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span className="font-heading font-semibold">配置已保存！ε={savedConfig.epsilon.toFixed(2)}</span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Research Content — collapsed by default */}
      <div className="rounded-xl bg-background shadow-neu-flat">
        <div
          className="flex items-center justify-between px-5 py-3 cursor-pointer"
          onClick={() => setShowResearch(!showResearch)}
        >
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-muted-foreground" />
            <span className="font-heading font-semibold text-ia-body text-muted-foreground">课题研究内容</span>
          </div>
          <span className="text-ia-label text-muted-foreground">{showResearch ? '收起 ▴' : '展开查看 ▾'}</span>
        </div>
        {showResearch && (
          <div className="border-t border-border px-5 py-4">
            <div className="grid md:grid-cols-2 gap-5">
              <div className="space-y-2.5">
                <h4 className="font-heading font-semibold text-ia-caption flex items-center gap-2">
                  <CheckCircle2 className="h-3.5 w-3.5 text-primary" />
                  研究重点
                </h4>
                <ul className="space-y-1.5 text-ia-caption text-muted-foreground">
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] mt-1.5" /><span>医疗数据稀疏性下的隐私预算优化分配策略</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] mt-1.5" /><span>深度学习梯度更新过程中的自适应噪声注入机制</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] mt-1.5" /><span>多阶段差分隐私组合定理的应用与隐私开销累积分析</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] mt-1.5" /><span>药物特征向量化过程中的局部差分隐私保护</span></li>
                </ul>
              </div>
              <div className="space-y-2.5">
                <h4 className="font-heading font-semibold text-ia-caption flex items-center gap-2">
                  <Activity className="h-3.5 w-3.5 text-secondary" />
                  技术路线
                </h4>
                <ul className="space-y-1.5 text-ia-caption text-muted-foreground">
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5" /><span>基于敏感度的自适应噪声缩放算法</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5" /><span>联邦学习框架下的分布式差分隐私实现</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5" /><span>隐私预算的动态调度与最优分配算法</span></li>
                  <li className="flex items-start gap-2"><div className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5" /><span>模型可解释性与隐私保护的协同优化</span></li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
