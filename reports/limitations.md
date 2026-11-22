# Threats to Validity and System Limitations of ThreatRAG

## 1. Overview
In accordance with academic rigor for MSc-level AI research, this document critically examines the threats to validity, empirical limitations, and operational boundaries of the ThreatRAG framework. We distinguish measured empirical findings from open research challenges.

---

## 2. Threats to Validity

### 2.1 Internal Validity
- **Information Leakage Prevention:** High-frequency network flow datasets often contain duplicated or highly correlated flow records across short time horizons. Splitting raw PCAP flows randomly can allow identical session pairs to leak between train and test splits, artificially inflating classification scores. ThreatRAG strictly enforces duplicate removal and group-aware stratified sampling.
- **Calibration Split Independence:** Model calibration parameters (Platt Scaling sigmoid coefficients and Isotonic regression step functions) were strictly fitted on a holdout 20% validation partition (`val_flows.csv`), completely isolated from the final 20% test partition (`test_flows.csv`).
- **Citation Verification Sensitivity:** The automated citation auditor uses regex-based chunk identifier extraction paired with lexical overlap thresholds. While this guarantees that generated claims match retrieved context words, it relies on heuristic semantic boundaries rather than full formal theorem-proving entailment.

### 2.2 External Validity
- **Telemetry Diversity:** The quantitative intrusion detection experiments are conducted on the widely benchmarked CIC-IDS2017 dataset. While CIC-IDS2017 reflects realistic benign and attack behaviors (DoS, DDoS, PortScan, BruteForce), synthetic testbed artifacts (such as predictable background traffic patterns) may not fully reflect messy production enterprise networks with proprietary middleboxes and VPN encapsulations.
- **Adversary Behavior Drift:** Cyber threat actors frequently alter their tactics, techniques, and procedures (TTPs) to evade signature detection. While ThreatRAG's updatable knowledge base mitigates temporal drift by ingesting daily CISA KEV feeds and MITRE ATT&CK updates, zero-day attacks with completely novel execution primitives may lack matching reference chunks.

### 2.3 Construct Validity
- **Retrieval Evaluation Queries:** Benchmark queries represent canonical cybersecurity investigation scenarios (Log4Shell, SolarWinds, DarkSide, WannaCry, MOVEit, LSASS dumping). While ground truth is mapped to official CISA advisory and ATT&CK technique IDs, real SOC tier-1 analyst tickets often feature ambiguous, truncated, or obfuscated user reports.
- **Faithfulness Metric:** RAGAS Faithfulness measures the proportion of claims supported by context. High faithfulness demonstrates that the generation is grounded in retrieved text, but it does not guarantee that the retrieved document itself is infallible truth.

---

## 3. System and Architectural Limitations

1. **Computational Constraints on Cross-Encoder Reranking:**
   While bi-encoder dense embeddings (all-MiniLM-L6-v2) and BM25 sparse retrieval execute in under 15 milliseconds, cross-encoder neural rerankers evaluate full self-attention across all query-candidate token pairs. For very large candidate pools ($K > 100$), reranking latency scales linearly and requires GPU acceleration for sub-second SLAs.
2. **Deterministic Governance and Defensive Boundary:**
   ThreatRAG strictly prohibits autonomous execution of active network disruptions (e.g., automated BGP route withdrawal or endpoint host isolation). While this prevents catastrophic self-inflicted denial-of-service, it introduces a human latency dependency during critical incidents.
3. **Absence of Native Multimodal PCAP Payload Inspection:**
   The current framework ingests structured statistical flow metrics (durations, packet counts, inter-arrival times, ports) and unstructured text reports. It does not parse raw application-layer PCAP binary byte streams directly within the neural embedding space.

---

## 4. Suggested Next Research Directions
1. **Hierarchical Graph RAG:** Integrate graph neural networks over knowledge graphs (e.g., AttacKG / ThreatKG) to navigate multi-hop adversary attack graphs directly during retrieval.
2. **Streaming Continuous Calibration:** Implement windowed adaptive calibration buffers that update temperature scaling dynamically as enterprise network traffic distributions shift over seasonal business cycles.
3. **Edge-Optimized Distillation:** Distill the cross-encoder reranker into a lightweight ColBERT-style late-interaction architecture to achieve sub-millisecond reranking on resource-constrained SOC edge nodes.
