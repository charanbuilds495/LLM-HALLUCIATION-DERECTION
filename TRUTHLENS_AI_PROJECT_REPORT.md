# TruthLens AI: Hallucination Detection in LLM-Generated Answers Using Semantic Entailment Scoring

**Individual Project Report**

Department of Computer Science and Engineering (Artificial Intelligence & Machine Learning)

**2026–2027**

Submitted in partial fulfilment for the completion of the course **[Course Code – Course Name]**

**BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE & ENGINEERING**

Submitted by: **Charan** (**[Registration / USN]**)

Under the guidance of: **[Guide Name]**, **[Designation]**, Department of Computer Science & Engineering

---

## Certificate

This is to certify that the project work for the course **[Course Code – Course Name]**, titled **“TruthLens AI: Hallucination Detection in LLM-Generated Answers Using Semantic Entailment Scoring”**, is carried out by **Charan** (**[Registration / USN]**), a bonafide student of Bachelor of Technology at the Department of Computer Science & Engineering, in partial fulfilment for the award of the degree of Bachelor of Technology in Computer Science and Engineering, during the year **2026–2027**.

Project Guide: **[Name]** \_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_

Program Head, Computer Science & Engineering: **[Name]** \_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_

---

## Declaration

I, **Charan** (**[Registration / USN]**), student of B.Tech in Computer Science & Engineering, hereby declare that the project work titled **“TruthLens AI: Hallucination Detection in LLM-Generated Answers Using Semantic Entailment Scoring”** has been carried out by me and submitted in partial fulfilment for the completion of the course **[Course Code – Course Name]** in Bachelor of Technology in Computer Science & Engineering during the academic year **2026–2027**.

Signature: \_\_\_\_\_\_\_\_\_\_\_\_\_\_ **Charan** (**[Registration / USN]**) &nbsp;&nbsp; Place: **[City]** &nbsp;&nbsp; Date: **[DD-MM-2026]**

---

## Contents

Nomenclature Used · Abstract · Chapter 1 Introduction · Chapter 2 Literature Survey · Chapter 3 System Design · Chapter 4 Implementation · Chapter 5 Tools and Technologies Required · Chapter 6 Software Requirements Specification · Chapter 7 Results and Discussion · Chapter 8 Conclusion and Future Scope · References

---

## Nomenclature Used

| Symbol / Term | Description |
| :--- | :--- |
| **LLM** | Large Language Model – autoregressive neural network generating fluent natural language text |
| **NLI** | Natural Language Inference – directional classification of whether a premise entails, contradicts, or is neutral toward a hypothesis |
| **Cross-Encoder** | Transformer architecture that processes `(Premise, Hypothesis)` jointly using full cross-token self-attention |
| **DeBERTa-v3** | Decoding-enhanced BERT with Disentangled Attention and ELECTRA-style pretraining (`cross-encoder/nli-deberta-v3-base`) |
| **TF-IDF** | Term Frequency–Inverse Document Frequency weighting used with cosine similarity to retrieve top candidate evidence sentences |
| **XAI** | Explainable Artificial Intelligence – surfacing matched evidence, probability scores, and human-readable decision rationales |
| **Softmax** | Normalization function converting raw classifier logits `z` into a three-class probability distribution summing to `1.0` |
| **HR** | Hallucination Risk Score – weighted aggregate penalty (`0–100%`) combining contradicted (`1.0`) and unsupported (`0.5`) claims |
| **EC** | Evidence Coverage – percentage of extracted claims classified as `supported` by supplied reference context |
| **REST API** | Representational State Transfer web interface exchanging validated JSON payloads over HTTP endpoints |
| **FastAPI** | High-performance asynchronous Python web framework serving the inference and history APIs |
| **SQLite** | Embedded relational database (`truthlens.db`) storing persistent audit history via SQLAlchemy ORM |
| **ONNX / WASM** | Open Neural Network Exchange runtime compiled to WebAssembly for standalone in-browser NLI inference |

---

## Abstract

Large Language Models (LLMs) routinely produce fluent, authoritative responses that nonetheless contain factual fabrications or direct contradictions relative to source documents—a failure mode known as **hallucination**. Conventional evaluation heuristics such as n-gram overlap and symmetric embedding cosine similarity treat opposing statements (for example, *“Water freezes at 0°C”* versus *“Water freezes at 10°C”*) as nearly identical because of shared vocabulary, failing to verify directional factual consistency. **TruthLens AI** (*“See Beyond AI. Verify Every Claim.”*) addresses these gaps within a single explainable verification platform.

The system decomposes an AI-generated answer into atomic factual claims while protecting decimal numbers and abbreviations, retrieves the most topically relevant reference sentences via unigram/bigram TF-IDF cosine similarity (`top_k = 5`), and scores each `(Premise, Claim)` pair using a cross-encoder NLI transformer (`cross-encoder/nli-deberta-v3-base`). Every claim is categorized as **Supported**, **Contradicted**, or **Insufficient Evidence**, accompanied by its three-way probability profile (`Entailment`, `Contradiction`, `Neutrality`), verbatim matched evidence, plain-language rationale, and an aggregated **Hallucination Risk Score**.

