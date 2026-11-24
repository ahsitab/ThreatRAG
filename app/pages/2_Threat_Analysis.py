import streamlit as st
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.orchestrator import ThreatRAGOrchestrator

st.set_page_config(page_title="ThreatRAG - Threat Analysis", page_icon="🚨", layout="wide")

st.title("🚨 Calibrated Threat Identification & Telemetry Analysis")
st.markdown("Submit network telemetry and security alerts for multi-agent evaluation, calibrated ML inference, and evidence verification.")

# Easy English Guide Expander
with st.expander("📖 Easy 30-Second Guide: How to use this page", expanded=False):
    st.markdown("""
    **Welcome to the Threat Analysis Workbench!** You can test cybersecurity incidents in 3 simple steps:
    1. **Choose an Example:** Click any of the **6 Example Buttons** below. The incident description and network telemetry numbers will automatically load!
    2. **(Optional) Customize:** You can tweak the numbers (like Destination Port or Packet Rate) or edit the description text to test your own ideas.
    3. **Click '🚀 Run ThreatRAG Analysis Pipeline':** Watch the **4 AI Agents** investigate in real time, map the attack to international MITRE standards, verify the evidence, and give you an exact firewall action plan!
    """)

@st.cache_resource
def get_cached_orchestrator():
    return ThreatRAGOrchestrator()

orchestrator = get_cached_orchestrator()

# -------------------------------------------------------------
# EXPANDED PRESETS (6 REALISTIC CYBERSECURITY SCENARIOS)
# -------------------------------------------------------------
PRESETS = {
    "🔥 Example 1: Port 80 Web DDoS Attack": {
        "title": "Port 80 Web DDoS Flood",
        "description": "High-volume SYN flood attack attempting to knock down an internal web server.",
        "query": "Telemetry shows sudden flood of 1.2 million SYN packets per second on destination port 80 targeting internal web servers. Traffic originates from over 8,500 spoofed external IP addresses. Firewall CPU utilization reached 98% with significant connection drops.",
        "Destination_Port": 80.0,
        "Flow_Duration": 8500.0,
        "Total_Fwd_Packets": 240.0,
        "Total_Backward_Packets": 4.0,
        "Flow_Bytes_s": 950000.0,
        "Flow_Packets_s": 85000.0,
        "Packet_Length_Mean": 18.5
    },
    "🔓 Example 2: MOVEit SQL Injection": {
        "title": "MOVEit Enterprise Zero-Day (CVE-2023-34362)",
        "description": "Web application SQL injection used by threat actors to place webshells and steal data.",
        "query": "Explain the attack chain of CVE-2023-34362 MOVEit Transfer SQL injection vulnerability. How did threat actors exploit the web application to achieve remote code execution and exfiltrate sensitive files?",
        "Destination_Port": 443.0,
        "Flow_Duration": 45000.0,
        "Total_Fwd_Packets": 65.0,
        "Total_Backward_Packets": 52.0,
        "Flow_Bytes_s": 180000.0,
        "Flow_Packets_s": 1200.0,
        "Packet_Length_Mean": 350.0
    },
    "🤖 Example 3: Mirai Botnet IoT Attack": {
        "title": "Mirai IoT Botnet DNS Amplification",
        "description": "Distributed attack using compromised smart cameras and DVRs to overwhelm DNS servers.",
        "query": "Find historical major cybersecurity incidents similar to a large-scale Mirai botnet attack utilizing compromised IoT devices for distributed DNS amplification.",
        "Destination_Port": 53.0,
        "Flow_Duration": 12000.0,
        "Total_Fwd_Packets": 500.0,
        "Total_Backward_Packets": 2.0,
        "Flow_Bytes_s": 1200000.0,
        "Flow_Packets_s": 150000.0,
        "Packet_Length_Mean": 512.0
    },
    "🕵️ Example 4: Stealthy Port Scan": {
        "title": "Internal Network Reconnaissance Scan",
        "description": "Automated sequential probing across low-range ports searching for open SSH and RDP services.",
        "query": "Rapid sequential connection attempts across low-range ports with minimal payload data and zero backward response packets targeting SSH and RDP.",
        "Destination_Port": 22.0,
        "Flow_Duration": 120.0,
        "Total_Fwd_Packets": 2.0,
        "Total_Backward_Packets": 0.0,
        "Flow_Bytes_s": 120.0,
        "Flow_Packets_s": 16666.0,
        "Packet_Length_Mean": 0.0
    },
    "🟢 Example 5: Safe Office Browsing": {
        "title": "Harmless Employee Office Web Browsing",
        "description": "Standard outbound HTTPS cloud connection with balanced packet flows (Benign/Safe).",
        "query": "Standard outbound user HTTPS session to cloud services. Normal symmetric packet flow and standard duration on port 443.",
        "Destination_Port": 443.0,
        "Flow_Duration": 1500000.0,
        "Total_Fwd_Packets": 18.0,
        "Total_Backward_Packets": 22.0,
        "Flow_Bytes_s": 12500.0,
        "Flow_Packets_s": 26.6,
        "Packet_Length_Mean": 450.0
    },
    "⚠️ Example 6: Zero-Evidence Test": {
        "title": "Fictional Zero-Evidence Test (Abstention Test)",
        "description": "A completely made-up worm query to prove the AI will NOT hallucinate false facts.",
        "query": "What is the zero-day exploit mechanism of the Quantum Tachyon Worm targeting deep sea submarine fiber optic routers in 1994?",
        "Destination_Port": 8080.0,
        "Flow_Duration": 500.0,
        "Total_Fwd_Packets": 5.0,
        "Total_Backward_Packets": 1.0,
        "Flow_Bytes_s": 500.0,
        "Flow_Packets_s": 10.0,
        "Packet_Length_Mean": 64.0
    }
}

