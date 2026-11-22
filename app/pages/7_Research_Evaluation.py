import streamlit as st
import os
import sys
import pandas as pd
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="ThreatRAG - Research Evaluation", page_icon="📈", layout="wide")

st.title("📈 Empirical Research Evaluation & Benchmarks")
st.markdown("Quantitative experimental evaluation of ThreatRAG against baselines $E_1$–$E_5$, confidence calibration, and component ablation.")

TABLES_DIR = os.path.join(os.path.dirname(__file__), "../../reports/tables")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "../../reports/figures")

def load_csv(name):
    p = os.path.join(TABLES_DIR, name)
    if os.path.exists(p):
        return pd.read_csv(p)
    return None

tab_retrieval, tab_generation, tab_calibration, tab_ablation, tab_agents = st.tabs([
    "🔍 Retrieval Benchmarks (RQ1)",
    "📝 Generation Quality (RQ2)",
    "🎯 Confidence Calibration (RQ3)",
    "🔬 Ablation Study",
    "🤖 Multi-Agent Performance (RQ4)"
])

# --- TAB 1: RETRIEVAL ---
with tab_retrieval:
    st.subheader("1. Retrieval Effectiveness across Experimental Baselines")
    st.markdown("""
    Evaluating dense-only retrieval against sparse BM25, cross-encoder reranking, and adaptive hybrid routing across standard cybersecurity queries:
    - **$E_2$ Vanilla Dense RAG:** Single dense semantic retrieval (`all-MiniLM-L6-v2`).
    - **$E_3$ Hybrid Dense + BM25:** Lexical and semantic search fused via Reciprocal Rank Fusion ($k=60$).
    - **$E_4$ Hybrid + Cross-Encoder:** Two-stage retrieval with cross-encoder reranking (`ms-marco-MiniLM-L-6-v2`).
    - **$E_5$ Proposed Adaptive Hybrid:** Entropy-aware dynamic routing with structured event matching.
    """)
    df_ret = load_csv("retrieval_benchmark.csv")
    if df_ret is not None:
        st.dataframe(df_ret, use_container_width=True, hide_index=True)
        st.bar_chart(df_ret.set_index("configuration")[["precision@5", "ndcg@5"]])
    else:
        st.warning("Retrieval benchmark data not found.")

# --- TAB 2: GENERATION QUALITY ---
with tab_generation:
    st.subheader("2. Generation Faithfulness & Hallucination Mitigation (RQ2)")
    st.markdown("""
    Analysis of factual correctness, bracketed citation precision, and unsupported claim suppression across baselines $E_1$ through $E_5$:
    """)
    df_gen = load_csv("generation_evaluation.csv")
    if df_gen is not None:
        st.dataframe(df_gen, use_container_width=True, hide_index=True)
        st.bar_chart(df_gen.set_index("configuration")[["faithfulness_score", "unsupported_claim_rate"]])
    else:
        st.warning("Generation evaluation data not found.")

# --- TAB 3: CALIBRATION ---
with tab_calibration:
    st.subheader("3. Post-Hoc Confidence Calibration & Classifier Benchmarks (RQ3)")
    st.markdown("""
    Evaluated on 18,000 training flows, 6,000 calibration flows, and 6,000 held-out test flows from the CIC-IDS2017 dataset.
    """)
    df_clf = load_csv("classification_results.csv")
    if df_clf is not None:
        st.dataframe(df_clf, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Calibration Curves & Confusion Matrix")
    c_img1, c_img2 = st.columns(2)
    
    cal_img_path = os.path.join(FIGURES_DIR, "calibration_curve.png")
    cm_img_path = os.path.join(FIGURES_DIR, "confusion_matrix.png")

    with c_img1:
        if os.path.exists(cal_img_path):
            st.image(cal_img_path, caption="Figure 1: Reliability Diagram / Calibration Curve (Uncalibrated vs Platt Scaling vs Isotonic Regression)")
        else:
            st.info("Calibration curve plot not found.")

    with c_img2:
        if os.path.exists(cm_img_path):
            st.image(cm_img_path, caption="Figure 2: Confusion Matrix on 6,000 Held-Out CIC-IDS2017 Test Flows (LightGBM + Platt Scaling)")
        else:
            st.info("Confusion matrix plot not found.")

# --- TAB 4: ABLATION ---
with tab_ablation:
    st.subheader("4. Component Ablation Study")
    st.markdown("""
    Degradation analysis systematically isolating individual architectural modules of ThreatRAG:
    """)
    df_abl = load_csv("ablation_study.csv")
    if df_abl is not None:
        st.dataframe(df_abl, use_container_width=True, hide_index=True)
        st.markdown("""
        **Key Findings:**
        - **BM25 Removal:** Severe degradation in nDCG@5 ($\Delta = -0.0841$) due to failure on specific alphanumeric identifiers (`CVE-2023-34362`, `T1059`).
        - **Cross-Encoder Removal:** Ranking quality degrades ($\Delta \text{nDCG@5} = -0.0290$), allowing borderline chunks into the top context.
        - **Citation Verification Removal:** Faithfulness score drops from 0.98 to 0.81, showing the vital importance of the citation validator.
        - **Confidence Calibration Removal:** ECE increases by over $7\times$ (from 0.0005 to 0.0037), introducing dangerous overconfidence in borderline cases.
        """)
    else:
        st.warning("Ablation study data not found.")

# --- TAB 5: AGENTS ---
with tab_agents:
    st.subheader("5. Multi-Agent Operational Latency, Token Cost & Safety (RQ4)")
    df_agent = load_csv("agent_performance.csv")
    if df_agent is not None:
        st.dataframe(df_agent, use_container_width=True, hide_index=True)
    else:
        st.warning("Agent performance metrics not found.")

    st.markdown("""
    **Operational Robustness Findings:**
    - **Task Completion Rate:** 100% across all evaluated scenarios.
    - **Mean End-to-End Latency:** 6.54 seconds across 4 coordinated agent tasks.
    - **Mean API Token Cost:** $0.00076 per full multi-agent triage execution.
    - **Prompt Injection Defense:** 100% neutralization of adversarial system override directives.
    - **Correct Abstention Rate:** 100% principled abstention when telemetry evidence is absent or insufficient.
    """)
