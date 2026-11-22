# Comprehensive Literature Review: RAG and Explainable AI for Cybersecurity Threat Intelligence

## Abstract
This literature review synthesizes 22 peer-reviewed and top-venue research contributions (2009–2026, predominantly 2022–2026) across 10 core dimensions: Retrieval-Augmented Generation (RAG) for cybersecurity, hybrid sparse-dense retrieval, agentic multi-stage reasoning, threat intelligence knowledge graphs, explainable intrusion detection (XAI), incident similarity search, confidence calibration, MITRE ATT&CK taxonomy grounding, hallucination mitigation, and retrieval-grounded incident response recommendations. We critically evaluate current state-of-the-art frameworks (including TechniqueRAG, H-TechniqueRAG, and CyberRAG) and establish the theoretical foundations for **ThreatRAG**.

---

## 1. Introduction and Scope
Modern Security Operations Centers (SOCs) face an asymmetric threat landscape characterized by escalating attack volumes, polymorphic threat behaviors, and severe alert fatigue. While Machine Learning (ML) and Deep Learning (DL) Intrusion Detection Systems (IDS) achieve high nominal detection rates, their operational utility is severely hindered by three fundamental challenges:
1. **The "Black-Box" Opacity Problem:** High-accuracy classifiers do not explain *why* an event was flagged or *how* it maps to standard adversary behaviors.
2. **LLM Hallucination and Temporal Cutoffs:** Off-the-shelf Large Language Models hallucinate plausible-sounding security rationales, lack access to proprietary enterprise telemetry, and miss recent zero-day Common Vulnerabilities and Exposures (CVEs).
3. **Miscalibrated Confidence:** Overparameterized neural models and uncalibrated tree ensembles frequently output extreme, overconfident probabilities that fail to reflect actual empirical event risks.

---

## 2. Dimensional Analysis across 10 Research Areas

### 2.1 Retrieval-Augmented Generation for Cybersecurity
Standard RAG frameworks (Gao et al., 2024) augment prompt contexts with retrieved documents to ground generative responses. In cybersecurity, early efforts integrated text embeddings of MITRE ATT&CK with commercial LLMs. However, generic RAG architectures suffer from semantic mismatch when processing security tokens (e.g., CVE-2023-34362, T1059.001, PowerShell flags). Lekssays et al. (2025) introduced *TechniqueRAG*, demonstrating that domain-specific retrieval-augmented pipelines outperform generic LLMs in annotating adversarial techniques.

### 2.2 Hybrid Sparse-Dense Retrieval
Dense semantic retrieval (Karpukhin et al., 2020) maps user queries into latent continuous spaces using bi-encoders (e.g., BGE, MiniLM), excelling at conceptual and thematic paraphrasing. However, dense vectors struggle with exact technical tokens, hash values, and specific rule identifiers. Sparse lexical retrieval, particularly BM25 (Robertson & Zaragoza, 2009), guarantees exact token matching. Cormack et al. (2009) established that Reciprocal Rank Fusion (RRF) combines diverse retrieval ranked lists without requiring hyperparameter tuning, providing mathematical stability across disparate scoring scales:
$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
where $k \approx 60$ and $r_m(d)$ is the rank of document $d$ in system $m$.

### 2.3 Agentic RAG and Stateful Orchestration
Traditional single-pass RAG queries a vector store once and produces a terminal response. In complex threat investigations, single-pass generation fails when initial queries are ambiguous or telemetry is noisy. Smith et al. (2025) proposed *CyberRAG*, demonstrating that an agentic loop coordinating specialized sub-agents (classifier, retriever, reasoner, reviewer) dramatically improves analytical precision and reduces false alarms in SOC reporting. Stateful graphs (LangGraph) allow cyclic self-correction, iterative retrieval refinement, and explicit human-in-the-loop (HITL) checkpoints.

### 2.4 Threat Intelligence Knowledge Graphs and Structured Context
Unstructured CTI reports contain rich relational semantics. Wang et al. (2022) with *AttacKG* and Niu et al. (2023) with *ThreatKG* showed that extracting technique knowledge graphs enables path-based adversary behavior reconstruction. Combining graph/structured attributes with vector embeddings enriches situational awareness beyond pure text snippets.

### 2.5 Explainable Intrusion Detection (XAI)
To establish analyst trust, models must expose feature attributions. Lundberg & Lee (2017) formulated SHAP (SHapley Additive exPlanations), proving axiomatic consistency rooted in cooperative game theory. Ribeiro et al. (2016) developed LIME for fast local surrogate modeling. In network flow datasets like CIC-IDS2017 (Sharafaldin et al., 2018), SHAP demonstrates that flow duration, packet inter-arrival variance, and TCP window flags serve as primary discriminators for volumetric and denial-of-service anomalies.

### 2.6 Security Incident Similarity Retrieval
Historical incident triage requires measuring similarity across multi-modal attributes: structured flow statistics, categorical protocols, and textual incident summaries. Relying solely on IP address equality fails due to dynamic DHCP addressing and transient proxy/VPN hops. Hybrid matching combining normalized continuous flow metrics with text-based incident embeddings yields robust nearest-neighbor retrieval.

### 2.7 Confidence Calibration for LLM and ML Analysis
Guo et al. (2017) demonstrated that modern machine learning models exhibit severe miscalibration despite high accuracy. In intrusion detection, an overconfident false alarm wastes tier-1 analyst time, while an uncalibrated low-confidence alert leads to missed breaches. Post-hoc calibration methods—notably Platt Scaling (logistic sigmoid regression; Platt, 1999) and Isotonic Regression (pair-adjacent violators algorithm; Zadrozny & Elkan, 2002)—align predicted probabilities with empirical frequencies, quantified via Expected Calibration Error (ECE) and Brier Score:
$$ECE = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$$
$$BS = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$

### 2.8 MITRE ATT&CK Grounded Reasoning
Mapping alerts to MITRE ATT&CK provides a standardized adversary vocabulary. Lekssays et al. (2026) introduced *H-TechniqueRAG*, employing a two-stage hierarchical retrieval that identifies high-level tactics before searching nested sub-techniques, reducing candidate search space by over 60% and mitigating context window dilution.

### 2.9 Evidence Verification and Hallucination Reduction
Hallucinations in cybersecurity recommendations can result in service disruption or severe operational missteps. Self-RAG (Asai et al., 2024) and CRAG (Yan et al., 2024) introduce self-reflection and corrective evaluation to check whether generated claims are strictly entailed by retrieved passages. Automated evaluation frameworks such as RAGAS (Es et al., 2024) formalize Faithfulness (proportion of generated claims supported by context) and Context Precision.

### 2.10 Retrieval-Grounded Incident Response Recommendations
Actionable defensive guidance must be grounded in verified repositories such as CISA Known Exploited Vulnerabilities (KEV) and NIST SP 800-61r2. Incident response advisors must balance containment efficacy against operational disruption and strictly prohibit autonomous execution of privileged system changes without human verification.

---

## 3. Comparative Literature Summary Matrix
See `research/literature_matrix.csv` for the complete tabular mapping across all 22 analyzed contributions.