The platform is delivered as a **FastAPI** backend with **SQLite** audit persistence and a responsive **React 18 + TypeScript + Tailwind CSS** SaaS web application supporting Dark and Light themes, interactive Recharts visualizations, an **Explainable AI Flow** inspector, and searchable audit history. For static hosting such as GitHub Pages, a standalone **WebAssembly NLI engine** (`Xenova/nli-deberta-v3-xsmall` via Transformers.js) executes client-side verification directly in the browser when no backend server is attached. TruthLens AI is an academic verification prototype that evaluates relative consistency against supplied reference context rather than universal real-world truth.

---

# Chapter 1: Introduction

Autoregressive language models generate responses by predicting statistically likely next tokens rather than checking factual provenance. For enterprise summaries, educational assistance, and Retrieval-Augmented Generation (RAG) pipelines, teams must know both *which* individual sentences inside an answer are trustworthy and *why* a detector flagged a claim. TruthLens AI is engineered around these two requirements.

## 1.1 Atomic Claim Extraction

AI-generated responses frequently bundle multiple independent assertions inside multi-sentence paragraphs or bulleted lists. TruthLens AI normalizes line breaks and list markers (`-`, `*`, `•`, `1.`), shields decimal values (`\d+\.\d+`) and 18 common abbreviations (`e.g.`, `i.e.`, `dr.`, `approx.`), and splits text along sentence boundaries into clean atomic hypotheses `C_1, C_2, ..., C_n`.

## 1.2 Directional Semantic Entailment Scoring

Instead of relying on symmetric embedding distance, TruthLens AI grounds each claim against candidate reference sentences retrieved via TF-IDF cosine similarity and evaluates directional implication (`Premise => Hypothesis`) with `cross-encoder/nli-deberta-v3-base`. Cross-attention across concatenated token sequences enables sensitivity to negation, numerical changes, and logical inversion, producing calibrated probabilities for **Entailment**, **Contradiction**, and **Neutrality**.

## 1.3 Explainable AI & Risk Quantification

Each claim receives an explicit classification (**Supported**, **Contradicted**, or **Insufficient Evidence**) with icon + label badges, the exact reference sentence used as evidence, lexical similarity percentage, three probability bars, and an automated plain-English explanation. Aggregated metrics compute **Hallucination Risk (`HR`)**, **Evidence Coverage (`EC`)**, **Contradiction Rate**, and **Unsupported Rate** transparently.

## 1.4 SaaS Web Platform & Standalone Browser Engine

The React 18 interface provides a landing showcase with an interactive Hero NLI preview alongside a multi-view SaaS workspace: **Overview**, **New Analysis** (AI Hallucination Analyzer + Results Dashboard + Explainable AI Flow), **Analysis History**, **About Project**, and **Settings**. When a FastAPI backend is unavailable (such as static GitHub Pages deployment), the frontend falls back to an in-browser WebAssembly DeBERTa-v3 NLI engine (`Xenova/nli-deberta-v3-xsmall`) with `localStorage` persistence.

## 1.5 Background and Motivation

Undetected hallucinations undermine reliability whenever LLMs summarize policies, medical notes, legal clauses, or technical documentation. Existing academic scripts often suffer from three weaknesses: (1) symmetric cosine similarity mistakes contradictions for high agreement, (2) binary `True/False` classifiers misclassify unmentioned facts as contradictions or truths, and (3) commercial LLM-as-a-judge evaluators require paid API keys and expose private context externally. TruthLens AI provides a local, zero-API-cost, three-way NLI alternative.

## 1.6 Objectives

1. To decompose AI-generated answers into clean, atomic claims while preserving numbers, decimals, and abbreviations.
2. To retrieve top candidate premise sentences from reference context using TF-IDF unigram/bigram cosine similarity.
3. To classify each claim as `supported`, `contradicted`, or `insufficient_evidence` using `cross-encoder/nli-deberta-v3-base` with dynamic `id2label` index mapping.
4. To compute transparent summary metrics including Hallucination Risk Score (`HR`), Evidence Coverage (`EC`), Contradiction Rate, and processing latency.
5. To expose full Explainable AI telemetry showing original claim, retrieved evidence, NLI probability simplex, and plain-language rationale.
6. To build an asynchronous FastAPI REST backend with Pydantic validation and SQLite audit persistence via SQLAlchemy.
7. To deliver a responsive Dark/Light SaaS React workspace with interactive Recharts visualizations, history search/filtering, and a standalone WebAssembly browser fallback.
8. To validate the backend pipeline, API contracts, and frontend compilation through automated Pytest and TypeScript checks.

## 1.7 Benefits

- **Directional Accuracy:** Distinguishes true entailment from negation and numeric distortion via cross-encoder NLI.
- **Epistemic Honesty:** Separates unsubstantiated claims (`Insufficient Evidence`, weight `0.5`) from direct contradictions (weight `1.0`).
- **Explainable Provenance:** Quotes the exact matched reference sentence and probability scores behind every label.
- **Zero External API Fees:** Runs locally on CPU PyTorch or directly in the browser via ONNX WebAssembly.
- **Full Auditability:** Persists every verification run in SQLite for retrospective filtering, trend tracking, and review.

---

# Chapter 2: Literature Survey

## 2.1 Introduction

