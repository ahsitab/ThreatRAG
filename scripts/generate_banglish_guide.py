"""
scripts/generate_banglish_guide.py
==================================
Generates a comprehensive Banglish guide:
1. docs/ThreatRAG_Agent_Input_Output_Guide_Banglish.html
2. docs/ThreatRAG_Agent_Input_Output_Guide_Banglish.pdf
Explaining:
- Exactly what each agent does in simple Banglish
- What inputs to give for all use cases (with exact copy-paste examples)
- What outputs are returned on screen
- Embedded real app screenshots
"""

import os
import sys
import base64
from xhtml2pdf import pisa

def get_base64_image(rel_path):
    if os.path.exists(rel_path):
        with open(rel_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{b64}"
    return ""

def generate_guide():
    img_website = get_base64_image("ThreatRAG_IEEE_Access_Clean_Final_Source/ThreatRAG_IEEE_Access_Clean_Final/figures/website_home.png")
    img_system = get_base64_image("docs/screenshots/02_system_overview.png")
    img_eval = get_base64_image("docs/screenshots/07_research_evaluation.png")
    img_metrics = get_base64_image("ThreatRAG_IEEE_Access_Clean_Final_Source/ThreatRAG_IEEE_Access_Clean_Final/figures/ai506_metrics_comparison.png")
    img_calib = get_base64_image("ThreatRAG_IEEE_Access_Clean_Final_Source/ThreatRAG_IEEE_Access_Clean_Final/figures/classification_calibration.png")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ThreatRAG: Agent Ki Kaj Kore, Ki Input Diben & Ki Output Paben? (Banglish Complete Guide)</title>
<style>
  @page {{
    size: letter portrait;
    margin: 0.5in 0.5in 0.5in 0.5in;
  }}
  body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    line-height: 1.35;
    color: #0f172a;
    background: #ffffff;
  }}
  .header-box {{
    background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
    color: #ffffff;
    padding: 14pt 16pt;
    border-radius: 6pt;
    margin-bottom: 12pt;
  }}
  .header-tag {{
    font-size: 8pt;
    font-weight: bold;
    color: #f43f5e;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  h1 {{
    font-size: 16pt;
    font-weight: bold;
    margin: 4pt 0 4pt 0;
    line-height: 1.2;
    color: #ffffff;
  }}
  .subtitle {{
    font-size: 9.5pt;
    color: #cbd5e1;
    margin: 0 0 8pt 0;
  }}
  .meta-info {{
    font-size: 8pt;
    color: #94a3b8;
    border-top: 1pt solid rgba(255,255,255,0.2);
    padding-top: 6pt;
  }}
  h2 {{
    font-size: 11pt;
    font-weight: bold;
    color: #1e3a8a;
    border-bottom: 1.5pt solid #cbd5e1;
    padding-bottom: 3pt;
    margin: 12pt 0 6pt 0;
  }}
  h3 {{
    font-size: 9.5pt;
    font-weight: bold;
    color: #0284c7;
    margin: 8pt 0 3pt 0;
  }}
  p {{
    margin: 0 0 6pt 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 8pt 14pt;
    padding: 0;
  }}
  li {{
    margin-bottom: 3pt;
  }}
  .card {{
    background: #f8fafc;
    border: 1pt solid #cbd5e1;
    border-radius: 5pt;
    padding: 8pt 10pt;
    margin-bottom: 8pt;
  }}
  .card-highlight {{
    background: #eff6ff;
    border-left: 3.5pt solid #1e3a8a;
    padding: 6pt 8pt;
    margin: 6pt 0;
  }}
  .card-alert {{
    background: #fef2f2;
    border-left: 3.5pt solid #e11d48;
    padding: 6pt 8pt;
    margin: 6pt 0;
  }}
  .card-success {{
    background: #f0fdf4;
    border-left: 3.5pt solid #10b981;
    padding: 6pt 8pt;
    margin: 6pt 0;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin: 6pt 0;
    background: #ffffff;
  }}
  table.data-table th {{
    background: #1e3a8a;
    color: #ffffff;
    padding: 4pt 6pt;
    text-align: left;
    font-weight: bold;
  }}
  table.data-table td {{
    padding: 4pt 6pt;
    border-bottom: 0.6pt solid #e2e8f0;
    vertical-align: top;
  }}
  .badge {{
    background: #e0f2fe;
    color: #0369a1;
    font-weight: bold;
    padding: 1pt 4pt;
    border-radius: 2pt;
    font-family: Courier, monospace;
    font-size: 7.5pt;
  }}
  .badge-agent {{
    background: #f1f5f9;
    color: #1e3a8a;
    font-weight: bold;
    padding: 1pt 4pt;
    border-radius: 2pt;
    border: 0.5pt solid #cbd5e1;
  }}
  .code-box {{
    background: #0f172a;
    color: #38bdf8;
    padding: 6pt 8pt;
    border-radius: 4pt;
    font-family: Courier, monospace;
    font-size: 7.5pt;
    line-height: 1.3;
    margin: 5pt 0;
  }}
  .img-box {{
    text-align: center;
    margin: 8pt 0;
  }}
  .img-box img {{
    max-width: 95%;
    border: 1pt solid #cbd5e1;
    border-radius: 4pt;
  }}
  .img-caption {{
    font-size: 7.5pt;
    color: #64748b;
    font-style: italic;
    margin-top: 3pt;
  }}
  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- HEADER BLOCK -->
