# 智医荐药：差分隐私保护的个性化医疗用药推荐系统

项目围绕医疗推荐场景构建，目标是在给出个性化用药建议时，同时兼顾 `推荐效果`、`安全约束` 和 `隐私保护`。系统包含 React 前端、Spring Boot 后端以及 FastAPI + PyTorch 模型服务。

## 项目亮点

- 面向医疗场景设计三层推荐流程：安全过滤、规则标记、个性化打分
- 将差分隐私约束放在模型评分层，而不是覆盖安全规则层
- 形成前端、后端、模型服务分层协作的完整可运行系统
- 兼顾业务展示页面、推荐接口、模型训练与隐私参数配置

## 解决的问题

医疗用药推荐场景除了关注推荐效果，还需要同时处理以下问题：

- 药物禁忌症和严重相互作用不能被推荐逻辑覆盖
- 患者数据涉及隐私，模型输出不能直接暴露敏感信息
- 推荐结果既要可展示，也要便于后端系统接入和验证

因此系统将“安全规则”和“隐私保护”纳入推荐流程，而不是仅依赖单一排序模型。

## 系统方案

```text
前端 (React + TypeScript)
  └─ 患者信息录入、推荐结果展示、隐私参数配置、统计面板

后端 (Spring Boot)
  ├─ 用户认证与权限控制
  ├─ 患者、药物、推荐记录、隐私配置管理
  └─ 调用模型服务并返回结构化推荐结果

模型服务 (FastAPI + PyTorch)
  ├─ DeepFM 预测
  ├─ 差分隐私噪声注入
  └─ 安全规则与相互作用校验
```

## 三层推荐架构

```text
第一层：SafetyFilter
  绝对禁忌症、严重相互作用、妊娠高风险药物直接排除

第二层：RuleMarker
  对相对禁忌症、中度相互作用等情况打标记，提示人工关注

第三层：DeepFM + DP
  使用模型输出个性化评分，并在该层引入差分隐私机制
```

该设计的重点在于：`安全规则优先于模型分数`，差分隐私仅作用于评分层，不覆盖硬性安全约束。

## 指标与验证

当前 README 中保留的项目指标如下：

| 指标 | 数值 |
|------|------|
| 推荐精度（AUC-PR） | `0.9668` |
| 药物候选集 | `1815` |
| 安全数据覆盖率 | `97.0%` |
| DP 模型区分度 | `0.85`（基线 `0.75`） |

项目中也记录了 `ε = 1.0` 配置下的隐私实验结果，用来观察差分隐私加入后的性能变化。

## 项目实现

- 实现前端展示层、后端接口层和模型服务层的协作与联调
- 设计三层推荐架构，将硬性安全规则与模型评分分离
- 在模型服务中加入差分隐私相关配置、参数校验和异常处理
- 实现用户认证、推荐记录、患者与隐私配置等基础业务模块
- 完成前端测试、后端测试与模型服务运行链路的基础验证

## 技术栈

### 前端

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Recharts / ECharts
- Vitest

### 后端

- Spring Boot 3.2
- Spring Security
- MyBatis
- JWT
- MySQL
- Maven

### 模型服务

- FastAPI
- PyTorch
- Opacus
- NumPy / Pandas / scikit-learn

## 代码结构

```text
.
├─ src/                  # React 前端
├─ medical-backend/      # Spring Boot 后端
├─ medical-model/        # FastAPI + PyTorch 模型服务
├─ docs/                 # 设计与说明文档
└─ data/                 # 训练和推理相关数据
```

## 本地运行

### 1. 初始化数据库

```bash
mysql -u root -p < medical-backend/sql/schema.sql
mysql -u root -p < medical-backend/sql/init_data.sql
mysql -u root -p < medical-backend/sql/drug_data.sql
```

### 2. 启动后端

```bash
cd medical-backend
mvn spring-boot:run
```

### 3. 启动模型服务

```bash
cd medical-model
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 4. 启动前端

```bash
npm install
npm run dev
```

## 测试

前端测试：

```bash
npm run test:run
```

前端覆盖率：

```bash
npm run test:coverage
```

后端测试：

```bash
cd medical-backend
mvn test
```

## 说明

本项目用于学习和作品展示，不构成真实医疗建议。

## 许可证

[MIT](LICENSE)
