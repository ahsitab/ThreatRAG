import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.evidence_explainer import EvidenceExplainerAgent

st.set_page_config(page_title="ThreatRAG - Evidence Explanation", page_icon="📝", layout="wide")

st.title("📝 Explainable Evidence & ATT&CK Grounding")
st.markdown("Examine evidence-grounded threat reasoning with rigorous separation between empirical telemetry observations and inferential hypotheses.")

@st.cache_resource
def get_explainer():
    return EvidenceExplainerAgent()

explainer = get_explainer()

col_input1, col_input2 = st.columns([1, 2])

with col_input1:
    threat_type = st.selectbox(
        "Identified Threat Classification:",
        ["Distributed Denial of Service (DDoS)", "Port Scan / Reconnaissance", "Web Application Exploit (SQLi)", "Command & Control Beaconing"]
    )
    observed_port = st.number_input("Destination Port", value=80, min_value=1, max_value=65535)
    packet_rate = st.number_input("Packet Rate (pkt/s)", value=120000, min_value=0)

with col_input2:
    observations_text = st.text_area(
        "Observed Empirical Telemetry Signals (one per line):",
        value=(
            "Rapid surge in inbound SYN requests exceeding 100,000 packets per second.\n"
            "Source IP entropy indicates highly distributed spoofed origins.\n"
            "Server socket exhaustion observed on web listener port 80.\n"
            "Absence of completed three-way TCP handshakes (ACK packets missing)."
        ),
        height=130
    )

observations = [line.strip() for line in observations_text.strip().split("\n") if line.strip()]

if st.button("🔬 Generate Grounded Explanation & Audit", type="primary"):
    with st.spinner("Retrieving ATT&CK techniques and auditing citation veracity..."):
        telemetry = {"Destination_Port": observed_port, "Flow_Packets_s": packet_rate}
        explanation_result = explainer.run(
            threat_type=threat_type,
            observations=observations,
            telemetry=telemetry
        )

    st.subheader("1. Factual Narrative Explanation")
    st.markdown(explanation_result.get("explanation", ""))

    st.markdown("---")
    st.subheader("2. Epistemic Separation: Facts vs. Hypotheses")
    
    col_emp, col_hyp = st.columns(2)
    with col_emp:
        st.markdown("#### 🔬 Verified Empirical Observations (Telemetry)")
        for obs in explanation_result.get("empirical_evidence", []):
            st.success(f"**Observed:** {obs}")

    with col_hyp:
        st.markdown("#### 💡 Inferential Hypotheses (Model Assessment)")
        for hyp in explanation_result.get("hypotheses", []):
            st.warning(f"**Hypothesis:** {hyp}")

    st.markdown("---")
    st.subheader("3. Grounded MITRE ATT&CK Matrix Alignment")
    techs = explanation_result.get("grounded_att_ck_techniques", [])
    if techs:
        tech_html = " ".join([f"<span style='background-color:#EDE9FE; color:#5B21B6; padding:6px 14px; border-radius:8px; font-weight:700; font-size:1.0rem; margin-right:8px;'>{t}</span>" for t in techs])
        st.markdown(tech_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("4. Citation Audit & Anti-Hallucination Report")
    audit = explanation_result.get("citation_audit", {})
    
    ac1, ac2, ac3 = st.columns(3)
    ac1.metric("Faithfulness Score", f"{audit.get('faithfulness_score', 1.0) * 100:.1f}%")
    ac2.metric("Citation Precision", f"{audit.get('citation_precision', 1.0) * 100:.1f}%")
    ac3.metric("Unsupported Claim Rate", f"{audit.get('unsupported_claim_rate', 0.0) * 100:.1f}%")

    st.markdown("#### Grounded Source References")
    citations = explanation_result.get("citations", [])
    if citations:
        for c in citations:
            with st.expander(f"Reference [{c.get('chunk_id')}]: {c.get('title')}"):
                st.write(f"- **Source:** {c.get('source')}")
                st.write(f"- **Content Snippet:** {c.get('snippet')}")
    else:
        st.info("No external citations required for this telemetry block.")