<div class="header-box">
  <div class="header-tag">ThreatRAG: Master Banglish Operational Guide &amp; Viva Manual</div>
  <h1>ThreatRAG: Agent-ra Ki Kaj Kore, Ki Input Diben &amp; Ki Output Paben?</h1>
  <div class="subtitle">MSc Project (AIML-507 / AI506) — Ekdom Shohoj Bhashay Shob Use Case, Input-Output &amp; App Screenshots</div>
  <div class="meta-info">
    <strong>Author / Candidate:</strong> Asfar Hossain Sitab &bull; 
    <strong>Course:</strong> AIML-507 / AI506 &bull; 
    <strong>Live App:</strong> http://localhost:8501 &bull; 
    <strong>GitHub:</strong> https://github.com/ahsitab/ThreatRAG
  </div>
</div>

<!-- SECTION 1 -->
<h2>1. ThreatRAG Asol-e Ki? Keno Eti Shadharon Chatbot Noy?</h2>
<p>Apnar mone shobcheye boro proshno hote pare: <em>"Ami ki baniyechi? Eta ki shudhu ekta ChatGPT ba bot?"</em></p>
<div class="card-highlight">
  <strong>Shohoj Kothay:</strong> ThreatRAG kono shadharon chatbot noy! Eta holo ekta <strong>Autonomous Multi-Agent Cybersecurity Co-Pilot</strong>। 
  Ekta real Security Operations Center (SOC)-e protidin hazar hazar suspicious network alert ashe। Shadharon ChatGPT ba LLM-ke jodi security query kora hoy, shey <strong>fake CVE number, vul firewall command, ba hallucinated logic</strong> banaye dey—jar karone server crash korte pare।
  <br><br>
  ThreatRAG ei shomossha solve kore! Ekhane <strong>4-ta Specialist Agent</strong> mile ekta disciplined team-er moto kaj kore, official MITRE ATT&amp;CK ebong CISA KEV data theke proman (evidence) khuje ber kore, ebong human analyst-er sign-off chhara kono action dispatch kore na।
</div>

<div class="img-box">
  <img src="{img_website}" style="width: 500pt;">
  <div class="img-caption">Figure 1: ThreatRAG Multi-Page Interactive Dashboard (Streamlit UI running live on Port 8501)</div>
</div>

