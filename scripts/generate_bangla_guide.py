"""
ThreatRAG: Updated Complete Bengali (বাংলা) Operational and Input/Output Manual Generator
Features:
  - 'গল্পের মাধ্যমে থ্রেটর‍্যাগ এর আসল রহস্য' (Engaging Story)
  - 'ইনফোগ্রাফিক ড্রয়িং (Visual SVG Drawing of Input -> 4 Agents -> Output)'
  - Detailed Input & Output Field-by-Field Breakdown
  - 5 Full Real-world Use Cases
  - Viva Board Speech & Q&A
  - Compiles to HTML and PDF (via Edge/Chrome Headless) with Kalpurush Bengali Font
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

svg_drawing = """
<div style="text-align: center; margin: 16px 0; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06); page-break-inside: avoid;">
  <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 3px;">
    🎨 থ্রেটর‍্যাগ ভিজ্যুয়াল ইনফোগ্রাফিক ড্রয়িং: ইনপুট থেকে আউটপুটের সম্পূর্ণ পথ পরিক্রমা
  </div>
  <div style="font-size: 12px; color: #64748b; margin-bottom: 10px;">
    (কী ইনপুট দিচ্ছেন ➔ অন্তরালে ৪ জন গোয়েন্দা কীভাবে তদন্ত করছে ➔ কী আউটপুট পাচ্ছেন)
  </div>

  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 490" width="100%" height="auto" style="font-family: 'Kalpurush', 'Hind Siliguri', 'Nirmala UI', sans-serif;">
    <defs>
      <!-- Gradients -->
      <linearGradient id="gradInput" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0284c7" />
        <stop offset="100%" stop-color="#0369a1" />
      </linearGradient>
      <linearGradient id="gradCoord" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#2563eb" />
        <stop offset="100%" stop-color="#1d4ed8" />
      </linearGradient>
      <linearGradient id="gradRet" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669" />
        <stop offset="100%" stop-color="#047857" />
      </linearGradient>
      <linearGradient id="gradReas" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#d97706" />
        <stop offset="100%" stop-color="#b45309" />
      </linearGradient>
      <linearGradient id="gradVer" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#7c3aed" />
        <stop offset="100%" stop-color="#6d28d9" />
      </linearGradient>
      <linearGradient id="gradOutput" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669" />
        <stop offset="100%" stop-color="#065f46" />
      </linearGradient>

      <!-- Drop Shadow -->
      <filter id="cardShadow" x="-10%" y="-10%" width="125%" height="125%">
        <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.12"/>
      </filter>

      <!-- Arrow Markers -->
      <marker id="arrowBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7" />
      </marker>
      <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669" />
      </marker>
      <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#dc2626" />
      </marker>
      <marker id="arrowDark" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#334155" />
      </marker>
    </defs>

    <!-- Background Framing -->
    <rect x="5" y="5" width="940" height="480" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>

    <!-- ==================== COLUMN 1: USER INPUT ==================== -->
    <g transform="translate(20, 25)">
      <!-- Box -->
      <rect x="0" y="0" width="220" height="435" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="220" height="45" rx="8" fill="url(#gradInput)"/>
      <rect x="0" y="37" width="220" height="8" fill="#0369a1"/>
      <text x="110" y="28" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">📥 ব্যবহারকারীর ইনপুট (INPUT)</text>

      <!-- Input Elements -->
      <rect x="12" y="60" width="196" height="70" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
      <text x="20" y="80" fill="#0369a1" font-size="12" font-weight="bold">১. অপরিশোধিত টেলিমেট্রি লগ:</text>
      <text x="20" y="98" fill="#334155" font-size="10.5">"1.2M SYN packets/sec flood</text>
      <text x="20" y="114" fill="#334155" font-size="10.5">on Port 80, CPU 98%..."</text>

      <rect x="12" y="140" width="196" height="65" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
      <text x="20" y="160" fill="#0369a1" font-size="12" font-weight="bold">২. নেটওয়ার্ক প্যারামিটার:</text>
      <text x="20" y="178" fill="#334155" font-size="11">• Port: 80 | Protocol: TCP</text>
      <text x="20" y="194" fill="#334155" font-size="11">• Rate: 1,200,000 pkts/sec</text>

      <rect x="12" y="215" width="196" height="65" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
      <text x="20" y="235" fill="#0369a1" font-size="12" font-weight="bold">৩. ব্যবহারকারীর আসল প্রশ্ন:</text>
      <text x="20" y="253" fill="#334155" font-size="10.5">"এটি কী আক্রমণ? কীভাবে</text>
      <text x="20" y="269" fill="#334155" font-size="10.5">আমাদের সার্ভার রক্ষা করব?"</text>

      <!-- Explanation note -->
      <rect x="12" y="295" width="196" height="125" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="20" y="318" fill="#1e40af" font-size="12" font-weight="bold">💡 গল্পের ভাষায় ইনপুট:</text>
      <text x="20" y="338" fill="#1e3a8a" font-size="11">এটি কোনো প্রশ্ন নয়, বরং একটি</text>
      <text x="20" y="356" fill="#1e3a8a" font-size="11">অপরাধের আলামত বা ক্রাইম</text>
      <text x="20" y="374" fill="#1e3a8a" font-size="11">সিনের রক্তাক্ত প্রমাণ, যা আপনি</text>
      <text x="20" y="392" fill="#1e3a8a" font-size="11">গোয়েন্দা দলের টেবিলে দিলেন।</text>
    </g>

    <!-- Arrow 1: Input to Agents -->
    <path d="M 242 220 L 278 220" fill="none" stroke="#0284c7" stroke-width="3" marker-end="url(#arrowBlue)"/>

    <!-- ==================== COLUMN 2: 4-AGENT SECURITY ROOM ==================== -->
    <g transform="translate(285, 25)">
      <!-- Main Outer Container -->
      <rect x="0" y="0" width="380" height="435" rx="8" fill="#ffffff" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="380" height="32" rx="8" fill="#334155"/>
      <rect x="0" y="26" width="380" height="6" fill="#1e293b"/>
      <text x="190" y="21" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">⚙️ থ্রেটর‍্যাগ অন্তরাল: ৪-ডিটেকটিভ স্পেশালিস্ট ল্যাব</text>

      <!-- Agent 1: Coordinator -->
      <g transform="translate(15, 42)">
        <rect x="0" y="0" width="350" height="70" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
        <rect x="0" y="0" width="350" height="22" rx="6" fill="url(#gradCoord)"/>
        <text x="10" y="16" fill="#ffffff" font-size="11" font-weight="bold">🕵️‍♂️ এজেন্ট ১: কোঅর্ডিনেটর / প্ল্যানার (তদন্ত প্রধান)</text>
        <text x="10" y="38" fill="#1e293b" font-size="10.5"><strong>দায়িত্ব:</strong> আলামত বিশ্লেষণ, ইনটেন্ট নির্ধারণ ও বিশেষজ্ঞদের দায়িত্ব বণ্টন।</text>
        <text x="10" y="55" fill="#475569" font-size="10">সিদ্ধান্ত: [DoS Attack Pattern Detected ➔ Trigger Hybrid Retrieval]</text>
      </g>

      <!-- Down Arrow 1 -->
      <path d="M 190 114 L 190 128" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#arrowDark)"/>

      <!-- Agent 2: Retrieval -->
      <g transform="translate(15, 132)">
        <rect x="0" y="0" width="350" height="75" rx="6" fill="#f0fdf4" stroke="#059669" stroke-width="1.5"/>
        <rect x="0" y="0" width="350" height="22" rx="6" fill="url(#gradRet)"/>
        <text x="10" y="16" fill="#ffffff" font-size="11" font-weight="bold">📚 এজেন্ট ২: রিট্রিভাল স্পেশালিস্ট (সাইবার লাইব্রেরিয়ান)</text>
        <text x="10" y="38" fill="#1e293b" font-size="10.5"><strong>দায়িত্ব:</strong> BM25 + FAISS (RRF) হাইব্রিড সার্চ দিয়ে খাঁটি প্রমাণ সংগ্রহ।</text>
        <text x="10" y="54" fill="#047857" font-size="10">নলেজ বেস: MITRE ATT&CK Matrix, CISA KEV, CVEs, Dyn DNS 2016</text>
        <text x="10" y="68" fill="#475569" font-size="9.5">আউটপুট: Top-5 Verified Evidence Passages + Document IDs</text>
      </g>

      <!-- Down Arrow 2 -->
      <path d="M 190 209 L 190 223" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#arrowDark)"/>

      <!-- Agent 3: Reasoning -->
      <g transform="translate(15, 227)">
        <rect x="0" y="0" width="350" height="70" rx="6" fill="#fffbeb" stroke="#d97706" stroke-width="1.5"/>
        <rect x="0" y="0" width="350" height="22" rx="6" fill="url(#gradReas)"/>
        <text x="10" y="16" fill="#ffffff" font-size="11" font-weight="bold">🧠 এজেন্ট ৩: সিকিউরিটি রিজনিং স্পেশালিস্ট (ফরেনসিক অ্যানালিস্ট)</text>
        <text x="10" y="38" fill="#1e293b" font-size="10.5"><strong>দায়িত্ব:</strong> প্রমাণের সাথে আলামত মিলিয়ে আক্রমণ শনাক্ত ও প্রেসক্রিপশন তৈরি।</text>
        <text x="10" y="55" fill="#92400e" font-size="10">শনাক্তকরণ: [T1499.002 SYN Flood] | প্রেসক্রিপশন: [Enable SYN Cookies]</text>
      </g>

      <!-- Down Arrow 3 -->
      <path d="M 190 299 L 190 313" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#arrowDark)"/>

      <!-- Agent 4: Verification -->
      <g transform="translate(15, 317)">
        <rect x="0" y="0" width="350" height="105" rx="6" fill="#faf5ff" stroke="#7c3aed" stroke-width="1.5"/>
        <rect x="0" y="0" width="350" height="22" rx="6" fill="url(#gradVer)"/>
        <text x="10" y="16" fill="#ffffff" font-size="11" font-weight="bold">⚖️ এজেন্ট ৪: এভিডেন্স ভেরিফিকেশন স্পেশালিস্ট (কঠোর বিচারক)</text>
        <text x="10" y="38" fill="#1e293b" font-size="10.5"><strong>দায়িত্ব:</strong> প্রতিটি দাবি নথির সাথে অক্ষর মিলিয়ে যাচাই করা।</text>
        
        <!-- Score branches -->
        <rect x="10" y="46" width="155" height="48" rx="4" fill="#ecfdf5" stroke="#10b981"/>
        <text x="18" y="62" fill="#065f46" font-size="10" font-weight="bold">✅ স্কোর >= ০.৭০ (প্রমাণিত):</text>
        <text x="18" y="76" fill="#047857" font-size="9.5">অনুমোদন ও চূড়ান্ত রিপোর্ট প্রকাশ</text>
        <text x="18" y="89" fill="#047857" font-size="9.5">(Approved for Output)</text>

        <rect x="175" y="46" width="165" height="48" rx="4" fill="#fef2f2" stroke="#ef4444"/>
        <text x="183" y="62" fill="#991b1b" font-size="10" font-weight="bold">❌ প্রমাণ অপ্রতুল (Low Score):</text>
        <text x="183" y="76" fill="#b91c1c" font-size="9.5">স্বয়ংক্রিয় ফিডব্যাক লুপ চালু</text>
        <text x="183" y="89" fill="#b91c1c" font-size="9.5">(Re-retrieve / Abstain)</text>
      </g>

      <!-- Feedback Loop Arrow (curved path back to Agent 2) -->
      <path d="M 365 375 C 385 375, 395 280, 395 175 C 395 175, 395 168, 368 168" fill="none" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="4,3" marker-end="url(#arrowRed)"/>
      <rect x="372" y="240" width="22" height="65" rx="3" fill="#fee2e2" stroke="#f87171"/>
      <text x="383" y="254" fill="#991b1b" font-size="9" font-weight="bold" text-anchor="middle" transform="rotate(90, 383, 272)">ফিডব্যাক লুপ (Feedback)</text>
    </g>

    <!-- Arrow 2: Agents to Output -->
    <path d="M 667 375 L 703 375" fill="none" stroke="#059669" stroke-width="3" marker-end="url(#arrowGreen)"/>

    <!-- ==================== COLUMN 3: SYSTEM OUTPUT ==================== -->
    <g transform="translate(710, 25)">
      <!-- Box -->
      <rect x="0" y="0" width="220" height="435" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#cardShadow)"/>
      <rect x="0" y="0" width="220" height="45" rx="8" fill="url(#gradOutput)"/>
      <rect x="0" y="37" width="220" height="8" fill="#065f46"/>
      <text x="110" y="28" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">📤 সিস্টেমের আউটপুট (OUTPUT)</text>

      <!-- Output Elements -->
      <rect x="12" y="58" width="196" height="68" rx="6" fill="#f0fdf4" stroke="#86efac"/>
      <text x="20" y="76" fill="#166534" font-size="11" font-weight="bold">১. আক্রমণের সঠিক নাম:</text>
      <text x="20" y="93" fill="#0f172a" font-size="10.5" font-weight="bold">• TCP SYN Flood Denial</text>
      <text x="20" y="108" fill="#0f172a" font-size="10.5">  of Service (DoS)</text>

      <rect x="12" y="132" width="196" height="68" rx="6" fill="#f0fdf4" stroke="#86efac"/>
      <text x="20" y="150" fill="#166534" font-size="11" font-weight="bold">২. আন্তর্জাতিক MITRE ধারা:</text>
      <text x="20" y="167" fill="#1e3a8a" font-size="10.5" font-weight="bold">• T1499.002 (Endpoint DoS)</text>
      <text x="20" y="183" fill="#1e3a8a" font-size="10.5" font-weight="bold">• T1046 (Network Discovery)</text>

      <rect x="12" y="206" width="196" height="68" rx="6" fill="#f0fdf4" stroke="#86efac"/>
      <text x="20" y="224" fill="#166534" font-size="11" font-weight="bold">৩. তীব্রতা ও সত্যতা স্কোর:</text>
      <text x="20" y="242" fill="#b91c1c" font-size="11" font-weight="bold">• Severity: CRITICAL (0.89)</text>
      <text x="20" y="259" fill="#059669" font-size="11" font-weight="bold">• Groundedness: 0.94 (Verified)</text>

      <rect x="12" y="280" width="196" height="85" rx="6" fill="#f0fdf4" stroke="#86efac"/>
      <text x="20" y="298" fill="#166534" font-size="11" font-weight="bold">৪. ডিফেন্সিভ প্রেসক্রিপশন:</text>
      <text x="20" y="315" fill="#334155" font-size="10">১. Enable TCP SYN Cookies</text>
      <text x="20" y="331" fill="#334155" font-size="10">২. Port 80 Rate Limiting</text>
      <text x="20" y="347" fill="#334155" font-size="10">৩. Cloud Scrubbing Traffic</text>

      <!-- Explanation note -->
      <rect x="12" y="372" width="196" height="52" rx="6" fill="#ecfdf5" stroke="#a7f3d0"/>
      <text x="20" y="390" fill="#065f46" font-size="11" font-weight="bold">💡 গল্পের ভাষায় আউটপুট:</text>
      <text x="20" y="406" fill="#047857" font-size="10">আদালতের সত্যায়িত রায় এবং</text>
      <text x="20" y="418" fill="#047857" font-size="10">সার্ভার বাঁচানোর নির্ভুল প্রেসক্রিপশন।</text>
    </g>
  </svg>