This chapter reviews the foundational NLP methods, transformer architectures, and hallucination detection techniques on which TruthLens AI is built. Table 2.1 summarizes the primary literature and frameworks.

| No. | Work / Technology | Year | Core Contribution | Use in This Project | Limitation |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | **Transformers** (Vaswani et al.) | 2017 | Multi-head self-attention replacing recurrence | Underlying sequence encoder architecture | Quadratic memory with sequence length |
| 2 | **DeBERTa / DeBERTa-v3** (He et al.) | 2021 / 2023 | Disentangled content-position attention & ELECTRA pretraining | Primary NLI classifier (`nli-deberta-v3-base`) | Higher CPU latency than tiny bi-encoders |
| 3 | **MNLI** (Williams et al.) | 2018 | Multi-genre corpus for 3-way entailment, contradiction, neutral | Pretraining benchmark for NLI cross-encoders | Domain shift on specialized technical prose |
| 4 | **Sentence-BERT** (Reimers & Gurevych) | 2019 | Siamese sentence embeddings for cosine similarity | Motivates contrast against symmetric similarity | Symmetric `Sim(A,B)` misses contradictions |
| 5 | **FactCC / SummaC** (Kryściński et al.; Laban et al.) | 2020 / 2022 | Sentence-level NLI consistency checking for summaries | Inspires claim-premise NLI scoring | Primarily targeted news summarization |
| 6 | **SelfCheckGPT** (Manakul et al.) | 2023 | Reference-free multi-sample consistency verification | Comparative baseline in literature review | Multiplies generation latency and API cost |
| 7 | **FActScore** (Min et al.) | 2023 | Atomic claim decomposition for factual precision | Basis for atomic claim-level granularity | Relies on external retrieval / LLM prompts |
| 8 | **TF-IDF + FastAPI** (Salton & Buckley; Ramírez) | 1988 / 2024 | Lexical n-gram retrieval & async Python REST API | Candidate grounding (`top_k = 5`) & API layer | TF-IDF alone lacks synonym awareness |

*Table 2.1: Literature survey of core methods, models, and tools.*

## 2.2 Problem Formulation and Proposed Work

**Problem statement.** Existing verification tools either (a) rely on undirected lexical/embedding similarity that overlooks negations and numeric changes, (b) force binary classifications without an explicit *Insufficient Evidence* tier, or (c) depend on paid external LLM APIs without transparent mathematical risk scoring.

**Proposed solution.** TruthLens AI combines abbreviation-safe atomic claim splitting, TF-IDF cosine evidence grounding, directional DeBERTa-v3 cross-encoder NLI inference, configurable threshold classification, and SQLite audit logging inside a unified FastAPI and React SaaS platform.

## 2.3 Proposed Algorithm

1. Accept `reference_context` and `ai_answer` (`10`–`20,000` characters each) alongside optional `entailment_threshold` and `contradiction_threshold` (default `0.60`).
2. Normalize line breaks/bullets and split both texts into atomic claims `C_1...C_n` and reference sentences `S_1...S_m` while preserving decimals and abbreviations.
3. For each claim `C_i`, vectorize `S ∪ {C_i}` with unigram/bigram TF-IDF (`stop_words='english'`) and rank the `top_k = 5` candidate premises by cosine similarity.
4. If the highest similarity is `< 0.10` (or no reference sentences exist), classify `C_i` directly as `insufficient_evidence` (`neutral_score = 1.0`).
5. Otherwise, evaluate relevant `(premise, C_i)` pairs in batch with `cross-encoder/nli-deberta-v3-base` (`max_length = 512`, `torch.no_grad()`), applying Softmax over dynamically mapped `id2label` indices.
6. Select the first candidate passing `sim >= max(0.15, 0.4 * top_sim)` where `P(entailment) >= t_entail` and `P(entailment) > P(contradiction)` (`supported`), or `P(contradiction) >= t_contra` and `P(contradiction) > P(entailment)` (`contradicted`); otherwise mark `insufficient_evidence`.
7. Compute `HR = min(100.0, ((1.0 * N_contradicted + 0.5 * N_unsupported) / N_total) * 100)` and `EC`, persist the JSON report to SQLite `analyses`, and return `AnalyzeResponse`.

## 2.4 Proposed Work Phases

- **Phase 1 – Text & Retrieval Design:** Define abbreviation/decimal protection rules and TF-IDF top-5 candidate ranking.
- **Phase 2 – NLI Engine & Risk Math:** Build `NLIEngine` singleton with dynamic label inspection, `ClaimClassifier`, and `risk_calculator.py`.
- **Phase 3 – Backend & Persistence:** Implement FastAPI endpoints, Pydantic v2 schemas, CORS, and SQLAlchemy `AnalysisRecord` storage.
- **Phase 4 – SaaS Frontend & XAI:** Engineer Landing Showcase, Workspace Sidebar, Analyzer, Recharts Analytics, Explainable AI Flow, History Table, and Dark/Light themes.
- **Phase 5 – Static Browser Fallback:** Port pipeline to `browserNli.ts` using `@huggingface/transformers` ONNX WebAssembly and `localStorage`.
- **Phase 6 – Verification & Packaging:** Execute 13 Pytest cases, `tsc && vite build`, live tunnel verification, and academic documentation.