<!-- SECTION 2 -->
<h2>2. Apnar 4-ta Agent Asol-e Ki Kaj Korche? (Real-Life Analogy)</h2>
<p>System-e jokhon kono network telemetry ba analyst query ashe, tokhon shob kaj ekta single model kore na। 4-jon agent nijeder moddhe responsibility divide kore ney:</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 25%;">Agent Name</th>
      <th style="width: 25%;">Real-Life Role</th>
      <th style="width: 50%;">Behind the Scenes Ki Kaj Kore?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Coordinator / Planner Agent</strong><br><span class="badge">coordinator.py</span></td>
      <td><strong>The Project Manager</strong></td>
      <td>User er query pore bujhe je ki dhoroner kaj dorkar। Ekta structured workflow plan banay (e.g. Threat ID lagbe, naki Incident Search lagbe)। Baki specialist agent-der execution order manage kore ebong verification fail korle <strong>Feedback Loop</strong> chalay (max 2 retries)।</td>
    </tr>
    <tr>
      <td><strong>2. Cybersecurity Retrieval Specialist</strong><br><span class="badge">retrieval_agent.py</span></td>
      <td><strong>The Research Librarian</strong></td>
      <td>Apnar 1,074-ta preprocessed security chunk (MITRE ATT&amp;CK, CISA KEV, historical incidents) theke <strong>Tri-Modal Hybrid Search</strong> kore। SentenceTransformer (dense vector) + BM25Okapi (sparse keyword) + Network Port matcher run kore top-5 evidence khuje aney।</td>
    </tr>
    <tr>
      <td><strong>3. Security Reasoning Specialist</strong><br><span class="badge">reasoning_agent.py</span></td>
      <td><strong>The Senior SOC Analyst &amp; ML Expert</strong></td>
      <td>Trained <strong>LightGBM Classifier</strong> chalay। Anomaly-r raw score-ke <strong>Platt Scaling</strong> diye calibrate kore exact probability (e.g. 99.98% confidence) ber kore। Tarpor behavior-ke MITRE technique (e.g. T1498.001)-e map kore ebong empirical facts theke hypotheses alada kore।</td>
    </tr>
    <tr>
      <td><strong>4. Evidence Verification Specialist</strong><br><span class="badge">verification_agent.py</span></td>
      <td><strong>The Strict Auditor &amp; Fact-Checker</strong></td>
      <td>Reasoning Agent-er answer check kore। Answer-er moddhe bracketed citation <span class="badge">[mitre-T1498.001]</span> asholei retrieved chunk theke ashche kina audit kore। Jodi fake claim ba low evidence pay, tokhon reject kore Coordinator-ke bole: <em>"Evidence kom, abar khojo!"</em> (Feedback Loop)। Jodi corpus-e asholei kono info na thake, tokhon fake answer na diye bole: <em>"Insufficient Evidence, I Abstain"</em>।</td>
    </tr>
  </tbody>
</table>

<div class="card-success">
  <strong>Human-in-the-Loop Safety Gate:</strong> Shob agent kaj sesh korle Playbook toiri hoy। Kintu system <strong>kono din nij theke server shut down ba firewall block korbe na</strong>। UI-te ekta mandatory checkbox thakbe: Analyst jokhon check korbe, tokhon-i action execute hobe।
</div>

<div class="page-break"></div>

<!-- SECTION 3 -->
<h2>3. Shobgulo Use Case: Ki Input Diben &amp; Ki Output Paben?</h2>
<p>Apnar system-e 5-ti prodhan Use Case ache। Niche prottekta use case-er jonno <strong>exact ki input likhben</strong>, <strong>checkbox ki select korben</strong>, ebong <strong>screen-e ki output ashbe</strong> ta deya holo:</p>

<!-- USE CASE 1 -->
<div class="card">
  <h3 style="color: #e11d48; margin-top: 0;">Use Case 1: Active DDoS / Network Flood Anomaly Dhora (With Telemetry)</h3>
  <p><strong>Goal:</strong> Live network flow data diye check kora je kono cyber attack hocche kina ebong tar exact confidence score ber kora।</p>
  
  <div class="card-highlight">
    <strong>Kothay Diben:</strong> Streamlit Dashboard theke <strong>"2_Threat_Analysis"</strong> page-e jan।
    <br><br>
    <strong>Ki Input Diben (Copy &amp; Paste):</strong>
    <div class="code-box">