# Session state initialization for presets
if "selected_preset_key" not in st.session_state:
    st.session_state["selected_preset_key"] = list(PRESETS.keys())[0]

st.subheader("1. Quick 1-Click Example Loaders")
st.markdown("Click any example button to automatically populate all parameters with real-world incident data:")

btn_c1, btn_c2, btn_c3 = st.columns(3)
with btn_c1:
    if st.button("🔥 Example 1: Web DDoS Attack", use_container_width=True, help="Load Port 80 SYN Flood scenario"):
        st.session_state["selected_preset_key"] = "🔥 Example 1: Port 80 Web DDoS Attack"
        st.rerun()
    if st.button("🔓 Example 2: MOVEit SQLi Exploit", use_container_width=True, help="Load MOVEit Transfer zero-day exploit"):
        st.session_state["selected_preset_key"] = "🔓 Example 2: MOVEit SQL Injection"
        st.rerun()

with btn_c2:
    if st.button("🤖 Example 3: Mirai Botnet Attack", use_container_width=True, help="Load IoT botnet DNS amplification scenario"):
        st.session_state["selected_preset_key"] = "🤖 Example 3: Mirai Botnet IoT Attack"
        st.rerun()
    if st.button("🕵️ Example 4: Stealthy Port Scan", use_container_width=True, help="Load reconnaissance scan scenario"):
        st.session_state["selected_preset_key"] = "🕵️ Example 4: Stealthy Port Scan"
        st.rerun()

with btn_c3:
    if st.button("🟢 Example 5: Safe Office Browsing", use_container_width=True, help="Load benign everyday employee traffic"):
        st.session_state["selected_preset_key"] = "🟢 Example 5: Safe Office Browsing"
        st.rerun()
    if st.button("⚠️ Example 6: Zero-Evidence Test", use_container_width=True, help="Test system abstention on fictional query"):
        st.session_state["selected_preset_key"] = "⚠️ Example 6: Zero-Evidence Test"
        st.rerun()

st.markdown("Or choose from the dropdown:")
preset_keys = list(PRESETS.keys())
current_idx = preset_keys.index(st.session_state["selected_preset_key"]) if st.session_state["selected_preset_key"] in preset_keys else 0
selected_preset = st.selectbox("Active Telemetry Preset:", preset_keys, index=current_idx)
st.session_state["selected_preset_key"] = selected_preset
preset_data = PRESETS[selected_preset]

st.caption(f"ℹ️ **Current Scenario:** {preset_data.get('description')}")