---

# Chapter 3: System Design

## 3.1 System Architecture

TruthLens AI follows a decoupled three-tier client–API–persistence architecture with an automatic browser-native fallback when hosted statically, illustrated in Figure 3.1.

```
User / Reviewer (inputs Reference Context & AI-Generated Answer)
      |
      +--> [Backend Online] --> FastAPI REST API (/api/analyze, asyncio.to_thread)
      |                               |
      |                               v
      |                         text_processing.py (atomic claims & premises)
      |                               |
      |                               v
      |                         EvidenceRetriever (TF-IDF 1-2 grams, top_k=5)
      |                               |
      |                               v
      |                         NLIEngine (cross-encoder/nli-deberta-v3-base)
      |                               |
      |                               v
      |                         Risk Calculator + SQLite (`analyses` table)
      |
      +--> [Static GitHub Pages] --> browserNli.ts (TF-IDF + Xenova/nli-deberta-v3-xsmall WASM + localStorage)
      |
      v
React 18 SaaS UI (Circular Risk Gauge, Donut/Bar Charts, Claim Cards, Explainable AI Flow, History)
```
*Figure 3.1: Overall system architecture.*

## 3.2 Layer Description

| Layer | Responsibility | Technology |
| :--- | :--- | :--- |
| **Presentation** | Landing showcase, workspace sidebar, analyzer, charts, XAI flow, Dark/Light themes | React 18, TypeScript, Tailwind CSS, Framer Motion, Recharts |
| **Application** | REST routing, Pydantic validation, worker-thread offloading, CORS | FastAPI, Uvicorn, Pydantic v2 |
| **Machine Learning** | Sentence segmentation, TF-IDF retrieval, cross-encoder NLI, risk scoring | PyTorch, Hugging Face Transformers, Scikit-Learn (or Transformers.js WASM) |
| **Persistence** | Audit log storage and retrieval | SQLAlchemy 2.x + SQLite (`truthlens.db`) / Browser `localStorage` |
| **Deployment** | Local dev proxy, public tunnel, static GitHub Pages bundle | Vite 5, Cloudflare Tunnel, GitHub Actions / `docs/` |

## 3.3 Module-Wise Design

| Module | Key Components | Decision / Control Logic | Output |
| :--- | :--- | :--- | :--- |
| **Text Processing** | `split_into_sentences`, `extract_claims`, `extract_evidence_sentences` | Shields decimals & 18 abbreviations; strips list prefixes | Atomic claim & premise arrays |
| **Evidence Retriever** | `EvidenceRetriever.retrieve_candidates` | TF-IDF cosine ranking; `min_evidence_similarity = 0.10` gate | Top-5 `(premise, similarity)` pairs |
| **NLI Engine** | `NLIEngine` (`_inspect_labels`, `predict_pairs`) | Dynamic `id2label` index resolution; fallback to `nli-distilroberta-base` | `entailment`, `contradiction`, `neutral` probabilities |
| **Claim Classifier** | `ClaimClassifier.analyze` | Compares filtered candidates against `t_entail` & `t_contra` | Per-claim classification + rationale |
| **Risk Calculator** | `calculate_hallucination_metrics` | Weights Contradicted (`1.0`) & Unsupported (`0.5`); assigns risk tier | `HR`, `EC`, rates, `risk_level` |
| **Frontend Workspace** | `DashboardPage`, `ResultsDashboard`, `HistoryPage`, `browserNli` | Uses FastAPI when reachable; else runs Browser WASM NLI | Interactive report & history log |

*Table 3.1: Module-wise functional design.*

## 3.4 Data Flow Diagrams

**Level 0:** The user supplies a reference context, an AI-generated answer, and optional thresholds to TruthLens AI, and receives a Hallucination Risk Score, claim classifications, visual probability charts, matched evidence citations, and Explainable AI rationales.

**Level 1:** Input text is validated (`1.0`), segmented into atomic claims and evidence sentences (`2.0`), matched via TF-IDF retrieval (`3.0`), scored by the DeBERTa-v3 NLI cross-encoder (`4.0`), aggregated into risk metrics (`5.0`), persisted in the `analyses` audit store (`6.0`), and rendered in the Results Dashboard and History table (`7.0`).

## 3.5 Data Design

- **`backend/app/schemas/analysis.py`**: Defines `ThresholdConfig`, `AnalyzeRequest` (min length `10`, max `20,000`), `ClaimResultSchema`, `SummaryMetricsSchema`, `AnalyzeResponse`, `HistoryItemSchema`, `HistoryListResponse`, `HealthResponse`, and `SystemInfoResponse`.
- **`backend/app/database/models.py` (`analyses` table)**: Persists `id` (`VARCHAR(36)` PK), `created_at` (`DATETIME`), `reference_context` (`TEXT`), `ai_answer` (`TEXT`), `total_claims`, `supported_count`, `contradicted_count`, `unsupported_count`, `contradiction_rate`, `unsupported_rate`, `evidence_coverage`, `hallucination_risk_score`, `risk_level`, `processing_time_ms`, `model_used`, and `claims_json`.

## 3.6 Repository Structure