Incident Description:<br>
"Inbound volumetric packet flood on destination port 80 exceeding 85,000 pkts/s with short flow duration (8500 us). Identify threat, map ATT&amp;CK, and advise containment."
    </div>
    <strong>Checkbox &amp; Telemetry Inputs:</strong>
    <ul>
      <li>Tick din: <strong>[x] Include Structured NetFlow Telemetry</strong></li>
      <li>Destination Port: <code>80</code></li>
      <li>Flow Packets/s: <code>85000</code></li>
      <li>Flow Duration: <code>8500</code></li>
      <li>Total Fwd Packets: <code>5000</code></li>
    </ul>
    Click korun: <strong>"Run ThreatRAG Analysis"</strong>
  </div>

  <div class="card-success">
    <strong>Screen-e Ki Output Paben (Exact Result):</strong>
    <ol>
      <li><strong>Threat Classification:</strong> <span class="badge">Distributed Denial of Service (DDoS)</span></li>
      <li><strong>Calibrated Probability:</strong> <span class="badge">99.98% Confidence</span> (Uncertainty: Low &bull; Platt Scaled &bull; ECE = 0.0005)</li>
      <li><strong>MITRE ATT&amp;CK Mapping:</strong> <span class="badge">T1498.001 (Network Denial of Service: Direct Network Flood)</span></li>
      <li><strong>Observable Agent Trace:</strong> Expandable cards jekhane Coordinator Plan, Retrieval chunks (similarity 0.82), Reasoning inference, ebong Verification Approved status dekha jabe।</li>
      <li><strong>Defensive Containment Playbook:</strong>
        <ul>
          <li>Phase 1 (Immediate Containment): Engage upstream DDoS scrubbing provider (Cloudflare/Akamai) within 15 minutes.</li>
          <li>Phase 2 (Eradication): Rate-limit SYN packets on border edge router to 10,000 pkts/s per source prefix.</li>
          <li>Phase 3 (Human Gate): "Authorize Mitigation Execution" checkbox with analyst digital signature.</li>
        </ul>
      </li>
    </ol>
  </div>
</div>

<!-- USE CASE 2 -->
<div class="card">
  <h3 style="color: #0284c7; margin-top: 0;">Use Case 2: Otiter Bikkhato Cyber Attack-er Sathe Tulona (Incident Similarity)</h3>
  <p><strong>Goal:</strong> Bortoman abnormal traffic otite ghote jaowa boro boro incident (e.g. Mirai Dyn DNS, SolarWinds, MOVEit)-er sathe mile kina ta ber kora।</p>
  
  <div class="card-highlight">
    <strong>Kothay Diben:</strong> <strong>"2_Threat_Analysis"</strong> ba <strong>"4_Similar_Incidents"</strong> page-e jan।
    <br><br>
    <strong>Ki Input Diben (Copy &amp; Paste):</strong>
    <div class="code-box">
Query Text:<br>
"How does an active port 80 SYN flood compare with the 2016 Dyn DNS incident?"
    </div>
    Click korun: <strong>"Run Analysis"</strong>
  </div>

  <div class="card-success">
    <strong>Screen-e Ki Output Paben (Exact Result):</strong>
    <ol>
      <li><strong>Matched Historical Incident:</strong> <span class="badge">2016 Dyn DNS Attack (Mirai Botnet)</span> (Similarity Score: <code>0.84</code>)</li>
      <li><strong>Protocol Disambiguation (Senior Analyst Insights):</strong>
        <ul>
          <li><em>Shared Traits:</em> Both exhibit massive packet volume aimed at edge service saturation.</li>
          <li><em>Crucial Difference:</em> The current flow targets web application servers over <strong>TCP Port 80 (HTTP)</strong>, whereas Dyn targeted DNS infrastructure over <strong>UDP Port 53</strong> using infected IoT cameras and DVRs.</li>
        </ul>
      </li>
      <li><strong>Lessons Learned:</strong> Relying solely on local firewalls fails during multi-gigabit volumetric floods; upstream anycast routing is required.</li>
    </ol>
  </div>
</div>

<!-- USE CASE 3 -->
<div class="card">
  <h3 style="color: #10b981; margin-top: 0;">Use Case 3: Zero-Day Exploit Bujha (MITRE ATT&amp;CK &amp; CISA KEV Grounding)</h3>
  <p><strong>Goal:</strong> Kono specific vulnerability ba exploit-er technical detail jante chawa (e.g. MOVEit Transfer CVE-2023-34362)।</p>
  
  <div class="card-highlight">
    <strong>Ki Input Diben (Copy &amp; Paste):</strong>
    <div class="code-box">
