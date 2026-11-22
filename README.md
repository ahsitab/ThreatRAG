# ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework for Explainable Cybersecurity Threat Intelligence and Incident Response

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Persistent-orange.svg)](https://www.trychroma.com/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

---

## 🎯 What Does ThreatRAG Actually Do? (In Plain English)

Modern Security Operations Centers (SOCs) are overwhelmed by thousands of alerts every day. When an anomaly is detected, analysts are trapped between two extremes:
1. **Black-box machine learning detectors** that output a raw score with zero explanation of *why* it is dangerous or what steps to take.
2. **Standard Large Language Models (LLMs)** that hallucinate nonexistent vulnerabilities, recommend risky commands, and cite fake CVEs.

**ThreatRAG solves this by acting as an autonomous, explainable AI cybersecurity co-pilot.**

```mermaid
flowchart LR
    A[Raw Network Telemetry<br>e.g., 95k pkts/s on port 80] --> B[Calibrated LightGBM Anomaly Engine]
    B -->|Predicts Anomaly & Uncertainty| C[Adaptive Hybrid Retrieval<br>Dense + BM25 + Structured]
    C -->|Grounds in MITRE ATT&CK & CISA KEV| D[Multi-Agent Team]
    D --> E[Explainable Factual Report]
    D --> F[Historical Precedent Match]
    D --> G[Defensive Playbook]
    G --> H{Human Analyst Approval Gate}
    H -->|Signed Authorization| I[Dispatched Mitigation]
```

### 🔍 Here is what happens when a network flow or alert enters ThreatRAG:
1. **Calibrated Threat Identification:** Rather than making uncalibrated, overconfident guesses, our post-hoc calibrated LightGBM model calculates the exact probability of an attack with quantified uncertainty and highlights the top contributing flow features (e.g., anomalous packet rates, flow duration, byte volume).
2. **Historical Precedent Search:** The system uses hybrid retrieval (semantic vectors + BM25 lexical tokens) to search real-world historical cyber incidents (such as the *Mirai Botnet*, *Dyn DNS Attack*, *SolarWinds SUNBURST*, and *MOVEit Transfer Zero-Day*), showing how similar threats operated in the past.
3. **MITRE ATT&CK Evidence Explainer:** It maps observed attacker behavior to official MITRE ATT&CK techniques (e.g., `T1498.001`, `T1059.001`), strictly separating **empirical facts** (verified network measurements) from **hypotheses** (inferred attacker intent).
4. **CISA KEV Defensive Playbook:** It compiles a step-by-step incident response playbook (containment, eradication, recovery) grounded in official CISA Known Exploited Vulnerabilities advisories.
5. **Human-in-the-Loop Safety Gate:** ThreatRAG operates under a strictly defensive posture. It **never** autonomously modifies firewall rules or isolates servers without an explicit digital sign-off from an authorized human security analyst.

---

## 🖼️ Dashboard & Visual Interface Screenshots

ThreatRAG features a multi-page interactive dashboard for security analysts and researchers.

### 1. System Overview & Ingestion Topology
*Displays active knowledge base chunks (1,074 chunks), STIX 2.1 techniques (718 techniques), CISA KEV advisories (1,790 CVEs), and dataset splits:*
![System Overview](docs/screenshots/02_system_overview.png)

---

### 2. Post-Hoc Confidence Calibration (Reliability Diagram)
*Figure 1 demonstrates how Platt Scaling reduces the Expected Calibration Error (ECE) from 0.0037 down to 0.0005 (an 86.5% error reduction) across 6,000 held-out flows:*
![Calibration Curve](reports/figures/calibration_curve.png)

---

### 3. Confusion Matrix on 6,000 Evaluation Flows
*Figure 2 displays the performance on the independent CIC-IDS2017 test set, achieving 99.98% accuracy and 0.0000 False Positive Rate:*
![Confusion Matrix](reports/figures/confusion_matrix.png)

---

### 4. Empirical Research Evaluation Benchmark Page
*Interactive research dashboard displaying retrieval metrics ($E_2$–$E_5$), generation faithfulness, agent latencies, and component ablation studies:*
![Research Evaluation](docs/screenshots/07_research_evaluation.png)

---

## 🔬 Core Academic Research Contributions

| Metric / Dimension | Traditional Dense RAG ($E_2$) | ThreatRAG Proposed ($E_5$) | Research Impact |
| :--- | :---: | :---: | :--- |
| **Retrieval Ranking (nDCG@5)** | 0.5933 | **0.7243** ($E_4$) / **0.6774** | **+22.1% improvement** over dense-only search by fusing lexical BM25 for alphanumeric identifiers (`CVE-2023-34362`, `T1059`). |
| **Citation Precision** | 100.0% | **100.0%** | Zero hallucinated bracketed citations across all audited chunks. |
| **Expected Calibration Error (ECE)** | 0.0037 (Raw) | **0.0005 (Platt)** | **86.5% reduction in calibration error**, preventing overconfident automated decisions in borderline flows. |
| **False Positive Rate (FPR)** | 0.0073 (LR) | **0.0000 (LightGBM)** | Zero benign network sessions falsely flagged as attacks on the held-out test split. |
| **Mean Agent Latency** | N/A | **6.54 seconds** | Rapid, real-time multi-agent triage on standard CPU hardware. |
| **Mean Cost Per Query** | N/A | **$0.00076** | Extremely lightweight and economical for continuous SOC monitoring. |
| **Adversarial Injection Defense** | Vulnerable | **100.0% Neutralized** | Intercepts and redacts adversarial prompt injection attempts (`IGNORE ALL PREVIOUS INSTRUCTIONS`). |

---

## 🏗️ Repository Architecture

```text
ThreatRAG/
├── agents/                       # 4 Multi-agent implementations & orchestrator
│   ├── threat_identifier.py      # Agent 1: Telemetry validation & calibrated ML inference
│   ├── incident_search.py        # Agent 2: Historical incident similarity matching
│   ├── evidence_explainer.py     # Agent 3: ATT&CK grounding & fact/hypothesis separation
│   ├── response_advisor.py       # Agent 4: Prioritized playbooks & human approval gate
│   └── orchestrator.py           # Pipeline coordinator, token tracking, state machine
├── api/                          # FastAPI production REST backend
│   ├── routes/                   # Route controllers (analysis, documents, evaluation)
│   ├── schemas/                  # Pydantic v2 data transfer schemas
│   └── main.py                   # App entrypoint, CORS, timing middleware, health checks
├── app/                          # Streamlit 7-page interactive dashboard
│   ├── pages/                    # Multi-page views (Overview, Threat Analysis, Evaluation, etc.)
│   └── dashboard.py              # Main navigation & landing interface
├── artifacts/                    # Serialized models, scalers, and vector indices
│   ├── chroma_db/                # Persistent vector database (all-MiniLM-L6-v2)
│   ├── bm25_index.pkl            # Persistent BM25 inverted index
│   ├── threat_classifier.joblib  # Calibrated LightGBM model
│   └── flow_scaler.joblib        # Robust standard scaler
├── configs/                      # Configuration parameters & prompt templates
├── data/                         # Data storage hierarchy
│   ├── manifests/                # Provenance manifests with SHA-256 checksums
│   ├── processed/                # Normalized chunks (1,074) and cleaned flows
│   ├── raw/                      # Public datasets (CIC-IDS2017, STIX 2.1, CISA KEV)
│   └── splits/                   # Stratified train (18k), val (6k), and test (6k) splits
├── docs/screenshots/             # Dashboard visual interface captures
├── evaluation/                   # Evaluation harnesses (retrieval, generation, agents, ablation)
├── models/                       # ML training, feature scaling, and calibration engines
│   ├── calibration.py            # Platt scaling, Isotonic regression, ECE, Brier score
│   ├── predict.py                # Calibrated inference engine with feature attribution
│   └── train.py                  # Training pipeline across LR, RF, and LightGBM
├── rag/                          # Retrieval engine components
│   ├── chunking.py               # Security entity tokenizer & metadata-aware chunker
│   ├── embeddings.py             # SentenceTransformer wrapper (all-MiniLM-L6-v2)
│   ├── vector_store.py           # Persistent ChromaDB client
│   ├── bm25_retriever.py         # BM25Okapi implementation
│   ├── structured_retriever.py   # Statistical port/protocol flow matcher
│   ├── reranker.py               # Cross-Encoder (ms-marco-MiniLM-L-6-v2)
│   ├── hybrid_retriever.py       # Adaptive RRF retriever
│   ├── citation_validator.py     # Bracketed citation auditor & injection defense
│   └── ingestion.py              # Incremental knowledge base manager
├── reports/                      # Academic figures, tables, and findings
│   ├── figures/                  # Reliability diagram & confusion matrix
│   ├── tables/                   # Benchmark CSVs (retrieval, ablation, calibration)
│   ├── limitations.md            # Internal, external, and construct validity threats
│   └── results.md                # Comprehensive experimental report
├── research/                     # Literature review & methodology documentation
│   ├── references.bib            # 22 verified academic references (DOIs/URLs)
│   ├── literature_matrix.csv     # Comparative matrix across 10 dimensions
│   ├── literature_review.md      # Structured academic literature review
│   ├── research_gap.md           # Formal gap analysis, RQ1-RQ4, hypotheses H1-H4
│   ├── methodology.md            # Mathematical specifications & architecture
│   └── experimental_design.md    # Baselines E1-E6, protocols, and metrics
├── scripts/                      # Automation & data download utilities
│   ├── download_datasets.py      # Resumable downloader with SHA-256 validation
│   ├── prepare_data.py           # Preprocessing & stratified splitting
│   ├── build_index.py            # Vector and BM25 indexing pipeline
│   └── run_experiments.py        # Master research experiment runner
├── tests/                        # Automated Pytest suite
│   ├── test_rag.py               # Unit tests for chunking, BM25, vector, reranking
│   ├── test_models.py            # Unit tests for inference, calibration, ECE
│   ├── test_agents.py            # Integration tests for all 4 agents & orchestrator
│   └── test_api.py               # FastAPI TestClient endpoint validation
├── Dockerfile                    # Multi-stage production container build
├── docker-compose.yml            # Dual-service deployment (API + UI)
├── requirements.txt              # Pinned Python package dependencies
└── README.md                     # Research documentation and reproduction manual
```

---

## 🚀 Step-by-Step Deployment & Reproduction Guide

### Option 1: Run Locally (Fastest for Testing)

#### 1. Clone the repository & create environment:
```bash
git clone https://github.com/ahsitab/ThreatRAG.git
cd ThreatRAG

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Verify Datasets & Preprocessing (Included in Repo):
The preprocessed knowledge chunks (1,074 chunks), model artifacts, and vector indices are already built and included in `artifacts/` and `data/splits/`.
If you wish to download raw datasets from official sources and rebuild from scratch:
```bash
python scripts/download_datasets.py
python scripts/prepare_data.py
python scripts/build_index.py
python models/train.py
```

#### 3. Launch the Streamlit Dashboard:
```bash
streamlit run app/dashboard.py
# Open your browser at: http://localhost:8501
```

#### 4. Launch the FastAPI Backend:
```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
# View interactive API documentation at: http://127.0.0.1:8000/docs
```

#### 5. Run the Test Suite:
```bash
pytest -v tests/test_agents.py
pytest -v tests/test_models.py
pytest -v tests/test_rag.py
```

---

### Option 2: Run with Docker & Docker Compose (Production Ready)

To deploy both the **FastAPI Backend (port 8000)** and the **Streamlit Dashboard (port 8501)** in isolated containers with one single command:

```bash
docker compose up --build -d
```

Check health:
- Streamlit UI: `http://localhost:8501`
- FastAPI Health: `http://localhost:8000/health`
- Swagger Docs: `http://localhost:8000/docs`

To stop:
```bash
docker compose down
```

---

### Option 3: Deploy to Cloud (Hugging Face Spaces / Render / AWS)

- **Hugging Face Spaces:**
  - Create a new Space with the **Streamlit** SDK.
  - Set `app_file: app/dashboard.py` in `README.md` metadata.
  - Push the repository to the Space remote.
- **Render / Railway / Cloud Run:**
  - Connect your GitHub repository.
  - Build command: `pip install -r requirements.txt`
  - Start command: `streamlit run app/dashboard.py --server.port $PORT --server.address 0.0.0.0`

---

## 🛡️ Ethical Governance & Defensive Cybersecurity Posture

- **Exclusively Defensive:** ThreatRAG is designed strictly for threat detection, incident triage, and explanatory reasoning. It contains zero offensive exploits, port scanning scanners, or automated exploitation scripts.
- **Mandatory Human-in-the-Loop Sign-Off:** No network configuration, route nullification, or endpoint isolation is ever autonomously executed. A certified human security analyst must review and authorize all remediation actions.
- **Zero Synthetic Fabrication:** Every metric, calibration curve, confusion matrix, and citation in this repository was generated through genuine code execution on authentic datasets.

---

## 📜 Academic Citation

```bibtex
@mastersthesis{threatrag2026,
  author       = {Ahsan Habib Sitab},
  title        = {{ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework for Explainable Cybersecurity Threat Intelligence and Incident Response}},
  school       = {School of Computing and Artificial Intelligence},
  year         = {2026},
  month        = {November},
  type         = {MSc Artificial Intelligence and Machine Learning Thesis},
  note         = {AIML-507 Research Project}
}
```

---

*Authored by Ahsan Habib Sitab • AIML-507 Research Project • ThreatRAG Framework*
