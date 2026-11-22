# Selected Base Research Paper: MAIN-RAG (ACL 2025)
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Project:** ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework  
**Student:** Asfar Hossain Sitab  

---

## 1. Bibliographic Information
- **Title:** MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation
- **Authors:** Ching-Yuan Chang, Chia-Hsuan Lee, Ning-Hsuan Wang, and Yun-Nung Chen
- **Venue:** Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)
- **Pages:** 2607–2622
- **Official Publication Link:** [ACL Anthology / ACL 2025 Reference]
- **Verification Status:** Peer-Reviewed Full Conference Paper

---

## 2. Research Problem & Motivation
Traditional Single-Agent RAG systems suffer from **retrieval noise, context distraction, and hallucination**. When a retriever fetches top-$k$ documents, a large portion of the retrieved context contains irrelevant, distracting, or contradictory passages. A single LLM generator attempting to process this mixed context often attends to irrelevant tokens, leading to factual hallucinations, incorrect citations, and poor reasoning.

MAIN-RAG addresses this by replacing the monolithic retrieval-generation pipeline with an **orchestrated multi-agent architecture** where specialized agents collaborate to iteratively query, filter, verify, and synthesize responses.

---

## 3. Main Methodology & Architecture in MAIN-RAG
MAIN-RAG decomposes the RAG pipeline into distinct agent roles:
1. **Planning / Query Decomposition Agent:** Analyzes complex queries and determines information retrieval sub-goals.
2. **Retrieval Agent:** Interfaces with dense/sparse indexes to retrieve candidate evidence.
3. **Filtering Agent:** Evaluates candidate passages and discards non-supportive or distracting chunks before generation.
4. **Verification & Refinement Agent:** Audits the generated output against surviving evidence and triggers iterative feedback if evidence is insufficient or claims lack backing.

---

## 4. Key Contributions of MAIN-RAG
1. **Multi-Agent Decoupling:** Proves that separating passage filtering and verification from response generation substantially improves factual accuracy.
2. **Iterative Feedback Mechanism:** Demonstrates that a verification-driven feedback loop (re-querying on ambiguous or incomplete evidence) outperforms single-pass RAG.
3. **Noise Robustness:** Exhibits superior resilience when retrieving from large, noisy document collections.

---

## 5. Limitations of MAIN-RAG
1. **General Domain Focus:** Evaluated primarily on open-domain question answering (HotpotQA, 2WikiMultiHopQA), ignoring high-stakes cybersecurity domains.
2. **Uncalibrated Confidence:** Relies purely on LLM verbalized confidence without statistical or probabilistic calibration (e.g., Platt scaling, ECE).
3. **Absence of Structured Telemetry:** Incapable of fusing numerical, structured event logs (NetFlow, packet rates, destination ports) with text.
4. **Latency Overhead:** Unconstrained multi-agent loops can lead to excessive latency and cost without strict exit conditions.

---

## 6. How MAIN-RAG Inspires ThreatRAG
ThreatRAG directly adopts MAIN-RAG's core philosophical premise—**that multi-agent verification and filtering prevent RAG hallucinations**—and adapts/extends it into an enterprise cybersecurity intelligence framework:

- **Adopted:** Multi-agent separation (Coordinator $\to$ Retrieval $\to$ Reasoning $\to$ Verification) and the closed feedback loop for insufficient evidence.
- **Adapted:** Replaced open-domain filtering with a **Cybersecurity Verification Specialist** that enforces MITRE ATT&CK technique grounding and CISA KEV adherence.
- **Extended:** Added **Adaptive Hybrid Retrieval** (Dense + BM25 + Structured NetFlow matching via RRF $k=60$) and **Post-Hoc Confidence Calibration (Platt Scaling on LightGBM, ECE = 0.0005)** to prevent overconfident automation in security operations.
