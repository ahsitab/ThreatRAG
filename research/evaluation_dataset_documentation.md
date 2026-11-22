# AI506 Evaluation Benchmark Dataset Documentation
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Project:** ThreatRAG: An Adaptive Hybrid RAG Framework for Explainable Threat Intelligence  
**Dataset Reference:** `data/evaluation/ai506_test_questions.json` / `ai506_test_questions.csv`  
**Total Examples:** 50 Curated Cybersecurity Questions  

---

## 1. Benchmark Overview & Purpose
This evaluation dataset is designed to provide a rigorous, reproducible, and balanced benchmark for assessing **Multi-Agent ThreatRAG** against a **Conventional Single-Agent RAG Baseline** in accordance with Section 7 of the AI506 Midterm Specification.

The questions reflect authentic operational queries faced by Security Operations Center (SOC) tier-1 to tier-3 analysts, incident responders, and threat hunters.

---

## 2. Dataset Distribution Across ThreatRAG Tasks

| Task Category | Question Range | Count | Primary Evaluated Capability |
| :--- | :---: | :---: | :--- |
| **Task 1: Threat Identification** | `TID-001` – `TID-015` | 15 | Flow telemetry classification, anomaly detection, port mapping, uncertainty quantification. |
| **Task 2: Historical Incident Similarity** | `HIS-001` – `HIS-010` | 10 | Precedent matching (Mirai, SolarWinds, MOVEit, WannaCry), shared traits & operational differences. |
| **Task 3: Evidence-Based Explanation** | `EBE-001` – `EBE-015` | 15 | ATT&CK technique grounding, empirical fact vs hypothesis separation, citation precision. |
| **Task 4: Defensive Response Recommendations** | `DRR-001` – `DRR-010` | 10 | Prioritized containment checklists, CISA KEV grounding, operational impact, human sign-off. |
| **Total Benchmark Suite** | — | **50** | Complete end-to-end multi-agent evaluation. |

---

## 3. Difficulty Level Distribution
- **Easy (16 Questions / 32%):** Direct lookup and standard telemetry profiles (e.g. well-known port 80 SYN flood, MITRE T1059 definition, CISA Log4j advisory).
- **Medium (24 Questions / 48%):** Multi-hop reasoning combining telemetry with technique descriptions, comparative difference analysis, and protocol amplification mechanics.
- **Hard / Edge-Cases (10 Questions / 20%):** Complex attack variants, low-and-slow Layer 7 exhaustion, and **adversarial / out-of-domain / ungrounded queries** requiring the system to acknowledge insufficient evidence.

---

## 4. Insufficient Evidence & Abstention Protocol
Crucially, **4 out of the 50 questions** (`TID-011`, `TID-014`, `HIS-010`, `EBE-014`, `DRR-010`) represent test cases where the knowledge corpus intentionally lacks ground truth evidence (e.g. fictional Martian attacks, quantum sub-space exploits, single dropped packet noise).
- **Single-Agent Baseline Behavior:** Typically hallucinates plausible-sounding explanations or issues unsupported generic claims.
- **Multi-Agent ThreatRAG Behavior:** The Verification Specialist flags `INSUFFICIENT_EVIDENCE`, triggers the Coordinator feedback loop, and if no evidence is retrieved after `max_retries = 2`, qualifies the response with explicit uncertainty warnings or principled abstention.

---

## 5. Evaluation Metrics & Scoring Rubric
1. **Answer Correctness (Exact Match / Token F1 / Semantic Overlap):**
   - Assesses whether the key threat label, technique ID, or recommended action matches the ground-truth rubric.
2. **Faithfulness Score (RAGAs formulation):**
   $$\text{Faithfulness} = \frac{|\text{Claims supported by retrieved context}|}{|\text{Total generated claims}|}$$
3. **Citation Precision:**
   $$\text{Citation Precision} = \frac{|\text{Valid bracketed references citing actual retrieved chunks}|}{|\text{Total generated citations}|}$$
4. **Efficiency Metrics:**
   - Response Latency (seconds per query).
   - Token Consumption (prompt + completion tokens).
   - Estimated API Cost ($USD).