Query Text:<br>
"Explain the technical mechanism of MOVEit Transfer exploit CVE-2023-34362 and give remediation."
    </div>
  </div>

  <div class="card-success">
    <strong>Screen-e Ki Output Paben:</strong>
    <ol>
      <li><strong>Empirical Facts (Promanito Tottho):</strong> SQL injection flaw in <code>guestaccess.aspx</code> allowing unauthenticated attackers to obtain active database sessions.</li>
      <li><strong>ATT&amp;CK Grounding:</strong> <span class="badge">T1190 (Exploit Public-Facing Application)</span> and <span class="badge">T1059.001 (PowerShell)</span>.</li>
      <li><strong>Analytical Hypotheses:</strong> Attacker is attempting web shell deployment (<code>human2.aspx</code>) to exfiltrate Azure blob storage assets.</li>
      <li><strong>Citation Audit:</strong> 100% precision with exact source link to CISA KEV Advisory date.</li>
    </ol>
  </div>
</div>

<div class="page-break"></div>

<!-- USE CASE 4 -->
<div class="card">
  <h3 style="color: #7c3aed; margin-top: 0;">Use Case 4: Hallucination Test / Out-of-Domain Query (Insufficient Evidence Handling)</h3>
  <p><strong>Goal:</strong> Sir-ke dekhano je apnar system fake/banano proshno korle ChatGPT-r moto fake answer banay na, balki honesty-r sathe bolbe <em>"Data nai"</em>।</p>
  
  <div class="card-alert">
    <strong>Ki Input Diben (Bujhe-shune banano science-fiction proshno):</strong>
    <div class="code-box">
Query Text:<br>
"Anomalous quantum tachyon modulation detected across local Ethernet switch ports."
    </div>
  </div>

  <div class="card-success">
    <strong>Screen-e Ki Output Paben (Eti Sir Khub Pochondo Korben!):</strong>
    <ol>
      <li><strong>Retrieval Specialist Status:</strong> Zero passages found with high similarity (Mean score &lt; 0.15).</li>
      <li><strong>Verification Specialist Alert:</strong> <span class="badge" style="background:#fee2e2; color:#b91c1c;">INSUFFICIENT_EVIDENCE DETECTED</span>.</li>
      <li><strong>Feedback Loop:</strong> Coordinator 1-bar re-query kore confirm hoy je corpus-e 'quantum tachyon' bole kono legitimate cyber threat nai।</li>
      <li><strong>Final Principled Abstention Output:</strong> 
        <em>"WARNING: The query references terms not substantiated by the knowledge base. No verified MITRE ATT&amp;CK techniques or CISA CVE advisories exist for quantum tachyon modulation. ThreatRAG abstains from generating speculative mitigations to prevent operational disruption."</em>
      </li>
    </ol>
  </div>
</div>

<!-- USE CASE 5 -->
<div class="card">
  <h3 style="color: #1e3a8a; margin-top: 0;">Use Case 5: Single-Agent vs Multi-Agent Head-to-Head Comparison Page</h3>
  <p><strong>Goal:</strong> Specification-er requirement onujayi Single-Agent Baseline-er sathe Multi-Agent ThreatRAG-er side-by-side tulona live dekhano।</p>
  
  <div class="card-highlight">
    <strong>Kothay Diben:</strong> Streamlit Dashboard-er <strong>"8_AI506_Baseline_Comparison"</strong> page-e jan।
    <br><br>
    <strong>Ki Korben:</strong>
    <ul>
      <li>Dropdown theke question select korun: <code>TID-001 (Port 80 Inbound Flood)</code></li>
      <li>Click korun: <strong>"Run Head-to-Head Comparison"</strong></li>
    </ul>
  </div>

  <div class="card-success">
    <strong>Screen-e Ki Output Paben:</strong>
    <table class="data-table">
      <thead>
        <tr>
          <th>Evaluated Feature</th>
          <th>Left Side: Conventional Single-Agent RAG</th>
          <th>Right Side: Proposed Multi-Agent ThreatRAG</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Workflow &amp; Trace</strong></td>
          <td>Kono agent trace nai; flat ekbar search kore answer banay।</td>
          <td>Visual Mermaid workflow diagram + Step-by-step 4-agent trace card।</td>
        </tr>
        <tr>
          <td><strong>Probability Calibration</strong></td>
          <td>Raw uncalibrated guessing (overconfident)।</td>
          <td><strong>Platt-calibrated 99.98% confidence</strong> (ECE = 0.0005)।</td>
        </tr>
        <tr>
          <td><strong>Citation Precision</strong></td>
          <td>50.0% (Majhe majhe fake chunk ID cite kore)।</td>
          <td><strong>100.0% (Zero hallucinated citations)</strong>।</td>
        </tr>
        <tr>
          <td><strong>Latency vs Quality</strong></td>
          <td>0.03 seconds (Dhruto kintu unreliable)।</td>
          <td>3.56 seconds (Careful multi-agent deliberation)।</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="img-box">
  <img src="{img_metrics}" style="width: 480pt;">
  <div class="img-caption">Figure 2: Measured Benchmark Performance: Single-Agent vs Multi-Agent ThreatRAG across 50 Questions</div>