```text
TruthLensAI/
  index.html, 404.html, .nojekyll       Root GitHub Pages entrypoints
  README.md, push_to_github.bat         Documentation & GitHub deploy helper
  run_backend.bat, run_frontend.bat     Local Windows launchers & test runner
  backend/
    requirements.txt                    Python dependencies
    app/main.py                         FastAPI app, lifespan warmup, CORS
    app/api/endpoints.py                /api/health, /info, /analyze, /history
    app/database/                       models.py, session.py, truthlens.db
    app/schemas/analysis.py             Pydantic request & response schemas
    app/services/                       nli_engine, evidence_retriever, claim_classifier, risk_calculator
    app/utils/text_processing.py        Abbreviation-safe sentence splitter
    tests/                              test_api.py, test_e2e.py, test_nli_engine.py
  frontend/
    package.json, vite.config.ts        Vite 5, React 18, Tailwind, Transformers.js
    src/components/                     Logo, Navbar, Footer, WorkspaceLayout, HeroAnalysisPreview, AnalysisLoader, ResultsDashboard
    src/pages/                          LandingPage, OverviewPage, DashboardPage, HistoryPage, AboutPage, SettingsPage
    src/services/                       api.ts, browserNli.ts
  docs/                                 Prebuilt static GitHub Pages bundle
```

---

# Chapter 4: Implementation

## 4.1 Module 1 – Claim & Evidence Text Processing

`backend/app/utils/text_processing.py` implements `split_into_sentences()`, normalizing CRLF/LF newlines, stripping bullet and numbered list prefixes (`-`, `*`, `•`, `1.`), shielding decimal numbers (`3.14`) and 18 abbreviations (`e.g.`, `i.e.`, `dr.`, `approx.`, etc.), and splitting cleanly on sentence boundaries. `EvidenceRetriever.retrieve_candidates()` in `evidence_retriever.py` vectorizes the extracted sentences and claim using `TfidfVectorizer(stop_words='english', ngram_range=(1, 2))` and returns the top 5 candidates by cosine similarity.

## 4.2 Module 2 – DeBERTa-v3 NLI Scoring Engine

`backend/app/services/nli_engine.py` loads `cross-encoder/nli-deberta-v3-base` (falling back to `cross-encoder/nli-distilroberta-base` if unreachable) as a singleton. `_inspect_labels()` inspects `model.config.id2label` dynamically so label indices are never assumed blindly. `predict_pairs()` tokenizes `(premise, hypothesis)` batches (`padding=True, truncation=True, max_length=512`) and normalizes logits via Softmax:

> **Softmax:** `P(y = k | P, H) = exp(z_k) / (exp(z_c) + exp(z_e) + exp(z_n))`

## 4.3 Module 3 – Claim Classification & Risk Calculator

`ClaimClassifier.analyze()` applies the `min_evidence_similarity = 0.10` relevance gate and evaluates candidates meeting `sim >= max(0.15, top_sim * 0.4)` against `entailment_threshold` and `contradiction_threshold` (default `0.60`). `calculate_hallucination_metrics()` computes:

> **Hallucination Risk:** `HR = min(100.0, ((1.0 * Contradictions + 0.5 * Unsupported) / Total) * 100)`

Risk levels map deterministically to **Severe** (`contradiction_rate >= 40%`), **High** (`HR >= 60%`), **Moderate** (`HR >= 30%` or any contradiction), **Low** (`HR > 0%`), and **Minimal** (`HR = 0%`).

## 4.4 Module 4 – FastAPI Backend and REST API

`backend/app/main.py` initializes SQLite tables and warms up `NLIEngine` during FastAPI startup (`lifespan`), executing inference off the event loop via `asyncio.to_thread`.

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Returns service health, `model_loaded` flag, and active device (`cpu`/`cuda`) |
| `/api/info` | `GET` | Returns model name, framework versions, device, and verified `label_mapping` |
| `/api/analyze` | `POST` | Runs full 5-stage NLI pipeline, persists report to SQLite, returns `AnalyzeResponse` |
| `/api/history` | `GET` | Lists paginated past evaluation summaries ordered by `created_at` descending |
| `/api/history/{id}` | `GET` | Retrieves complete claim-level breakdown for a stored `analysis_id` |
| `/api/history/{id}` | `DELETE` | Deletes a single audit record from SQLite |
| `/api/history` | `DELETE` | Clears all stored audit records |

## 4.5 Module 5 – React SaaS Interface & Browser WASM Engine

The frontend (`frontend/src/`) implements a dual-surface architecture:
- **Landing Showcase (`LandingPage.tsx`, `HeroAnalysisPreview.tsx`)**: Hero section with interactive claim-to-premise verification preview, 6 feature cards, 4-step workflow diagram, and mathematical entailment overview.
- **SaaS Workspace (`WorkspaceLayout.tsx`)**: Collapsible sidebar (`Overview`, `New Analysis`, `Analysis History`, `About Project`, `Settings`), persistent Dark/Light toggle (`ThemeContext.tsx`), and toast alerts (`ToastContext.tsx`).
- **Analyzer & Results (`DashboardPage.tsx`, `AnalysisLoader.tsx`, `ResultsDashboard.tsx`)**: Dual context/answer textareas with validation, 5-stage honest pipeline loader with live elapsed timer, animated circular risk gauge, Recharts Donut and Claim-Level NLI Bar charts, filterable claim cards, and a 4-block **Explainable AI Flow** tab.
- **Standalone Static Mode (`browserNli.ts`)**: When no backend responds (e.g., GitHub Pages), `api.ts` routes inference to `Xenova/nli-deberta-v3-xsmall` (quantized `q8` ONNX via `@huggingface/transformers`) and persists reports in `localStorage`.

