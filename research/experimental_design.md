# Experimental Design and Evaluation Protocol

## 1. Experimental Configurations
To isolate the individual and collective contributions of each component, we formulate six standardized experimental configurations:

- **E1 (Direct Generation / No Retrieval):** Pure LLM reasoning without document retrieval, testing parametric memory alone.
- **E2 (Standard Dense RAG):** Vanilla bi-encoder dense vector search (BGE / MiniLM embeddings) with top-5 retrieved passages.
- **E3 (Hybrid Dense + BM25 RAG):** Bi-encoder dense search merged with BM25Okapi lexical retrieval using Reciprocal Rank Fusion ($k=60$).
- **E4 (Hybrid RAG + Cross-Encoder Reranking):** E3 candidate pool expanded to top-20 candidates and reranked using a cross-encoder model to yield the top-5 contexts.
- **E5 (Proposed Adaptive Hybrid RAG):** Full tri-modal retrieval with dynamic query-intent classification routing (Dense + BM25 + Structured Event Matching) followed by cross-encoder reranking.
- **E6 (ThreatRAG with Calibrated Confidence):** E5 integrated with calibrated statistical classifiers (Platt / Isotonic) and strict citation-validation guardrails.

---

## 2. Benchmark Datasets and Partitions

### 2.1 Intrusion Detection Telemetry: CIC-IDS2017
- **Raw Source:** Canadian Institute for Cybersecurity (UNB).
- **Representative Subset:** 30,000 stratified flow records across Benign, DoS/DDoS, PortScan, Brute Force, and Botnet classes.
- **Splits:**
  - Training Partition: 60% (18,000 records)
  - Calibration Partition: 20% (6,000 records)
  - Holdout Test Partition: 20% (6,000 records)
- **Leakage Prevention:** Zero overlap across splits; group-aware sampling where flow clusters share identical IP-port quadruplets.

### 2.2 Cybersecurity Knowledge Repositories
- **MITRE ATT&CK Enterprise (v15 STIX 2.1):** 600+ normalized techniques, sub-techniques, tactics, and mitigations.
- **CISA KEV Catalog:** Actively exploited vulnerability entries, remediation timelines, and advisory recommendations.
- **Documented Historical Incident Corpus:** Real-world breach post-mortems and incident records with documented ATT&CK technique alignments.

---

## 3. Evaluation Metrics

### 3.1 Retrieval Metrics
- **Recall@1, Recall@5:** Proportion of relevant ground-truth passages retrieved in the top-1 and top-5 positions.
- **Precision@5:** Fraction of retrieved top-5 passages that are relevant.
- **Mean Reciprocal Rank (MRR):** Multiplicative inverse of the rank of the first relevant document.
- **Normalized Discounted Cumulative Gain (nDCG@5):** Position-weighted grading of retrieval relevance.

### 3.2 Classification & Calibration Metrics
- **Multi-Class Accuracy, Precision, Recall, Macro F1:** Traditional discriminative performance metrics.
- **False Positive Rate (FPR):** Critical in SOC environments to assess alert fatigue.
- **Expected Calibration Error (ECE):** Deviation between predicted confidence and empirical accuracy across 10 probability bins.
- **Brier Score (BS):** Mean squared error between predicted probabilities and one-hot true class indicators.

### 3.3 Generation & Factuality Metrics
- **Faithfulness Score (RAGAS):** Fraction of generated claims directly supported by retrieved source passages.
- **Citation Precision & Recall:** Proportion of cited statements that accurately map to the cited source chunk ID.
- **Unsupported Claim Rate:** Percentage of assertions lacking textual evidence in the retrieved context.

### 3.4 Operational & System Metrics
- **End-to-End Latency:** Wall-clock response time in seconds per incident triage query.
- **Token Consumption & API Cost:** Total prompt and completion tokens per analysis.
- **Task Completion & Abstention Accuracy:** Ability of agents to complete workflow goals or safely abstain when evidence is insufficient.

---

## 4. Component Ablation Protocol
To quantify the necessity of each architectural component, systematic ablation is executed:
1. Ablate BM25 (Dense-only).
2. Ablate Dense Retrieval (Sparse-only).
3. Ablate Structured Event Matching (Text-only).
4. Ablate Cross-Encoder Reranker (Direct RRF top-5).
5. Ablate Query Adaptive Routing (Fixed uniform weights).
6. Ablate Citation Verification Guardrail.
7. Ablate Probability Calibration (Raw classifier outputs).
