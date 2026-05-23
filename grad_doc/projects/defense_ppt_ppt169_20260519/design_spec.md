# defense_ppt - Design Spec

> Human-readable design narrative. Machine-readable execution contract: `spec_lock.md`.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | defense_ppt |
| **Canvas Format** | PPT 16:9 (1280×720) |
| **Page Count** | 11 |
| **Design Style** | Top Consulting + academic defense |
| **Target Audience** | 答辩委员会（计算机科学方向教授3-5人） |
| **Use Case** | 本科毕业设计答辩，6分钟陈述 |
| **Created Date** | 2026-05-19 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280×720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | Left/right 60px, top 50px, bottom 40px |
| **Content Area** | 1160×630 (after margins) |

---

## III. Visual Theme

### Theme Style

- **Style**: Top Consulting + academic defense
- **Theme**: Light theme (cream background from university template)
- **Tone**: Academic, data-driven, logical persuasion

### Color Scheme

Based on 河南工业大学PPT模板 extracted colors, adapted for defense readability.

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#EFE6DD` | 页面底色（模板奶油色） |
| **Secondary bg** | `#FFFFFF` | 卡片、内容区背景 |
| **Primary** | `#2E3F55` | 标题、重点文字、图标 |
| **Accent** | `#AE6339` | 数据高亮、关键指标、强调色 |
| **Secondary accent** | `#D4B5B2` | 辅助装饰、分隔线 |
| **Body text** | `#2E3F55` | 正文 |
| **Secondary text** | `#6B7B8D` | 说明文字、注释 |
| **Border/divider** | `#D4B5B2` | 卡片边框、分隔线 |
| **Success** | `#2E7D32` | 正向指标（DP不降质等） |
| **Warning** | `#C62828` | 安全警告标记 |

### Gradient Scheme

