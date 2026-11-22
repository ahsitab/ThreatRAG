import streamlit as st
import os
import sys

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Define modern multi-page navigation for Streamlit Cloud & local execution
pages = [
    st.Page("app/dashboard.py", title="System Home", icon="🛡️", default=True),
    st.Page("app/pages/1_Overview.py", title="Knowledge Base Overview", icon="📊"),
    st.Page("app/pages/2_Threat_Analysis.py", title="Calibrated Threat Analysis", icon="🚨"),
    st.Page("app/pages/3_Similar_Incidents.py", title="Similar Incident Search", icon="🔍"),
    st.Page("app/pages/4_Evidence_Explanation.py", title="Evidence & Grounding", icon="📝"),
    st.Page("app/pages/5_Defensive_Response.py", title="Defensive Response Plan", icon="🛡️"),
    st.Page("app/pages/6_Knowledge_Manager.py", title="Knowledge Base Manager", icon="🗄️"),
    st.Page("app/pages/7_Research_Evaluation.py", title="Research Evaluation", icon="📈"),
]

pg = st.navigation(pages)
pg.run()
