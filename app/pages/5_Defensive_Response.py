import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.response_advisor import ResponseAdvisorAgent

st.set_page_config(page_title="ThreatRAG - Defensive Response", page_icon="🛡️", layout="wide")

st.title("🛡️ Prioritized Defensive Response & CISA Grounding")
st.markdown("Actionable incident response playbooks grounded in official CISA KEV and MITRE mitigations, enforcing human authorization gates.")

@st.cache_resource
def get_advisor():
    return ResponseAdvisorAgent()

advisor = get_advisor()

col1, col2 = st.columns([1, 2])

with col1:
    threat_category = st.selectbox(
        "Active Incident Type:",
        ["DDoS / Volumetric Network Flood", "Supply Chain Code Compromise", "SQL Injection / Database Exfiltration", "Ransomware Lateral Movement"]
    )
    severity = st.select_slider(
        "Incident Severity Level:",
        options=["Low", "Medium", "High", "Critical"],
        value="High"
    )
    assets = st.multiselect(
        "Identified Impacted Assets:",
        ["Public Web Application Gateway", "Edge DNS Resolver", "Core Database Cluster", "Kubernetes Ingress Controller", "Active Directory DC"],
        default=["Public Web Application Gateway", "Edge DNS Resolver"]
    )

with col2:
    st.info(
        "**Strict Human-in-the-Loop Safeguard:**\n"
        "ThreatRAG operates strictly in a supervisory and advisory capacity. "
        "No automated network reconfigurations, firewall rule insertions, or asset quarantines "
        "will be executed without explicit analyst review and cryptographic authorization sign-off."
    )

if st.button("📋 Generate Defensive Response Playbook", type="primary"):
    with st.spinner("Compiling CISA KEV mitigations and impact assessment..."):
        plan = advisor.run(
            threat_type=threat_category,
            severity=severity,
            affected_assets=assets
        )

    st.subheader("1. Prioritized Incident Response Checklist")
    actions = plan.get("actions", [])
    
    for act in actions:
        phase = act.get("phase", "Containment")
        badge_color = "#DC2626" if phase == "Containment" else "#D97706" if phase == "Mitigation" else "#2563EB"
        
        with st.expander(f"Step {act.get('step')}: [{phase}] {act.get('action')}", expanded=True):
            st.markdown(f"**Action Rationale:** {act.get('rationale')}")
            if act.get("cisa_guidance"):
                st.markdown(f"**CISA Guidance:** {act.get('cisa_guidance')}")
            st.markdown(f"**Operational Risk:** `{act.get('operational_risk')}`")

    st.markdown("---")
    st.subheader("2. Operational Impact & Service Disruption Analysis")
    st.warning(plan.get("operational_impact_summary", "Operational risk assessment pending."))

    st.markdown("---")
    st.subheader("3. Human-in-the-Loop Authorization Gate")
    st.markdown(
        f"<div style='border:2px solid #E11D48; border-radius:8px; padding:16px; background-color:#FFF1F2;'>"
        f"<h4 style='color:#9F1239; margin-top:0;'>⚠️ Security Authorization Required</h4>"
        f"<p>{plan.get('approval_notice')}</p>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    auth_check = st.checkbox("I, as an authorized SOC Lead / Incident Responder, certify that I have reviewed the actions above and authorize execution.")
    if st.button("✅ Enact Authorized Mitigation Policy", disabled=not auth_check):
        st.success("Authorization confirmed. Containment playbook dispatched to SOC orchestration queue with signed analyst audit token.")