```xml
<linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#2E3F55"/>
  <stop offset="100%" stop-color="#AE6339"/>
</linearGradient>

<radialGradient id="bgDecor" cx="80%" cy="20%" r="50%">
  <stop offset="0%" stop-color="#2E3F55" stop-opacity="0.08"/>
  <stop offset="100%" stop-color="#2E3F55" stop-opacity="0"/>
</radialGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: academic serif title + CJK sans body (方案B Contrast)

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `SimSun` | `Georgia` | `serif` |
| **Body** | `"Microsoft YaHei", "PingFang SC"` | `Arial` | `sans-serif` |
| **Emphasis** | `SimSun` | `Georgia` | `serif` |
| **Code** | — | `Consolas, "Courier New"` | `monospace` |

**Per-role font stacks**:

- Title: `Georgia, SimSun, serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `SimSun, Georgia, serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 20px (medium density, defense readability)

| Purpose | Ratio to body | Example @ body=20 | Weight |
| ------- | ------------- | ------------------ | ------ |
| Cover title | 2.5-5x | 50-100px | Bold |
| Chapter / section opener | 2-2.5x | 40-50px | Bold |
| Page title | 1.5-2x | 30-40px | Bold |
| Subtitle | 1.2-1.5x | 24-30px | SemiBold |
| **Body content** | **1x** | **20px** | Regular |
| Annotation / caption | 0.7-0.85x | 14-17px | Regular |
| Page number / footnote | 0.5-0.65x | 10-13px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 0-80px — page title with accent underline
- **Content area**: 80-660px — main content zone
- **Footer area**: 660-720px — page number, slide number indicator

### Layout Pattern Library

| Pattern | Pages Using |
| ------- | ----------- |
| Single column centered | P01 Cover, P11 Thanks |
| Asymmetric split (3:7) | P03 Background, P04 Requirements |
| Center-radiating | P05 Architecture (core radiating 4 layers) |
| Symmetric split (5:5) | P06 DP mechanism (left: principle, right: application) |
| Three-column cards | P07 DeepFM (FM / Deep / Fusion) |
| Four-quadrant / matrix | P08 System (4 module screenshots) |
| Full-bleed + floating text | P02 TOC |
| Z-pattern / waterfall | P09 Results (alternating data points) |
| Negative-space-driven | P10 Conclusion |

### Spacing Specification

**Universal**:

| Element | Value |
| ------- | ----- |
| Safe margin from canvas edge | 50px |
| Content block gap | 30px |
| Icon-text gap | 12px |

**Card-based layouts**:

| Element | Value |
| ------- | ----- |
| Card gap | 24px |
| Card padding | 24px |
| Card border radius | 10px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `templates/icons/chunk-filled/`
- **Usage method**: SVG placeholder `<use data-icon="chunk-filled/icon-name" .../>`

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| 研究背景 | `chunk-filled/book-open` | P02, P03 |
| 需求分析 | `chunk-filled/clipboard` | P02, P04 |
| 架构设计 | `chunk-filled/layers` | P02, P05 |
| 安全/隐私 | `chunk-filled/shield` | P02, P06 |
| 模型/AI | `chunk-filled/bolt` | P02, P07 |
| 系统实现 | `chunk-filled/code-block` | P02, P08 |
| 实验结果 | `chunk-filled/chart-bar` | P02, P09 |
| 结论 | `chunk-filled/circle-checkmark` | P02, P10 |
| 目标 | `chunk-filled/target` | P03 |
| 安全检查 | `chunk-filled/shield-check` | P05 |
| 用药/医疗 | `chunk-filled/pills` | P03, P05 |
| 图表趋势 | `chunk-filled/chart-line` | P09 |
| 列表 | `chunk-filled/list` | P04 |
| 成功 | `chunk-filled/checkmark` | P10 |

---

## VII. Visualization Reference List

Catalog read: 71 templates

| Page | Template | Path | Summary-quote (verbatim) | Usage |
| ---- | -------- | ---- | ------------------------------------------------- | ----- |
| P05 | layered_architecture | `templates/charts/layered_architecture.svg` | "Pick for 3-4 horizontal architecture layers (presentation/service/data), 2-4 module cards per layer, each card = title + 1-line description (description required, even if source brief). Skip if no per-module descriptions (use icon_grid) or no horizontal layering (use module_composition)." | 四层推荐架构：KnowledgeRouter / SafetyFilter / RuleMarker / DeepFM |
| P07 | module_composition | `templates/charts/module_composition.svg` | "Pick for one parent container wrapping 3-N child module cards, each = title + 2-3 bullets — fits 'Feature X contains 3 parts, each with its own description'. Skip if source has only labels without descriptions (use numbered_steps or icon_grid)." | DeepFM模型组成：MultiFieldFM / Deep / Continuous Bypass |
| P09 | grouped_bar_chart | `templates/charts/grouped_bar_chart.svg` | "Pick for 2-4 series side-by-side across the same categories (e.g. YoY/QoQ). Skip if showing composition within each category (use stacked_bar_chart)." | No-DP / DP ε=1.0 / DP ε=0.5 三组AUC-PR与separation对比 |

**Runners-up considered**:

- `icon_grid` | rejected for P05: 四层架构需要层级关系展示，icon_grid是扁平并列
- `process_flow` | rejected for P05: 推荐架构不是线性流程，而是逐层过滤的层级结构
- `hub_spoke` | rejected for P07: DeepFM组件是并列组成关系，不是中心辐射
- `numbered_steps` | rejected for P07: 三个模块是并列结构，非顺序步骤
- `bar_chart` | rejected for P09: 需要多系列对比（3组实验条件），bar_chart仅支持单系列
- `radar_chart` | rejected for P09: 实验指标以AUC-PR和separation为主，雷达图维度不够

---

## VIII. Image Resource List

No images required. All visual elements (architecture diagrams, model diagrams, charts) rendered as SVG.

---

## IX. Content Outline

### Part 1: 开场

#### Slide 01 - 封面

- **Layout**: Single column centered
- **Title**: 差分隐私保护的AI驱动个性化医疗用药推荐系统
- **Subtitle**: 本科毕业设计答辩
- **Info**: 晋修慧 / 河南工业大学 / 2026年5月
- **rhythm**: anchor

#### Slide 02 - 研究框架总览

- **Layout**: Full-bleed + floating text (目录页)
- **Title**: 研究框架
- **Content**:
  - 01 研究背景与意义
  - 02 系统需求分析
  - 03 核心架构设计
  - 04 差分隐私机制
  - 05 DeepFM模型设计
  - 06 系统实现与实验
  - 07 研究结论与展望
- **rhythm**: anchor

---

### Part 2: 研究背景

#### Slide 03 - 研究背景与意义

- **Layout**: Asymmetric split (3:7)
- **Title**: 医疗用药推荐面临安全与隐私双重挑战
- **Content**:
  - 问题1：药物不良反应致死率居高不下，传统推荐缺乏安全过滤
  - 问题2：患者健康数据在推荐过程中存在隐私泄露风险
  - 目标：构建安全过滤+隐私保护+个性化推荐的统一框架
- **rhythm**: breathing

---

### Part 3: 需求与架构

#### Slide 04 - 系统需求分析

- **Layout**: Asymmetric split (3:7)
- **Title**: 三层需求驱动系统设计
- **Content**:
  - 功能需求：患者信息管理、智能推荐、安全审查、隐私预算追踪
  - 非功能需求：推荐延迟<2s、DP预算可配置、多层安全保障
  - 安全需求：绝对禁忌硬过滤、相对禁忌软标记、DP噪声仅作用于评分层
- **rhythm**: dense

#### Slide 05 - 四层推荐架构设计

- **Layout**: Center-radiating / layered_architecture
- **Title**: 四层架构：安全优先，隐私保护，精准推荐
- **Visualization**: layered_architecture
- **Content**:
  - Layer 0: KnowledgeRouter — 语义匹配候选药物集
  - Layer 1: SafetyFilter — 确定性硬排除（禁忌症、过敏、妊娠X级）
  - Layer 2: RuleMarker — 软标记不排除（相对禁忌、C/D级妊娠警告）
  - Layer 3: DeepFM — 安全候选集上个性化评分 + DP噪声
  - 关键：DP噪声永远不影响Layer 1安全性
- **rhythm**: anchor

---

### Part 4: 核心技术

#### Slide 06 - 差分隐私机制

- **Layout**: Symmetric split (5:5)
- **Title**: DP噪声仅作用于评分层，临床安全不受影响
- **Content**:
  - 左侧 — DP原理：
    - Laplace: scale = sensitivity/ε
    - Gaussian: σ = sensitivity × √(2ln(1.25/δ))/ε
    - 预算追踪：强组合定理，ε总 = Σ√(2k·ln(1/δ'))·εi
  - 右侧 — 安全后处理：
    - 评分<0.15 → 置零（公开阈值，DP后处理定理）
    - 上限: min(1.0, raw+0.35) 防止噪声放大低分
    - 置信区间（95% CI）与异常标记
- **rhythm**: dense

#### Slide 07 - DeepFM模型设计

- **Layout**: Three-column cards
- **Title**: DeepFM: FM捕获交叉 + Deep捕获高阶 + 连续特征旁路
- **Visualization**: module_composition
- **Content**:
  - FM模块：Merged Embedding（单nn.Embedding + field_offsets，Opacus兼容）
  - Deep模块：MLP (64→32) + LayerNorm + ReLU + 差异化Dropout
  - 连续特征旁路：age_raw, bmi_raw, gfr_raw, liver_score_raw 直接连输出层
  - 训练：Focal Loss处理类别不平衡，14类别字段 + 4连续特征
- **rhythm**: dense

---

### Part 5: 系统实现与实验

#### Slide 08 - 系统实现

- **Layout**: Four-quadrant / matrix
- **Title**: 三层架构完整落地
- **Content**:
  - 前端：React 18 + TypeScript + Tailwind CSS（推荐页面、隐私可视化、审查面板）
  - 后端：Spring Boot 3.2 + MyBatis + MySQL（JWT认证、推荐代理、预算管理）
  - 模型服务：FastAPI + PyTorch DeepFM（三层推荐 + DP噪声 + 翻译管线）
  - 安全数据：禁忌症95.3%、交互81.5%、综合97.0%覆盖
- **rhythm**: dense

#### Slide 09 - 实验结果与分析

- **Layout**: Z-pattern / waterfall
- **Title**: DP保护不降质，模型区分度反而提升
- **Visualization**: grouped_bar_chart
- **Content**:
  - 核心发现1：AUC-PR基本持平（0.9668 → 0.9658 @ ε=1.0 → 0.9662 @ ε=0.5）
  - 核心发现2：Separation显著提升（0.7506 → 0.8505 → 0.8506）
  - 核心发现3：DP模型更好区分高分/低分药物
  - 安全验证：SafetyFilter层DP噪声零穿透，安全过滤100%保留
  - 训练数据：58525样本，1815药物候选
- **rhythm**: anchor

---

### Part 6: 结论

#### Slide 10 - 研究结论与展望

- **Layout**: Negative-space-driven
- **Title**: 安全与隐私可以兼得
- **Content**:
  - 结论1：四层推荐架构实现安全过滤与个性化推荐的统一
  - 结论2：差分隐私保护不降低推荐质量，反而提升模型区分度
  - 结论3：安全后处理机制确保DP噪声不影响临床安全性
  - 展望：联邦学习扩展多机构协作、更大规模药物数据集验证
- **rhythm**: breathing

#### Slide 11 - 致谢

- **Layout**: Single column centered
- **Title**: 谢谢各位老师
- **Content**: 感谢指导教师与答辩委员会
- **rhythm**: anchor

---

## X. Speaker Notes Requirements

- **Total duration**: 6 minutes
- **Notes style**: Formal / academic
- **Presentation purpose**: Persuade (convince committee of system's effectiveness)
- **File naming**: Match SVG names (e.g., `01_cover.md`)

---

## XI. Technical Constraints Reminder

### SVG Generation Must Follow:

1. viewBox: `0 0 1280 720`
2. Background uses `<rect>` elements
3. Text wrapping uses `<tspan>` (`<foreignObject>` FORBIDDEN)
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` FORBIDDEN
5. FORBIDDEN: `mask`, `<style>`, `class`, `foreignObject`
6. FORBIDDEN: `textPath`, `animate*`, `script`
7. Text characters: raw Unicode (em dash `—`, en dash `–`, `→`); HTML named entities FORBIDDEN
8. `marker-start` / `marker-end` conditionally allowed: `<marker>` in `<defs>`, `orient="auto"`
9. `clipPath` conditionally allowed only on `<image>` elements

### PPT Compatibility Rules:

- `<g opacity="...">` FORBIDDEN; set opacity on each child element
- Image transparency uses overlay mask layer
- Inline styles only; external CSS and `@font-face` FORBIDDEN
