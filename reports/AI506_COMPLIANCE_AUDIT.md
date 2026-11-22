# AI506 MSc Midterm Project Compliance Audit: ThreatRAG
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Project:** ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework for Explainable Cybersecurity Threat Intelligence and Incident Response  
**Author / Researcher:** Asfar Hossain Sitab  
**Audit Date:** 2026-11-23  

---

## 1. Executive Summary
This audit inspects the current ThreatRAG codebase against the **AI506 MSc Midterm Project Specification: Multi-Agent Retrieval-Augmented Generation System**. The existing project provides a robust, working cybersecurity RAG engine (hybrid retrieval, calibrated ML classifier, persistent vector store, and multi-page dashboard). This audit identifies existing components, partially implemented areas, and the precise additions required for 100% compliance.

---

## 2. Requirement-by-Requirement Compliance Matrix

| Requirement | Specification | Current Implementation Status | Gap & Required Modifications | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Req 1: Base Paper** | Inspired by $\ge 1$ peer-reviewed conference/journal paper (ACL 2025/2026 candidate). | Currently references general literature matrix (22 papers in `research/`). Explicit base paper deep-dive not yet isolated. | Investigate MAIN-RAG (ACL 2025) and MASS-RAG (Findings of ACL 2026). Select, map adopted/adapted/extended ideas in `research/selected_base_paper.md` and `research/paper_to_project_mapping.md`. | **NEEDS IMPLEMENTATION** |
| **Req 2: Multi-Agent Roles** | $\ge 3$ distinct logical agent roles (Coordinator, Retrieval Specialist, Reasoning Specialist, Verification Specialist). | 4 task-based agents exist (`ThreatIdentifier`, `IncidentSearch`, `EvidenceExplainer`, `ResponseAdvisor`) executing sequentially. | Refactor/augment agents with formal logical roles: Coordinator/Planner, Retrieval Specialist, Reasoning Specialist, Verification Specialist with state sharing. | **NEEDS ENHANCEMENT** |
| **Req 3: Agent Feedback Loop** | Dynamic feedback loop: Coordinator $\to$ Retrieval $\to$ Reasoning $\to$ Verification $\to$ (if insufficient) $\to$ Retrieval with max retry limit. | Verification occurs post-hoc via `CitationValidator`, but does not trigger a re-retrieval loop on insufficient evidence. | Implement a dynamic feedback loop in orchestrator with configurable `max_retries` (default: 2) and fallback qualifier. | **NEEDS IMPLEMENTATION** |
| **Req 4: Agent Trace Panel** | Observable agent communication trace in UI (decisions, selected agents, evidence passages, verification, retries). | Streamlit currently displays final summaries and metric badges, but lacks a dedicated step-by-step Execution Trace Panel. | Build a dedicated "Agent Execution Trace Panel" in Streamlit and add a new "Agent Handoff & Trace" view. | **NEEDS IMPLEMENTATION** |
| **Req 5: Single-Agent Baseline** | Fair comparison against conventional Single-Agent RAG using identical corpus, models, and retrieval budget. | Earlier evaluated baselines E1-E4, but single-agent baseline code was embedded inside evaluation scripts rather than a standalone class. | Create a clean `rag/baseline_single_agent.py` and a dedicated side-by-side comparison page in Streamlit. | **NEEDS IMPLEMENTATION** |
| **Req 6: 30–50 Test Questions** | Target set of 50 cybersecurity benchmark questions across the 4 tasks with ground truth and rubrics. | Benchmark suite had 10 synthetic queries; need formal 50-question curated dataset covering all 4 tasks + insufficient evidence cases. | Compile `data/evaluation/ai506_test_questions.json` (50 items) and `.csv`, documented in `research/evaluation_dataset_documentation.md`. | **NEEDS IMPLEMENTATION** |
| **Req 7: Empirical Evaluation** | Measure Answer Correctness, Faithfulness, Citation Correctness, and Latency/Tokens/Cost across both systems. | Partial evaluations run; need formal head-to-head evaluation on the 50-question benchmark with CSV and report. | Execute benchmark runner comparing System A (Single-Agent RAG) vs System B (Multi-Agent ThreatRAG); save `reports/ai506_baseline_comparison.csv`. | **NEEDS IMPLEMENTATION** |
| **Req 8: Agent Ablation** | Optional ablation study: Full ThreatRAG vs w/o Verification vs w/o Reasoning vs Single-Agent. | Earlier ablation covered retrieval components; need agent-level ablation table. | Conduct agent ablation study over benchmark questions; record in `reports/ai506_evaluation_results.md`. | **NEEDS IMPLEMENTATION** |
| **Req 9: IEEE 4–6 Page Report** | Official IEEE two-column conference format report (`.tex` and `.pdf`). | Currently markdown reports exist (`reports/results.md`); need full IEEE LaTeX template and compiled PDF. | Write `reports/ThreatRAG_AI506_IEEE.tex` and compile `reports/ThreatRAG_AI506_IEEE.pdf` (4–6 pages, 2-column, excluding references). | **NEEDS IMPLEMENTATION** |
| **Req 10: Presentation Slides** | 10–12 slide professional PowerPoint presentation (`.pptx` and `.pdf`). | Not yet generated. | Create `presentation/ThreatRAG_AI506_Presentation.pptx` (12 slides) following the recommended outline. | **NEEDS IMPLEMENTATION** |
| **Req 11: Demo & Viva Preparation** | Live demonstration script, viva preparation guide, and demo query bank. | Working app is live, but structured demo script and viva Q&A document are missing. | Write `presentation/DEMO_SCRIPT.md`, `presentation/VIVA_PREPARATION.md`, and `presentation/DEMO_QUERIES.json`. | **NEEDS IMPLEMENTATION** |
| **Req 12: GitHub Repository** | Clean, accessible GitHub repository with runnable code and zero secrets. | Repository initialized, pushed to `https://github.com/ahsitab/ThreatRAG.git`. | Update repository with all AI506 compliance additions and verify clean git status. | **ALREADY WORKING / UPDATE REQUIRED** |
| **Req 13: Regression Testing** | Verify existing capabilities still work + add tests for feedback loops and agent handoffs. | Pytest suite exists (19 tests). | Expand tests in `tests/test_agents.py` to cover feedback loop, single-agent baseline, and execution traces. | **NEEDS ENHANCEMENT** |
| **Req 14: Final Compliance Report** | Structured compliance validation checklist with PASS/PARTIAL/FAIL and evidence paths. | Will be compiled upon completion of Tasks 2–13. | Compile `reports/FINAL_AI506_COMPLIANCE_REPORT.md`. | **PENDING EXECUTION** |

---

## 3. Preserved Working Assets
The following existing assets must be strictly preserved without rebuilding:
1. `data/raw/`, `data/splits/` (stratified 18k train, 6k val, 6k test flows).
2. `artifacts/chroma_db/` (persistent vector store with 1,074 chunks).
3. `artifacts/bm25_index.pkl` (persistent BM25 index).
4. `artifacts/threat_classifier.joblib` and `flow_scaler.joblib` (calibrated LightGBM model, ECE = 0.0005).
5. All working Streamlit dashboard pages in `app/pages/` (will be augmented with trace panel and baseline comparator).
6. FastAPI backend in `api/`.
