# Scientific Audit and Submission Checklist

## What was included
- [x] User-provided website home screenshot (`figures/website_home.png`).
- [x] User-provided results screenshot (`figures/website_research_results.png`).
- [x] Knowledge-corpus EDA, flow distributions, feature correlations (unchanged notebook exports).
- [x] Latest classification CSV: 9 calibration/model configurations.
- [x] Latest retrieval CSV: 4 experimental configurations E2–E5.
- [x] Latest generation CSV: E1–E5 and its evaluator inconsistency.
- [x] Latest component-ablation CSV: 8 variants.
- [x] Latest 5-case agent-performance CSV.
- [x] Latest 50-question baseline CSV with recomputed means/denominators.
- [x] MAIN-RAG as the primary methodological paper, with correct Predictor–Judge–Final-Predictor description.
- [x] 20 additional DOI-linked peer-reviewed related studies.
- [x] Merged 21-study related-work table, agent-capability table, and interpretive text after every display.
- [x] 12-page compiled IEEE journal-style PDF, full editable LaTeX.

## Must resolve before peer-reviewed submission
- [ ] Reproduce the LightGBM performance and calibration on the exact same data, feature order, label encoding and artifact version; reconcile the saved notebook's 50% classification against the newer 99.98% CSV.
- [ ] Establish whether baseline timing included the same LLM generation and network calls as ThreatRAG.
- [ ] Validate citations by sentence-level entailment with independent review; current constant precision scores are not sufficient.
- [ ] Investigate why adaptive E5 nDCG@5 is worse than the reranked E4 configuration.
- [ ] Re-run ablations with direct controlled executions, not manually synthesized or untraceable aggregates.
- [ ] Validate that retrieval relevance labels are independent of tuning and expand the 10-query benchmark.
- [ ] Evaluate performance on realistic class imbalance, unseen dates and other intrusion datasets.
- [ ] Report uncertainty intervals on the 50-question comparison and separately examine abstention.
- [ ] Reconcile conflicting report Markdown and raw CSV aggregates; preserve experiment hashes and timestamps.
- [ ] Migrate final source to the latest official `ieeeaccess.cls` package, which was not available offline.
- [ ] Confirm authorship, correspondence, affiliations, research ethics and dataset licenses.
- [ ] Confirm DOI bibliographic data in the final publisher submission system.

## Interpretation of screenshot claims
- The homepage visibly reports KB chunks 1,074; ATT&CK techniques 718; CISA KEV entries 1,790; calibrated ECE 0.0005. These are author-supplied screenshot observations, not server-side checks.
- The research-contributions screenshot labels nDCG@5 0.7243 (E4) / 0.6774 (E5), while citing a +22.1% increase. The +22.1% increase corresponds to E4 relative to E2, not E5.
- The screenshot's ``100% adversarial injection defense'' claim is unsupported by the provided 5-row performance CSV, where one adversarial task is merely marked completed.
- The screenshot's baseline FPR for Logistic Regression 0.0073 differs from the raw Logistic Regression row in the classification CSV (0.0143).

## Reference verification
All 21 scholarly entries have a populated DOI and a clickable DOI URL. MAIN-RAG and TechniqueRAG match ACL Anthology metadata, as do MASS-RAG, the recent 2025/2026 studies, and key background papers. Non-scholarly datasets and repository items can lack a DOI and should instead carry an official source URL and access date.
