# DP-Medical-Recommendation

> Differential Privacy-Protected AI-Powered Personalized Medical Drug Recommendation System

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.2-brightgreen)](https://spring.io/projects/spring-boot)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An intelligent drug recommendation system that combines **DeepFM deep learning** with **differential privacy** to deliver personalized medication suggestions while providing mathematically provable patient data protection.

---

## Highlights

| Metric | Value |
|--------|-------|
| Recommendation accuracy (AUC-PR) | **0.9668** |
| Drug candidates | **1,815** |
| Training samples | **58,525** |
| Safety data coverage | **97.0%** |
| DP model separation score | **0.85** (vs 0.75 baseline) |
| Privacy budget (ε) | **≤ 1.0** |

**Key finding**: Differential privacy protection does **not** degrade model quality. DP-fine-tuned models (ε=1.0) achieve AUC-PR=0.9658 — only 0.001 below the no-DP baseline — while providing formally guaranteed privacy.

---

## Three-Layer Recommendation Architecture

This is the core innovation of the system. Each layer has a distinct responsibility, and **DP noise is applied only at the scoring layer**, ensuring clinical safety is never compromised:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: SafetyFilter — Hard Exclusion                 │
│  Absolute contraindications, allergy conflicts,         │
│  major drug interactions, pregnancy category X          │
│  → DP noise NEVER touches this layer                    │
└──────────────────────────┬──────────────────────────────┘
                           │ safe candidates only
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: RuleMarker — Soft Flagging                    │
│  Relative contraindications, moderate interactions,     │
│  pregnancy C/D warnings → adds review flags             │
│  → Does not alter candidate set                         │
└──────────────────────────┬──────────────────────────────┘
                           │ flagged safe candidates
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: DeepFM Ranking + DP Noise                     │
│  Personalized scoring of safe candidates                │
│  → DP noise (Laplace/Gaussian) applied ONLY here       │
│  → Post-processing: scores < 0.15 zeroed,              │
│    ceiling at min(1.0, raw + 0.35)                      │
└─────────────────────────────────────────────────────────┘
```

### Why This Design Matters

1. **Safety is non-negotiable**: Layer 1 deterministically excludes dangerous drug-patient combinations. No amount of noise can override a contraindication.
2. **Clinical awareness preserved**: Layer 2 flags drugs requiring extra review without removing them, supporting doctor decision-making.
3. **Privacy where it belongs**: Layer 3 is the only layer touched by DP noise, protecting individual patient data in the scoring function without affecting clinical safety.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (React 18)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │  Home    │ │Recommend.│ │ Privacy  │ │  Visualiz. │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                Backend (Spring Boot 3.2)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │Auth (JWT)│ │ Drug API │ │Patient   │ │ Privacy    │  │
│  │          │ │          │ │API       │ │ Budget API │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
└──────┬──────────────┬──────────────┬─────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌───────────┐  ┌─────────────┐  ┌───────────┐
│  MySQL    │  │Model Service│  │ChromaDB   │
│  8.0      │  │ (FastAPI)   │  │(RAG)      │
└───────────┘  │ DeepFM + DP │  └───────────┘
               └─────────────┘
```

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Framer Motion |
| **Backend** | Spring Boot 3.2, MyBatis, Spring Security, JWT |
| **Model Service** | Python, FastAPI, PyTorch, NumPy |
| **Database** | MySQL 8.0 |
| **RAG Module** | ChromaDB, Sentence Transformers |
| **Privacy** | Differential Privacy (Laplace / Gaussian mechanisms) |

---

## DeepFM Model

- **Architecture**: Factorization Machine (FM) + Deep Neural Network with LayerNorm
- **Input**: 14 categorical fields + 4 continuous features
- **Embedding**: `embed_dim=8`, merged field-aware embedding (Opacus-compatible)
- **Deep layers**: `[64, 32]` with per-layer differentiated dropout
- **Continuous bypass**: age, BMI, GFR, liver score fed directly into output
- **Training**: 58,525 samples, best AUC-PR = 0.9466 (production model)

### DP Fine-tuning Results

| Configuration | AUC-PR | Separation |
|--------------|--------|------------|
| No DP baseline | 0.9668 | 0.7506 |
| DP ε=1.0 | 0.9658 | 0.8505 |
| DP ε=0.5 | 0.9662 | 0.8506 |

---

## Quick Start

### Prerequisites

- **Node.js** >= 18.0
- **Java** >= 17
- **Python** >= 3.10
- **MySQL** >= 8.0
- **Maven** >= 3.8

### 1. Clone

```bash
git clone https://github.com/felixxx04/dp-medical-recommendation.git
cd dp-medical-recommendation
```

### 2. Database Setup

```bash
mysql -u root -p < medical-backend/sql/schema.sql
mysql -u root -p < medical-backend/sql/init_data.sql
mysql -u root -p < medical-backend/sql/drug_data.sql
```

### 3. Backend

```bash
cd medical-backend
cp .env.example .env   # Edit DB password and JWT secret
mvn spring-boot:run
```

Runs on `http://localhost:8080`

### 4. Model Service

```bash
cd medical-model
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Runs on `http://localhost:8001`

### 5. Frontend

```bash
npm install
npm run dev
```

Runs on `http://localhost:5173`

---

## Project Structure

```
dp-medical-recommendation/
├── src/                              # Frontend (React + TypeScript)
│   ├── components/                   # UI components
│   ├── pages/                        # Page components
│   ├── lib/                          # Utilities (privacy, recommendation)
│   └── App.tsx                       # Router config
│
├── medical-backend/                  # Backend (Spring Boot)
│   ├── src/main/java/com/medical/
│   │   ├── controller/               # REST controllers
│   │   ├── service/                  # Business logic
│   │   ├── entity/                   # JPA entities
│   │   ├── repository/               # Data access
│   │   ├── security/                 # JWT + Spring Security
│   │   └── config/                   # App configuration
│   ├── sql/                          # Database scripts
│   └── src/main/resources/
│
├── medical-model/                    # Model service (FastAPI + PyTorch)
│   ├── app/
│   │   ├── models/                   # DeepFM architecture
│   │   ├── services/                 # Inference + 3-layer pipeline
│   │   ├── rag/                      # RAG module (ChromaDB)
│   │   └── main.py                   # FastAPI entry
│   ├── data/                         # Pipeline data
│   └── saved_models/                 # Trained model weights
│
└── docs/                             # Documentation
```

---

## API Overview

### Backend (Port 8080)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | JWT authentication |
| `/api/auth/me` | GET | Current user info |
| `/api/drugs` | GET | Drug catalog |
| `/api/patients` | GET/POST | Patient management |
| `/api/recommendation/predict` | POST | Drug recommendation |
| `/api/privacy/config` | GET/PUT | DP parameter config |
| `/api/privacy/budget` | GET | Budget consumption status |

### Model Service (Port 8001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/model/status` | GET | Model status |
| `/model/predict` | POST | Three-layer recommendation |
| `/model/train` | POST | Model training |
| `/model/load-drugs` | POST | Load drug catalog |
| `/model/privacy/budget` | GET | Privacy budget tracker |

---

## Differential Privacy Implementation

| Parameter | Description | Default |
|-----------|-------------|---------|
| ε (epsilon) | Privacy budget — lower = stronger protection | 0.1 |
| δ (delta) | Upper bound on privacy breach probability | 1e-5 |
| Sensitivity | Maximum change in query output | 1.0 |
| Mechanism | Laplace / Gaussian noise distribution | Laplace |

**Dual budget tracking**: MySQL-backed persistent tracking (per-user) + in-memory strong composition theorem (per-session).

**Post-processing guarantees**: Clinical safety threshold (0.15) and score ceiling (1.0) are public parameters — applying them after DP noise does not violate privacy guarantees (post-processing theorem).

---

## License

[MIT](LICENSE)
