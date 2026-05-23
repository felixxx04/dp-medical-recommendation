# 毕业设计答辩PPT - Design Spec

> Human-readable design narrative. Machine-readable execution contract: `spec_lock.md`.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | 毕业设计答辩 — 差分隐私保护的AI驱动个性化医疗用药推荐系统 |
| **Canvas Format** | PPT 16:9 (1280×720) |
| **Page Count** | 13 |
| **Design Style** | B) General Consulting + 学术答辩，简洁专业 |
| **Target Audience** | 答辩委员会（3-5位评委老师） |
| **Use Case** | 本科毕业设计答辩，约15-20分钟陈述 |
| **Created Date** | 2026-05-15 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280×720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | 左右60px，上下50px |
| **Content Area** | 1160×620 (60px左右边距, 50px上下边距) |

---

## III. Visual Theme

### Theme Style

- **Style**: 学术答辩，简洁专业
- **Theme**: Light theme
- **Tone**: 克制、专业、数据驱动，避免花哨装饰

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#FFFFFF` | 页面白色背景 |
| **Secondary bg** | `#F5F7FA` | 卡片/区块浅灰背景 |
| **Primary** | `#00796B` | Teal绿 — 标题装饰、关键标记、图标主色 |
| **Accent** | `#1565C0` | 深蓝 — 数据标注、技术术语、链接 |
| **Secondary accent** | `#FF8F00` | 琥珀色 — 注意事项/警告标记 |
| **Body text** | `#1A1A2E` | 深蓝黑正文 |
| **Secondary text** | `#546E7A` | 灰蓝 — 标注/说明/副标题 |
| **Tertiary text** | `#90A4AE` | 浅灰蓝 — 页脚/页码 |
| **Border/divider** | `#E0E0E0` | 卡片边框、分割线 |
| **Success** | `#2E7D32` | 安全/通过标记（绿色） |
| **Warning** | `#C62828` | 禁忌/危险标记（红色） |

### Gradient Scheme

