import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(
    page_title="ThreatRAG - Quickstart Tutorial",
    page_icon="📖",
    layout="wide"
)

# Custom header styling
st.markdown("""
<style>
    .tutorial-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.3rem;
    }
    .tutorial-sub {
        font-size: 1.15rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .step-card {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .badge-agent {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="tutorial-header">📖 Quickstart Tutorial: How to Use ThreatRAG</div>', unsafe_allow_html=True)
st.markdown('<div class="tutorial-sub">A simple, beginner-friendly guide to understanding inputs, outputs, and the 4 AI agents.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# SECTION 1: WHAT IS THREATRAG IN SIMPLE WORDS?
# -------------------------------------------------------------
st.subheader("1. What is ThreatRAG in Simple Words?")

c1, c2 = st.columns([3, 2])
with c1:
    st.markdown("""
    Imagine you are a security officer protecting a bank's website. At 2:00 AM, the server suddenly stops responding. 
    Thousands of strange connections are hitting your website. You need to know:
    1. **What kind of attack is this?**
    2. **Which cybercrime technique is being used?**
    3. **How do we stop it right now to save our servers?**

    Normally, you would wake up an entire team of senior cybersecurity experts. **ThreatRAG is an AI cybersecurity team** 
    that does this investigation for you in **2 seconds**!

    #### 💡 Why not just use ChatGPT?
    - ChatGPT can **make up fake CVE codes** or give wrong firewall rules (called *Hallucination*).
    - **ThreatRAG never guesses.** It searches official databases (*MITRE ATT&CK, CISA Known Exploited Vulnerabilities, and real historical incident logs*) 
      and proves every single claim with verified evidence. If there is no proof, it honestly tells you: *"No technical evidence found."*
    """)

with c2:
    st.info("""
    ### 🎯 The 3-Step Workflow
    
    1. **Step 1: Input the Symptoms**  
       Pick one of our pre-built examples or paste a security alert.
       
    2. **Step 2: Watch 4 Agents Collaborate**  
       The Planner, Librarian, Analyst, and Auditor investigate in real-time.
       
    3. **Step 3: Get Your Action Plan**  
       See the exact attack name, danger level, and step-by-step firewall commands!
    """)

st.markdown("---")

# -------------------------------------------------------------
# SECTION 2: MEET YOUR 4 AI AGENTS (THE DETECTIVE TEAM)
# -------------------------------------------------------------
st.subheader("2. Meet the 4 AI Agents: Your Digital Investigation Squad")
st.markdown("Instead of one model doing everything, ThreatRAG divides the work among **4 specialized AI agents**:")

col_ag1, col_ag2 = st.columns(2)
with col_ag1:
    st.markdown("""
    <div class="step-card" style="border-left: 5px solid #2563EB;">
        <h4 style="color: #1E40AF; margin-top:0;">🕵️‍♂️ Agent 1: The Coordinator (Team Manager)</h4>
        <p><strong>What it does:</strong> Reads your security alert, figures out what kind of problem it is (DDoS, Malware, or Data Leak), and assigns tasks to the specialist agents.</p>
        <span class="badge-agent" style="background:#DBEAFE; color:#1E40AF;">Input: Raw User Alert</span>
        <span class="badge-agent" style="background:#EDE9FE; color:#5B21B6;">Output: Action Plan</span>
    </div>
    
    <div class="step-card" style="border-left: 5px solid #D97706;">
        <h4 style="color: #92400E; margin-top:0;">🧠 Agent 3: Reasoning Specialist (Senior SOC Analyst)</h4>
        <p><strong>What it does:</strong> Compares the evidence against your server symptoms. It names the exact attack, maps the official <strong>MITRE ATT&CK technique code</strong> (like T1499), and writes the defensive prescription.</p>
        <span class="badge-agent" style="background:#FEF3C7; color:#92400E;">Input: Evidence Passages</span>
        <span class="badge-agent" style="background:#FEE2E2; color:#991B1B;">Output: Triage & Fixes</span>
    </div>
    """, unsafe_allow_html=True)

with col_ag2:
    st.markdown("""
    <div class="step-card" style="border-left: 5px solid #059669;">
        <h4 style="color: #065F46; margin-top:0;">📚 Agent 2: Retrieval Specialist (Cyber Librarian)</h4>
        <p><strong>What it does:</strong> Searches through 1,074 verified knowledge documents using Hybrid Search (Keywords + Semantic Vectors) to fetch the top 5 most relevant proof passages.</p>
        <span class="badge-agent" style="background:#DCFCE7; color:#166534;">Input: Search Keywords</span>
        <span class="badge-agent" style="background:#D1FAE5; color:#065F46;">Output: Verified Evidence</span>
    </div>
    
    <div class="step-card" style="border-left: 5px solid #7C3AED;">
        <h4 style="color: #6B21A8; margin-top:0;">⚖️ Agent 4: Verification Specialist (Strict Auditor)</h4>
        <p><strong>What it does:</strong> The ultimate judge. It checks every single sentence written by Agent 3 against the official documents. If any claim is unproven, it triggers a <strong>Feedback Loop</strong> saying: <em>"Find better evidence!"</em></p>
        <span class="badge-agent" style="background:#F3E8FF; color:#6B21A8;">Input: Draft Report</span>
        <span class="badge-agent" style="background:#DCFCE7; color:#166534;">Output: Verified Stamp (Score)</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# SECTION 3: WHAT IS AN INPUT & WHAT IS AN OUTPUT?
# -------------------------------------------------------------
st.subheader("3. What is an Input and What is an Output?")

in_col, out_col = st.columns(2)

with in_col:
    st.markdown("""
    ### 📥 What is an INPUT?
    In ThreatRAG, an input is **not a casual greeting**. It is **the evidence from a crime scene** or **the symptoms of an ailing server**:
    
    1. **Incident Description (Text):**  
       A short explanation of what you are seeing.  
       *Example:* `"Sudden flood of 1.2M SYN packets per second targeting port 80..."`
    2. **Destination Port (Number):**  
       The network door being knocked on (e.g. `80` for Web, `443` for Secure Web, `22` for SSH).
    3. **Packet Rate (Number):**  
       How fast data is arriving (e.g. `1,200,000` packets/second indicates a huge DDoS flood).
    4. **Duration (Microseconds):**  
       How long the abnormal traffic lasted.
    """)

with out_col:
    st.markdown("""
    ### 📤 What is an OUTPUT?
    The output is a **certified medical prescription for your computer network**:
    
    1. **Identified Threat Name:**  
       The exact scientific name of the attack (*e.g. TCP SYN Flood Denial of Service*).
    2. **MITRE ATT&CK Code:**  
       The international cybersecurity standard tag (*e.g. T1499.002*).
    3. **Danger Rating (Severity):**  
       Tells you if this is `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
    4. **Groundedness Score:**  
       Proof that the answer is backed by real documents (*e.g. 0.94 / 1.00*).
    5. **Defensive Action Plan:**  
       Exact commands to configure your firewall and block the attack immediately!
    """)

st.markdown("---")

# -------------------------------------------------------------
# SECTION 4: IN-BUILT EXAMPLES — CLICK & TEST INSTANTLY!
# -------------------------------------------------------------
st.subheader("4. Built-in Examples (Ready to Try with 1 Click!)")
st.markdown("You do not need to invent inputs yourself! Pick any of these **5 real-world scenarios** to see how the system behaves:")

ex_tabs = st.tabs([
    "🔥 Example 1: Web DDoS Attack",
    "🔓 Example 2: MOVEit SQL Injection",
    "🤖 Example 3: Mirai IoT Botnet",
    "🟢 Example 4: Normal Office Web",
    "⚠️ Example 5: Zero-Evidence Test"
])

with ex_tabs[0]:
    st.markdown("""
    #### Scenario: Massive Port 80 Web Server Flood
    - **What happened:** Attackers sent 1.2 million fake connection requests per second to crash an internal web server.
    - **What you will see:** ThreatRAG identifies `TCP SYN Flood (T1499.002)`, marks it as **CRITICAL**, and instructs you to enable **SYN Cookies** on your border firewalls.
    """)
    st.code("Telemetry shows sudden flood of 1.2 million SYN packets per second on destination port 80 targeting internal web servers. Traffic originates from over 8,500 spoofed external IP addresses.", language="text")

with ex_tabs[1]:
    st.markdown("""
    #### Scenario: MOVEit Transfer Enterprise Zero-Day (CVE-2023-34362)
    - **What happened:** Hackers exploited an SQL injection vulnerability in a file transfer web application to steal sensitive documents.
    - **What you will see:** The system traces the entire 4-step attack chain (`T1190` -> Unauthorized Session -> `human2.aspx` webshell -> Azure Blob data theft).
    """)
    st.code("Explain the attack chain of CVE-2023-34362 MOVEit Transfer SQL injection vulnerability. How did threat actors exploit the web application to achieve remote code execution and exfiltrate sensitive files?", language="text")

with ex_tabs[2]:
    st.markdown("""
    #### Scenario: Mirai Botnet IoT Distributed Attack (Historical Search)
    - **What happened:** Millions of hacked smart cameras and DVRs were used to take down major internet DNS providers in 2016.
    - **What you will see:** ThreatRAG compares this to historical incident logs and finds an **87.4% match with the Dyn DNS Cyberattack of October 2016**.
    """)
    st.code("Find historical major cybersecurity incidents similar to a large-scale Mirai botnet attack utilizing compromised IoT devices for distributed DNS amplification.", language="text")

with ex_tabs[3]:
    st.markdown("""
    #### Scenario: Harmless Everyday Office Web Browsing (Benign)
    - **What happened:** An employee opened cloud applications and Google Drive over standard HTTPS (Port 443).
    - **What you will see:** ThreatRAG classifies this as **BENIGN (Safe)** with 0.00% threat probability and does not suggest unnecessary firewall blocks.
    """)
    st.code("Standard outbound user HTTPS session to cloud services. Normal symmetric packet flow and standard duration on port 443.", language="text")

with ex_tabs[4]:
    st.markdown("""
    #### Scenario: Fake Alien Worm (Hallucination & Grounding Test)
    - **What happened:** A made-up question asking about a fictional "Quantum Tachyon Worm in 1994".
    - **What you will see:** Standard ChatGPT would make up a fake story. **ThreatRAG safely says:**  
      `[ThreatRAG Abstention Notice]: No verified technical evidence found in MITRE ATT&CK or CISA KEV. The system abstains from answering to prevent false claims.`
    """)
    st.code("What is the zero-day exploit mechanism of the Quantum Tachyon Worm targeting deep sea submarine fiber optic routers in 1994?", language="text")

st.markdown("---")

# Quick launch button
st.markdown("### Ready to Try It Yourself?")
st.markdown("Click below to go directly to the **Threat Analysis Workbench** where you can select any of these presets with 1 click!")

if st.button("🚀 Go to Threat Analysis Workbench", type="primary", use_container_width=True):
    st.switch_page("app/pages/2_Threat_Analysis.py")
