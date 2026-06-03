# 智医荐药 — 差分隐私保护的智能用药推荐系统

> 全栈 AI 编程构建 (Claude Code) · DeepFM + 三层安全架构

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.2-brightgreen)](https://spring.io/projects/spring-boot)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 核心亮点

| 指标 | 数值 |
|------|------|
| 推荐精度 (AUC-PR) | **0.9668** |
| 药物候选集 | **1,815 种** |
| 安全数据覆盖率 | **97.0%** |
| DP 模型区分度 | **0.85**（基线 0.75） |

差分隐私 (ε=1.0) 微调后 AUC-PR 仅降 0.001，隐私保护不损失模型质量。

## 三层推荐架构

```
第一层：SafetyFilter（硬性排除）
  绝对禁忌症 · 过敏冲突 · 严重相互作用 · 妊娠 X 类
  → DP 噪声永远不会触及此层
          │ 仅安全候选
          ▼
第二层：RuleMarker（软性标记）
  相对禁忌症 · 中度相互作用 · 妊娠 C/D 警告
  → 添加审核标记，不改变候选集
          │ 已标记的安全候选
          ▼
第三层：DeepFM + DP 噪声
  个性化评分 · Laplace/Gaussian 噪声仅在此层施加
  → 后处理保证：安全阈值 0.15 和上限 1.0 为公开参数，不违反后处理定理
```

安全不可妥协——第一层确定性排除危险用药，噪声无法覆盖禁忌症；隐私施加于正确位置——仅在打分层保护个体数据。

## 开发方式

整个系统通过 AI 编程完成：React 前端、Spring Boot 后端、FastAPI + PyTorch 模型服务、差分隐私算法、三层安全管道——全部由开发者与 AI 协作从零构建，覆盖需求分析、架构设计、编码实现、调试优化的完整流程。

## 技术栈

**前端** React 18 · TypeScript · Vite · Tailwind CSS · Recharts
**后端** Spring Boot 3.2 · MyBatis · Spring Security · JWT · MySQL 8.0
**模型** FastAPI · PyTorch (DeepFM) · ChromaDB (RAG)
**隐私** 差分隐私 (Laplace / Gaussian) · 双重预算追踪

## 快速开始

```bash
# 数据库
mysql -u root -p < medical-backend/sql/schema.sql
mysql -u root -p < medical-backend/sql/init_data.sql
mysql -u root -p < medical-backend/sql/drug_data.sql

# 后端 (localhost:8080)
cd medical-backend && cp .env.example .env && mvn spring-boot:run

# 模型服务 (localhost:8001)
cd medical-model && pip install -r requirements.txt && uvicorn app.main:app --port 8001

# 前端 (localhost:5173)
npm install && npm run dev
```

## 许可证

[MIT](LICENSE)
