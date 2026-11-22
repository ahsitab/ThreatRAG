# ThreatRAG — Clean IEEE-style manuscript

This revision removes file-format terminology from scholarly captions, converts the research metrics screenshot into an editable LaTeX table, and improves float placement.

## Build
From this directory, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error ThreatRAG_IEEE_Access_Clean_Final.tex
pdflatex -interaction=nonstopmode -halt-on-error ThreatRAG_IEEE_Access_Clean_Final.tex
```

The manuscript uses the IEEEtran journal class; final submissions to IEEE Access must use the publisher's current class/template.

## Reproducibility
`data_snapshots/` contains original experiment records; `source_artifacts/` contains the notebook and base-paper material. The manuscript describes conflicting experimental runs rather than silently combining them.