</div>

<!-- SECTION 4 -->
<h2>4. Viva Board-e Sir-ke 3-Minute-e Kibhabe Bujhaben? (Exact Pitch)</h2>
<p>Sir jokhon bolben: <em>"Sitab, tomar project ta ki kore ebong architecture ta bujhao"</em>, tokhon ei point gulo bolben:</p>
<ol>
  <li><strong>Intro:</strong> <em>"Sir, ThreatRAG holo ekta Explainable Multi-Agent Cybersecurity System। Amader base paper holo ACL 2025-er <strong>MAIN-RAG</strong>, jekhane proof kora hoyeche je multi-agent filtering single-agent-er cheye onek beshi accurate।"</em></li>
  <li><strong>The 4 Agents:</strong> <em>"Amra 4-ta logical agent implement korechi: <strong>Coordinator</strong> plan kore, <strong>Retrieval Specialist</strong> 1,074-ta MITRE ATT&amp;CK chunk theke hybrid search kore, <strong>Reasoning Specialist</strong> LightGBM model diye 99.98% Platt-calibrated probability ber kore, ebong <strong>Verification Specialist</strong> citation audit kore।"</em></li>
  <li><strong>The Feedback Loop:</strong> <em>"Jodi retrieved evidence kom thake ba reasoning incomplete hoy, Verification Agent Coordinator-ke bole re-retrieval korte (Feedback Loop, max 2 retries)। Ebong out-of-domain fake proshno korle amader system hallucinate na kore safely <strong>Abstain</strong> kore।"</em></li>
  <li><strong>Baseline Comparison:</strong> <em>"Amra 50-ta question benchmark-e measure korechi: Conventional Single-Agent RAG-er accuracy 0% (strict match) theke Multi-Agent-e <strong>12% (passing) ebong correctness score 0.11 theke 0.34 (+207% relative increase)</strong> hoyeche, citation precision 50% theke <strong>100%</strong> hoyeche।"</em></li>
</ol>

<div class="card-highlight" style="text-align: center;">
  <strong>Shob Kisu Ready:</strong> Live Streamlit Dashboard (Port 8501), FastAPI (Port 8000), IEEE Conference Report PDF, 12-Slide Presentation PPTX, ebong 22-cell Executed Research Notebook apnar repository-te active ache!
</div>

</body>
</html>
"""

    out_html = "docs/ThreatRAG_Agent_Input_Output_Guide_Banglish.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[HTML] Generated {out_html}")

    out_pdf = "docs/ThreatRAG_Agent_Input_Output_Guide_Banglish.pdf"
    with open(out_html, "r", encoding="utf-8") as f:
        html = f.read()
    with open(out_pdf, "wb") as f:
        res = pisa.CreatePDF(html, dest=f)

    if res.err == 0:
        print(f"[SUCCESS] Compiled PDF: {out_pdf} ({os.path.getsize(out_pdf)} bytes)")
    else:
        print(f"[WARN] xhtml2pdf returned error code {res.err}")

if __name__ == "__main__":
    generate_guide()