</div>
"""

html_content = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<title>ThreatRAG: মাল্টি-এজেন্ট সিস্টেমের পূর্ণাঙ্গ ব্যবহার নির্দেশিকা ও ইনপুট-আউটপুট ম্যানুয়াল</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
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
    line-height: 1.6;
    font-size: 13px;
    margin: 0;
    padding: 0;
  }}

  .header-container {{
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 10px;
    margin-bottom: 18px;
  }}

  .badge-container {{
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
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
    font-size: 21px;
    color: #0f172a;
    margin: 4px 0 6px 0;
    font-weight: 700;
  }}

  .meta-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 9px 12px;
    font-size: 11.5px;
    margin-top: 8px;
  }}

  .meta-item strong {{
    color: #334155;
  }}

  h2 {{
    font-size: 15.5px;
    color: #1e3a8a;
    border-left: 4px solid #2563eb;
    padding-left: 10px;
    margin-top: 20px;
    margin-bottom: 10px;
    font-weight: 700;
  }}

  h3 {{
    font-size: 13.5px;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 5px;
    font-weight: 600;
  }}

  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}

  .story-card {{
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 14px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }}

  .agent-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 11px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}

  .agent-card.coord {{ border-left: 5px solid #2563eb; background: #f8fafc; }}
  .agent-card.retrieval {{ border-left: 5px solid #059669; background: #f0fdf4; }}
  .agent-card.reasoning {{ border-left: 5px solid #d97706; background: #fffbeb; }}
  .agent-card.verify {{ border-left: 5px solid #7c3aed; background: #faf5ff; }}

  .agent-title {{
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
  }}

  .use-case-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }}

  .use-case-header {{
    font-size: 13.5px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 6px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
  }}

  .code-block {{
    font-family: 'Fira Code', Consolas, monospace;
    background: #0f172a;
    color: #f8fafc;
    padding: 9px 11px;
    border-radius: 5px;
    font-size: 11px;
    line-height: 1.45;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 5px 0 8px 0;
  }}

  .output-box {{
    background: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 5px;
    padding: 9px 11px;
    font-size: 11.5px;
    margin-top: 5px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 11.5px;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 7px 9px;
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
    margin: 12px 0;
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
    font-size: 10.5px;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }}

  .callout {{
    padding: 9px 12px;
    border-radius: 6px;
    margin: 10px 0;
    font-size: 12px;
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
  <div style="font-size: 12px; color: #475569;">
    সাইবার সিকিউরিটি থ্রেট ইন্টেলিজেন্স ও ইনসিডেন্ট রেসপন্সের জন্য ৪-এজেন্ট কোলাবোরেশন, গল্পে গল্পে ইনপুট-আউটপুট গাইড ও ফলাফল বিশ্লেষণ
  </div>

  <div class="meta-grid">
    <div class="meta-item"><strong>গবেষক ও শিক্ষার্থী:</strong> Asfar Hossain Sitab</div>
    <div class="meta-item"><strong>কোর্স কোড ও নাম:</strong> AIML-507 / AI506 (MSc in AI & Cyber Security)</div>
    <div class="meta-item"><strong>বেস রিসার্চ পেপার:</strong> MAIN-RAG (ACL 2025) & MASS-RAG (ACL 2026)</div>
    <div class="meta-item"><strong>সিস্টেম আর্কিটেকচার:</strong> 4-Agent LangGraph Workflow with Verification Feedback Loop</div>
  </div>
</div>

<!-- ==================== SPECIAL CHAPTER: THE STORY & DRAWING ==================== -->
<h2>বিশেষ অধ্যায়: গল্প ও ড্রয়িংয়ের মাধ্যমে থ্রেটর‍্যাগ এর আসল রহস্য</h2>
<p>
  অনেকের মনেই প্রশ্ন জাগে: <em>"আমি আসলে ড্যাশবোর্ডে কী জিনিস ইনপুট দিচ্ছি? আর সিস্টেমটাই বা আমাকে কী জিনিস আউটপুট দিচ্ছে?"</em><br>
  পুরো জটিল টেকনিক্যাল বিষয়টিকে একটি সহজ বাস্তব গল্পের মাধ্যমে বুঝে নেওয়া যাক:
</p>

<div class="story-card">
  <div style="font-size: 14px; font-weight: 700; color: #1e3a8a; margin-bottom: 8px;">
    📖 গল্প: রাত ২টায় একটি ব্যাংকের সার্ভার রুমে রহস্যময় সাইবার আক্রমণ
  </div>
  
  <p>
    <strong>ঘটনার সূত্রপাত:</strong> রাত ঠিক ২টা ১৫ মিনিট। একটি বড় আন্তর্জাতিক ব্যাংকের অনলাইন ব্যাংকিং হঠাৎ স্তব্ধ হয়ে গেল। গ্রাহকরা অ্যাপে ঢুকতে পারছেন না। সার্ভার রুমের মনিটরে লাল বাতি জ্বলছে এবং ফায়ারওয়ালের সিপিইউ লোড ১০০% এ গিয়ে ঠেকেছে।
  </p>

  <p>
    <strong>১. আপনি আসলে কী ইনপুট দিলেন? (The INPUT Concept):</strong><br>
    আপনি হলেন ব্যাংকের অন-ডিউটি সাইবার সিকিউরিটি ইঞ্জিনিয়ার। আপনি মনিটরে তাকিয়ে দেখলেন: <em>"প্রতি সেকেন্ডে ১২ লাখ প্যাকেট পোর্ট ৮০-তে আঘাত করছে, সাড়ে আট হাজার ফেক আইপি থেকে রিকোয়েস্ট আসছে।"</em><br>
    আপনি এই অস্বাভাবিক দৃশ্যপট আর সংখ্যাগুলো ড্যাশবোর্ডের ইনপুট বক্সে টাইপ করে দিলেন।<br>
    <span style="color: #0369a1; font-weight: 600;">👉 অর্থাৎ, আপনার ইনপুট কোনো সাধারণ চ্যাট মেসেজ নয়! আপনার ইনপুট হলো একটি অপরাধের আলামত (Crime Scene Evidence) বা সার্ভারের অসুস্থতার উপসর্গ (Symptoms)।</span>
  </p>

  <p>
    <strong>২. ভেতরে ৪ জন স্পেশালিস্ট গোয়েন্দা কীভাবে তদন্ত করল? (The 4-Agent Secret Lab):</strong><br>
    আপনার ইনপুট সাবমিট করার সাথে সাথে ThreatRAG এর তদন্ত টিম অ্যাক্টিভ হয়ে গেল:
  </p>
  <ul style="margin: 4px 0 8px 16px; padding: 0;">
    <li><strong>গোয়েন্দা ১ (কোঅর্ডিনেটর):</strong> সে ফাইলটি দেখে বলল—<em>"আলামত বলছে এটা ওয়েব সার্ভার জ্যাম করার আক্রমণ। লাইব্রেরিয়ান, দ্রুত ডিডস (DDoS) আক্রমণের সব রেকর্ড নিয়ে এসো!"</em></li>
    <li><strong>গোয়েন্দা ২ (সাইবার লাইব্রেরিয়ান / রিট্রিভাল স্পেশালিস্ট):</strong> সে আন্তর্জাতিক সাইবার ডাটাবেস (MITRE ATT&CK, CISA KEV, ২০১৬ সালের Dyn DNS অ্যাটাক রেকর্ড) ঘেঁটে সবচেয়ে প্রাসঙ্গিক ৫টি পাতা টেবিলে এনে রাখল।</li>
    <li><strong>গোয়েন্দা ৩ (ফরেনসিক অ্যানালিস্ট / রিজনিং স্পেশালিস্ট):</strong> সে লাইব্রেরিয়ানের আনা রেকর্ড আর আপনার সার্ভার লগ মিলিয়ে বলল—<em>"ধরা পড়েছে! এটা সাধারণ ট্রাফিক নয়, এটা TCP SYN Flood অ্যাটাক (আন্তর্জাতিক কোড T1499.002)। এখনই ব্যবস্থা না নিলে আগামী ৫ মিনিটে পুরো ব্যাংক ডাটাবেস ক্র্যাশ করবে!"</em></li>
    <li><strong>গোয়েন্দা ৪ (হাইকোর্টের বিচারক / ভেরিফিকেশন স্পেশালিস্ট):</strong> সে অত্যন্ত কঠোর অডিটর। সে বলল—<em>"দাঁড়াও! ফরেনসিক অ্যানালিস্ট কি বানিয়ে বানিয়ে কিছু বলল, নাকি লাইব্রেরির নথিতে সত্যি প্রমাণ আছে? বাহ, নথির সাথে কথার ৯৪% হুবহু মিল আছে! রিপোর্ট অনুমোদিত।"</em> (যদি নথিতে প্রমাণ না থাকত, তবে সে রিপোর্ট আটকে দিয়ে লাইব্রেরিয়ানকে আবার নতুন প্রমাণ আনতে বাধ্য করত!)</li>
  </ul>

  <p>
    <strong>৩. সিস্টেম আপনাকে কী আউটপুট দিল? (The OUTPUT Concept):</strong><br>
    মাত্র ২ সেকেন্ডের মাথায় আপনার ড্যাশবোর্ডে বিচারকের সিলমোহর দেওয়া একটি সম্পূর্ণ <strong>'ইনসিডেন্ট ট্রিয়াজ ও প্রেসক্রিপশন রিপোর্ট'</strong> ফুটে উঠল:
  </p>
  <ul style="margin: 4px 0 0 16px; padding: 0;">
    <li><strong>রোগের নাম (Threat Name):</strong> TCP SYN Flood Denial-of-Service (DoS)</li>
    <li><strong>অপরাধের আন্তর্জাতিক ধারা (MITRE Code):</strong> T1499.002 (Service Exhaustion Flood)</li>
    <li><strong>বিপদের মাত্রা (Severity):</strong> CRITICAL (বিপদ সূচক: ০.৮৯)</li>
    <li><strong>সার্ভার বাঁচানোর প্রেসক্রিপশন (Defensive Action):</strong> (১) বর্ডার ফায়ারওয়ালে সাথে সাথে <em>TCP SYN Cookies</em> সক্রিয় করুন, (২) পোর্ট ৮০-তে রেট-লিমিট লাগান, (৩) ক্লাউড স্ক্রাবিং সেন্টারে ট্রাফিক পাঠান।</li>
  </ul>
  <p style="margin-top: 6px;">
    <span style="color: #166534; font-weight: 600;">👉 অর্থাৎ, আপনার আউটপুট কোনো বানোয়াট গল্প নয়! আপনার আউটপুট হলো শতভাগ সত্য প্রমাণিত সাইবার রিপোর্ট এবং তাৎক্ষণিক সার্ভার বাঁচানোর নির্ভুল প্রেসক্রিপশন!</span>
  </p>
</div>

<!-- INSERT SVG DRAWING -->
{svg_drawing}

<div class="page-break"></div>

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
  চারজন বিশেষজ্ঞের দায়িত্ব ও প্রযুক্তিগত কাজের বিবরণ:
</p>

<div class="agent-card coord">
  <div class="agent-title" style="color: #1e40af;">
    <span>১. কোঅর্ডিনেটর / প্ল্যানার এজেন্ট (Coordinator / Planner Agent)</span>
    <span>[ভূমিকা: প্রজেক্ট ম্যানেজার]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> ব্যবহারকারী যখন ড্যাশবোর্ডে কোনো কুয়েরি বা আক্রমণ সংক্রান্ত লগ ইনপুট দেন, কোঅর্ডিনেটর প্রথমে পুরো কুয়েরি পড়ে। সে নির্ধারণ করে এটি কোন ধরনের নিরাপত্তা সমস্যা (Threat Identification, Historical Search, নাকি Exploit Analysis)। এরপর সে কাজের একটি সুস্পষ্ট কর্মপরিকল্পনা তৈরি করে পরবর্তী এজেন্টদের দায়িত্ব বণ্টন করে।
  </p>
  <div style="font-size: 11px; color: #475569;">
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
  <div style="font-size: 11px; color: #475569;">
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
  <div style="font-size: 11px; color: #475569;">
    <strong>ইনপুট:</strong> ব্যবহারকারীর কুয়েরি + রিট্রিভ করা প্রামাণ্য পাসজ। &nbsp;|&nbsp; <strong>আউটপুট:</strong> প্রাথমিক সাইবার থ্রেট রিপোর্ট ও মেটাডাটা।
  </div>
</div>

<div class="agent-card verify">
  <div class="agent-title" style="color: #6b21a8;">
    <span>৪. এভিডেন্স ভেরিফিকেশন স্পেশালিস্ট (Evidence Verification Specialist Agent)</span>
    <span>[ভূমিকা: কঠোর অডিটর ও বিচারক]</span>
  </div>
  <p>
    <strong>আসল কাজ:</strong> রিজনিং এজেন্ট যে রিপোর্ট তৈরি করেছে, ভেরিফিকেশন এজেন্ট সেটি নিয়ে রিট্রিভ করা প্রামাণ্য নথির সাথে লাইন বাই লাইন তুলনা করে। কোনো বাক্য যদি প্রমাণের সাথে না মেলে, সে সেটিকে চিহ্নিত করে। যদি ভেরিফিকেশন স্কোর ০.৭০ এর বেশি হয়, তবেই রিপোর্টটি অনুমোদিত (Approved) হয়। 
  </p>
  <p>
    <strong>ফিডব্যাক লুপ (Feedback Loop):</strong> যদি স্কোর কম হয়, ভেরিফিকেশন এজেন্ট রিপোর্টটি আটকে দেয় এবং পুনরায় রিট্রিভাল এজেন্টকে নির্দেশ দেয়: <em>"আরও স্পষ্ট প্রমাণ নিয়ে আসো (Re-retrieve)"</em>। সর্বোচ্চ ২ বার এই লুপ চলার পর চূড়ান্ত উত্তর দেওয়া হয়।
  </p>
  <div style="font-size: 11px; color: #475569;">
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
  <div style="font-size: 11.5px; margin-bottom: 5px;">
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
    <p style="margin: 0; font-size: 11px; color: #7f1d1d;">
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
  <div style="font-size: 11.5px; margin-bottom: 5px;">
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
  <p style="margin-top: 5px;">
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

<div class="callout callout-info" style="margin-top: 14px;">
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
