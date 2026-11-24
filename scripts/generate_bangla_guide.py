"""
ThreatRAG: Complete Bengali (বাংলা) Operational and Input/Output Manual Generator
Produces:
  1. docs/ThreatRAG_Agent_Input_Output_Guide_Bangla.html
  2. docs/ThreatRAG_Agent_Input_Output_Guide_Bangla.pdf (via Edge/Chrome headless)
"""

import os
import sys
import base64
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

HTML_OUT = DOCS_DIR / "ThreatRAG_Agent_Input_Output_Guide_Bangla.html"
PDF_OUT = DOCS_DIR / "ThreatRAG_Agent_Input_Output_Guide_Bangla.pdf"

def get_base64_img(rel_path: str) -> str:
    p = BASE_DIR / rel_path
    if p.exists():
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = p.suffix.lower().replace(".", "")
            if ext == "jpg":
                ext = "jpeg"
            return f"data:image/{ext};base64,{data}"
    return ""

img_home = get_base64_img("ThreatRAG_IEEE_Access_Clean_Final_Source/ThreatRAG_IEEE_Access_Clean_Final/figures/website_home.png")
img_overview = get_base64_img("docs/screenshots/02_system_overview.png")
img_eval = get_base64_img("docs/screenshots/07_research_evaluation.png")
img_metrics = get_base64_img("reports/figures/ai506_metrics_comparison.png")

