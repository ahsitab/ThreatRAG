import streamlit as st
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.orchestrator import ThreatRAGOrchestrator

st.set_page_config(page_title="ThreatRAG - Threat Analysis", page_icon="🚨", layout="wide")

st.title("🚨 Calibrated Threat Identification & Telemetry Analysis")
st.markdown("Submit live network flow telemetry and security alerts for multi-agent evaluation, calibrated ML inference, and uncertainty quantification.")

@st.cache_resource
def get_cached_orchestrator():
    return ThreatRAGOrchestrator()

orchestrator = get_cached_orchestrator()

# Presets for quick evaluation
st.subheader("1. Select Telemetry Preset or Enter Custom Flow")

PRESETS = {
    "DDoS Flood Alert (Port 80 HTTP Flood)": {
        "query": "High-volume ingress packet spike detected targeting web gateway on port 80. Excessive packet rates exceeding 100k packets/s observed.",
        "Destination_Port": 80.0,
        "Flow_Duration": 8500.0,
        "Total_Fwd_Packets": 240.0,
        "Total_Backward_Packets": 4.0,
        "Flow_Bytes_s": 950000.0,
        "Flow_Packets_s": 85000.0,
        "Packet_Length_Mean": 18.5
    },
    "Benign Web Browsing (HTTPS Session)": {
        "query": "Standard outbound user HTTPS session to cloud services. Normal symmetric packet flow and standard duration.",
        "Destination_Port": 443.0,
        "Flow_Duration": 1500000.0,
        "Total_Fwd_Packets": 18.0,
        "Total_Backward_Packets": 22.0,
        "Flow_Bytes_s": 12500.0,
        "Flow_Packets_s": 26.6,
        "Packet_Length_Mean": 450.0
    },
    "Reconnaissance Port Scan": {
        "query": "Rapid sequential connection attempts across low-range ports with minimal payload data and zero backward response packets.",
        "Destination_Port": 22.0,
        "Flow_Duration": 120.0,
        "Total_Fwd_Packets": 2.0,
        "Total_Backward_Packets": 0.0,
        "Flow_Bytes_s": 120.0,
        "Flow_Packets_s": 16666.0,
        "Packet_Length_Mean": 0.0
    }
}

selected_preset = st.selectbox("Choose a Telemetry Preset:", list(PRESETS.keys()))
preset_data = PRESETS[selected_preset]

with st.expander("Telemetry & Query Parameters (Customizable)", expanded=True):
    user_query = st.text_area("Analyst Description / Security Event Alert:", value=preset_data["query"], height=70)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dest_port = st.number_input("Destination Port", value=float(preset_data["Destination_Port"]), min_value=1.0, max_value=65535.0)
        flow_duration = st.number_input("Flow Duration (µs)", value=float(preset_data["Flow_Duration"]), min_value=0.0)
    with col2:
        flow_packets_s = st.number_input("Flow Packets / s", value=float(preset_data["Flow_Packets_s"]), min_value=0.0)
        flow_bytes_s = st.number_input("Flow Bytes / s", value=float(preset_data["Flow_Bytes_s"]), min_value=0.0)
    with col3:
        pkt_len_mean = st.number_input("Packet Length Mean (bytes)", value=float(preset_data["Packet_Length_Mean"]), min_value=0.0)
        fwd_pkts = st.number_input("Total Forward Packets", value=float(preset_data["Total_Fwd_Packets"]), min_value=0.0)

telemetry_dict = {
    "Destination_Port": dest_port,
    "Flow_Duration": flow_duration,
    "Flow_Packets_s": flow_packets_s,
    "Flow_Bytes_s": flow_bytes_s,
    "Packet_Length_Mean": pkt_len_mean,
    "Total_Fwd_Packets": fwd_pkts,
    "Total_Backward_Packets": float(preset_data["Total_Backward_Packets"])
}

st.markdown("---")

if st.button("🚀 Run ThreatRAG Analysis Pipeline", type="primary", use_container_width=True):
    with st.spinner("Executing adaptive hybrid retrieval and multi-agent pipeline..."):
        start_t = time.time()
        pipeline_result = orchestrator.run(query=user_query, telemetry=telemetry_dict)
        latency = time.time() - start_t

    st.success(f"Analysis completed in {latency:.2f} seconds.")

    threat_info = pipeline_result.get("threat_identification", {})
    is_threat = threat_info.get("threat_detected", False)
    prob = threat_info.get("calibrated_probability", 0.0)
    conf = threat_info.get("confidence_level", "Medium")
    uncertainty = threat_info.get("uncertainty", 0.1)

    # Top Results Cards
    st.subheader("2. Threat Classification & Calibration Results")
    rc1, rc2, rc3, rc4 = st.columns(4)

    with rc1:
        if is_threat:
            st.error(f"🚨 **Verdict:** {threat_info.get('predicted_label', 'DDoS')}")
        else:
            st.success(f"✅ **Verdict:** {threat_info.get('predicted_label', 'BENIGN')}")

    with rc2:
        st.metric(label="Calibrated Probability", value=f"{prob * 100:.2f}%")
        st.progress(float(prob))

    with rc3:
        st.metric(label="Confidence Tier", value=conf)

    with rc4:
        st.metric(label="Predictive Uncertainty", value=f"{uncertainty:.4f}")

    # Salient Features & Attribution
    st.subheader("3. Salient Flow Feature Attribution")
    features = threat_info.get("top_contributing_features", [])
    if features:
        feat_cols = st.columns(len(features))
        for idx, f in enumerate(features):
            with feat_cols[idx]:
                st.info(f"**{f.get('feature')}**\n\nValue: `{f.get('observed_value')}`\nImpact: {f.get('impact')}")

    # MITRE ATT&CK Mappings
    st.subheader("4. Grounded MITRE ATT&CK Techniques")
    techniques = threat_info.get("mapped_att_ck_techniques", [])
    if techniques:
        tech_html = " ".join([f"<span style='background-color:#E0F2FE; color:#0369A1; padding:4px 10px; border-radius:6px; font-weight:600; margin-right:8px;'>{t}</span>" for t in techniques])
        st.markdown(tech_html, unsafe_allow_html=True)
    else:
        st.write("No direct ATT&CK technique mapping required for benign telemetry.")

    st.markdown("---")
    st.subheader("5. Analyst Summary")
    st.markdown(threat_info.get("analyst_summary", "No summary generated."))

    with st.expander("Audit Trail & Token Consumption"):
        metrics = pipeline_result.get("execution_metrics", {})
        st.write(f"- **Total Tokens Consumed:** {metrics.get('total_tokens', 0)}")
        st.write(f"- **Estimated Model Cost:** ${metrics.get('estimated_cost_usd', 0.0):.6f}")
        st.write(f"- **Agents Executed:** {', '.join(metrics.get('agents_executed', []))}")
