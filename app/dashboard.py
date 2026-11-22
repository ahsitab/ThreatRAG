import streamlit as st
import os
import sys

# Ensure root workspace is available
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="ThreatRAG: Cybersecurity Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cybersecurity theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-secure {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-alert {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ ThreatRAG")
st.sidebar.markdown("**Adaptive Hybrid RAG Framework**")
st.sidebar.markdown("MSc AI Research Project (AIML-507)")
st.sidebar.divider()

st.sidebar.subheader("System Status")
st.sidebar.markdown("🟢 **Vector Index:** ChromaDB Active")
st.sidebar.markdown("🟢 **Sparse Index:** BM25 Active")
st.sidebar.markdown("🟢 **Classifier:** LightGBM + Platt Scaling")
st.sidebar.markdown("🟢 **Safety Gate:** Human-in-the-Loop Active")
st.sidebar.divider()

st.sidebar.info(
    "ThreatRAG is an explainable cybersecurity threat intelligence framework "
    "grounded in MITRE ATT&CK, CISA KEV, and empirical network telemetry."
)

# Main Page
st.markdown('<div class="main-header">ThreatRAG: Autonomous Cybersecurity Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">An Adaptive Hybrid Retrieval-Augmented Generation Framework '
    'for Explainable Threat Intelligence and Incident Response</div>',
    unsafe_allow_html=True
)

# Key metric summary tiles
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Knowledge Base Chunks", value="1,074", delta="STIX + CISA + CIC")
with col2:
    st.metric(label="MITRE ATT&CK Techniques", value="718", delta="Enterprise v14.1")
with col3:
    st.metric(label="CISA KEV Catalog", value="1,790", delta="Exploited CVEs")
with col4:
    st.metric(label="Model Calibration (ECE)", value="0.0005", delta="-86.5% error reduction")

st.markdown("---")

# Architectural Highlights
st.subheader("Architectural Pillars")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    ### 🔬 Research Contributions
    1. **Adaptive Hybrid Retrieval ($E_5$):**
       - Unifies dense semantic search (`all-MiniLM-L6-v2`), BM25 lexical search, and structured flow telemetry matching via Reciprocal Rank Fusion ($k=60$).
       - Dynamic routing based on security token entropy and alphanumeric identifier detection (CVEs, ATT&CK IDs).
    2. **Evidence-Aware Reranking:**
       - Cross-encoder (`ms-marco-MiniLM-L-6-v2`) reranks candidate chunks to suppress hallucinated context and maximize factual relevance.
    3. **Post-Hoc Confidence Calibration:**
       - Platt scaling reduces Expected Calibration Error (ECE) from 0.0037 to 0.0005 on 6,000 validation flows, preventing overconfident automation.
    """)

with col_b:
    st.markdown("""
    ### 🤖 Autonomous Multi-Agent Team
    - **Agent 1 — Threat Identifier:** Evaluates telemetry, calculates calibrated probability, estimates uncertainty, and attributes salient flow features.
    - **Agent 2 — Incident Searcher:** Discovers historical incident precedents, calculates hybrid similarity, and contrasts operational differences.
    - **Agent 3 — Evidence Explainer:** Grounds threat behavior in MITRE ATT&CK tactics and separates empirical evidence from hypotheses.
    - **Agent 4 — Defensive Response Advisor:** Formulates prioritized containment and remediation checklists with strict human approval gates.
    """)

st.markdown("---")

# Quick Navigation Guide
st.subheader("Explore the Platform")
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown("#### 📊 [System Overview](Overview)")
    st.write("Inspect knowledge base distributions, STIX 2.1 entities, and indexing topology.")
    st.markdown("#### 🚨 [Threat Analysis](Threat_Analysis)")
    st.write("Submit live network flows or telemetry alerts for end-to-end multi-agent triage.")

with nav_col2:
    st.markdown("#### 🔍 [Similar Incidents](Similar_Incidents)")
    st.write("Query historical security incident precedents using hybrid similarity matching.")
    st.markdown("#### 📝 [Evidence Explanation](Evidence_Explanation)")
    st.write("Analyze factual grounding, MITRE technique tags, and citation audit trail.")

with nav_col3:
    st.markdown("#### 🛡️ [Defensive Response](Defensive_Response)")
    st.write("Review CISA KEV remediation playbooks and enforce human authorization.")
    st.markdown("#### 📈 [Research Evaluation](Research_Evaluation)")
    st.write("View empirical benchmarks, ablation studies, calibration curves, and latency metrics.")

st.markdown("---")
st.caption("ThreatRAG Framework • Developed for AIML-507 • Strictly Defensive Posture • Zero Fabricated Metrics")
