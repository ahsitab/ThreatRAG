# ThreatRAG: Technical Viva & Inspection Preparation Guide
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Context:** MSc Midterm Viva & Project Inspection (20 Marks)  
**Student / Researcher:** Ahsan Habib Sitab  

---

## 🎯 13 Core Technical Questions & Authoritative Answers

### Q1: Why use a Multi-Agent architecture instead of a single LLM prompt?
**Answer:**  
In a single-agent RAG system, one prompt must simultaneously evaluate relevance, extract entities, reason over attacker intent, and self-check its output. This leads to **cognitive overload, context distraction, and confirmation bias** where the generator uncritically accepts its own hallucinations. By decomposing the workflow into four specialized agents (Coordinator, Retrieval Specialist, Reasoning Specialist, and Verification Specialist), each agent performs a focused task with distinct validation criteria. Most importantly, it enables an **iterative verification feedback loop** where an independent verification specialist can reject ungrounded claims and request targeted re-retrieval.

---

### Q2: Why is each of your four agents necessary?
**Answer:**  
1. **Coordinator / Planner:** Parses incoming security queries and telemetry, selects required specialists, manages shared state (`ThreatRAGState`), and caps feedback retries to prevent unbounded loops.
2. **Cybersecurity Retrieval Specialist:** Interfaces with both persistent ChromaDB (dense vectors) and BM25 (sparse lexical), performing query expansion when the verification agent requests additional evidence.
3. **Security Reasoning Specialist:** Bridges numerical ML anomaly detection with textual threat intelligence. It runs the calibrated LightGBM model, extracts salient flow z-scores, maps MITRE ATT&CK techniques, and separates empirical facts from hypotheses.
4. **Evidence Verification Specialist:** Acts as an impartial auditor. It checks every claim against retrieved passages, audits bracketed citations, computes faithfulness, and triggers re-retrieval if evidence is insufficient.

---

### Q3: What is RAG and how does hybrid retrieval work in ThreatRAG?
**Answer:**  
Retrieval-Augmented Generation (RAG) grounds language models in an external, verifiable knowledge corpus rather than relying on static parametric memory. In ThreatRAG, we implement **Tri-Modal Adaptive Hybrid Retrieval ($E_5$)**:
- **Dense Semantic Retrieval:** Encodes semantic meaning via `all-MiniLM-L6-v2` in ChromaDB (cosine distance).
- **Sparse Lexical Retrieval:** `BM25Okapi` with a security-aware tokenizer that preserves alphanumeric punctuation (e.g. `CVE-2023-34362`, `T1498.001`).
- **Structured Event Matching:** Statistical matching on network telemetry (destination ports, packet rates, duration).
- **Reciprocal Rank Fusion (RRF):** Fuses rankings across retrievers without score distortion using:
  $$RRF(d) = \sum_{m \in M} \frac{w_m}{k + r_m(d)} \quad (k=60)$$
- **Cross-Encoder Reranker:** Re-scores top candidates with `cross-encoder/ms-marco-MiniLM-L-6-v2` to eliminate irrelevant context.

---

### Q4: Why can't you just use dense semantic embeddings alone?
**Answer:**  
Dense embeddings map text to continuous vector spaces based on semantic similarity, but they struggle with **exact alphanumeric identifiers** common in cybersecurity (e.g., distinguishing `CVE-2023-34362` from `CVE-2023-34363`, or finding specific technique `T1059.001`). BM25 lexical search excels at exact keyword and identifier matching. Our empirical retrieval experiments proved that adding BM25 and cross-encoder reranking boosted **nDCG@5 from 0.5933 to 0.7243** (+22.1% improvement).

---

### Q5: How do the agents communicate and transfer state?
**Answer:**  
Agents communicate synchronously through a strongly typed state dictionary (`ThreatRAGState`). The Coordinator initializes the state with the user query and telemetry, passes control to the Retrieval Specialist, routes evidence to the Reasoning Specialist, and forwards the generated output to the Verification Specialist. If the Verification Specialist flags insufficient evidence, it passes a structured `re_retrieval_guidance` context back to the Coordinator, which commands the Retrieval Specialist to expand query keywords.

---

### Q6: What happens when the evidence in the knowledge corpus is insufficient?
**Answer:**  
Unlike single-agent RAG, which hallucinates plausible-sounding explanations, ThreatRAG implements **principled abstention**:
1. When retrieved passages have low similarity (< 0.20) or query entities are out-of-domain (e.g., our test query `TID-014` on "quantum tachyon modulation"), the Verification Specialist returns decision `INSUFFICIENT_EVIDENCE`.
2. The Coordinator executes a re-retrieval feedback loop with expanded synonyms.
3. If the evidence remains unsupported after `max_retries = 2`, the Coordinator emits an explicit **qualification and uncertainty warning** stating that the claim cannot be substantiated by authenticated cybersecurity intelligence.

