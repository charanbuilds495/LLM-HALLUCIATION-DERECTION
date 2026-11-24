# TruthLens AI: Hallucination Detection in LLM-Generated Answers Using Semantic Entailment Scoring

---

### 🌐 [👉 CLICK HERE TO OPEN THE LIVE WEB APPLICATION 👈](https://charanbuilds495.github.io/LLM-Halluciation-Detection/)
**Live Website URL:** [https://charanbuilds495.github.io/LLM-Halluciation-Detection/](https://charanbuilds495.github.io/LLM-Halluciation-Detection/)

---

[![Live Web App](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-purple?style=for-the-badge&logo=github)](https://charanbuilds495.github.io/LLM-Halluciation-Detection/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61dafb.svg)](https://reactjs.org/)
[![NLI Model](https://img.shields.io/badge/NLI%20Model-DeBERTa--v3--base-purple.svg)](https://huggingface.co/cross-encoder/nli-deberta-v3-base)
[![License](https://img.shields.io/badge/License-Academic%20Research-green.svg)]()

> **Academic Engineering Project** • Category: **Generative AI & Natural Language Processing (NLP)**  
> **Tagline:** *"Detect AI Hallucinations. Verify What Matters."*

---

## 1. Project Overview & Abstract

Large Language Models (LLMs) such as GPT-4, LLaMA, and Gemini frequently generate syntactically fluent answers that are factually unfaithful to source context—a phenomenon known as **hallucination**. 

**TruthLens AI** is a full-stack, research-oriented web platform designed to detect, classify, and quantify hallucinations in LLM-generated responses using **Natural Language Inference (NLI)** and **Semantic Entailment Scoring**. Unlike naive approaches that rely on symmetric cosine similarity (which fails to detect negations and direct contradictions), TruthLens extracts individual atomic claims, retrieves candidate evidence sentences, and evaluates directional premise-hypothesis entailment using the deep cross-encoder `cross-encoder/nli-deberta-v3-base`.

### Key Capabilities
- **Claim-Level Decomposition**: Breaks long AI answers into atomic factual claims while protecting abbreviations, numbers, and bullet points.
- **Topical Evidence Grounding**: Retrieves candidate premise sentences using TF-IDF cosine similarity to ground the evaluation without semantic bias.
- **Directional NLI Cross-Encoder**: Evaluates (Premise, Hypothesis) pairs with DeBERTa-v3 to produce exact probability distributions across **Entailment**, **Contradiction**, and **Neutrality**.
- **Three Factual Classifications**:
  - 🟢 **Supported**: High entailment confidence ($\ge 60\%$).
  - 🔴 **Contradicted**: High contradiction confidence ($\ge 60\%$).
  - 🟠 **Insufficient Evidence**: Neither entailed nor contradicted; the reference does not substantiate the claim.
- **Transparent Hallucination Risk Scoring**: Calculates overall answer risk via a documented mathematical formula.
- **Explainable AI (XAI)**: Generates deterministic, evidence-cited explanations for why each claim was classified into its respective category.
- **Audit History & Telemetry**: Saves all evaluations into SQLite for retrospective analysis and trend visualization.
- **100% Free & Open-Source**: Runs locally on CPU PyTorch without paid API keys.

---

## 2. Mathematical & Theoretical Framework

### 2.1 The Entailment Probability Simplex
For a premise evidence sentence $P$ and a claim hypothesis $H$, the cross-encoder transformer computes raw logits $z = [z_c, z_e, z_n]$. These are normalized via the softmax function:

$$P(y = k \mid P, H) = \frac{\exp(z_k)}{\exp(z_c) + \exp(z_e) + \exp(z_n)}, \quad k \in \{\text{Contradiction}, \text{Entailment}, \text{Neutral}\}$$

Such that:
$$P(\text{Entailment}) + P(\text{Contradiction}) + P(\text{Neutral}) = 1.0$$

### 2.2 Hallucination Risk Score Formula
Given total claims $N$, contradicted claims $N_{con}$, unsupported claims $N_{unsup}$, and penalty weights $W_c = 1.0$ (severe factual error) and $W_u = 0.5$ (epistemic uncertainty):

$$\text{Hallucination Risk Score} = \min\left(100.0, \frac{1.0 \times N_{con} + 0.5 \times N_{unsup}}{N} \times 100\right)$$

### 2.3 Evidence Coverage Metric
$$\text{Evidence Coverage} = \frac{N_{supported}}{N} \times 100\%$$

---

## 3. Technology Stack

### Backend
- **Python 3.12**
- **FastAPI**: Modern, high-performance web framework for APIs.
- **Uvicorn**: Lightning-fast ASGI web server.
- **PyTorch 2.15 (CPU)**: CPU-optimized deep learning inference.
- **Hugging Face Transformers**: Cross-encoder sequence classification.
- **Model**: `cross-encoder/nli-deberta-v3-base` (with fallback to `cross-encoder/nli-distilroberta-base`).
- **Scikit-Learn**: TF-IDF evidence vectorization and cosine similarity.
- **SQLAlchemy 2.0 & SQLite**: Local relational database persistence.
- **Pytest 9.2 & HTTPX**: Comprehensive automated test runner.

### Frontend
- **React 18** + **Vite 5** + **TypeScript 5**
- **Tailwind CSS 3**: Custom dark navy SaaS theme (`#070b19`, `#0a0f24`, `#8b5cf6`, `#06b6d4`).
- **Lucide React**: Clean SVG icon system.
- **Recharts**: Responsive Donut charts, score profiles, and history trend lines.

---

## 4. Project Directory Structure

```
TruthLensAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py        # REST API route handlers
│   │   ├── database/
│   │   │   ├── models.py           # SQLAlchemy AnalysisRecord model
│   │   │   ├── session.py          # SQLite engine and session factory
│   │   │   └── truthlens.db        # SQLite database
│   │   ├── schemas/
│   │   │   └── analysis.py         # Pydantic schemas for requests/responses
│   │   ├── services/
│   │   │   ├── claim_classifier.py # Main orchestration & classification logic
│   │   │   ├── evidence_retriever.py# TF-IDF candidate evidence matching
│   │   │   ├── nli_engine.py       # DeBERTa-v3 cross-encoder PyTorch engine
│   │   │   └── risk_calculator.py  # Mathematical risk scoring metrics
│   │   ├── utils/
│   │   │   └── text_processing.py  # Robust sentence splitting & claim extraction
│   │   └── main.py                 # FastAPI application instance & lifespan
│   ├── tests/
│   │   ├── test_nli_engine.py      # Unit tests for text splitting and NLI inference
│   │   ├── test_api.py             # API route tests (health, info, analyze, history)
│   │   └── test_e2e.py             # Comprehensive End-to-End integration tests
│   ├── .venv/                      # Python virtual environment
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx          # Navigation, brand, and live engine status pill
│   │   │   └── Footer.tsx          # Research disclaimers and academic info
│   │   ├── pages/
│   │   │   ├── LandingPage.tsx     # Hero section, how-it-works, feature cards
│   │   │   ├── DashboardPage.tsx   # Interactive analysis workbench & results view
│   │   │   ├── HistoryPage.tsx     # Saved reports list & trend chart
│   │   │   └── AboutPage.tsx       # Research thesis, architecture, viva defense
│   │   ├── services/
│   │   │   └── api.ts              # Fetch client connecting to FastAPI
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript interfaces
│   │   ├── App.tsx                 # Root application component
│   │   ├── main.tsx                # React DOM entrypoint
│   │   └── index.css               # Tailwind CSS directives
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── run_backend.bat                 # One-click Windows launcher for backend
├── run_frontend.bat                # One-click Windows launcher for frontend
├── run_tests.bat                   # One-click Windows test runner
├── .gitignore
└── README.md
```

---

## 5. Execution Instructions (Step-by-Step for Windows)

### Prerequisites Already Verified:
- **Python 3.12**
- **Node.js v20+ / v26+** and **npm**

### Quick Launch (Double-Click Batch Files)
1. Double-click `run_backend.bat` (starts FastAPI on `http://127.0.0.1:8000`).
2. Double-click `run_frontend.bat` (starts React Vite dev server on `http://localhost:5173`).
3. Open `http://localhost:5173` in your web browser.

---

### Manual Terminal Commands (VS Code or Windows Command Prompt)

#### Terminal 1: Backend Server
```cmd
cd TruthLensAI\backend
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/api/health`

#### Terminal 2: Frontend Client
```cmd
cd TruthLensAI\frontend
npm.cmd run dev
```
- Open `http://localhost:5173` in your browser.

---

## 6. Running the Test Suite

TruthLens AI includes 13 automated tests across unit, API, and E2E suites:

```cmd
cd TruthLensAI
backend\.venv\Scripts\pytest.exe backend\tests -v
```

### Verified Test Results:
```
backend/tests/test_api.py::test_api_root PASSED                          [  7%]
backend/tests/test_api.py::test_api_health PASSED                        [ 15%]
backend/tests/test_api.py::test_api_info PASSED                          [ 23%]
backend/tests/test_api.py::test_api_analyze_validation PASSED            [ 30%]
backend/tests/test_api.py::test_api_analyze_and_history_flow PASSED      [ 38%]
backend/tests/test_e2e.py::test_e2e_benchmark_water PASSED               [ 46%]
backend/tests/test_e2e.py::test_e2e_all_supported_scenario PASSED        [ 53%]
backend/tests/test_e2e.py::test_e2e_empty_and_invalid_inputs PASSED      [ 61%]
backend/tests/test_e2e.py::test_e2e_history_lifecycle PASSED             [ 69%]
backend/tests/test_nli_engine.py::test_split_into_sentences PASSED       [ 76%]
backend/tests/test_nli_engine.py::test_extract_claims_with_bullet_points PASSED [ 84%]
backend/tests/test_nli_engine.py::test_risk_calculator PASSED            [ 92%]
backend/tests/test_nli_engine.py::test_nli_sample_analysis_benchmark PASSED [100%]

============================= 13 passed in 58.27s =============================
```

---

## 7. Sample Benchmark Demonstration

Clicking the **"Load Benchmark Sample"** button on the Dashboard loads the following verified evaluation:

### Reference Context:
```text
Water boils at approximately 100 degrees Celsius at standard atmospheric pressure. Water freezes at 0 degrees Celsius under standard atmospheric pressure.
```

### AI-Generated Answer:
```text
Water boils at 100 degrees Celsius at standard atmospheric pressure. Water freezes at 10 degrees Celsius under standard atmospheric pressure. Water is composed of hydrogen and oxygen.
```

### DeBERTa-v3 Analysis Output:
| Claim # | Claim Text | NLI Classification | Entailment | Contradiction | Neutral | Matched Evidence |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | *"Water boils at 100 degrees Celsius at standard atmospheric pressure."* | 🟢 **Supported** | **98.1%** | 0.1% | 1.8% | *"Water boils at approximately 100 degrees Celsius..."* |
| **2** | *"Water freezes at 10 degrees Celsius under standard atmospheric pressure."* | 🔴 **Contradicted** | 0.0% | **99.9%** | 0.1% | *"Water freezes at 0 degrees Celsius..."* |
| **3** | *"Water is composed of hydrogen and oxygen."* | 🟠 **Insufficient Evidence** | 0.0% | 0.0% | **99.9%** | Not mentioned in context |

- **Summary Metrics**:
  - Total Claims: `3`
  - Supported: `1` (33.3% Evidence Coverage)
  - Contradicted: `1` (33.3% Contradiction Rate)
  - Unsupported: `1` (33.3% Unverified Rate)
  - **Hallucination Risk Score**: `50.0%` (Moderate/High Risk)

---

## 8. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check, device status, and model loaded state. |
| `GET` | `/api/info` | Framework versions, primary model identifier, and label mappings. |
| `POST` | `/api/analyze` | Performs claim extraction, evidence retrieval, NLI inference, and saves to SQLite. |
| `GET` | `/api/history` | Fetches historical analysis runs with pagination. |
| `GET` | `/api/history/{id}` | Retrieves full claim-by-claim analysis report for a past run. |
| `DELETE` | `/api/history/{id}` | Deletes a specific analysis record from SQLite. |
| `DELETE` | `/api/history` | Clears all historical records. |

---

## 9. Viva / Defense Preparation Guide

When presenting this project for an academic defense or technical review, be prepared for these core questions:

1. **Why is NLI superior to sentence embedding cosine similarity?**  
   *Answer:* Cosine similarity measures word/topic co-occurrence without directional logic. A claim like *"The patient does NOT have diabetes"* has ~95% cosine similarity with *"The patient has diabetes"*, leading to false positives. NLI evaluates asymmetric entailment ($P \implies H$) and correctly classifies contradictions.

2. **How are class indices handled in your model loader?**  
   *Answer:* The code does not hardcode indices (`0, 1, 2`). Instead, it dynamically queries `model.config.id2label` to map string representations containing `"entail"`, `"contra"`, and `"neutral"` to their respective tensor output positions.

3. **How does the system prevent non-mentioned claims from falsely passing as true?**  
   *Answer:* By computing both similarity relevance and NLI neutrality. If a claim is absent from the reference text, its neutral probability $P(\text{Neutral})$ dominates, classifying it as **Insufficient Evidence** and penalizing the Hallucination Risk Score.

4. **Does TruthLens establish absolute real-world truth?**  
   *Answer:* No. TruthLens verifies *relative faithfulness* to the provided reference context. This distinction is essential in academic NLP and avoids false claims of universal factuality.

---

## 10. License & Academic Disclaimer
Developed for B.Tech academic engineering evaluation. Built with open-source tools.
TruthLens AI assesses whether claims are grounded in provided reference materials; it does not replace domain-expert human oversight.