## 4.6 Hardware and Software Environment

Development and verification were carried out on **Windows 11 (64-bit)** using **Python 3.12.9**, **PyTorch 2.6.0+cpu**, **Transformers 5.22.1**, **FastAPI 0.115.5**, **SQLAlchemy 2.1.9**, **Node.js v26.13.1**, **Vite 5.4.21**, and **Microsoft Edge / Google Chrome**.

---

# Chapter 5: Tools and Technologies Required

## 5.1 Programming Languages

**Python 3.12** for the FastAPI REST backend, NLP utilities, PyTorch NLI inference, and Pytest suite; **TypeScript 5.4**, **HTML5**, and **CSS3** for the React SaaS frontend and WebAssembly inference service.

## 5.2 Libraries and Frameworks

| Area | Tools & Verified Versions |
| :--- | :--- |
| **Deep Learning & NLI** | PyTorch (`2.6.0+cpu`), Hugging Face Transformers (`5.22.1`), `cross-encoder/nli-deberta-v3-base` |
| **Browser Inference** | `@huggingface/transformers` (ONNX Runtime Web / WASM, `Xenova/nli-deberta-v3-xsmall`) |
| **Information Retrieval** | Scikit-Learn (`1.9.1` `TfidfVectorizer` & `cosine_similarity`), NumPy (`2.5.4`) |
| **Web Backend** | FastAPI (`0.115.5`), Uvicorn (`0.32.0`), Pydantic (`2.9.2`) |
| **Database** | SQLAlchemy (`2.1.9`), SQLite (`truthlens.db`) |
| **Frontend UI & Charts** | React (`18.3.1`), Vite (`5.4.21`), Tailwind CSS (`3.4.3`), Framer Motion, Recharts, Lucide React |
| **Testing & Tunneling** | Pytest (`8.3.3`), HTTPX (`0.27.2`), TypeScript (`tsc`), Cloudflare Tunnel (`cloudflared`) |

## 5.3 Models and Verification Benchmarks

TruthLens AI uses `cross-encoder/nli-deberta-v3-base` on the backend (with automatic fallback to `cross-encoder/nli-distilroberta-base`), and `Xenova/nli-deberta-v3-xsmall` (`q8`) for zero-backend browser execution. Verification covers the canonical three-claim water physics benchmark (entailment, numeric contradiction, and unmentioned claim) alongside multi-scenario end-to-end tests.

## 5.4 Deployment Options

1. **Local Full-Stack Launch:** `run_backend.bat` (`127.0.0.1:8000`) + `run_frontend.bat` (`localhost:5173` with Vite `/api` proxy).
2. **Public Internet Tunnel:** `run_public_tunnel.bat` / `cloudflared` exposing the local Vite + FastAPI stack over HTTPS (`trycloudflare.com`).
3. **Static GitHub Pages Hosting:** Deployed via `.github/workflows/deploy.yml` (`./frontend/dist`) or `docs/`, running standalone DeBERTa-v3 WASM inference in the visitor's browser.

---

# Chapter 6: Software Requirements Specification (SRS)

## 6.1 Functional Requirements

1. **FR-1 Text Input & Validation:** The system shall accept `reference_context` and `ai_answer` inputs (`10`–`20,000` characters), provide a sample benchmark loader, clear button, and return validation errors (`400`/`422`) for empty or undersized inputs.
2. **FR-2 Claim Extraction & Grounding:** The system shall extract atomic sentences and retrieve up to 5 candidate evidence sentences per claim via TF-IDF similarity.
3. **FR-3 Three-Way NLI Classification:** The system shall classify every claim as `supported`, `contradicted`, or `insufficient_evidence` using configurable thresholds (`0.10`–`1.00`).
4. **FR-4 Risk & Telemetry Metrics:** The system shall compute Hallucination Risk Score, risk tier, Evidence Coverage, Contradiction Rate, Unsupported Rate, and latency in milliseconds.
5. **FR-5 Explainable AI Visualization:** The system shall display original claim, matched premise, three NLI probabilities, and plain-language rationale in expandable cards and a connected Explainable AI Flow inspector.
6. **FR-6 Audit History Management:** The system shall persist evaluations and support viewing, searching, filtering by risk level, deleting individual items, and clearing history.
7. **FR-7 Appearance & Endpoint Settings:** The system shall persist Dark/Light theme selection, default thresholds, and optional custom FastAPI URLs in `localStorage`.

## 6.2 Non-Functional Requirements