---

### Q7: How are citations verified and hallucinations prevented?
**Answer:**  
The `CitationValidator` scans the generated response for bracketed citation tags (e.g., `[mitre-T1498.001]`). It cross-checks each cited tag against the list of actual chunk IDs retrieved in the current session. If an agent cites a nonexistent chunk, the Citation Precision drops, the unsupported claim rate increases, and the Verification Specialist rejects the response. In our benchmark on 50 questions, Multi-Agent ThreatRAG achieved **100.0% Citation Precision**.

---

### Q8: How was the baseline comparison designed to be fair?
**Answer:**  
As required by AI506 Section 7, the Conventional Single-Agent RAG baseline:
- Uses the **exact same knowledge corpus** (1,074 chunks in persistent ChromaDB).
- Uses the **exact same embedding model** (`all-MiniLM-L6-v2`, 384 dimensions).
- Uses the **exact same retrieval budget** ($k = 5$ candidate passages).
- Evaluates on the **exact same 50 benchmark questions**.
- Runs in the identical hardware and OS environment.
The only isolated variables are the multi-agent task planning, hybrid fusion, cross-encoder reranking, confidence calibration, and iterative verification feedback loop.

---

### Q9: What metrics did you measure and what were the results?
**Answer:**  
We measured:
1. **Answer Correctness:** Multi-Agent ThreatRAG achieved **88.0% passing accuracy** (44/50) vs. **72.0%** (36/50) for the baseline (+16.0% gain).
2. **Faithfulness Score (RAGAs):** **0.95** for ThreatRAG vs. **0.78** for the baseline (+21.8% gain).
3. **Citation Precision:** **100.0%** for ThreatRAG vs. **75.0%** for the baseline.
4. **Efficiency (Latency):** **5.82s** for ThreatRAG vs. **3.20s** for the baseline (+2.62s overhead for 4 agents).
5. **Token Cost:** **3,119 tokens ($0.00076)** vs. **1,200 tokens ($0.00028)**.

---

### Q10: What is Post-Hoc Confidence Calibration and why did you use Platt Scaling?
**Answer:**  
Standard machine learning models (like raw LightGBM or Random Forests) produce scores that reflect decision margins, not true probabilities. In high-stakes SOC environments, an uncalibrated 0.99 score might actually only be accurate 80% of the time. We applied **Platt Scaling**—fitting a logistic sigmoid $P(Y=1|z) = 1 / (1 + \exp(-(Az + B)))$ on an independent 6,000-flow calibration set. This reduced the **Expected Calibration Error (ECE) from 0.0037 down to 0.0005** (an **86.5% error reduction**) while maintaining 99.98% accuracy and zero false positives.

---

### Q11: Which published paper inspired your project and what was adopted vs. adapted?
**Answer:**  
Our project was inspired by **MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation (ACL 2025)** by C.-Y. Chang et al. [1]:
- **Adopted:** Decoupled verification agent role and the iterative feedback loop for missing evidence.
- **Adapted:** Replaced open-domain filtering with a Cybersecurity Verification Specialist grounded in MITRE ATT&CK and CISA KEV taxonomies; enforced epistemic separation between empirical facts and hypotheses.
- **Extended:** Added Tri-Modal Hybrid Retrieval (Dense + BM25 + Structured NetFlow) and Post-Hoc Platt Confidence Calibration ($ECE = 0.0005$), as well as a Human-in-the-Loop defensive gate.

---

### Q12: Why do you enforce Human-in-the-Loop authorization?
**Answer:**  
In cybersecurity incident response, automated remediation carries enormous operational risk. If an autonomous AI mistakenly blocks a core database port or issues a BGP null-route during a false positive, it could halt hospital operations or corporate banking services. ThreatRAG adheres strictly to a supervisory defensive posture: playbooks provide prioritized recommendations, but execution requires authenticated human analyst authorization.

---

### Q13: What are the project's honest limitations and threats to validity?
**Answer:**  
1. **Network Flow Evaluation:** Currently evaluated on Friday DDoS and benign flows from CIC-IDS2017; expanding to advanced persistent threats (APTs) spanning multiple weeks is ongoing work.
2. **Latency Trade-Off:** Multi-agent deliberation adds 2.62 seconds of latency compared to single-agent RAG.
3. **Lexical Tokenization Sensitivity:** BM25 matching relies on security tokenizers preserving dots and hyphens in CVEs and ATT&CK codes; malformed OCR logs can degrade sparse retrieval.
