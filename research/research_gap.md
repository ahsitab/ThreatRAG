# Research Gap and Contributions of ThreatRAG

## 1. Problem Statement
Contemporary cybersecurity operations rely heavily on automated intrusion detection systems and threat intelligence platforms. However, existing methodologies exhibit critical operational disconnects:
1. **Isolated Modalities:** Machine learning intrusion detectors output raw label predictions or probabilities without textual context or actionable response playbooks. Conversely, conversational LLMs and pure RAG chatbots answer user queries without direct grounding in network-flow telemetry or calibrated statistical classifiers.
2. **Retrieval Blindspots in Security:** Dense-only retrieval frequently misses exact indicator matches (CVE IDs, ATT&CK codes, specific IP/port strings), while sparse-only retrieval fails on natural language conceptual descriptions.
3. **Absence of Calibrated Reliability:** Security analysts cannot distinguish between high-confidence model detections and low-confidence statistical guesses because standard models produce uncalibrated probabilities, and LLMs hallucinate unjustified certainty.
4. **Lack of Evidence Provenance:** Generated threat summaries frequently hallucinate attack vectors or cite non-existent documentation, lacking rigorous sentence-level citation verification.

---

## 2. Identified Research Gap
While recent works have investigated individual facets—such as *TechniqueRAG* (CTI-to-ATT&CK mapping via dense RAG), *CyberRAG* (agentic workflow for attack reporting), and post-hoc calibration on intrusion datasets—**no published framework unifies adaptive hybrid retrieval (dense semantic + sparse BM25 + structured telemetry matching), cross-encoder evidence reranking, post-hoc confidence calibration, and multi-agent defensive recommendation into an end-to-end explainable system.**

ThreatRAG directly addresses this empirical and methodological gap.

---

## 3. Research Questions & Hypotheses

### Research Questions
- **RQ1 (Retrieval Effectiveness):** Does adaptive hybrid retrieval (combining dense semantic search, BM25 lexical search, and structured event matching) achieve higher retrieval accuracy (Recall@5, nDCG@5, MRR) for cybersecurity queries compared with standard dense-only retrieval?
- **RQ2 (Factual Grounding & Citation Quality):** Does cross-encoder evidence reranking and claim-level verification significantly reduce hallucination rates and increase citation accuracy in generated threat explanations?
- **RQ3 (Confidence Calibration & Reliability):** Does post-hoc probability calibration (Platt scaling and Isotonic regression) significantly lower the Expected Calibration Error (ECE) and Brier score of network threat classification without degrading discriminative capability?
- **RQ4 (Multi-Agent Utility & Efficiency):** Can a specialized 4-agent architecture (Threat Identifier, Historical Search, Evidence Explainer, Response Advisor) deliver coherent, actionable defensive recommendations within acceptable operational latency and token costs?

### Research Hypotheses
- **$H_1$:** Adaptive hybrid retrieval will achieve a statistically significant improvement in Recall@5 and nDCG@5 ($p < 0.05$) over dense-only baseline retrieval on mixed cybersecurity queries.
- **$H_2$:** Integrating a cross-encoder reranker prior to context assembly will increase RAGAS Faithfulness and citation precision by at least 15% relative to unranked retrieval.
- **$H_3$:** Platt scaling and Isotonic regression will reduce Expected Calibration Error (ECE) by at least 50% on holdout network flow validation sets compared to uncalibrated classifier outputs.
- **$H_4$:** Task-specialized agent modularity maintains human review compliance and limits unsupported claim rate to under 5% under ambiguous or out-of-distribution inputs.

---

## 4. Key Contributions of ThreatRAG
1. **Adaptive Tri-Modal Hybrid Retrieval Engine:** An adaptive retrieval pipeline that dynamically weights Dense Semantic Search, BM25 Lexical Search, and Structured Security Event Matching based on query intent and input telemetry.
2. **Evidence-Grounded Cross-Encoder Reranking & Provenance Validator:** A verification layer that filters low-relevance noise, ranks factual snippets, and validates claim-to-chunk provenance before LLM synthesis.
3. **Calibrated Machine Learning Threat Triage:** Trained lightweight classifiers on realistic network flows (CIC-IDS2017) coupled with post-hoc Platt and Isotonic calibration to provide trustworthy confidence scores.
4. **Four-Pillar LangGraph Agent Ecosystem:** A modular multi-agent workflow implementing:
   - *Agent 1: Threat Identification* (telemetry classification + calibrated uncertainty + feature attribution).
   - *Agent 2: Historical Incident Similarity* (hybrid multi-attribute incident retrieval).
   - *Agent 3: Evidence-Based Threat Explanation* (ATT&CK technique grounding + strict claim citation).
   - *Agent 4: Defensive Response Advisor* (prioritized mitigation checklist + mandatory human approval boundary).
5. **Reproducible Benchmark and Open Architecture:** Full automated test suite, FastAPI service, and interactive Streamlit research dashboard.