- **Usability:** Clean responsive SaaS workspace supporting desktop, tablet, and mobile viewports with zero horizontal overflow and keyboard focus indicators.
- **Reliability:** Graceful fallback from `nli-deberta-v3-base` to `nli-distilroberta-base` on the backend, and from FastAPI to in-browser WASM NLI when hosted statically.
- **Accessibility & Clarity:** Claim classifications never rely on color alone; every status combines a distinct icon (`CheckCircle2`, `XCircle`, `HelpCircle`), uppercase text label, and accessible contrast.
- **Security & Privacy:** All local inference executes on-device with no external LLM API calls; Pydantic enforces payload lengths and types.
- **Maintainability:** Modular separation across `services/`, `utils/`, `schemas/`, `database/`, `components/`, and `pages/`, covered by automated tests.

## 6.3 Hardware Requirements

Dual-core x86_64 processor (minimum) or quad-core CPU / CUDA GPU (recommended); 4 GB RAM minimum (8 GB+ recommended for transformer inference); 2 GB free disk space for Python, Node.js, and Hugging Face model cache.

## 6.4 Software Requirements

Windows 10/11, Ubuntu 20.04+, or macOS 12+; Python 3.10+ (tested on `3.12.9`); Node.js 18+ (tested on `v26.13.1`); packages listed in `backend/requirements.txt` and `frontend/package.json`; modern browser (Chrome, Edge, Firefox, or Safari).

## 6.5 Constraints and Limitations

- TruthLens AI verifies **relative factual consistency** strictly against the user-supplied reference context; it does not establish universal truth if the reference context itself is flawed.
- TF-IDF retrieval relies on lexical overlap (`1–2` n-grams); claims phrased with completely disjoint synonyms may score below `0.10` similarity and default to `insufficient_evidence`.
- Transformer inference on CPU incurs ~300–1500 ms per multi-claim request, and first-time Browser WASM use downloads ~87 MB of quantized ONNX weights into browser cache.

---

# Chapter 7: Results and Discussion

## 7.1 Introduction

This chapter presents empirical verification results observed from the live DeBERTa-v3 FastAPI backend, automated Pytest execution, TypeScript/Vite production bundling, and live tunnel endpoint testing.

## 7.2 Benchmark Verification Performance

Using the canonical Water Physics benchmark (*Reference:* `"Water boils at approximately 100 degrees Celsius at standard atmospheric pressure. Water freezes at 0 degrees Celsius under standard atmospheric pressure."` | *Answer:* `"Water boils at 100 degrees Celsius at standard atmospheric pressure. Water freezes at 10 degrees Celsius under standard atmospheric pressure. Water is composed of hydrogen and oxygen."`), the system achieved the results in Table 7.1.

| Claim # | Extracted Claim | Classification | Entailment | Contradiction | Neutral |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | Water boils at 100 degrees Celsius at standard atmospheric pressure. | **Supported** | `98.1%` | `0.1%` | `1.8%` |
| **2** | Water freezes at 10 degrees Celsius under standard atmospheric pressure. | **Contradicted** | `0.0%` | `99.9%` | `0.1%` |
| **3** | Water is composed of hydrogen and oxygen. | **Insufficient Evidence** | `0.0%` | `0.1%` | `99.9%` |

*Table 7.1: Water physics benchmark verification output (`Hallucination Risk: 50.0%`, `Evidence Coverage: 33.33%`).*

Additionally, a live two-claim inference request executed over the public Cloudflare Tunnel (`POST /api/analyze`) completed in **`318.84 ms`**, reporting `total_claims = 2`, `supported_count = 1`, `contradicted_count = 1`, `evidence_coverage = 50.0%`, and `hallucination_risk_score = 50.0%` (`Severe` tier due to `50%` contradiction rate).

## 7.3 Comparative Evaluation: Cosine Similarity vs. NLI

| Test Pair (Premise vs. Claim) | TF-IDF / Lexical Overlap | DeBERTa-v3 NLI Result | Outcome Accuracy |
| :--- | :---: | :--- | :--- |
| `"Water freezes at 0°C"` vs `"Water freezes at 10°C"` | High (`0.88`) | Contradiction (`99.9%`) | **Correctly Flagged** |
| `"Water boils at approx. 100°C"` vs `"Water boils at 100°C"` | High (`0.90`) | Entailment (`98.1%`) | **Correctly Verified** |
| Context omits composition vs `"Water is composed of H and O"` | Negligible (`0.049`) | Insufficient Evidence (`99.9%` Neutral) | **Correctly Unverified** |

*Table 7.2: Empirical comparison showing how directional NLI resolves the lexical similarity paradox.*

## 7.4 Explainability Results

In the **Results Dashboard**, users inspect an animated circular Hallucination Risk gauge, four summary metric cards, a Recharts Claim Distribution Donut chart, and a Claim-Level NLI Probability Bar chart. Switching to the **Explainable AI Flow** tab renders four connected visual blocks per selected claim: (1) Original Claim (Hypothesis), (2) Retrieved Evidence (Premise + TF-IDF similarity badge), (3) NLI Probability Simplex (`Entailment`, `Contradiction`, `Neutrality` vs. active thresholds), and (4) Final Classification & Decision Rationale.

## 7.5 Workspace and History Interface

The **Analysis History** view displays a responsive table (collapsing cleanly into cards on mobile) with Analysis ID, timestamp, claim breakdown (`S / C / U`), Risk Score, status badge, search input, risk-level filter pills, a risk score trend line chart, and View/Delete actions.

## 7.6 Automated Testing