with st.expander("📝 Incident Description & Network Parameters (Customizable)", expanded=True):
    user_query = st.text_area(
        "Analyst Description / Security Event Alert:",
        value=preset_data["query"],
        height=75,
        help="Type or edit the security alert text here. This tells the AI what is happening on your network."
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dest_port = st.number_input(
            "Destination Port",
            value=float(preset_data["Destination_Port"]),
            min_value=1.0,
            max_value=65535.0,
            help="The network port being targeted (e.g. 80 for HTTP, 443 for HTTPS, 22 for SSH, 53 for DNS)."
        )
        flow_duration = st.number_input(
            "Flow Duration (µs)",
            value=float(preset_data["Flow_Duration"]),
            min_value=0.0,
            help="Length of the connection flow in microseconds."
        )
    with col2:
        flow_packets_s = st.number_input(
            "Flow Packets / s",
            value=float(preset_data["Flow_Packets_s"]),
            min_value=0.0,
            help="Rate of incoming packets per second. Heavy flood attacks typically exceed 50,000 pkts/s."
        )
        flow_bytes_s = st.number_input(
            "Flow Bytes / s",
            value=float(preset_data["Flow_Bytes_s"]),
            min_value=0.0,
            help="Total volume of data transferred per second in bytes."
        )
    with col3:
        pkt_len_mean = st.number_input(
            "Packet Length Mean (bytes)",
            value=float(preset_data["Packet_Length_Mean"]),
            min_value=0.0,
            help="Average size of incoming packets. Floods often use very small packets (e.g. <64 bytes)."
        )
        fwd_pkts = st.number_input(
            "Total Forward Packets",
            value=float(preset_data["Total_Fwd_Packets"]),
            min_value=0.0,
            help="Total number of packets sent toward the target server."
        )

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
    with st.spinner("Executing adaptive hybrid retrieval and 4-agent collaborative pipeline..."):
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
            st.success(f"✅ **Verdict:** {threat_info.get('predicted_label', 'BENIGN (Safe)')}")

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

    # --- AI506 MANDATORY: AGENT EXECUTION TRACE PANEL ---
    st.markdown("---")
    st.subheader("🕵️‍♂️ Multi-Agent Execution Trace Panel (AI506 Live Trace)")
    st.markdown(
        "*Step-by-step observable agent handoffs, task planning, retrieval scores, verification decisions, and feedback loops.*"
    )

    trace = pipeline_result.get("execution_trace", [])
    fb_count = pipeline_result.get("feedback_loops_count", 0)

    # Workflow summary status bar
    st.markdown(f"""
    <div style="background-color: #F1F5F9; border-left: 5px solid #1E3A8A; padding: 12px 16px; border-radius: 4px; margin-bottom: 16px;">
        <strong>Multi-Agent Status:</strong> Orchestration Complete &bull; 
        <strong>Active Agents:</strong> 4 Logical Specialists &bull; 
        <strong>Feedback Loops Triggered:</strong> {fb_count} &bull; 
        <strong>Latency:</strong> {latency:.2f}s
    </div>
    """, unsafe_allow_html=True)

    # Visual Workflow Diagram
    st.markdown("""
    ```mermaid
    graph LR
        Q[User Query / Telemetry] --> C[Coordinator / Planner]
        C -->|Assigns Hybrid Search| R[Retrieval Specialist]
        R -->|Top-k Grounded Chunks| S[Reasoning Specialist]
        S -->|Synthesized Claims| V[Verification Specialist]
        V -->|Feedback Loop If Insufficient| R
        V -->|Verified & Grounded| F[Final Answer + Citations]
    ```
    """)

    if trace:
        for idx, step in enumerate(trace, 1):
            agent_name = step.get("agent", "Agent")
            action = step.get("action", "Execution Step")
            status = step.get("status", "Complete")
            details = step.get("details", "")

            # Badge styling based on agent
            if "Coordinator" in agent_name:
                badge_bg = "#EDE9FE"
                badge_color = "#5B21B6"
            elif "Retrieval" in agent_name:
                badge_bg = "#E0F2FE"
                badge_color = "#0369A1"
            elif "Reasoning" in agent_name:
                badge_bg = "#FEF3C7"
                badge_color = "#92400E"
            elif "Verification" in agent_name:
                badge_bg = "#DCFCE7" if status == "APPROVED" else "#FEE2E2"
                badge_color = "#166534" if status == "APPROVED" else "#991B1B"
            else:
                badge_bg = "#F3F4F6"
                badge_color = "#374151"

            with st.expander(f"Step {idx}: [{agent_name}] — {action} ({status})", expanded=(idx <= 2 or "Verification" in agent_name)):
                st.markdown(
                    f"<span style='background-color:{badge_bg}; color:{badge_color}; padding:4px 10px; border-radius:6px; font-weight:700;'>{status}</span>",
                    unsafe_allow_html=True
                )
                if isinstance(details, dict):
                    st.json(details)
                else:
                    st.write(details)
    else:
        st.info("Execution trace details captured in background pipeline.")

    with st.expander("Audit Trail & Token Consumption"):
        metrics = pipeline_result.get("execution_metrics", {})
        st.write(f"- **Total Tokens Consumed:** {metrics.get('total_tokens', 0)}")
        st.write(f"- **Estimated Model Cost:** ${metrics.get('estimated_cost_usd', 0.0):.6f}")
        st.write(f"- **Agents Executed:** {', '.join(metrics.get('agents_executed', []))}")