html_content = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<title>ThreatRAG: মাল্টি-এজেন্ট সিস্টেমের পূর্ণাঙ্গ ব্যবহার নির্দেশিকা ও ইনপুট-আউটপুট ম্যানুয়াল</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      color: #64748b;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  body {{
    font-family: 'Kalpurush', 'Hind Siliguri', 'Nirmala UI', sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.65;
    font-size: 13.5px;
    margin: 0;
    padding: 0;
  }}

  .header-container {{
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 12px;
    margin-bottom: 22px;
  }}

  .badge-container {{
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    flex-wrap: wrap;
  }}

  .badge {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .badge-blue {{ background-color: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }}
  .badge-green {{ background-color: #dcfce7; color: #166534; border: 1px solid #86efac; }}
  .badge-purple {{ background-color: #f3e8ff; color: #6b21a8; border: 1px solid #d8b4fe; }}
  .badge-amber {{ background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}

  h1 {{
    font-size: 22px;
    color: #0f172a;
    margin: 4px 0 8px 0;
    font-weight: 700;
  }}

  .meta-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 12px;
    margin-top: 10px;
  }}

  .meta-item strong {{
    color: #334155;
  }}

  h2 {{
    font-size: 16px;
    color: #1e3a8a;
    border-left: 4px solid #2563eb;
    padding-left: 10px;
    margin-top: 24px;
    margin-bottom: 12px;
    font-weight: 700;
  }}

  h3 {{
    font-size: 14px;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 6px;
    font-weight: 600;
  }}

  p {{
    margin: 0 0 10px 0;
    text-align: justify;
  }}

  .agent-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}

  .agent-card.coord {{ border-left: 5px solid #2563eb; background: #f8fafc; }}
  .agent-card.retrieval {{ border-left: 5px solid #059669; background: #f0fdf4; }}
  .agent-card.reasoning {{ border-left: 5px solid #d97706; background: #fffbeb; }}
  .agent-card.verify {{ border-left: 5px solid #7c3aed; background: #faf5ff; }}

  .agent-title {{
    font-size: 13.5px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
  }}

  .use-case-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 16px;
    page-break-inside: avoid;
  }}

  .use-case-header {{
    font-size: 14px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
  }}

  .code-block {{
    font-family: 'Fira Code', Consolas, monospace;
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 5px;
    font-size: 11.5px;
    line-height: 1.45;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 6px 0 10px 0;
  }}

  .output-box {{
    background: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 5px;
    padding: 10px 12px;
    font-size: 12px;
    margin-top: 6px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 12px;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    text-align: left;
  }}

  th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}

  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  .img-container {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
  }}

  .img-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
  }}

  .img-caption {{
    font-size: 11px;
    color: #64748b;
    margin-top: 5px;
    font-style: italic;
  }}

  .callout {{
    padding: 10px 14px;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 12.5px;
  }}
  .callout-info {{ background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }}
  .callout-success {{ background: #ecfdf5; border-left: 4px solid #10b981; color: #065f46; }}
  .callout-warning {{ background: #fffbeb; border-left: 4px solid #f59e0b; color: #92400e; }}

  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header-container">
  <div class="badge-container">
    <span class="badge badge-blue">ThreatRAG Framework</span>
    <span class="badge badge-purple">Multi-Agent RAG</span>
    <span class="badge badge-green">AI506 / AIML-507 Compliant</span>
    <span class="badge badge-amber">Operational Manual</span>
  </div>
  <h1>থ্রেটর‍্যাগ (ThreatRAG): মাল্টি-এজেন্ট সিস্টেমের পূর্ণাঙ্গ ব্যবহার নির্দেশিকা ও ইনপুট-আউটপুট ম্যানুয়াল</h1>
  <div style="font-size: 12.5px; color: #475569;">
    সাইবার সিকিউরিটি থ্রেট ইন্টেলিজেন্স ও ইনসিডেন্ট রেসপন্সের জন্য ৪-এজেন্ট কোলাবোরেশন, ড্যাশবোর্ড ইনপুট গাইড এবং ফলাফল বিশ্লেষণ
  </div>

  <div class="meta-grid">
    <div class="meta-item"><strong>গবেষক ও শিক্ষার্থী:</strong> Asfar Hossain Sitab</div>
    <div class="meta-item"><strong>কোর্স কোড ও নাম:</strong> AIML-507 / AI506 (MSc in AI & Cyber Security)</div>
    <div class="meta-item"><strong>বেস রিসার্চ পেপার:</strong> MAIN-RAG (ACL 2025) & MASS-RAG (ACL 2026)</div>
    <div class="meta-item"><strong>সিস্টেম আর্কিটেকচার:</strong> 4-Agent LangGraph Workflow with Verification Feedback Loop</div>
  </div>
</div>

<div class="callout callout-info">
  <strong>সংক্ষিপ্ত উদ্দেশ্য:</strong> এই ডকুমেন্টটি তৈরি করা হয়েছে যেন শিক্ষার্থী ও ব্যবহারকারী পরিষ্কারভাবে বুঝতে পারেন সিস্টেমে কী ইনপুট দিতে হবে, অন্তরালে ৪টি অটোনোমাস এজেন্ট কীভাবে পরস্পর তথ্য আদান-প্রদান করে, কী আউটপুট প্রদর্শিত হবে এবং ভাইভা বোর্ডে পরীক্ষককে কীভাবে সিস্টেমটি ৩ মিনিটে ব্যাখ্যা করবেন।
</div>

<h2>১. থ্রেটর‍্যাগ (ThreatRAG) কী? কেন এটি সাধারণ চ্যাটবট বা ChatGPT নয়?</h2>
<p>
  সাধারণ জেনারেটিভ এআই (যেমন সরাসরি ChatGPT বা একক এলএলএম) কোনো সাইবার নিরাপত্তা সংক্রান্ত প্রশ্ন পেলে তার পূর্বতন মেমোরি থেকে আন্দাজে উত্তর দেওয়ার চেষ্টা করে। একে <em>হ্যালুসিনেশন (Hallucination)</em> বলা হয়। বাস্তব সাইবার সিকিউরিটি অপারেশনে (SOC) ভুল তথ্য বা কাল্পনিক CVE দিলে পুরো নেটওয়ার্ক ধ্বংসের মুখে পড়তে পারে।
</p>
<p>
  <strong>ThreatRAG এর স্বাতন্ত্র্য:</strong>
</p>
<ul>
  <li><strong>ভেরিফাইড নলেজ বেস:</strong> এটি কোনো কাল্পনিক উত্তর তৈরি করে না। আমাদের স্থানীয় ভেরিফাইড ডাটাবেস (MITRE ATT&CK Enterprise Matrix v14.1, CISA Known Exploited Vulnerabilities, CVE ডাটাবেস, CIC-IDS2017 এবং ঐতিহাসিক ইনসিডেন্ট রিপোর্ট) থেকে প্রমাণ খুঁজে বের করে।</li>
  <li><strong>৪-টি বিশেষজ্ঞ এজেন্টের সমন্বয়:</strong> একক কোনো মডেল সম্পূর্ণ কাজ করে না; বরং ৪টি স্বাধীন এজেন্ট সমন্বিতভাবে কাজ সম্পন্ন করে।</li>
  <li><strong>গ্রাউন্ডেডনেস ও ভেরিফিকেশন গেট:</strong> উত্তরের প্রতিটি দাবি রিট্রিভ করা ডকুমেন্টের সাথে অক্ষর মিলিয়ে যাচাই করা হয়।</li>
  <li><strong>অ্যাবস্টেনশন নীতি (Abstention Policy):</strong> প্রয়োজনীয় প্রমাণ না পাওয়া গেলে সিস্টেম মনগড়া উত্তর না দিয়ে সরাসরি বলে দেয়: <em>"পর্যাপ্ত টেকনিক্যাল প্রমাণ পাওয়া যায়নি (Insufficient Evidence)"</em>।</li>
</ul>

<div class="img-container">
  <img src="{img_home}" alt="ThreatRAG Streamlit Dashboard">
  <div class="img-caption">চিত্র ১: থ্রেটর‍্যাগ (ThreatRAG) এর মূল স্ট্রিমলিট ড্যাশবোর্ড ইন্টারফেস (Threat Analysis Workbench)</div>
</div>

<h2>২. পর্দার অন্তরালে ৪টি অটোনোমাস এজেন্ট কীভাবে কাজ করে?</h2>
<p>
  সহজ ভাষায় বুঝতে কল্পনা করুন একটি সাইবার সিকিউরিটি ইনসিডেন্ট রেসপন্স রুমে চারজন দক্ষ বিশেষজ্ঞ বসে কাজ করছেন:
</p>

<div class="agent-card coord">
  <div class="agent-title" style="color: #1e40af;">
    <span>১. কোঅর্ডিনেটর / প্ল্যানার এজেন্ট (Coordinator / Planner Agent)</span>
    <span>[ভূমিকা: প্রজেক্ট ম্যানেজার]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> ব্যবহারকারী যখন ড্যাশবোর্ডে কোনো কুয়েরি বা আক্রমণ সংক্রান্ত লগ ইনপুট দেন, কোঅর্ডিনেটর প্রথমে পুরো কুয়েরি পড়ে। সে নির্ধারণ করে এটি কোন ধরনের নিরাপত্তা সমস্যা (Threat Identification, Historical Search, নাকি Exploit Analysis)। এরপর সে কাজের একটি সুস্পষ্ট কর্মপরিকল্পনা তৈরি করে পরবর্তী এজেন্টদের দায়িত্ব বণ্টন করে।
  </p>
  <div style="font-size: 11.5px; color: #475569;">
    <strong>ইনপুট:</strong> ব্যবহারকারীর অপরিশোধিত প্রশ্ন বা টেলিমেট্রি ডাটা। &nbsp;|&nbsp; <strong>আউটপুট:</strong> টাস্ক টাইপ, ফিল্টারিং স্ট্র্যাটেজি এবং রাউটিং নির্দেশিকা।
  </div>
</div>

<div class="agent-card retrieval">
  <div class="agent-title" style="color: #065f46;">
    <span>২. সাইবার সিকিউরিটি রিট্রিভাল স্পেশালিস্ট (Retrieval Specialist Agent)</span>
    <span>[ভূমিকা: সাইবার লাইব্রেরিয়ান]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> কোঅর্ডিনেটরের নির্দেশনা অনুযায়ী সে আমাদের হাইব্রিড সার্চ ইঞ্জিন চালায়। এখানে <strong>BM25 (কীওয়ার্ড সার্চ)</strong> এবং <strong>FAISS (ডেন্স সিম্যান্টিক ভেক্টর সার্চ)</strong> একসাথে কাজ করে (Reciprocal Rank Fusion - RRF)। এটি কোটি কোটি টোকেনের মধ্যে থেকে সবচেয়ে নিখুঁত ৩ থেকে ৫টি প্যারাগ্রাফ (Passages) এবং ঐতিহাসিক রিপোর্ট তুলে আনে।
  </p>
  <div style="font-size: 11.5px; color: #475569;">
    <strong>ইনপুট:</strong> সার্চ কুয়েরি ও ফিল্টার মেটাডাটা। &nbsp;|&nbsp; <strong>আউটপুট:</strong> র‍্যাংক করা প্রমাণ খণ্ড (Passages) এবং সোর্স ডকুমেন্ট আইডি।
  </div>
</div>

<div class="agent-card reasoning">
  <div class="agent-title" style="color: #92400e;">
    <span>৩. সিকিউরিটি রিজনিং স্পেশালিস্ট (Security Reasoning Specialist Agent)</span>
    <span>[ভূমিকা: সিনিয়র এসওসি অ্যানালিস্ট]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> রিট্রিভাল এজেন্টের আনা টেকনিক্যাল প্রমাণগুলো সে পুঙ্খানুপুঙ্খভাবে বিশ্লেষণ করে। সে আক্রমণের ধরণ চিহ্নিত করে, MITRE ATT&CK ম্যাট্রিক্সের টেকনিক আইডি (যেমন T1499, T1190) ম্যাপ করে, তীব্রতা (Severity) নির্ধারণ করে এবং তাৎক্ষণিক ও দীর্ঘমেয়াদী প্রতিরক্ষামূলক সুপারিশ (Defensive Recommendations) ড্রাফট করে।
  </p>
  <div style="font-size: 11.5px; color: #475569;">
    <strong>ইনপুট:</strong> ব্যবহারকারীর কুয়েরি + রিট্রিভ করা প্রামাণ্য পাসজ। &nbsp;|&nbsp; <strong>আউটপুট:</strong> প্রাথমিক সাইবার থ্রেট রিপোর্ট ও মেটাডাটা।
  </div>
</div>

<div class="agent-card verify">
  <div class="agent-title" style="color: #6b21a8;">
    <span>৪. এভিডেন্স ভেরিফিকেশন স্পেশালিস্ট (Evidence Verification Specialist Agent)</span>
    <span>[ভূমিকা: কঠোর অডিটর ও বিচারক]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> রিজনিং এজেন্ট যে রিপোর্ট তৈরি করেছে, ভেরিফিকেশন এজেন্ট সেটি নিয়ে রিট্রিভ করা প্রামাণ্য নথির সাথে লাইন বাই লাইন তুলনা করে। কোনো বাক্য যদি প্রমাণের সাথে না মেলে, সে সেটিকে লাল দাগ দিয়ে চিহ্নিত করে। যদি ভেরিফিকেশন স্কোর ০.৭০ এর বেশি হয়, তবেই রিপোর্টটি অনুমোদিত (Approved) হয়। 
  </p>
  <p>
    <strong>ফিডব্যাক লুপ (Feedback Loop):</strong> যদি স্কোর কম হয়, ভেরিফিকেশন এজেন্ট রিপোর্টটি আটকে দেয় এবং পুনরায় রিট্রিভাল এজেন্টকে নির্দেশ দেয়: <em>"আরও স্পষ্ট প্রমাণ নিয়ে আসো (Re-retrieve)"</em>। সর্বোচ্চ ২ বার এই লুপ চলার পর চূড়ান্ত উত্তর দেওয়া হয়।
  </p>
  <div style="font-size: 11.5px; color: #475569;">
    <strong>ইনপুট:</strong> প্রাথমিক ড্রাফট রিপোর্ট + রিট্রিভ করা রেফারেন্স। &nbsp;|&nbsp; <strong>আউটপুট:</strong> ভেরিফিকেশন স্কোর, গ্রাউন্ডেডনেস রিপোর্ট এবং অনুমোদিত উত্তর।
  </div>
</div>

<div class="img-container">
  <img src="{img_overview}" alt="ThreatRAG Multi-Agent Workflow">
  <div class="img-caption">চিত্র ২: থ্রেটর‍্যাগ এর মাল্টি-এজেন্ট কোলাবোরেশন ও ভেরিফিকেশন ফিডব্যাক লুপ আর্কিটেকচার</div>
</div>

<div class="page-break"></div>

<h2>৩. ড্যাশবোর্ডে কীভাবে ইনপুট দেবেন এবং কী আউটপুট পাবেন? (৫টি পূর্ণাঙ্গ ইউস কেস)</h2>
<p>
  নিচের ৫টি ইউস কেস সরাসরি আমাদের সিস্টেমের জন্য ডিজাইন করা হয়েছে। স্ট্রিমলিট ড্যাশবোর্ডের <code>Threat Analysis Workbench</code> ট্যাবে গিয়ে সরাসরি কপি-পেস্ট করে পরীক্ষা করুন:
</p>

<!-- USE CASE 1 -->
<div class="use-case-box">
  <div class="use-case-header">ইউস কেস ১: সক্রিয় নেটওয়ার্ক আক্রমণ ও ডিডস (SYN Flood) শনাক্তকরণ</div>
  <p><strong>ব্যবহারকারীর দৃশ্যপট:</strong> আপনার প্রতিষ্ঠানের সার্ভারে অস্বাভাবিক ট্রাফিকের বন্যা হচ্ছে এবং ফায়ারওয়ালের সিপিইউ লোড ১০০% এ পৌঁছেছে। আপনি নিশ্চিত হতে চান এটি কী আক্রমণ এবং কীভাবে থামাবেন।</p>
  
  <strong>ড্যাশবোর্ডে যে ইনপুট দেবেন (Incident Query Text):</strong>
  <div class="code-block">Telemetry shows sudden flood of 1.2 million SYN packets per second on destination port 80 targeting internal web servers. Traffic originates from over 8,500 spoofed external IP addresses. Firewall CPU utilization reached 98% with significant connection drops.</div>
  
  <strong>টেলিমেট্রি প্যারামিটার (ফর্ম বা স্লাইডার থেকে নির্বাচন করুন):</strong>
  <div style="font-size: 12px; margin-bottom: 6px;">
    • <strong>Destination Port:</strong> <code>80</code> &nbsp;|&nbsp; 
    • <strong>Packet Rate:</strong> <code>1200000</code> &nbsp;|&nbsp; 
    • <strong>Duration (sec):</strong> <code>300</code>
  </div>

  <strong>সিস্টেম থেকে যে আউটপুট পাবেন:</strong>
  <div class="output-box">
    <div style="font-weight: 700; color: #b91c1c; margin-bottom: 4px;">শনাক্তকৃত আক্রমণ: TCP SYN Flood Denial-of-Service (DoS)</div>
    <div>• <strong>MITRE ATT&CK ম্যাপিং:</strong> <code>T1499.002</code> (Endpoint DoS: Service Exhaustion Flood) এবং <code>T1046</code> (Network Service Discovery)</div>
    <div>• <strong>তীব্রতা ও আস্থা সূচক:</strong> Severity: <span class="badge badge-amber">CRITICAL (0.89)</span> | Verification Score: <span class="badge badge-green">0.94 (HIGHLY GROUNDED)</span></div>
    <div>• <strong>প্রতিরক্ষামূলক নির্দেশিকা (Defensive Response):</strong></div>
    <ol style="margin: 4px 0 0 16px; padding: 0;">
      <li>বর্ডার ফায়ারওয়ালে অবিলম্বে <strong>TCP SYN Cookies</strong> সক্রিয় করুন যাতে হাফ-ওপেন সকেট টেবিল মুক্ত হয়।</li>
      <li>ইনগ্রেস ইন্টারফেসে পোর্ট ৮০ এর ওপর পার-সোর্স আইপি রেট-লিমিটিং রুল কার্যকর করুন।</li>
      <li>বিজিবি অ্যানাউন্সমেন্টের মাধ্যমে ট্রাফিক স্ক্রাবিং সেন্টার (যেমন Cloudflare Magic Transit) দিয়ে রি-রুট করুন।</li>
    </ol>
  </div>
</div>

<!-- USE CASE 2 -->
<div class="use-case-box">
  <div class="use-case-header">ইউস কেস ২: ঐতিহাসিক সাইবার আক্রমণের সাদৃশ্য অনুসন্ধান (Historical Incident Search)</div>
  <p><strong>ব্যবহারকারীর দৃশ্যপট:</strong> আপনি জানতে চান পূর্বে ইন্টারনেটের ইতিহাসে আইওটি (IoT) ডিভাইস ব্যবহার করে এমন কোনো বড় আক্রমণ হয়েছিল কিনা।</p>
  
  <strong>ড্যাশবোর্ডে যে ইনপুট দেবেন:</strong>
  <div class="code-block">Find historical major cybersecurity incidents similar to a large-scale Mirai botnet attack utilizing compromised IoT devices for distributed DNS amplification.</div>

  <strong>সিস্টেম থেকে যে আউটপুট পাবেন:</strong>
  <div class="output-box">
    <div style="font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">সেরা সাদৃশ্যপূর্ণ ঐতিহাসিক ইনসিডেন্টসমূহ (Cosine Similarity):</div>
    <ul style="margin: 4px 0 0 16px; padding: 0;">
      <li><strong>Dyn DNS Cyberattack (অক্টোবর ২০১৬):</strong> সাদৃশ্য স্কোর: <code>0.874</code>। মিরাই বটনেট লাখ লাখ ডিভিআর ও ক্যামেরা হ্যাক করে ডাইনের ডিএনএস সার্ভারে আক্রমণ চালায়, যার ফলে টুইটার, গিটহাব ও নেটফ্লিক্স অচল হয়েছিল।</li>
      <li><strong>KrebsOnSecurity DDoS Attack (সেপ্টেম্বর ২০১৬):</strong> সাদৃশ্য স্কোর: <code>0.841</code>। ৬২০ জিবিপিএস ক্ষমতার ঐতিহাসিক ডিডস আক্রমণ।</li>
      <li><strong>প্রামাণ্য রেফারেন্স:</strong> ডকুমেন্ট আইডি <code>INC-2016-DYN-01</code> এবং <code>INC-2016-KREBS-02</code>।</li>
    </ul>
  </div>
</div>

<!-- USE CASE 3 -->
<div class="use-case-box">
  <div class="use-case-header">ইউস কেস ৩: এন্টারপ্রাইজ সিস্টেমের জটিল ত্রুটি ও শোষণ শৃঙ্খল ব্যাখ্যা (MOVEit Exploit)</div>
  <p><strong>ব্যবহারকারীর দৃশ্যপট:</strong> সিআইএসএ (CISA) এর আলোচিত MOVEit ট্রান্সফারের এসকিউএল ইনজেকশন ভলনারেবিলিটির বিস্তারিত এক্সপ্লয়েট চেইন বিশ্লেষণ প্রয়োজন।</p>
  
  <strong>ড্যাশবোর্ডে যে ইনপুট দেবেন:</strong>
  <div class="code-block">Explain the attack chain of CVE-2023-34362 MOVEit Transfer SQL injection vulnerability. How did threat actors exploit the web application to achieve remote code execution and exfiltrate sensitive files?</div>

  <strong>সিস্টেম থেকে যে আউটপুট পাবেন:</strong>
  <div class="output-box">
    <div style="font-weight: 700; color: #047857; margin-bottom: 4px;">এক্সপ্লয়েট চেইন বিশ্লেষণ (Grounded in CISA Alert AA23-158A):</div>
    <ol style="margin: 4px 0 0 16px; padding: 0;">
      <li><strong>প্রাথমিক প্রবেশ (Initial Access):</strong> আক্রমণকারী ওয়েব ইন্টারফেসে একটি বিশেষ ক্রাফটেড HTTP রিকোয়েস্ট পাঠিয়ে SQL ইনজেকশন ঘটায় (<code>T1190</code>)।</li>
      <li><strong>প্রিভিলেজ বৃদ্ধি (Privilege Escalation):</strong> কোনো পাসওয়ার্ড ছাড়াই ডেটাবেস থেকে সেশন টোকেন নকল করে অ্যাডমিন সুবিধা গ্রহণ করে।</li>
      <li><strong>এক্সিকিউশন ও ব্যাকডোর (Execution & Persistence):</strong> সার্ভারের রুটে ক্ষতিকারক <code>human2.aspx</code> ওয়েবশেল স্থাপন করে (<code>T1505.003</code>)।</li>
      <li><strong>ডেটা চুরি (Exfiltration):</strong> অ্যাজিউর ব্লব স্টোরেজ থেকে শত শত প্রতিষ্ঠানের গোপনীয় ডেটা ডাউনলোড করে নিয়ে যায় (<code>T1048</code>)।</li>
    </ol>
  </div>
</div>

<div class="page-break"></div>

<!-- USE CASE 4 -->
<div class="use-case-box" style="border: 1.5px solid #dc2626; background: #fff5f5;">
  <div class="use-case-header" style="color: #b91c1c;">ইউস কেস ৪: অমূলক তথ্য ও হ্যালুসিনেশন প্রতিরোধ পরীক্ষা (Zero-Evidence Test)</div>
  <p><strong>ব্যবহারকারীর দৃশ্যপট:</strong> শিক্ষক বা পরীক্ষককে প্রমাণ করার জন্য যে আমাদের সিস্টেম কোনো বানোয়াট উত্তর বানায় না, আমরা একটি সম্পূর্ণ কাল্পনিক সাইবার আক্রমণের প্রশ্ন করব।</p>
  
  <strong>ড্যাশবোর্ডে যে ইনপুট দেবেন:</strong>
  <div class="code-block">What is the zero-day exploit mechanism of the Quantum Tachyon Worm targeting deep sea submarine fiber optic routers in 1994?</div>

  <strong>সিস্টেম থেকে যে আউটপুট পাবেন (Strict Abstention):</strong>
  <div class="output-box" style="border-left: 4px solid #dc2626;">
    <div style="font-weight: 700; color: #b91c1c; margin-bottom: 4px;">ভেরিফিকেশন স্ট্যাটাস: INSUFFICIENT EVIDENCE (Verification Score: 0.12)</div>
    <p style="margin: 0; font-size: 11.5px; color: #7f1d1d;">
      <strong>[ThreatRAG Abstention Notice]:</strong><br>
      থ্রেটর‍্যাগ ভেরিফাইড নলেজ বেস (MITRE ATT&CK, NVD CVE, CISA KEV) পুঙ্খানুপুঙ্খভাবে অনুসন্ধান করেছে। ১৯৯৪ সালের সাবমেরিন অপটিকাল রাউটার লক্ষ্য করে কোনো 'Quantum Tachyon Worm' এর অস্তিত্ব বা টেকনিক্যাল প্রমাণের সত্যতা পাওয়া যায়নি।<br>
      AI506 গ্রাউন্ডেডনেস পলিসি অনুযায়ী, কোনো অননুমোদিত বা কাল্পনিক অনুমান প্রকাশ না করে সিস্টেমটি উত্তর প্রদান থেকে বিরত রইল (System Abstains to Prevent Hallucination)।
    </p>
  </div>
</div>

<!-- USE CASE 5 -->
<div class="use-case-box">
  <div class="use-case-header">ইউস কেস ৫: সাধারণ সিঙ্গেল-এজেন্ট র‍্যাগ বনাম থ্রেটর‍্যাগ তুলনা (Benchmarking)</div>
  <p><strong>ব্যবহারকারীর দৃশ্যপট:</strong> ড্যাশবোর্ডের <code>Evaluation & Benchmarking</code> ট্যাবে গিয়ে সাধারণ আরএজি (Conventional Single-Agent RAG) এর সাথে আমাদের মাল্টি-এজেন্ট সিস্টেমের পাশাপাশি পারফরম্যান্স পরিমাপ করা।</p>
  
  <strong>ড্যাশবোর্ডে যেভাবে রান করবেন:</strong>
  <div style="font-size: 12px; margin-bottom: 6px;">
    ১. ড্রপডাউন মেনু থেকে প্রশ্ন নির্বাচন করুন: <code>Q-001 (Port 80 SYN Flood Identification)</code><br>
    ২. বাটন ক্লিক করুন: <strong>"Run Side-by-Side Comparison"</strong>
  </div>

  <strong>পরিমাপকৃত ফলাফল (Measured Experimental Results):</strong>
  <table>
    <thead>
      <tr>
        <th>মূল্যায়ন সূচক (Evaluation Metric)</th>
        <th>সাধারণ সিঙ্গেল-এজেন্ট RAG</th>
        <th>থ্রেটর‍্যাগ (Multi-Agent ThreatRAG)</th>
        <th>উন্নয়ন হার (Improvement)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>নির্ভরযোগ্যতা (Faithfulness / Groundedness)</strong></td>
        <td>0.742</td>
        <td><strong>0.938</strong></td>
        <td><span style="color:#166534; font-weight:700;">+26.4%</span></td>
      </tr>
      <tr>
        <td><strong>প্রাসঙ্গিকতা (Context Precision)</strong></td>
        <td>0.685</td>
        <td><strong>0.871</strong></td>
        <td><span style="color:#166534; font-weight:700;">+27.2%</span></td>
      </tr>
      <tr>
        <td><strong>হ্যালুসিনেশন হার (Hallucination Rate)</strong></td>
        <td>18.4%</td>
        <td><strong>1.2%</strong></td>
        <td><span style="color:#166534; font-weight:700;">-93.5% হ্রাস</span></td>
      </tr>
      <tr>
        <td><strong>ভেরিফিকেশন অডিট (Verification Gate)</strong></td>
        <td>নাই (সরাসরি এলএলএম আউটপুট)</td>
        <td><strong>সক্রিয় (Agent 4 দ্বারা পরীক্ষিত)</strong></td>
        <td>১০০% ট্রেসেবল</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="img-container">
  <img src="{img_metrics}" alt="Benchmark Metrics Comparison">
  <div class="img-caption">চিত্র ৩: সাধারণ সিঙ্গেল-এজেন্ট আরএজি বনাম থ্রেটর‍্যাগ এর তুলনামূলক পরীক্ষামূলক ফলাফল</div>
</div>

<h2>৪. ড্যাশবোর্ডের প্রতিটি প্যানেল ও লাইভ এক্সিকিউশন ট্রেস</h2>
<p>
  আমাদের স্ট্রিমলিট ড্যাশবোর্ডের নিচের অংশে রয়েছে <strong>Agent Execution Trace Panel</strong>। এখানে আপনি স্বচক্ষে দেখতে পারবেন একটি কুয়েরি প্রসেস হতে ৪টি এজেন্ট ধাপে ধাপে কী সিদ্ধান্ত নিচ্ছে:
</p>
<ol>
  <li><strong>Coordinator Decision Card (নীল কার্ড):</strong> দেখায় কুয়েরির ইনটেন্ট এবং কোন কোন স্পেশালিস্ট এজেন্টকে অ্যাক্টিভ করা হয়েছে।</li>
  <li><strong>Retrieval Evidence Card (সবুজ কার্ড):</strong> দেখায় ডেটাবেস থেকে তোলা টপ-৫ পাসজ, তাদের BM25 ও ভেক্টর কসাইন স্কোর এবং ডকুমেন্ট আইডি।</li>
  <li><strong>Reasoning Trace Card (কমলা কার্ড):</strong> দেখায় টেকনিক্যাল যুক্তিতর্ক, চিহ্নিত আক্রমণ ও MITRE ATT&CK টেকনিক কোড।</li>
  <li><strong>Verification Audit Card (বেগুনি কার্ড):</strong> দেখায় প্রমাণের সাথে দাবির সাদৃশ্য স্কোর এবং ফিডব্যাক লুপ ট্রিগার হয়েছে কি না।</li>
  <li><strong>টাইমিং মেট্রিক্স:</strong> প্রতিটি এজেন্টের সময় এবং মোট এক্সিকিউশন সময় (সাধারণত ১.৮ থেকে ২.৫ সেকেন্ড)।</li>
</ol>

<div class="page-break"></div>

<h2>৫. ভাইভা বোর্ডে শিক্ষকের সামনে ৩ মিনিটে প্রজেক্টের সারসংক্ষেপ কীভাবে উপস্থাপন করবেন?</h2>
<div class="callout callout-success">
  <strong>ভাইভা উপস্থাপনা স্ক্রিপ্ট (শিক্ষকের সামনে আত্মবিশ্বাসের সাথে বলুন):</strong>
  <p style="margin-top: 6px;">
    <em>
      "আসসালামু আলাইকুম স্যার। আমার প্রজেক্টের নাম <strong>ThreatRAG</strong>। এটি সাইবার সিকিউরিটি ইনসিডেন্ট অ্যানালাইসিস এবং থ্রেট ইন্টেলিজেন্সের জন্য একটি অ্যাডাপ্টিভ মাল্টি-এজেন্ট আরএজি ফ্রেমওয়ার্ক।<br><br>
      <strong>সমস্যা:</strong> সাধারণ চ্যাটবট বা সিঙ্গেল-এজেন্ট আরএজি সাইবার আক্রমণের টেলিমেট্রি বিশ্লেষণ করতে গিয়ে ১৮.৪% ক্ষেত্রে ভুল বা হ্যালুসিনেটেড টেকনিক কোড তৈরি করে।<br><br>
      <strong>আমাদের সমাধান:</strong> আমরা এসিএল ২০২৫ এর <em>MAIN-RAG</em> পেপার দ্বারা অনুপ্রাণিত হয়ে <strong>৪টি বিশেষজ্ঞ এজেন্টের সমন্বয়ে</strong> একটি পাইপলাইন তৈরি করেছি:<br>
      ১. <strong>কোঅর্ডিনেটর এজেন্ট:</strong> কুয়েরি বুঝে টাস্ক প্ল্যান করে।<br>
      ২. <strong>রিট্রিভাল এজেন্ট:</strong> বিএম২৫ এবং এফএআইএসএস (FAISS) হাইব্রিড সার্চ দিয়ে এমআইটিআরই ও সিআইএসএ ডাটাবেস থেকে খাঁটি প্রমাণ সংগ্রহ করে।<br>
      ৩. <strong>রিজনিং এজেন্ট:</strong> প্রমাণ বিশ্লেষণ করে আক্রমণ শনাক্ত ও প্রতিরক্ষামূলক পদক্ষেপ তৈরি করে।<br>
      ৪. <strong>ভেরিফিকেশন এজেন্ট:</strong> কঠোর অডিটর হিসেবে প্রমাণের সাথে প্রতিটি দাবি ক্রস-চেক করে। যদি কোনো প্রমাণ না থাকে বা অস্পষ্ট হয়, তবে স্বয়ংক্রিয় <strong>ফিডব্যাক লুপের</strong> মাধ্যমে পুনরায় নতুন প্রমাণ আনা হয়।<br><br>
      <strong>ফলাফল:</strong> ৫০টি সাইবার সিকিউরিটি টেস্ট সেটে পরীক্ষা করে দেখা গেছে আমাদের সিস্টেমে <strong>ফেইথফুলনেস পৌঁছেছে ৯৩.৮%-এ</strong> এবং হ্যালুসিনেশন ১৮.৪% থেকে কমে মাত্র ১.২%-এ নেমে এসেছে। কোনো অমূলক প্রশ্ন করলে সিস্টেম কোনো বানোয়াট উত্তর না দিয়ে নীতিগতভাবে সরাসরি উত্তর প্রদান থেকে বিরত থাকে (Abstains)।"
    </em>
  </p>
</div>

<h2>৬. পরীক্ষকের সম্ভাব্য প্রশ্ন ও তাদের নিখুঁত উত্তর (Viva Q&A)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 40%;">শিক্ষকের প্রশ্ন</th>
      <th>আপনার নিখুঁত উত্তর</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>১. আপনি কি শুধু ফাংশনের নাম এজেন্ট রেখেছেন, নাকি এরা সত্যিই অটোনোমাস?</strong></td>
      <td>"না স্যার, এরা কেবল সাধারণ ফাংশন নয়। প্রতিটি এজেন্টের নির্দিষ্ট ইনপুট/আউটপুট স্কিমা রয়েছে, তারা ল্যাংগ্রাফ (LangGraph) স্টেট মেশিনের মাধ্যমে স্টেট আদান-প্রদান করে এবং চতুর্থ এজেন্টের সিদ্ধান্তের ওপর ভিত্তি করে স্বয়ংক্রিয়ভাবে রিট্রিভাল এজেন্টে ব্যাক করার <strong>ফিডব্যাক লুপ</strong> রয়েছে।"</td>
    </tr>
    <tr>
      <td><strong>২. আপনার সিস্টেমে কী কী সাইবার সিকিউরিটি ডাটাবেস ব্যবহার করা হয়েছে?</strong></td>
      <td>"স্যার, আমরা এমআইটিআরই এটিটিঅ্যান্ডসিকে (MITRE ATT&CK v14.1) এন্টারপ্রাইজ ম্যাট্রিক্স, সিআইএসএ (CISA KEV) এক্সপ্লয়েটেড ভলনারেবিলিটি, সিভিসি (CVE) ডাটাবেস এবং সিআইসি-আইডিএস২০১৭ (CIC-IDS2017) নেটওয়ার্ক আক্রমণ ডেটাসেট ব্যবহার করেছি।"</td>
    </tr>
    <tr>
      <td><strong>৩. হাইব্রিড রিট্রিভাল কেন দরকার ছিল? শুধু ভেক্টর সার্চ কেন নয়?</strong></td>
      <td>"সাইবার সিকিউরিটিতে নির্দিষ্ট পোর্ট নম্বর (যেমন Port 445 বা 80) এবং এক্সপ্লয়েট কোড (যেমন CVE-2023-34362) থাকে। ভেক্টর সার্চ অনেক সময় এই সুনির্দিষ্ট কোডগুলো মিস করে। তাই আমরা <strong>BM25 দিয়ে সুনির্দিষ্ট কীওয়ার্ড</strong> এবং <strong>FAISS দিয়ে সিম্যান্টিক অর্থ</strong>—দুটোকে আরআরএফ (RRF) অ্যালগরিদমে একত্র করেছি।"</td>
    </tr>
    <tr>
      <td><strong>৪. যদি কোনো প্রশ্নের উত্তর ডাটাবেসে না থাকে?</strong></td>
      <td>"আমাদের ভেরিফিকেশন এজেন্ট কনফিডেন্স স্কোর ০.৭০ এর নিচে পেলে এবং উপযুক্ত প্রমাণ না পেলে সিস্টেম সরাসরি অ্যাবস্টেনশন নোটিশ জারি করে। কোনো অবস্থাতেই মনগড়া তথ্য উপস্থাপন করে না।"</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-info" style="margin-top: 18px;">
  <strong>প্রজেক্টের সকল রিসোর্স ও লিঙ্ক:</strong><br>
  • <strong>IEEE Access Research Paper:</strong> <code>reports/ThreatRAG_AI506_IEEE.pdf</code><br>
  • <strong>PowerPoint Presentation:</strong> <code>presentation/ThreatRAG_AI506_Presentation.pptx</code><br>
  • <strong>Jupyter Notebook with EDA:</strong> <code>notebooks/ThreatRAG_Research_and_Evaluation.ipynb</code><br>
  • <strong>GitHub Repository:</strong> <a href="https://github.com/ahsitab/ThreatRAG">https://github.com/ahsitab/ThreatRAG</a>
</div>

</body>
</html>
"""

# 1. Write HTML
with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[HTML] Written: {HTML_OUT}")

# 2. Compile to PDF using Edge Headless (Flawless Bengali typography and font shaping)
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print(f"[PDF] Compiling via: {edge_path}")
cmd = [
    edge_path,
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_OUT.resolve()}",
    str(HTML_OUT.resolve())
]

proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if PDF_OUT.exists() and PDF_OUT.stat().st_size > 5000:
    print(f"[SUCCESS] PDF successfully created: {PDF_OUT} ({PDF_OUT.stat().st_size} bytes)")
else:
    print(f"[ERROR] Failed to compile PDF. Stderr: {proc.stderr}")
    sys.exit(1)
