# 智医荐药 — 差分隐私保护的智能用药推荐系统

> 基于 DeepFM 深度学习与差分隐私保护的个性化医疗用药推荐系统，在提供精准用药建议的同时提供可证明的患者隐私保护。

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.2-brightgreen)](https://spring.io/projects/spring-boot)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 核心亮点

| 指标 | 数值 |
|------|------|
| 推荐精度 (AUC-PR) | **0.9668** |
| 药物候选集 | **1,815 种** |
| 训练样本 | **58,525 条** |
| 安全数据覆盖率 | **97.0%** |
| DP 模型区分度 | **0.85**（无 DP 基线 0.75） |
| 隐私预算 (ε) | **≤ 1.0** |

**核心发现**：差分隐私保护**不会降低模型质量**。DP 微调模型 (ε=1.0) 的 AUC-PR 为 0.9658，仅比无 DP 基线低 0.001，同时提供了严格的数学隐私保证。

---

## 三层推荐架构

本系统的核心创新。每一层职责明确，**DP 噪声仅在打分层施加**，确保临床安全不受影响：

```
┌─────────────────────────────────────────────────────────┐
│  第一层：SafetyFilter — 硬性排除                         │
│  绝对禁忌症、过敏冲突、严重药物相互作用、妊娠 X 类          │
│  → DP 噪声永远不会触及此层                                │
└──────────────────────────┬──────────────────────────────┘
                           │ 仅安全候选
                           ▼
┌─────────────────────────────────────────────────────────┐
│  第二层：RuleMarker — 软性标记                           │
│  相对禁忌症、中度相互作用、妊娠 C/D 级警告                │
│  → 添加审核标记，不改变候选集                             │
└──────────────────────────┬──────────────────────────────┘
                           │ 已标记的安全候选
                           ▼
┌─────────────────────────────────────────────────────────┐
│  第三层：DeepFM 排序 + DP 噪声                          │
│  对安全候选进行个性化评分                                 │
│  → DP 噪声 (Laplace/Gaussian) 仅在此层施加              │
│  → 后处理：分数 < 0.15 置零，上限 min(1.0, 原始+0.35)   │
└─────────────────────────────────────────────────────────┘
```

### 设计意义

1. **安全不可妥协**：第一层确定性排除危险用药组合，任何噪声都无法覆盖禁忌症判断
2. **临床感知保留**：第二层标记需额外审核的药物但不移除，支持医生决策
3. **隐私施加于正确位置**：第三层是唯一受 DP 噪声影响的层，保护评分函数中的个体患者数据，且不影响临床安全

---

## 系统架构

```
┌──────────────────────────────────────────────────────────┐
│                     前端 (React 18)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │   首页   │ │ 药物推荐 │ │ 隐私配置 │ │  可视化    │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                后端 (Spring Boot 3.2)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │认证(JWT) │ │ 药物API  │ │ 患者API  │ │ 隐私预算   │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└──────┬──────────────┬──────────────┬─────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌───────────┐  ┌─────────────┐  ┌───────────┐
│  MySQL    │  │  模型服务   │  │ ChromaDB  │
│  8.0      │  │  (FastAPI)  │  │  (RAG)    │
└───────────┘  │ DeepFM + DP │  └───────────┘
               └─────────────┘
```

---

## 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Framer Motion |
| **后端** | Spring Boot 3.2, MyBatis, Spring Security, JWT |
| **模型服务** | Python, FastAPI, PyTorch, NumPy |
| **数据库** | MySQL 8.0 |
| **RAG 模块** | ChromaDB, Sentence Transformers |
| **隐私保护** | 差分隐私 (Laplace / Gaussian 机制) |

---

## DeepFM 模型

- **架构**：因子分解机 (FM) + 带有 LayerNorm 的深度神经网络
- **输入**：14 个类别字段 + 4 个连续特征
- **嵌入**：`embed_dim=8`，合并字段感知嵌入（兼容 Opacus）
- **深层网络**：`[64, 32]`，逐层差异化 Dropout
- **连续特征旁路**：年龄、BMI、GFR、肝功能评分直接输入输出层
- **训练**：58,525 条样本，最优 AUC-PR = 0.9466（生产模型）

### DP 微调实验结果

| 配置 | AUC-PR | 区分度 (Separation) |
|------|--------|---------------------|
| 无 DP 基线 | 0.9668 | 0.7506 |
| DP ε=1.0 | 0.9658 | 0.8505 |
| DP ε=0.5 | 0.9662 | 0.8506 |

---

## 快速开始

### 环境要求

- **Node.js** >= 18.0
- **Java** >= 17
- **Python** >= 3.10
- **MySQL** >= 8.0
- **Maven** >= 3.8

### 1. 克隆项目

```bash
git clone https://github.com/felixxx04/dp-medical-recommendation.git
cd dp-medical-recommendation
```

### 2. 数据库配置

```bash
mysql -u root -p < medical-backend/sql/schema.sql
mysql -u root -p < medical-backend/sql/init_data.sql
mysql -u root -p < medical-backend/sql/drug_data.sql
```

### 3. 后端启动

```bash
cd medical-backend
cp .env.example .env   # 编辑数据库密码和 JWT 密钥
mvn spring-boot:run
```

运行于 `http://localhost:8080`

### 4. 模型服务启动

```bash
cd medical-model
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

运行于 `http://localhost:8001`

### 5. 前端启动

```bash
npm install
npm run dev
```

运行于 `http://localhost:5173`

---

## 项目结构

```
dp-medical-recommendation/
├── src/                              # 前端源码 (React + TypeScript)
│   ├── components/                   # UI 组件
│   ├── pages/                        # 页面组件
│   ├── lib/                          # 工具库 (隐私、推荐)
│   └── App.tsx                       # 路由配置
│
├── medical-backend/                  # 后端 (Spring Boot)
│   ├── src/main/java/com/medical/
│   │   ├── controller/               # REST 控制器
│   │   ├── service/                  # 业务逻辑
│   │   ├── entity/                   # JPA 实体
│   │   ├── repository/               # 数据访问层
│   │   ├── security/                 # JWT + Spring Security
│   │   └── config/                   # 应用配置
│   ├── sql/                          # 数据库脚本
│   └── src/main/resources/
│
├── medical-model/                    # 模型服务 (FastAPI + PyTorch)
│   ├── app/
│   │   ├── models/                   # DeepFM 架构
│   │   ├── services/                 # 推理 + 三层管道
│   │   ├── rag/                      # RAG 模块 (ChromaDB)
│   │   └── main.py                   # FastAPI 入口
│   ├── data/                         # 管线数据
│   └── saved_models/                 # 训练好的模型权重
│
└── docs/                             # 文档
```

---

## API 概览

### 后端 API (端口 8080)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login` | POST | JWT 认证登录 |
| `/api/auth/me` | GET | 获取当前用户 |
| `/api/drugs` | GET | 药物目录 |
| `/api/patients` | GET/POST | 患者管理 |
| `/api/recommendation/predict` | POST | 药物推荐 |
| `/api/privacy/config` | GET/PUT | DP 参数配置 |
| `/api/privacy/budget` | GET | 隐私预算消耗状态 |

### 模型服务 API (端口 8001)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/model/status` | GET | 模型状态 |
| `/model/predict` | POST | 三层推荐推理 |
| `/model/train` | POST | 模型训练 |
| `/model/load-drugs` | POST | 加载药物目录 |
| `/model/privacy/budget` | GET | 隐私预算追踪 |

---

## 差分隐私实现

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ε (epsilon) | 隐私预算，越小保护越强 | 0.1 |
| δ (delta) | 隐私泄露概率上限 | 1e-5 |
| 敏感度 | 查询函数最大变化范围 | 1.0 |
| 噪声机制 | Laplace / Gaussian 分布 | Laplace |

**双重预算追踪**：MySQL 持久化追踪（按用户）+ 内存强组合定理追踪（按会话）。

**后处理保证**：临床安全阈值 (0.15) 和分数上限 (1.0) 为公开参数，在 DP 噪声之后施加不违反隐私保证（后处理定理）。

---

## 许可证

[MIT](LICENSE)