Executing `python -m pytest backend/tests -v` validated **13 out of 13 tests (`100% PASS`) in `41.08s`**:

- **`backend/tests/test_api.py` (5 passed):** `test_api_root`, `test_api_health`, `test_api_info`, `test_api_analyze_validation`, `test_api_analyze_and_history_flow`.
- **`backend/tests/test_e2e.py` (4 passed):** `test_e2e_benchmark_water`, `test_e2e_all_supported_scenario`, `test_e2e_empty_and_invalid_inputs`, `test_e2e_history_lifecycle`.
- **`backend/tests/test_nli_engine.py` (4 passed):** `test_split_into_sentences`, `test_extract_claims_with_bullet_points`, `test_risk_calculator`, `test_nli_sample_analysis_benchmark`.

Frontend verification via `tsc && vite build` completed with **0 TypeScript errors**, producing `dist/index.html` (`2.23 kB`), `dist/assets/index-BLydhsfP.css` (`47.74 kB`), `dist/assets/index-CdtBzp5I.js` (`1,426.62 kB`), and `ort-wasm-simd-threaded.asyncify-CxOG5pUO.wasm` (`26,861.78 kB`). Live endpoints (`/`, `/api/health`) returned HTTP `200` and `status: healthy`.

## 7.7 Discussion

- Separating `insufficient_evidence` (`0.5` weight) from `contradicted` (`1.0` weight) avoids treating benign omissions as severe falsehoods while still warning reviewers about ungrounded statements.
- Dynamic inspection of `model.config.id2label` eliminates silent label-index bugs across different NLI checkpoints (`deberta-v3-base`, `distilroberta-base`, `nli-deberta-v3-xsmall`).
- Providing both a FastAPI PyTorch server and a Browser WASM fallback enables effortless live demonstrations across local development, Cloudflare Tunnels, and static GitHub Pages.

## 7.8 Conclusion of Results

TruthLens AI achieves its design goals: accurate directional entailment scoring, deterministic explainability, SQLite audit persistence, and a validated full-stack + browser-native deployment.

---

# Chapter 8: Conclusion and Future Scope

## 8.1 Conclusion

This project designed, implemented, and tested **TruthLens AI**, an explainable hallucination detection platform for LLM-generated answers. By combining abbreviation-safe atomic claim extraction, TF-IDF evidence retrieval, directional DeBERTa-v3 cross-encoder NLI scoring, weighted risk quantification, SQLite audit logging, and a modern React SaaS interface with a WebAssembly browser fallback, TruthLens AI demonstrates that factual verification can be accurate, transparent, privacy-preserving, and free of external API dependencies.

## 8.2 Future Scope

1. Implement **multi-hop premise aggregation** to verify claims synthesized across multiple dispersed reference sentences.
2. Replace or augment TF-IDF candidate retrieval with **hybrid dense + sparse embeddings** to handle paraphrased claims with low lexical overlap.
3. Add **token-level attribution heatmaps** highlighting specific contradictory words (such as mismatched numbers or negations) inside Explainable AI Flow.
4. Export **downloadable JSON and PDF verification certificates** directly from the Results Dashboard.
5. Integrate optional **real-time web/RAG knowledge connectors** (e.g., Wikipedia or internal document stores) when manual reference text is unavailable.
6. Apply **INT8 ONNX quantization** on the backend server to push CPU inference latency under `100 ms`.
7. Add **role-based authentication and multi-tenant workspaces** for enterprise deployment.

## 8.3 Final Remarks

Building TruthLens AI reinforced core principles across Natural Language Inference, full-stack asynchronous API engineering, and explainable AI interface design—showing that trustworthy generative AI systems require verification and transparency built into the workflow from the ground up.

---

## References

1. A. Vaswani, N. Shazeer, N. Parmar, et al., “Attention Is All You Need,” *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017.
2. P. He, X. Liu, J. Gao, and W. Chen, “DeBERTa: Decoding-enhanced BERT with Disentangled Attention,” *International Conference on Learning Representations (ICLR)*, 2021.
3. P. He, J. Gao, and W. Chen, “DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing,” *ICLR / arXiv:2111.09543*, 2023.
4. A. Williams, N. Nangia, and S. R. Bowman, “A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference,” *NAACL-HLT*, 2018, pp. 1112–1122.
5. W. Kryściński, B. McCann, C. Xiong, and R. Socher, “Evaluating the Factual Consistency of Abstractive Text Summarization,” *EMNLP*, 2020, pp. 9332–9346.
6. P. Laban, T. Schnabel, P. Bennett, and M. A. Hearst, “SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization,” *TACL*, vol. 10, 2022, pp. 163–177.
7. P. Manakul, A. Liusie, and M. J. Gales, “SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models,” *EMNLP*, 2023, pp. 9004–9017.
8. S. Min, K. Krishna, X. Lyu, et al., “FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation,” *EMNLP*, 2023, pp. 12076–12099.
9. N. Reimers and I. Gurevych, “Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,” *EMNLP*, 2019, pp. 3982–3992.
10. FastAPI, SQLAlchemy, Hugging Face Transformers, and React Documentation. Available at: https://fastapi.tiangolo.com/, https://huggingface.co/docs/transformers/, https://react.dev/.
