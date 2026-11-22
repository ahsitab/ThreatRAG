"""
scripts/update_author_and_course.py
===================================
Updates author name to 'Asfar Hossain Sitab' and aligns course code to 'AIML-507 / AI506'
across all documentation, scripts, reports, research files, presentation, and notebooks.
"""

import os
import glob

files_to_update = [
    "README.md",
    "docs/ThreatRAG_Guide_Bangla.html",
    "presentation/DEMO_SCRIPT.md",
    "presentation/VIVA_PREPARATION.md",
    "presentation/ThreatRAG_AI506_Presentation.html",
    "reports/AI506_COMPLIANCE_AUDIT.md",
    "reports/FINAL_AI506_COMPLIANCE_REPORT.md",
    "reports/ThreatRAG_AI506_IEEE.html",
    "reports/ThreatRAG_AI506_IEEE.tex",
    "research/paper_to_project_mapping.md",
    "research/selected_base_paper.md",
    "scripts/build_and_run_notebook.py",
    "scripts/compile_ai506_deliverables.py",
    "scripts/generate_presentation.py"
]

for rel_path in files_to_update:
    if os.path.exists(rel_path):
        with open(rel_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace("Ahsan Habib Sitab", "Asfar Hossain Sitab")
        new_content = new_content.replace("Ahsan Habib", "Asfar Hossain")
        new_content = new_content.replace("আহসান হাবিব সিতাব", "আসফার হোসেন সিতাব")
        new_content = new_content.replace("AI506 Course Project", "AIML-507 / AI506 Course Project")

        if content != new_content:
            with open(rel_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[UPDATED] {rel_path}")
        else:
            print(f"[UNCHANGED] {rel_path}")
    else:
        print(f"[NOT FOUND] {rel_path}")
