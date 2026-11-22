# Paper to Project Mapping: MAIN-RAG (ACL 2025) to ThreatRAG
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Project:** ThreatRAG: An Adaptive Hybrid RAG Framework for Explainable Threat Intelligence  
**Base Paper:** *MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation* (ACL 2025) [1]  
**Author:** Ahsan Habib Sitab  

---

## 1. Systematic Comparison Matrix

| Architectural Dimension | Base Paper: MAIN-RAG (ACL 2025) | Adapted & Implemented: ThreatRAG | Justification for Adaptation / Extension |
| :--- | :--- | :--- | :--- |
| **Domain** | Open-Domain Multi-hop QA (HotpotQA, 2Wiki) | Enterprise Cybersecurity & SOC Threat Intelligence | High-stakes operational environments where hallucination causes severe downtime. |
| **Agent Roles** | 1. Planner<br>2. Retriever<br>3. Passage Filter<br>4. Answer Verifier | 1. **Coordinator / Planner**<br>2. **Cybersecurity Retrieval Specialist**<br>3. **Security Reasoning Specialist**<br>4. **Evidence Verification Specialist** | Tailored to cybersecurity workflows: separating empirical network facts from adversary intent hypotheses. |
| **Retrieval Modality** | Dense-only text passage retrieval | **Tri-Modal Adaptive Hybrid Retrieval** (Dense `all-MiniLM-L6-v2` + BM25 Lexical + Structured NetFlow Telemetry) | Pure dense retrieval fails on exact CVE IDs (`CVE-2023-34362`) and ATT&CK codes (`T1059.001`); BM25 and structured flow matching are mandatory. |
| **Fusion & Reranking** | Top-k passage thresholding | **Reciprocal Rank Fusion (RRF, $k=60$)** + Cross-Encoder Reranker (`ms-marco-MiniLM-L-6-v2`) | Unifies heterogeneous score distributions across vector distances, BM25 scores, and numerical flow statistics without scale bias. |
| **Verification & Loop** | Filter checks passage relevance; triggers query re-write | **Evidence Verification Agent** checks bracketed citations, detects insufficient evidence, triggers feedback loop with `max_retries = 2` | Ensures zero fabricated citations; forces principled abstention when telemetry evidence is missing. |
| **Confidence & Certainty** | Verbalized token log-probabilities | **Post-Hoc Platt Scaling on LightGBM ($ECE = 0.0005$)** | Verbalized confidence is notoriously miscalibrated in LLMs; Platt scaling provides true empirical probability. |
| **Governance & Safety** | Standard automated generation | **Human-in-the-Loop Authorization Gate** + Prompt Injection Defense | Prevents autonomous malicious reconfigurations of production firewalls and drops adversarial override prompts. |

---

## 2. Detailed Breakdown of Conceptual Transfer

### 2.1 Ideas Adopted Directly
1. **Decoupled Verification from Generation:** In single-agent RAG, the generator evaluates its own retrieved context, compounding hallucination. ThreatRAG adopts MAIN-RAG's core principle of dedicating a separate specialist agent solely to fact-checking and citation auditing.
2. **Iterative Verification-Driven Feedback Loop:** When the Verification Specialist flags that retrieved passages fail to support a claim or that evidence is insufficient, control loops back to the Retrieval Specialist with an augmented query rather than outputting an unsupported guess.
3. **Multi-Agent State Sharing:** A shared workflow state object (`ThreatRAGState`) tracks agent decisions, intermediate passages, verification scores, and token overhead.

### 2.2 Ideas Adapted for Cybersecurity
1. **Security-Aware Passage Filtering:** Instead of generic semantic relevance, the Retrieval and Reasoning agents filter passages based on explicit cybersecurity taxonomies (MITRE ATT&CK Enterprise Matrix v14.1 and CISA KEV).
2. **Epistemic Evidence Separation:** Adapted the synthesis step to enforce a strict dichotomy:
   - **Empirical Evidence:** Directly observed NetFlow metrics, packet rates, and destination ports.
   - **Hypotheses:** Inferred adversary objectives, threat actors, and recommended mitigations.
3. **Structured Citation Verification:** Adapted MAIN-RAG's verification checks to require verifiable bracketed chunk provenance tags (e.g., `[T1498]`, `[CISA-KEV-2023]`), calculating explicit Faithfulness and Citation Precision scores.

### 2.3 Ideas Extended Beyond MAIN-RAG
1. **Adaptive Hybrid Tri-Modal Retrieval ($E_5$):** MAIN-RAG relies exclusively on single-modal dense retrieval. ThreatRAG extends this to fuse dense vectors, sparse lexical BM25, and structured telemetry matching via RRF ($k=60$), dynamically boosting BM25 when alphanumeric identifiers (CVEs, ATT&CK codes) are detected in the query.
2. **Post-Hoc Confidence Calibration (RQ3):** MAIN-RAG does not address probabilistic calibration. ThreatRAG introduces parametric Platt Scaling over gradient-boosted trees (LightGBM), reducing Expected Calibration Error from $0.0037$ to $0.0005$ on 6,000 held-out flows.
3. **Human-in-the-Loop Defensive Governance:** Automated RAG systems in cybersecurity cannot be permitted to execute active countermeasures autonomously. ThreatRAG adds a mandatory human authorization gate for all containment playbooks.

### 2.4 Ideas Not Implemented & Justification
1. **Unconstrained Multi-Turn Query Rewriting:** MAIN-RAG permits arbitrary open-ended re-querying loops. ThreatRAG caps the feedback loop to a maximum of 2 iterations (`max_retries = 2`) to ensure strict response latency SLAs (< 10 seconds) required for real-time SOC operations.
2. **End-to-End LLM Fine-Tuning:** ThreatRAG utilizes off-the-shelf sentence transformers and calibrated tree ensembles rather than fine-tuning a massive 70B parameter LLM, ensuring the entire framework runs locally and economically on CPU hardware.
