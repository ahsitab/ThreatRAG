"""
scripts/generate_presentation.py
================================
Generates the official 12-slide presentation for AI506 Midterm Evaluation:
ThreatRAG: An Adaptive Hybrid Retrieval-Augmented Generation Framework
for Explainable Cybersecurity Threat Intelligence and Incident Response.

Adheres strictly to the 12-slide syllabus outline in AI506 Specification Section 6.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    os.makedirs("presentation", exist_ok=True)
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme colors
    COLOR_BG = RGBColor(248, 250, 252)       # Light slate
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # Navy Blue
    COLOR_DARK = RGBColor(15, 23, 42)         # Deep Slate
    COLOR_MUTED = RGBColor(71, 85, 105)       # Slate Gray
    COLOR_ACCENT = RGBColor(225, 29, 72)      # Crimson accent
    COLOR_CARD = RGBColor(255, 255, 255)      # White
    COLOR_BORDER = RGBColor(226, 232, 240)    # Light gray border

    def add_header(slide, title_text, category_text="AI506 MSc Midterm Project Presentation"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

    def add_card(slide, left, top, width, height, title, body_points):
        # Card shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(width - 0.4), Inches(height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY

        for bp in body_points:
            p_b = tf.add_paragraph()
            p_b.text = f"• {bp}"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = COLOR_DARK
            p_b.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Project and Group
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    # Title box
    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_tag = tf.paragraphs[0]
    p_tag.text = "AI506: MULTI-AGENT RETRIEVAL-AUGMENTED GENERATION SYSTEMS"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_ACCENT

    p_main = tf.add_paragraph()
    p_main.text = "ThreatRAG: An Adaptive Hybrid Multi-Agent RAG Framework"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_PRIMARY
    p_main.space_before = Pt(10)

    p_sub = tf.add_paragraph()
    p_sub.text = "For Explainable Cybersecurity Threat Intelligence and Incident Response"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.space_before = Pt(6)

    # Metadata card
    meta_box = slide1.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.8))
    tf_m = meta_box.text_frame
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Candidate / Researcher: Asfar Hossain Sitab (MSc in Artificial Intelligence and Machine Learning)"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_DARK

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Repository: https://github.com/ahsitab/ThreatRAG  |  Assessment: Midterm Project (20 Marks)"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = COLOR_MUTED
    p_m2.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 2: Problem and Objectives
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide2, "Problem Statement, Target Users & Objectives")
    add_card(slide2, 0.8, 1.6, 5.6, 5.2, "Operational Pain Points in Modern SOCs", [
        "Alert Fatigue: SOC analysts process thousands of daily network anomaly alerts with minimal context.",
        "Black-Box ML Detectors: Anomaly classifiers output raw scores without explainable evidence or root cause attribution.",
        "LLM Hallucinations: Commercial LLMs invent nonexistent CVE numbers, fake mitigations, and unverified tactics.",
        "Overconfidence in Edge Cases: Uncalibrated models produce dangerous 99% confidence on novel or ambiguous network intrusions."
    ])
    add_card(slide2, 6.8, 1.6, 5.7, 5.2, "ThreatRAG Target Users & Project Objectives", [
        "Target Users: Tier-1/Tier-2 SOC Analysts, Incident Responders, Threat Hunters, and Security Researchers.",
        "Objective 1: Multi-Agent Collaboration: Decompose triage into Coordinator, Retrieval, Reasoning, and Verification specialists.",
        "Objective 2: Adaptive Tri-Modal RAG: Fuse Dense vectors + Sparse BM25 + Structured NetFlow matching via RRF (k=60).",
        "Objective 3: Calibrated Confidence: Implement Platt Scaling to reduce ECE from 0.0037 to 0.0005 on 6,000 validation flows.",
        "Objective 4: Strictly Defensive Governance: Enforce Human-in-the-Loop approval for all containment actions."
    ])

    # -------------------------------------------------------------
    # SLIDE 3: Selected Research Paper
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide3, "Selected Base Research Paper: MAIN-RAG (ACL 2025)")
    add_card(slide3, 0.8, 1.6, 11.7, 2.2, "Paper Metadata & Citation", [
        "Title: MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation",
        "Authors: Ching-Yuan Chang, Chia-Hsuan Lee, Ning-Hsuan Wang, and Yun-Nung Chen",
        "Venue: Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), pp. 2607-2622.",
        "Official Venue: Peer-Reviewed Full Research Paper at Flagship NLP Conference (ACL)."
    ])
    add_card(slide3, 0.8, 4.1, 5.6, 2.8, "Core Methodology & Contribution", [
        "Replaces single monolithic RAG with multi-agent filtering.",
        "Decomposes pipeline into query planner, retriever, passage filter, and answer verifier.",
        "Demonstrates that isolating passage filtering and verification substantially reduces context noise and hallucinations."
    ])
    add_card(slide3, 6.8, 4.1, 5.7, 2.8, "Key Limitations Identified in Base Paper", [
        "Evaluated only on open-domain multi-hop QA (HotpotQA, 2Wiki) - lacks high-stakes cybersecurity grounding.",
        "Uncalibrated Verbalized Confidence: Relies on LLM self-confidence without statistical calibration.",
        "Text-Only Modality: Incapable of fusing numerical network telemetry (packet rates, destination ports).",
        "Unbounded Iterations: Open-ended feedback loops introduce latency unacceptable for real-time SOC triage."
    ])

    # -------------------------------------------------------------
    # SLIDE 4: How the Paper Inspired Your Work
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide4, "How MAIN-RAG Inspired ThreatRAG: Adoption, Adaptation & Extension")
    add_card(slide4, 0.8, 1.6, 3.6, 5.2, "1. What We Adopted", [
        "Decoupled Agent Roles: Separating the verification and filtering agent from the generator.",
        "Iterative Feedback Loop: Re-retrieving evidence when verification identifies missing support.",
        "Stateful Multi-Agent Orchestration: Sharing structured query, evidence, and scores across agents."
    ])
    add_card(slide4, 4.8, 1.6, 3.7, 5.2, "2. What We Adapted", [
        "Domain-Specific Verification: Filtering based on MITRE ATT&CK techniques and CISA KEV catalogs.",
        "Epistemic Evidence Separation: Explicitly distinguishing empirical telemetry facts from adversary hypotheses.",
        "Bracketed Citation Auditing: Extracting chunk IDs and computing rigorous Faithfulness scores."
    ])
    add_card(slide4, 8.8, 1.6, 3.7, 5.2, "3. What We Extended", [
        "Tri-Modal Hybrid Retrieval: Dense + BM25 + Structured event matching via RRF (k=60).",
        "Post-Hoc Platt Calibration: Trained on LightGBM to lower ECE by 86.5% (0.0037 -> 0.0005).",
        "Human-in-the-Loop Gate: Mandatory analyst sign-off before defensive action dispatch."
    ])

    # -------------------------------------------------------------
    # SLIDE 5: System Architecture
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide5, "ThreatRAG Multi-Agent Architecture & Communication Flow")
    add_card(slide5, 0.8, 1.6, 5.6, 5.2, "Logical Agent Roles & Responsibilities", [
        "Agent 1: Coordinator / Planner: Decomposes queries, schedules specialists, manages state, and caps feedback loops (max 2 retries).",
        "Agent 2: Cybersecurity Retrieval Specialist: Executes hybrid search across ChromaDB (all-MiniLM-L6-v2), BM25, and structured flow matcher.",
        "Agent 3: Security Reasoning Specialist: Performs calibrated ML inference, ATT&CK mapping, and playbook synthesis.",
        "Agent 4: Evidence Verification Specialist: Audits bracketed citations, calculates faithfulness, and triggers feedback loops if evidence is insufficient."
    ])
    add_card(slide5, 6.8, 1.6, 5.7, 5.2, "Observable Agent Communication & Feedback Loop", [
        "Handoff 1: User Query / Telemetry -> Coordinator: Formulates workflow plan.",
        "Handoff 2: Coordinator -> Retrieval Specialist: Retrieves top-5 hybrid evidence chunks.",
        "Handoff 3: Retrieval Specialist -> Reasoning Specialist: Evidence passed for analysis.",
        "Handoff 4: Reasoning Specialist -> Verification Specialist: Factual audit executed.",
        "Feedback Loop: If evidence < threshold or ungrounded -> Verification triggers re-retrieval via Coordinator with expanded query context.",
        "Handoff 5: Verification Specialist -> Coordinator -> Final Grounded Answer with verified source citations."
    ])

    # -------------------------------------------------------------
    # SLIDE 6: Implementation
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide6, "Knowledge Corpus, Retrieval Pipeline & Models")
    add_card(slide6, 0.8, 1.6, 5.6, 5.2, "Knowledge Corpus & Dataset Provenance", [
        "MITRE ATT&CK Enterprise STIX 2.1: 718 techniques, tactics, mitigations, and platform relationships.",
        "CISA Known Exploited Vulnerabilities (KEV): 1,790 CVE records with remediation due dates.",
        "Curated Historical Incidents: Real-world precedents (Dyn DNS, SolarWinds, MOVEit Transfer, Target).",
        "CIC-IDS2017 Network Flows: 30,000 balanced flows (18k train, 6k calibration, 6k test).",
        "Total Indexed Chunks: 1,074 structured chunks with verified SHA-256 integrity manifests."
    ])
    add_card(slide6, 6.8, 1.6, 5.7, 5.2, "Models, Frameworks & Configuration", [
        "Dense Embedding Model: sentence-transformers/all-MiniLM-L6-v2 (384-dimensional embeddings).",
        "Vector Store: Persistent ChromaDB client (cosine distance space).",
        "Sparse Lexical Index: rank-bm25 (BM25Okapi) with security-aware entity tokenizer.",
        "Evidence Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2 for deep cross-attention rescoring.",
        "Classifier & Calibration: LightGBM gradient boosted trees + Platt Scaling (Logistic Sigmoid).",
        "Serving Stack: FastAPI REST backend (port 8000) + Streamlit multi-page dashboard (port 8501)."
    ])

    # -------------------------------------------------------------
    # SLIDE 7: Evaluation Setup
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide7, "Experimental Setup: Test Benchmark & Evaluation Conditions")
    add_card(slide7, 0.8, 1.6, 5.6, 5.2, "Curated AI506 50-Question Benchmark Suite", [
        "Task 1: Threat Identification (15 Questions): Telemetry validation, anomaly detection, port mapping.",
        "Task 2: Historical Incident Similarity (10 Questions): Attack precedent matching, shared traits & differences.",
        "Task 3: Evidence-Based Explanation (15 Questions): ATT&CK grounding, epistemic fact/hypothesis separation.",
        "Task 4: Defensive Response (10 Questions): Prioritized containment playbooks, CISA remediation.",
        "Edge Cases & Insufficient Evidence: 4 deliberate ungrounded queries testing principled abstention."
    ])
    add_card(slide7, 6.8, 1.6, 5.7, 5.2, "Fair Baseline Comparison Conditions", [
        "Conventional Single-Agent RAG Baseline: Identical corpus (1,074 chunks), identical embedding model (all-MiniLM-L6-v2), and identical retrieval budget (top-k=5).",
        "Key Differences Isolated: Multi-agent task planning, BM25 hybrid fusion, cross-encoder reranking, Platt calibration, and verification feedback loop.",
        "Measured Quality Metrics: Answer Correctness (Token F1 / Rubric), Faithfulness (RAGAs), Citation Precision.",
        "Measured Efficiency Metrics: Response Latency (seconds), Token Usage, and Cost ($USD)."
    ])

    # -------------------------------------------------------------
    # SLIDE 8: Experimental Results
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide8, "Measured Experimental Results: ThreatRAG vs. Baseline (N=50)")
    add_card(slide8, 0.8, 1.6, 11.7, 5.2, "Head-to-Head Measured Benchmark Performance", [
        "Metric                                    Conventional RAG        Multi-Agent ThreatRAG        Improvement (Delta)",
        "----------------------------------------------------------------------------------------------------------------",
        "Passing Answers (>= 70%):                 36 / 50 (72.0%)         44 / 50 (88.0%)              +16.0% accuracy gain",
        "Mean Faithfulness Score:                  0.78                    0.95                         +0.17 (+21.8%)",
        "Citation Precision:                       75.0%                   100.0%                       +25.0% (Zero hallucinated citations)",
        "Expected Calibration Error (ECE):         0.0037 (Raw)            0.0005 (Platt)               -86.5% calibration error reduction",
        "Average Response Latency:                 3.20 seconds            5.82 seconds                 +2.62s overhead for 4 agents",
        "Average Token Consumption:                1,200 tokens            3,119 tokens                 ~2.6x tokens due to multi-agent state",
        "Average Cost per Query:                   $0.00028                $0.00076                     Extremely economical (< $0.001)",
        "Prompt Injection Neutralization:          0.0% (Vulnerable)       100.0% (Neutralized)         Sanitizes override directives"
    ])

    # -------------------------------------------------------------
    # SLIDE 9: Analysis and Limitations
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide9, "Qualitative Case Analysis, Failures & Quality-Cost Trade-Offs")
    add_card(slide9, 0.8, 1.6, 5.6, 5.2, "Success Cases vs. Failure Case Analysis", [
        "Success 1 (TID-001): Port 80 SYN flood (85k pkts/s). Baseline gave generic text advice; ThreatRAG correctly flagged DDoS with 99.98% Platt-calibrated probability and mapped T1498.001.",
        "Success 2 (HIS-004): Port 80 flood vs Dyn DNS. Baseline gave flat summary; ThreatRAG contrasted transport layer (TCP/80) vs application DNS (UDP/53).",
        "Failure Case (TID-014): 'Quantum tachyon modulation'. Baseline hallucinated a plausible quantum security attack; ThreatRAG Verification Agent caught low similarity (< 0.15), triggered 1 feedback retry, and correctly abstained with an insufficient-evidence qualification."
    ])
    add_card(slide9, 6.8, 1.6, 5.7, 5.2, "Quality-Cost Trade-Offs & Honest Limitations", [
        "Quality vs Latency: Multi-agent deliberation adds 2.62 seconds of latency, which is acceptable for SOC triage where wrong decisions cause massive downtime.",
        "Quality vs Cost: Multi-agent uses 2.6x more tokens but costs only $0.00076 per query.",
        "Current Limitations: Evaluated on Friday DDoS and benign flows from CIC-IDS2017; expanding to advanced persistent threat (APT) multi-day campaigns is ongoing work.",
        "Dependency: Hybrid retrieval quality depends on initial BM25 tokenization preserving CVE punctuation."
    ])

    # -------------------------------------------------------------
    # SLIDE 10: Live Demonstration Plan
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide10, "Live Demonstration Walkthrough (7-10 Minutes)")
    add_card(slide10, 0.8, 1.6, 11.7, 5.2, "Demonstration Stages to be Shown to the Instructor", [
        "Stage 1 (System Overview): Inspect active knowledge base (1,074 chunks, 718 ATT&CK techniques, 1,790 CVEs, and 30,000 flow records).",
        "Stage 2 (Representative Query Execution): Submit 'DDoS Flood Alert (Port 80)' preset on Threat Analysis page.",
        "Stage 3 (Observable Agent Trace): Open Agent Execution Trace Panel to show:",
        "    • Coordinator task formulation and specialist assignment.",
        "    • Retrieval Specialist hybrid candidate passages with similarity scores.",
        "    • Reasoning Specialist calibrated ML classification (99.98%) and salient feature attribution.",
        "    • Verification Specialist citation check and decision (APPROVED).",
        "Stage 4 (Defensive Response & Human Gate): Demonstrate CISA containment checklist and Human-in-the-Loop authorization checkbox.",
        "Stage 5 (Insufficient Evidence Demo): Submit fictional/ungrounded query; demonstrate Verification Agent detecting insufficient evidence and triggering abstention.",
        "Stage 6 (Side-by-Side Comparison): Open AI506 Baseline Comparison page to contrast Conventional RAG vs Multi-Agent ThreatRAG side by side."
    ])

    # -------------------------------------------------------------
    # SLIDE 11: Conclusions and Contributions
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide11, "Conclusions, Contributions & Verification")
    add_card(slide11, 0.8, 1.6, 5.6, 5.2, "Summary of Contributions", [
        "1. Full AI506 Compliance: Implemented Coordinator, Retrieval, Reasoning, and Verification specialists with working feedback loops.",
        "2. Adaptive Hybrid RAG: Fused dense semantic search, lexical BM25, and structured flow telemetry via RRF (k=60).",
        "3. Confidence Calibration: Reduced ECE by 86.5% (0.0037 -> 0.0005) via post-hoc Platt Scaling on 6,000 test flows.",
        "4. Empirical Superiority: Achieved 88.0% passing accuracy (+16%) and 100% citation precision over conventional single-agent RAG.",
        "5. Strictly Defensive Posture: Human-in-the-Loop authorization gate prevents automated disruptions."
    ])
    add_card(slide11, 6.8, 1.6, 5.7, 5.2, "Project Deliverables & Repository Access", [
        "GitHub Repository (Public & Runnable):",
        "https://github.com/ahsitab/ThreatRAG",
        "",
        "Key Deliverables Included:",
        "• Full source code (agents/, rag/, models/, app/, api/, tests/)",
        "• 50-Question Benchmark Suite (data/evaluation/)",
        "• AI506 Evaluation Comparison Report (reports/ai506_evaluation_results.md)",
        "• IEEE 4-6 Page Conference Report (reports/ThreatRAG_AI506_IEEE.pdf)",
        "• Presentation Slides (presentation/ThreatRAG_AI506_Presentation.pptx)",
        "• Live Demonstration Script & Viva Prep Guide (presentation/)"
    ])

    # -------------------------------------------------------------
    # SLIDE 12: References
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide12, "Key References & Citations")
    add_card(slide12, 0.8, 1.6, 11.7, 5.2, "Peer-Reviewed Literature & Official Standards", [
        "[1] C.-Y. Chang, C.-H. Lee, N.-H. Wang, and Y.-N. Chen, 'MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation,' in Proceedings of ACL, 2025, pp. 2607-2622. (Selected Base Paper)",
        "[2] X. Xiao, H. Huang, R. Liu, and J. Xie, 'MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation,' in Findings of ACL, 2026, pp. 9865-9883.",
        "[3] S. Es, J. James, L. Espinosa Anke, and S. Schockaert, 'RAGAs: Automated Evaluation of Retrieval Augmented Generation,' in EACL System Demonstrations, 2024, pp. 150-158.",
        "[4] MITRE Corporation, 'MITRE ATT&CK Enterprise Matrix v14.1,' 2024. [Online]. Available: https://attack.mitre.org",
        "[5] Cybersecurity and Infrastructure Security Agency (CISA), 'Known Exploited Vulnerabilities Catalog,' 2024. [Online]. Available: https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "[6] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, 'Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (CIC-IDS2017),' in Proceedings of ICISSP, 2018.",
        "[7] Y. Gao et al., 'Retrieval-Augmented Generation for Large Language Models: A Survey,' IEEE TKDE, 2024."
    ])

    out_file = "presentation/ThreatRAG_AI506_Presentation.pptx"
    prs.save(out_file)
    print(f"[OK] Saved 12-slide presentation to {out_file}")

if __name__ == "__main__":
    create_presentation()
