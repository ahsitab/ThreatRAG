# AI506 MSc Midterm Project Specification: Final Compliance Report
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Project Name:** ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework for Explainable Cybersecurity Threat Intelligence and Incident Response  
**Candidate / Student:** Asfar Hossain Sitab  
**Assessment Total:** 20 Marks (Presentation & Viva: 20–30 Minutes)  
**Verification Date:** 2026-11-23  
**Overall Compliance Grade:** 100% COMPLIANT (PASS ON ALL 20 CRITERIA)  

---

## 1. Compliance Checklist (Section by Section)

| Rubric ID | AI506 Specification Requirement | Implementation Evidence & File Reference | Status |
| :--- | :--- | :--- | :---: |
| **REQ-01** | Base research paper selected from peer-reviewed venue (ACL, EMNLP, NeurIPS, etc.) | `MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation` (ACL 2025, pp. 2607–2622). Verified in `research/selected_base_paper.md`. | **PASS** |
| **REQ-02** | Explicit mapping of adopted, adapted, and extended concepts | Complete breakdown in `research/paper_to_project_mapping.md` and Slide 4. | **PASS** |
| **REQ-03** | Verified references bibliography with DOIs/URLs | BibTeX file updated at `research/references.bib`. | **PASS** |
| **REQ-04** | At least 3 specialized logical agents with distinct responsibilities | 4 Agents implemented in `agents/`: Coordinator (`coordinator.py`), Retrieval (`retrieval_agent.py`), Reasoning (`reasoning_agent.py`), Verification (`verification_agent.py`). | **PASS** |
| **REQ-05** | Iterative verification feedback loop | Verification agent detects unsupported claims or low similarity (<0.20) and triggers coordinator re-retrieval (max retries = 2). Implemented in `agents/coordinator.py`. | **PASS** |
| **REQ-06** | Observable Agent Execution Trace in UI | Real-time interactive trace panel with Mermaid workflow diagram, step cards, and timing in `app/pages/2_Threat_Analysis.py`. | **PASS** |
| **REQ-07** | Conventional Single-Agent RAG Baseline | Fully implemented in `rag/baseline_single_agent.py` using identical 1,074 chunks and `all-MiniLM-L6-v2`. | **PASS** |
| **REQ-08** | Side-by-Side Comparison UI | Interactive comparison page allowing head-to-head testing across questions in `app/pages/8_AI506_Baseline_Comparison.py`. | **PASS** |
| **REQ-09** | 50-Question Benchmark Suite | 50 curated questions with ground truth rubrics, MITRE IDs, CVEs, and edge cases in `data/evaluation/ai506_test_questions.json` & `.csv`. | **PASS** |
| **REQ-10** | Empirical Head-to-Head Evaluation | Executed on all 50 questions; results in `reports/ai506_baseline_comparison.csv` and `reports/ai506_evaluation_results.md`. | **PASS** |
| **REQ-11** | Agent Ablation Study | Empirical comparison of Full System vs. w/o Verification vs. w/o Reasoning vs. Baseline in Table II of IEEE report. | **PASS** |
| **REQ-12** | Sufficient vs Insufficient Evidence Testing | Evaluated on 4 ungrounded queries (e.g., `TID-014`); single-agent hallucinates while ThreatRAG safely abstains. | **PASS** |
| **REQ-13** | Quality-Cost Trade-Off Analysis | Measured trade-off documented: +207% correctness & 100% citation precision for +3.53s latency and $0.00063/query. | **PASS** |
| **REQ-14** | IEEE 4–6 Page Conference Report | Written in LaTeX (`reports/ThreatRAG_AI506_IEEE.tex`) and compiled to PDF (`reports/ThreatRAG_AI506_IEEE.pdf`). | **PASS** |
| **REQ-15** | 12-Slide Presentation matching Syllabus | PowerPoint created at `presentation/ThreatRAG_AI506_Presentation.pptx` and PDF at `presentation/ThreatRAG_AI506_Presentation.pdf`. | **PASS** |
| **REQ-16** | 7–10 Minute Live Demonstration Script | Precise step-by-step walkthrough created at `presentation/DEMO_SCRIPT.md`. | **PASS** |
| **REQ-17** | Demonstration Queries Profile | 4 curated live demonstration query profiles formatted in `presentation/DEMO_QUERIES.json`. | **PASS** |
| **REQ-18** | Viva Preparation Guide (13 Questions) | In-depth technical questions and bulletproof answers in `presentation/VIVA_PREPARATION.md`. | **PASS** |
| **REQ-19** | Defensive Cybersecurity & Human-in-the-Loop | Mandatory analyst approval checkbox enforced before any containment playbook dispatch; zero autonomous disruption. | **PASS** |
| **REQ-20** | Synchronized GitHub Repository | Complete repository synchronized at `https://github.com/ahsitab/ThreatRAG.git`. | **PASS** |

---

## 2. Summary of Measured Results

```
======================================================================
AI506 EMPIRICAL EVALUATION SUMMARY (N = 50 Questions)
======================================================================
Metric                        Conventional RAG    Multi-Agent ThreatRAG
----------------------------------------------------------------------
Passing Answers (>=70%):      0/50 (0.0%)         6/50 (12.0%)  [+12.0%]
Mean Correctness Score:       0.1113              0.3423        [+207% rel.]
Mean Faithfulness Score:      0.7958              0.8000        [+0.4%]
Citation Correctness:         50.0%               100.0%        [+50.0%]
Average Response Latency:     0.03 seconds        3.56 seconds  [+3.53s]
Average Token Consumption:    1,519 tokens        2,255 tokens  [~1.5x]
Average Cost per Query:       $0.000340           $0.000631     [<$0.001]
Expected Calib. Error (ECE):  0.0037 (Raw)        0.0005 (Platt)[-86.5%]
======================================================================
```

---

## 3. Deliverables Artifact Directory

- **IEEE Conference Report:**
  - LaTeX Source: `reports/ThreatRAG_AI506_IEEE.tex`
  - HTML Rendition: `reports/ThreatRAG_AI506_IEEE.html`
  - Printable PDF: `reports/ThreatRAG_AI506_IEEE.pdf`
- **Presentation Slide Deck:**
  - PowerPoint Presentation: `presentation/ThreatRAG_AI506_Presentation.pptx`
  - HTML Slide Deck: `presentation/ThreatRAG_AI506_Presentation.html`
  - Printable PDF: `presentation/ThreatRAG_AI506_Presentation.pdf`
- **Evaluation Benchmark Data:**
  - JSON Benchmark Suite: `data/evaluation/ai506_test_questions.json`
  - CSV Benchmark Suite: `data/evaluation/ai506_test_questions.csv`
  - Head-to-Head Comparison CSV: `reports/ai506_baseline_comparison.csv`
  - Full Evaluation Report: `reports/ai506_evaluation_results.md`
  - Metric Comparison Figure: `reports/figures/ai506_metrics_comparison.png`
- **Live Demo & Viva:**
  - Demo Script: `presentation/DEMO_SCRIPT.md`
  - Viva Preparation Guide: `presentation/VIVA_PREPARATION.md`
  - Demo Queries: `presentation/DEMO_QUERIES.json`
- **Base Paper Research:**
  - Base Paper Study: `research/selected_base_paper.md`
  - Paper to Project Mapping: `research/paper_to_project_mapping.md`
  - Citations BibTeX: `research/references.bib`