```xml
<!-- 标题下划线装饰渐变 -->
<linearGradient id="titleUnderline" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#00796B"/>
  <stop offset="100%" stop-color="#1565C0"/>
</linearGradient>

<!-- 封面背景装饰 -->
<radialGradient id="coverDecor" cx="80%" cy="20%" r="60%">
  <stop offset="0%" stop-color="#00796B" stop-opacity="0.08"/>
  <stop offset="100%" stop-color="#00796B" stop-opacity="0"/>
</radialGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: 学术对比 — 楷体标题+微软雅黑正文

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `KaiTi` | `Georgia` | `serif` |
| **Body** | `"Microsoft YaHei"`, `"PingFang SC"` | `Arial` | `sans-serif` |
| **Emphasis** | `KaiTi` | `Georgia` | `serif` |
| **Code** | — | `Consolas`, `"Courier New"` | `monospace` |

**Per-role font stacks**:

- Title: `KaiTi, Georgia, serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `KaiTi, Georgia, serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 20px (中等密度)

| Purpose | Ratio | px | Weight |
| ------- | ----- | --- | ------ |
| Cover title | 2.5-5x | 52-64px | Bold |
| Page title | 1.5-2x | 30-36px | Bold |
| Subtitle | 1.2-1.5x | 24-28px | SemiBold |
| **Body content** | **1x** | **20px** | Regular |
| Annotation / caption | 0.7-0.85x | 14-17px | Regular |
| Page number | 0.5-0.65x | 10-13px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 高50px，左侧页面标题，标题下方2px渐变下划线装饰
- **Content area**: 高580px，主体内容
- **Footer area**: 高40px，右下角页码

### Layout Pattern Library

| Pattern | 本PPT适用页面 |
| ------- | ------------- |
| **Single column centered** | P01封面、P13致谢 |
| **Asymmetric split (4:6)** | P02背景痛点（左图右文） |
| **Center-radiating** | P03研究目标（四层架构核心概念） |
| **Top-bottom split** | P04系统架构（上图下说明） |
| **Three/four column cards** | P05核心算法1（三层并排） |
| **Center-radiating / flow** | P06核心算法2（推荐流程） |
| **Asymmetric split (5:5)** | P07差分隐私（左原理右数据） |
| **Three-column cards** | P08 DeepFM模型改进 |
| **Four-quadrant** | P09关键实现 |
| **Top-bottom split** | P10界面截图 |
| **Symmetric split + table** | P11实验结果 |
| **Single column + bullets** | P12结论展望 |
| **Negative-space-driven** | P13致谢 |

### Spacing Specification

**Universal**:

| Element | Range | Current Project |
| ------- | ----- | --------------- |
| Safe margin from canvas edge | 40-60px | 60px |
| Content block gap | 24-40px | 32px |
| Icon-text gap | 8-16px | 12px |

**Card-based layouts** (dense pages):

| Element | Range | Current Project |
| ------- | ----- | --------------- |
| Card gap | 20-32px | 24px |
| Card padding | 20-32px | 24px |
| Card border radius | 8-16px | 10px |
| Three-column card width | 360-380px | 370px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `templates/icons/tabler-outline/` (stroke-style)
- **Stroke width**: 2 (deck-wide)

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| 安全过滤 | `tabler-outline/shield-check` | P05, P06 |
| 隐私锁定 | `tabler-outline/lock` | P07 |
| 大脑/智能 | `tabler-outline/brain` | P08 |
| 数据库 | `tabler-outline/database` | P04 |
| 用户/角色 | `tabler-outline/users` | P09 |
| 图表 | `tabler-outline/chart-bar` | P11 |
| 警告 | `tabler-outline/alert-triangle` | P05, P07 |
| 过滤器 | `tabler-outline/filter` | P05 |
| 层叠架构 | `tabler-outline/layers` | P04 |
| 胶囊/药物 | `tabler-outline/capsule` | P02 |
| 实验瓶 | `tabler-outline/flask` | P11 |
| 确认 | `tabler-outline/circle-check` | P09 |
| 眼睛/可视化 | `tabler-outline/eye` | P10 |
| 目标 | `tabler-outline/target` | P03 |
| 闪电/性能 | `tabler-outline/bolt` | P11 |
| 代码 | `tabler-outline/code` | P08 |

---

## VII. Visualization Reference List

Catalog read: 71 templates

| Page | Template | Path | Summary-quote (verbatim) | Usage |
| ---- | -------- | ---- | ------------------------ | ----- |
| P05 | process_flow | `templates/charts/process_flow.svg` | "Pick for 3-8 sequential steps connected by simple arrows — approval workflows, customer onboarding, request handling, lifecycle stages. Skip if cyclical (use circular_stages) or stages produce named outputs (use pipeline_with_stages)." | 三层推荐架构的顺序流程展示 |
| P11 | kpi_cards | `templates/charts/kpi_cards.svg` | "Pick for 4-8 standalone numeric metrics shown as overview cards (2x2 or 1x4) — exec summary opener, dashboard headline, quarterly recap, results-at-a-glance. Skip if metrics have target baselines (use bullet_chart) or single hero number (use gauge_chart)." | 实验结果关键指标概览 |

**Runners-up considered**:

- `numbered_steps` | rejected for P05: 三层架构需要展示层间关系和箭头连接，numbered_steps缺乏连接语义
- `icon_grid` | rejected for P05: 需要顺序流程而非并行特征展示
- `vertical_list` | rejected for P11: 实验结果适合KPI卡片展示，比纯文本列表更直观

---

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Status | Acquire Via | Reference |
| -------- | --------- | ----- | ------- | ---- | ------ | ----------- | --------- |
| screenshot_review.png | 1280x720 | 1.78 | 推荐审核界面截图 | Photography | Placeholder | user | 推荐审核页面，左侧待审核列表+右侧审核面板 |
| screenshot_privacy.png | 1280x720 | 1.78 | 隐私配置界面截图 | Photography | Placeholder | user | 隐私配置页面，参数配置+效用权衡图表 |
| screenshot_dashboard.png | 1280x720 | 1.78 | 推荐统计仪表板截图 | Photography | Placeholder | user | 推荐统计页面，趋势图+分类分布+安全分层 |
| screenshot_home.png | 1280x720 | 1.78 | 系统首页截图 | Photography | Placeholder | user | 系统首页，核心数据指标+功能模块卡片 |

---

## IX. Content Outline

### Part 1: 封面

#### Slide 01 - Cover

- **Layout**: Single column centered + radial gradient装饰
- **Title**: 差分隐私保护的AI驱动的个性化医疗用药推荐系统的设计与实现
- **Subtitle**: 本科毕业设计答辩
- **Info**: 学生：晋修慧 / 指导教师：侯慧莹 讲师 / 院系：人工智能与大数据 大数据2203 / 2026年3月

### Part 2: 研究背景与痛点

#### Slide 02 - 研究背景与痛点

- **Layout**: Asymmetric split (左4右6)
- **Title**: 研究背景与痛点
- **Content**:
  - 医疗数据年增长30%+，互联网医院超2700家，电子病历普及率超85%
  - 2022年全球医疗行业700+起重大数据泄露，影响5000万+患者
  - 传统隐私保护（K-匿名、L-多样性）无法抵御关联攻击和背景知识推断
  - ε-差分隐私提供数学可证明的安全保障，但与推荐系统融合研究匮乏
  - 现有医疗推荐可解释性不足，隐私保护与推荐精度难以兼顾

### Part 3: 研究目标与整体思路

#### Slide 03 - 研究目标与整体思路

- **Layout**: Center-radiating（四层架构核心概念）
- **Title**: 研究目标：四层推荐架构
- **Content**:
  - 核心目标：在差分隐私保护下兼顾临床安全与推荐精度
  - 第零层 KnowledgeRouter：四级确定性路由（L1口语标准化→L2疾病归类→L3适应症映射→L4药品召回），解决中文疾病名→英文适应症的语义鸿沟
  - 第一层 SafetyFilter：12条绝对安全红线硬排除，9类软标记
  - 第二层 RuleMarker：相对禁忌/中等交互/妊娠C-D警告等软标记
  - 第三层 DeepFM：个性化排序，DP噪声仅在此层应用

### Part 4: 系统总体架构

#### Slide 04 - 系统总体架构

- **Layout**: Top-bottom split（架构图+技术栈说明）
- **Title**: 系统总体架构
- **Content**:
  - 三服务微服务架构：前端(React 18 + TypeScript + Vite, port 5173) ↔ 后端(Spring Boot 3.2 + MyBatis + MySQL, port 8080) ↔ 模型服务(FastAPI + PyTorch DeepFM, port 8001)
  - 数据流：前端→后端(认证/CRUD)→模型服务(/model/predict)→三层架构+DP噪声→返回推荐
  - 启动时后端加载全部1807种药物→模型服务(/model/load-drugs)
  - 数据库：sys_user / patient / drug / recommendation / privacy_config / privacy_ledger

### Part 5: 核心算法1

#### Slide 05 - 临床知识路由与三层安全架构

- **Layout**: Three-column cards（三列并排展示三层）
- **Title**: 三层推荐安全架构
- **Visualization**: process_flow
- **Content**:
  - SafetyFilter（左列）：12条硬排除规则 — 过敏冲突、绝对禁忌症、致命交互、妊娠X级、儿科禁忌、哺乳期L5等；9类软标记 — 相对禁忌改为"标记待审"，医生做最终判断
  - RuleMarker（中列）：7种软标记规则 — 相对禁忌症、中等交互、妊娠C/D警告、肾功能警告、肝功能警告、生育力警告、数据未验证；标记而非排除，候选药物保留参与排序
  - DeepFM排序（右列）：对安全候选药物精准评分，DP噪声仅在此层应用；关键原则：噪声不影响安全过滤的确定性判断

### Part 6: 核心算法2

#### Slide 06 - 推荐流程与口语增强

- **Layout**: Top-bottom split（上方流程图，下方口语增强说明）
- **Title**: 推荐流程与患者口语增强
- **Content**:
  - 完整推荐9步流程：获取患者信息→DiseaseMapper中文→英文映射→SafetyFilter过滤→RuleMarker标记→DeepFM评分+DP噪声→疾病平衡选择→解释生成→DDI检查→质量保障
  - 患者口语增强PatientInputEnhancer：三层fallback — 精确匹配→关键词匹配→症状组合推理；全部失败则降级为症状级推荐+低置信度标记
  - 审核反馈闭环：医生确认/修改/拒绝→FeedbackLearner渐进式惩罚（1次×0.7, 2次×0.5, 3次+×0.3）→持续优化推荐权重

### Part 7: 差分隐私推理阶段保护

#### Slide 07 - 差分隐私推理阶段保护

- **Layout**: Asymmetric split (5:5)
- **Title**: 差分隐私推理阶段保护
- **Content**:
  - 噪声机制：Laplace (scale=Δf/ε) 和 Gaussian (σ=Δf×√(2ln(1.25/δ))/ε)
  - 临床阈值后处理（基于DP后处理定理，不降低隐私保护）：
    - score < 0.15 置零（低分药物不被噪声意外提升）
    - ceiling = min(1.0, raw+0.35)（防止噪声将低分放大超过3.5倍）
    - dpAnomaly标记（噪声显著改变排序方向时触发）
    - 95%置信区间（Laplace CI=±2b/√3, Gaussian CI=±1.96σ）
  - 隐私预算管理：强组合定理追踪 + BudgetWarningLevel三级预警 + 双重追踪（MySQL持久化 + 内存Tracker）
  - 默认配置：ε=0.1 Gaussian噪声

### Part 8: DeepFM v3模型改进

#### Slide 08 - DeepFM v3模型改进

- **Layout**: Three-column cards
- **Title**: DeepFM v3模型改进
- **Content**:
  - 合并嵌入(Merged Embedding)：单个nn.Embedding + field_offsets寄存器 → Opacus兼容DP训练；15个类别字段共享嵌入空间，embed_dim=8
  - 连续特征旁路：4个连续特征(age_raw, bmi_raw, gfr_raw, liver_score_raw)绕过嵌入/FM/Deep，独立线性变换后与FM+Deep输出拼接；避免连续特征经嵌入层的信息损失，GFR和肝功能评分直接参与评分
  - 训练优化：LayerNorm替代BatchNorm（推理无需批统计量）、差异化Dropout(0.3/0.1)、Focal Loss(α=0.25, γ=2.0)应对正负样本不平衡

### Part 9: 关键实现

#### Slide 09 - 关键实现

- **Layout**: Four-quadrant (2×2)
- **Title**: 关键实现
- **Content**:
  - 三角色RBAC：管理员(全权限)/医生(患者管理+推荐审核)/研究员(隐私分析)；前后端双重权限校验
  - 审核反馈闭环：医生确认/修改/拒绝→FeedbackLearner渐进式惩罚→持续优化
  - 推荐解释生成：适应症匹配详情+安全性分析+推荐理由说明；ClinicalMatcher标准化匹配替代子串匹配，准确率95%+
  - 全字段中文翻译：drug_translator + translation_mapper，药物名/安全类型/副作用等全字段英→中

### Part 10: 系统界面截图

#### Slide 10 - 系统界面展示

- **Layout**: Top-bottom split (上方2×2截图网格，下方简短标注)
- **Title**: 系统界面展示
- **Content**:
  - 推荐审核页面：左侧待审核列表 + 右侧审核面板 + 安全级别标签(绿/黄/橙/紫)
  - 隐私配置页面：ε/δ/噪声机制参数配置 + 隐私-效用权衡图表 + 预算管理
  - 推荐统计仪表板：趋势折线图 + 药物推荐频次Top10 + ATC分类饼图 + 安全分层漏斗
  - 系统首页：核心数据指标 + 四大功能模块

### Part 11: 实验与测试结果

#### Slide 11 - 实验与测试结果

- **Layout**: KPI cards (上方4个指标卡) + 下方数据表格
- **Title**: 实验与测试结果
- **Visualization**: kpi_cards
- **Content**:
  - KPI卡片：ε=0.1准确率下降约10%、DP性能开销≈5ms、推荐响应<2s、药物候选1807种
  - 隐私预算vs准确率：ε=1.0下降约2%，ε=0.5下降约5%，ε=0.1下降约10%
  - 安全数据覆盖：禁忌症95.3%(1831/1815)、交互81.5%(1480/1815)、总体97.0%
  - 适应症路由覆盖率92.5%，支持1295种中文疾病输入
  - 功能测试12项全部通过，SafetyFilter不受DP噪声影响

### Part 12: 结论与未来工作

#### Slide 12 - 结论与未来工作

- **Layout**: Single column + bullets（上下分：结论+展望）
- **Title**: 结论与未来工作
- **Content**:
  - 主要工作：四层推荐架构（知识路由+安全过滤+规则标记+DeepFM排序）；差分隐私与深度学习融合，推理阶段临床阈值后处理保障安全性不受噪声干扰；口语增强+审核反馈闭环，构建从患者表达到药品推荐的完整链路
  - 未来方向：扩充120个罕见病路由覆盖至100%；审核反馈数据持续优化路由权重；安全性数据编码为DeepFM特征实现更精细排序

### Part 3: 致谢

#### Slide 13 - 致谢

- **Layout**: Negative-space-driven（大面积留白，居中文字）
- **Title**: 致谢
- **Content**:
  - 感谢指导教师侯慧莹老师的悉心指导
  - 感谢人工智能与大数据学院各位老师的培养
  - 感谢家人的理解与支持

---

## X. Speaker Notes Requirements

- **Duration**: 15-20分钟
- **Notes style**: conversational — 自然口吻，像在跟评委老师讲故事
- **Filename**: 匹配SVG名称 (01_cover.md, 02_background.md, ...)
- **Content**: 每页2-3个要点关键词，时间提示，过渡语

---

## XI. Technical Constraints Reminder

1. viewBox: `0 0 1280 720`
2. Background uses `<rect>` elements
3. Text wrapping uses `<tspan>` (`<foreignObject>` FORBIDDEN)
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` FORBIDDEN
5. FORBIDDEN: `mask`, `<style>`, `class`, `foreignObject`
6. FORBIDDEN: `textPath`, `animate*`, `script`
7. Text characters: raw Unicode (em dash `—`, en dash `–`, `→`, NBSP etc.); HTML named entities FORBIDDEN; XML reserved chars escaped as `&amp;` `&lt;` `&gt;` `&quot;` `&apos;`
8. `marker-start` / `marker-end` conditionally allowed: `<marker>` in `<defs>`, `orient="auto"`, triangle/diamond/circle shape
9. `clipPath` conditionally allowed only on `<image>` elements
10. `<g opacity="...">` FORBIDDEN; set opacity on each child individually
