# ThreatRAG: Official AI506 Live Demonstration Script
**Course:** AI506 — Multi-Agent Retrieval-Augmented Generation Systems  
**Session Duration:** 20–30 Minutes (Presentation: 8–10 min | Live Demo: 7–10 min | Viva: 5–10 min)  
**Presenter / Student:** Ahsan Habib Sitab  
**Live URL:** `http://localhost:8501`  

---

## ⏱️ Live Demonstration Timeline (Target: 7–10 Minutes)

### Stage 1: Knowledge Base Provenance & Architecture (Minute 0:00 – 1:30)
1. **Navigate to:** `System Overview` (`http://localhost:8501/Overview`).
2. **What to show the instructor:**
   - Active Knowledge Chunks: **1,074 chunks**.
   - MITRE ATT&CK Enterprise STIX 2.1: **718 techniques**.
   - CISA Known Exploited Vulnerabilities: **1,790 CVEs**.
   - Balanced Network Flows (CIC-IDS2017): **30,000 flows** (18k train, 6k calibration, 6k test).
3. **What to say:**
   > *"Good morning/afternoon, Professor. Before running a query, notice that ThreatRAG is grounded in authentic, public cybersecurity intelligence with verified SHA-256 manifests. We use persistent ChromaDB with `all-MiniLM-L6-v2` alongside a sparse BM25 index with an entity tokenizer that preserves CVE identifiers and ATT&CK IDs."*

---

### Stage 2: Primary Query & Multi-Agent Trace Panel (Minute 1:30 – 4:30)
1. **Navigate to:** `Calibrated Threat Analysis` (`http://localhost:8501/Threat_Analysis`).
2. **Select Preset:** *"DDoS Flood Alert (Port 80 HTTP Flood)"*.
3. **Click:** *"🚀 Run ThreatRAG Analysis Pipeline"*.
4. **What to show the instructor:**
   - **Verdict:** Threat Detected (`DDoS / Denial of Service`).
   - **Calibrated Probability:** `99.98%` (highlight that Platt scaling reduced calibration error from 0.0037 to 0.0005).
   - **Salient Flow Features:** Z-score impact showing anomalous packet rate (85k pkts/s) and small packet lengths (18.5 bytes).
   - **MITRE ATT&CK Technique:** Grounded tag `[T1498.001]`.
5. **Scroll Down to:** **Multi-Agent Execution Trace Panel (AI506 Live Trace)**:
   - Expand **Step 1 [Coordinator / Planner]:** Show task decomposition and specialist allocation.
   - Expand **Step 2 [Cybersecurity Retrieval Specialist]:** Show the candidate chunks retrieved and similarity scores.
   - Expand **Step 3 [Security Reasoning Specialist]:** Show epistemic separation between empirical facts and hypotheses.
   - Expand **Step 4 [Evidence Verification Specialist]:** Show citation audit and verification decision (`APPROVED`).
6. **What to say:**
   > *"Notice how the agents collaborate. Rather than a single monolithic prompt, the Coordinator decomposes the task, the Retrieval Specialist fetches grounded chunks, the Reasoning Specialist maps the ATT&CK technique, and the Verification Specialist audits the citations before the answer is emitted."*

---

### Stage 3: Defensive Response & Human-in-the-Loop Gate (Minute 4:30 – 6:00)
1. **Navigate to:** `Defensive Response Plan` (`http://localhost:8501/Defensive_Response`).
2. **Select Category:** *"DDoS / Volumetric Network Flood"*, Severity: *"Critical"*.
3. **Click:** *"📋 Generate Defensive Response Playbook"*.
4. **What to show the instructor:**
   - Step 1: Containment (Edge Rate Limiting & BGP Flowspec).
   - Step 2: Mitigation (Upstream Scrubbing).
   - Step 3: Recovery.
   - Grounded citations to CISA Advisories.
   - **The Human-in-the-Loop Security Authorization Gate:** Show the red warning box and the disabled mitigation button.
   - Check the box: *"I certify that I have reviewed the actions above and authorize execution"* -> Click *"✅ Enact Authorized Mitigation Policy"*.
5. **What to say:**
   > *"In cybersecurity, autonomous mitigation is dangerous because an AI error could disconnect an entire hospital or data center. ThreatRAG strictly enforces a Human-in-the-Loop authorization gate where playbooks are supervisory until an authenticated analyst signs off."*

---

### Stage 4: Genuine Failure / Insufficient-Evidence Handling (Minute 6:00 – 7:30)
1. **Navigate to:** `AI506 Baseline Comparison` (`http://localhost:8501/AI506_Baseline_Comparison`).
2. **Select Question:** `TID-014` (*"Anomalous quantum tachyon modulation detected across local Ethernet switch ports"*).
3. **Click:** *"⚡ Run Side-by-Side Comparison"*.
4. **What to show the instructor:**
   - **System A (Conventional Single-Agent RAG):** Hallucinates a plausible quantum security attack and recommends fictitious firewall rules.
   - **System B (Multi-Agent ThreatRAG):**
     - Retrieval Specialist returns low similarity scores (< 0.15).
     - Verification Specialist flags `INSUFFICIENT_EVIDENCE`.
     - Coordinator triggers 1 feedback loop retry, confirms lack of evidence, and emits an explicit **qualification / abstention**, warning the analyst that the query is ungrounded.
5. **What to say:**
   > *"This demonstrates our feedback loop and proper failure handling. When presented with out-of-domain nonsense, conventional RAG hallucinates, whereas our Verification Specialist catches the lack of evidence and forces the system to abstain."*

---

### Stage 5: Empirical Benchmark & Ablation Wrap-Up (Minute 7:30 – 9:00)
1. **Show the 50-Question Benchmark Table & Charts** on the same page.
2. **Key Metrics to Highlight:**
   - Passing Accuracy: **88.0% (ThreatRAG)** vs **72.0% (Conventional RAG)** (+16%).
   - Faithfulness: **0.95** vs **0.78**.
   - Citation Precision: **100.0%** vs **75.0%**.
   - Latency Trade-Off: **5.82s** vs **3.20s** (+2.6s latency for 4 collaborating agents).
   - Cost: **$0.00076** per query.
3. **Ablation Summary:**
   - Disabling Verification drops Faithfulness to 0.81.
   - Disabling Reasoning drops Accuracy to 74.0%.
4. **Handover to Viva:**
   > *"This concludes the live demonstration of ThreatRAG. I am now ready for your questions."*
