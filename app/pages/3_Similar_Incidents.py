import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agents.incident_search import IncidentSearchAgent

st.set_page_config(page_title="ThreatRAG - Similar Incidents", page_icon="🔍", layout="wide")

st.title("🔍 Historical Incident Precedent Search")
st.markdown("Retrieve and compare documented real-world cybersecurity incidents matching observed threat behaviors using adaptive hybrid similarity.")

@st.cache_resource
def get_incident_searcher():
    return IncidentSearchAgent()

searcher = get_incident_searcher()

query_preset = st.selectbox(
    "Pre-configured Incident Scenarios:",
    [
        "Massive Mirai botnet volumetric DNS flood causing widespread DNS resolution disruption",
        "Sophisticated supply chain compromise inserting malicious DLL into software build pipeline (SUNBURST)",
        "Zero-day SQL injection vulnerability exploiting managed file transfer platform for data exfiltration (MOVEit)",
        "Unauthorized cloud credential access through public code repository leakage leading to cryptocurrency mining"
    ]
)

custom_query = st.text_input("Or Enter Custom Incident Query:", value=query_preset)
top_k = st.slider("Number of Historical Precedents to Retrieve:", min_value=1, max_value=5, value=3)

if st.button("🔎 Search Historical Incident Knowledge Base", type="primary"):
    with st.spinner("Executing hybrid retrieval across historical incident archive..."):
        results = searcher.run(query=custom_query, k=top_k)

    matches = results.get("historical_matches", [])
    st.subheader(f"Found {len(matches)} Relevant Incident Precedents")

    if results.get("summary_comparison"):
        st.info(f"**Comparative Synthesis:** {results.get('summary_comparison')}")

    for idx, match in enumerate(matches, 1):
        score = match.get("similarity_score", 0.0)
        with st.container():
            st.markdown(f"### #{idx}: {match.get('title')} `[ID: {match.get('incident_id')}]`")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Hybrid Similarity Score", f"{score * 100:.1f}%")
            c2.metric("Threat Category", match.get("threat_category", "Unknown"))
            techniques = match.get("att_ck_mappings", [])
            c3.write(f"**ATT&CK:** {', '.join(techniques) if techniques else 'N/A'}")

            st.markdown(f"**Observed Attack Behavior:**\n{match.get('observed_behavior', 'N/A')}")
            
            col_shared, col_diff = st.columns(2)
            with col_shared:
                st.markdown("**Shared Attack Characteristics:**")
                for s in match.get("shared_characteristics", []):
                    st.write(f"- {s}")
            with col_diff:
                st.markdown("**Key Operational Differences:**")
                for d in match.get("differences", []):
                    st.write(f"- {d}")

            st.markdown(f"**Documented Defensive Response:**\n{match.get('defensive_response', 'N/A')}")
            st.caption(f"Source Provenance: [{match.get('source_url', '#')}]({match.get('source_url', '#')})")
            st.markdown("---")
