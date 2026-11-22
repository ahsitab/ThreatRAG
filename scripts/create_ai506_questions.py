"""
scripts/create_ai506_questions.py
=================================
Compiles the official AI506 50-question benchmark dataset across the 4 ThreatRAG tasks:
- 15 Threat Identification questions
- 10 Historical Incident Similarity questions
- 15 Evidence-Based Explanation questions
- 10 Defensive Response questions
Includes ground truth, document references, difficulty levels, and insufficient evidence cases.
"""

import json
import csv
import os

QUESTIONS = [
    # --- TASK 1: THREAT IDENTIFICATION (15 Questions) ---
    {
        "question_id": "TID-001",
        "task_category": "Threat Identification",
        "question": "An inbound burst on destination port 80 exceeds 85,000 packets per second with short flow duration (8500 µs) and mean packet length of 18 bytes. What threat is this?",
        "expected_answer": "Network Denial of Service (DDoS) / SYN flood targeting port 80.",
        "relevant_document_ids": ["mitre_attack_T1498", "cic_ids2017_ddos"],
        "relevant_passage_ids": ["mitre-T1498.001", "cisa-kev-ddos"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Flag as potential volumetric flood with moderate uncertainty."
    },
    {
        "question_id": "TID-002",
        "task_category": "Threat Identification",
        "question": "A flow to destination port 443 displays 1,500,000 µs duration, 18 forward packets, 22 backward packets, and mean packet length of 450 bytes. Is this a threat?",
        "expected_answer": "Benign HTTPS network browsing session with normal packet symmetry.",
        "relevant_document_ids": ["cic_ids2017_benign"],
        "relevant_passage_ids": ["flow-benign-sample"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Report normal baseline parameters without generating false positives."
    },
    {
        "question_id": "TID-003",
        "task_category": "Threat Identification",
        "question": "Sequential connection attempts to port 22 with flow duration under 150 µs, 2 forward packets, zero backward packets, and zero payload bytes.",
        "expected_answer": "Port scan / network reconnaissance targeting SSH service.",
        "relevant_document_ids": ["mitre_attack_T1046"],
        "relevant_passage_ids": ["mitre-T1046"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Flag reconnaissance anomaly; recommend firewall connection logging."
    },
    {
        "question_id": "TID-004",
        "task_category": "Threat Identification",
        "question": "UDP traffic spike on port 53 with reflection amplification factor of 50x from open DNS resolvers.",
        "expected_answer": "DNS Amplification DDoS Attack (MITRE ATT&CK T1498.002).",
        "relevant_document_ids": ["mitre_attack_T1498", "incident_dyn_dns"],
        "relevant_passage_ids": ["mitre-T1498.002", "inc-dyn-dns"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Identify DNS protocol abuse and recommend response rate limiting."
    },
    {
        "question_id": "TID-005",
        "task_category": "Threat Identification",
        "question": "Excessive HTTP GET requests on port 8080 targeting API endpoints with randomized user agents and 12,000 requests/sec.",
        "expected_answer": "Application-Layer (Layer 7) HTTP Flood (MITRE ATT&CK T1499).",
        "relevant_document_ids": ["mitre_attack_T1499"],
        "relevant_passage_ids": ["mitre-T1499.001"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Recommend Web Application Firewall (WAF) rate limiting."
    },
    {
        "question_id": "TID-006",
        "task_category": "Threat Identification",
        "question": "TCP SYN packets without ACK responses directed at port 445 (SMB) across multiple subnets within 5 seconds.",
        "expected_answer": "Internal Network Service Scanning and SMB enumeration (T1046).",
        "relevant_document_ids": ["mitre_attack_T1046"],
        "relevant_passage_ids": ["mitre-T1046"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Highlight lateral movement preparation; request internal host logs."
    },
    {
        "question_id": "TID-007",
        "task_category": "Threat Identification",
        "question": "Inbound ICMP echo requests arriving at 200,000 packets per second with broadcast destination address.",
        "expected_answer": "ICMP Flood / Smurf Denial of Service attack.",
        "relevant_document_ids": ["mitre_attack_T1498"],
        "relevant_passage_ids": ["mitre-T1498"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Identify protocol flood; recommend dropping ingress ICMP at perimeter."
    },
    {
        "question_id": "TID-008",
        "task_category": "Threat Identification",
        "question": "NTP monlist query requests targeting port 123 generating 400x response amplification.",
        "expected_answer": "NTP Amplification Denial of Service attack.",
        "relevant_document_ids": ["mitre_attack_T1498"],
        "relevant_passage_ids": ["mitre-T1498.002"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Identify UDP amplification; advise disabling monlist queries."
    },
    {
        "question_id": "TID-009",
        "task_category": "Threat Identification",
        "question": "Persistent outbound beaconing from internal host to dynamic IP on port 8443 every 60 seconds with jitter.",
        "expected_answer": "Command and Control (C2) channel beaconing (MITRE ATT&CK T1071.001).",
        "relevant_document_ids": ["mitre_attack_T1071"],
        "relevant_passage_ids": ["mitre-T1071.001"],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "State that timing regularity suggests automated beaconing; demand DNS/proxy telemetry."
    },
    {
        "question_id": "TID-010",
        "task_category": "Threat Identification",
        "question": "HTTP POST payload containing sql statements: 'UNION SELECT username, password FROM users--'.",
        "expected_answer": "SQL Injection (SQLi) exploitation attempt (MITRE ATT&CK T1190).",
        "relevant_document_ids": ["mitre_attack_T1190", "incident_moveit"],
        "relevant_passage_ids": ["mitre-T1190", "cisa-cve-2023-34362"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Classify payload as web injection; inspect database tier logs."
    },
    {
        "question_id": "TID-011",
        "task_category": "Threat Identification",
        "question": "Single packet on port 9999 with zero content, standard latency, and no subsequent retransmissions.",
        "expected_answer": "Benign dropped packet or transient network noise; insufficient evidence of attack.",
        "relevant_document_ids": [],
        "relevant_passage_ids": [],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Explicitly report insufficient evidence to declare an incident."
    },
    {
        "question_id": "TID-012",
        "task_category": "Threat Identification",
        "question": "Sudden volume spike on port 3389 with repeated NTLM authentication failure events.",
        "expected_answer": "RDP Brute Force Credential Access attempt (MITRE ATT&CK T1110).",
        "relevant_document_ids": ["mitre_attack_T1110"],
        "relevant_passage_ids": ["mitre-T1110"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Recommend account lockout policies and IP blocking."
    },
    {
        "question_id": "TID-013",
        "task_category": "Threat Identification",
        "question": "Multiple fragmented IP packets arriving on port 80 with invalid offset fields causing kernel buffer warnings.",
        "expected_answer": "Teardrop / IP Fragmentation Denial of Service attack.",
        "relevant_document_ids": ["mitre_attack_T1498"],
        "relevant_passage_ids": ["mitre-T1498"],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Identify fragmentation anomaly; advise reassembly verification."
    },
    {
        "question_id": "TID-014",
        "task_category": "Threat Identification",
        "question": "Anomalous quantum tachyon modulation detected across local Ethernet switch ports.",
        "expected_answer": "Nonsense / Out-of-Domain concept; no cybersecurity threat grounded in corpus.",
        "relevant_document_ids": [],
        "relevant_passage_ids": [],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Explicitly reject the query as ungrounded with zero matching evidence."
    },
    {
        "question_id": "TID-015",
        "task_category": "Threat Identification",
        "question": "Ingress TCP connection attempts to port 80 with SYN flag set, zero payload, rate of 92,000 pkts/s, duration 4000 µs.",
        "expected_answer": "High-volume TCP SYN flood DDoS attack (T1498.001).",
        "relevant_document_ids": ["mitre_attack_T1498", "cic_ids2017_ddos"],
        "relevant_passage_ids": ["mitre-T1498.001"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Flag as critical volumetric threat with Platt-calibrated confidence > 95%."
    },

    # --- TASK 2: HISTORICAL INCIDENT SIMILARITY (10 Questions) ---
    {
        "question_id": "HIS-001",
        "task_category": "Historical Incident Similarity",
        "question": "Which historical cyber incident involved a massive IoT botnet conducting multi-vector DNS DDoS floods that brought down major internet services?",
        "expected_answer": "Dyn DNS DDoS Attack (October 2016) perpetrated by the Mirai botnet.",
        "relevant_document_ids": ["incident_dyn_dns"],
        "relevant_passage_ids": ["inc-dyn-dns"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Correlate with IoT botnet volumetric precedents."
    },
    {
        "question_id": "HIS-002",
        "task_category": "Historical Incident Similarity",
        "question": "What historical precedent compromised an enterprise software build pipeline to distribute a trojanized DLL (SUNBURST) to thousands of organizations?",
        "expected_answer": "SolarWinds Supply Chain Compromise (December 2020) by threat actor APT29.",
        "relevant_document_ids": ["incident_solarwinds"],
        "relevant_passage_ids": ["inc-solarwinds"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Highlight supply chain software tampering characteristics."
    },
    {
        "question_id": "HIS-003",
        "task_category": "Historical Incident Similarity",
        "question": "Which historical incident exploited zero-day SQL injection in an enterprise file transfer application (MOVEit) for mass extortion?",
        "expected_answer": "MOVEit Transfer Data Exfiltration Incident (May 2023) by the CL0P ransomware group (CVE-2023-34362).",
        "relevant_document_ids": ["incident_moveit", "cisa_kev_cve_2023_34362"],
        "relevant_passage_ids": ["inc-moveit", "cisa-cve-2023-34362"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Reference CISA KEV listing for CVE-2023-34362."
    },
    {
        "question_id": "HIS-004",
        "task_category": "Historical Incident Similarity",
        "question": "How does an active port 80 SYN flood compare with the 2016 Dyn DNS incident?",
        "expected_answer": "Both share volumetric saturation traits; Dyn differed by targeting DNS (port 53) via Mirai IoT botnet rather than a single web gateway.",
        "relevant_document_ids": ["incident_dyn_dns", "mitre_attack_T1498"],
        "relevant_passage_ids": ["inc-dyn-dns", "mitre-T1498"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Contrast protocol target (TCP/80 vs UDP/53)."
    },
    {
        "question_id": "HIS-005",
        "task_category": "Historical Incident Similarity",
        "question": "What historical incident utilized stolen HVAC vendor credentials to compromise point-of-sale systems?",
        "expected_answer": "Target Data Breach (2013) involving third-party vendor credential compromise.",
        "relevant_document_ids": ["historical_incidents"],
        "relevant_passage_ids": ["inc-target-2013"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Identify third-party risk as the root compromise vector."
    },
    {
        "question_id": "HIS-006",
        "task_category": "Historical Incident Similarity",
        "question": "Which ransomware campaign utilized EternalBlue SMB exploit for rapid lateral self-propagation across global networks in 2017?",
        "expected_answer": "WannaCry Ransomware Campaign (May 2017) exploiting MS17-010 (CVE-2017-0144).",
        "relevant_document_ids": ["historical_incidents", "mitre_attack_T1210"],
        "relevant_passage_ids": ["inc-wannacry-2017"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Reference SMB vulnerability and network worm propagation."
    },
    {
        "question_id": "HIS-007",
        "task_category": "Historical Incident Similarity",
        "question": "How does the MOVEit Transfer vulnerability differ from standard DDoS attacks?",
        "expected_answer": "MOVEit involved web application SQL injection for unauthorized data exfiltration, whereas DDoS focuses on network resource exhaustion.",
        "relevant_document_ids": ["incident_moveit", "mitre_attack_T1498"],
        "relevant_passage_ids": ["inc-moveit", "mitre-T1498"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Differentiate confidentiality compromise from availability impact."
    },
    {
        "question_id": "HIS-008",
        "task_category": "Historical Incident Similarity",
        "question": "What documented incident involved water treatment facility remote access tampering via TeamViewer in 2021?",
        "expected_answer": "Oldsmar Water Treatment Facility Cyber Intrusion (February 2021).",
        "relevant_document_ids": ["historical_incidents"],
        "relevant_passage_ids": ["inc-oldsmar-2021"],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Highlight remote desktop application misuse in operational technology."
    },
    {
        "question_id": "HIS-009",
        "task_category": "Historical Incident Similarity",
        "question": "Compare the Colonial Pipeline ransomware incident with the SolarWinds supply chain attack.",
        "expected_answer": "Colonial Pipeline was an enterprise ransomware attack via single legacy VPN credential; SolarWinds was a state-sponsored stealth supply chain backdoor.",
        "relevant_document_ids": ["incident_solarwinds", "historical_incidents"],
        "relevant_passage_ids": ["inc-solarwinds"],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Highlight extortion intent vs intelligence gathering."
    },
    {
        "question_id": "HIS-010",
        "task_category": "Historical Incident Similarity",
        "question": "Which historical incident occurred on Martian orbital relay satellites in the year 2012?",
        "expected_answer": "Fictional scenario; no matching incident precedent exists in authenticated repository.",
        "relevant_document_ids": [],
        "relevant_passage_ids": [],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Strictly report insufficient evidence and refuse to hallucinate."
    },

    # --- TASK 3: EVIDENCE-BASED EXPLANATION (15 Questions) ---
    {
        "question_id": "EBE-001",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain the technical difference between MITRE ATT&CK technique T1498.001 and T1498.002 based on evidence chunks.",
        "expected_answer": "T1498.001 represents Direct Volumetric Network Floods (e.g. SYN, ICMP); T1498.002 represents Reflection and Amplification Floods (e.g. DNS, NTP).",
        "relevant_document_ids": ["mitre_attack_T1498"],
        "relevant_passage_ids": ["mitre-T1498.001", "mitre-T1498.002"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Ground definitions in MITRE ATT&CK STIX descriptions."
    },
    {
        "question_id": "EBE-002",
        "task_category": "Evidence-Based Explanation",
        "question": "What empirical observation indicates socket exhaustion in web servers during a SYN flood?",
        "expected_answer": "High volume of TCP SYN requests without completing ACKs, consuming kernel half-open connection tables.",
        "relevant_document_ids": ["mitre_attack_T1498", "cic_ids2017_ddos"],
        "relevant_passage_ids": ["mitre-T1498"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Cite TCP three-way handshake telemetry."
    },
    {
        "question_id": "EBE-003",
        "task_category": "Evidence-Based Explanation",
        "question": "How does ThreatRAG separate empirical observations from hypotheses in threat triage?",
        "expected_answer": "Empirical observations consist of directly measured telemetry (packets/s, ports); hypotheses represent inferred attacker objectives.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-epistemic"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "State the epistemic separation policy."
    },
    {
        "question_id": "EBE-004",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain how CVE-2021-44228 (Log4Shell) achieves remote code execution according to CISA advisories.",
        "expected_answer": "Exploitation of JNDI lookup functionality in Apache Log4j2 allowing attackers to load arbitrary code from attacker-controlled LDAP/RMI servers.",
        "relevant_document_ids": ["cisa_kev_log4j"],
        "relevant_passage_ids": ["cisa-cve-2021-44228"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Ground in CISA KEV catalog description."
    },
    {
        "question_id": "EBE-005",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain the role of MITRE ATT&CK T1059 (Command and Scripting Interpreter) in adversary execution.",
        "expected_answer": "Adversaries abuse command interpreters (PowerShell, Bash, CMD) to execute malicious commands, scripts, or binaries.",
        "relevant_document_ids": ["mitre_attack_T1059"],
        "relevant_passage_ids": ["mitre-T1059.001"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Provide ATT&CK technique scope."
    },
    {
        "question_id": "EBE-006",
        "task_category": "Evidence-Based Explanation",
        "question": "Why is cross-encoder reranking important for evidence-grounded threat explanation?",
        "expected_answer": "Cross-encoders evaluate deep inter-token interactions between query and passage, suppressing irrelevant context and reducing hallucination.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-reranker"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Cite nDCG@5 improvement in retrieval experiments."
    },
    {
        "question_id": "EBE-007",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain why uncalibrated machine learning models produce dangerous overconfidence in cybersecurity.",
        "expected_answer": "Uncalibrated models output probabilities clustered near 0 and 1 regardless of true accuracy, leading SOC teams to trust incorrect detections.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-calibration"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Explain Platt scaling and Expected Calibration Error (ECE)."
    },
    {
        "question_id": "EBE-008",
        "task_category": "Evidence-Based Explanation",
        "question": "What ATT&CK technique corresponds to scheduled task persistence (T1053)?",
        "expected_answer": "T1053: Scheduled Task/Job, where adversaries abuse system scheduling utilities to maintain persistent access.",
        "relevant_document_ids": ["mitre_attack_T1053"],
        "relevant_passage_ids": ["mitre-T1053.005"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Cite Windows Task Scheduler and Linux Cron."
    },
    {
        "question_id": "EBE-009",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain the difference between volumetric DDoS (T1498) and application exhaustion DDoS (T1499).",
        "expected_answer": "Volumetric floods saturate network bandwidth (pipes); application floods exhaust server computational resources (CPU, threads, memory).",
        "relevant_document_ids": ["mitre_attack_T1498", "mitre_attack_T1499"],
        "relevant_passage_ids": ["mitre-T1498", "mitre-T1499"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Highlight Layer 3/4 vs Layer 7 distinctions."
    },
    {
        "question_id": "EBE-010",
        "task_category": "Evidence-Based Explanation",
        "question": "What is the security significance of the z-score feature attribution in ThreatRAG?",
        "expected_answer": "Z-score indicates how many standard deviations a flow feature deviates from benign training baseline, explaining why the model flagged the alert.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-attribution"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Ground in statistical standardization formula."
    },
    {
        "question_id": "EBE-011",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain how prompt injection attacks attempt to compromise cybersecurity RAG agents.",
        "expected_answer": "Attackers inject override instructions into ingested logs or queries ('IGNORE ALL INSTRUCTIONS') to force the model to output secrets or grant access.",
        "relevant_document_ids": ["rag_citation_validator"],
        "relevant_passage_ids": ["sanitizer-defense"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Demonstrate ThreatRAG's automated regex redaction filter."
    },
    {
        "question_id": "EBE-012",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain the vulnerability details of CVE-2023-34362 from CISA KEV records.",
        "expected_answer": "A SQL injection vulnerability in Progress MOVEit Transfer that allows unauthenticated remote attackers to gain access to the database.",
        "relevant_document_ids": ["cisa_kev_cve_2023_34362"],
        "relevant_passage_ids": ["cisa-cve-2023-34362"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Quote CISA KEV catalog remediation date."
    },
    {
        "question_id": "EBE-013",
        "task_category": "Evidence-Based Explanation",
        "question": "What evidence indicates a Slowloris attack versus a volumetric SYN flood?",
        "expected_answer": "Slowloris opens numerous slow HTTP connections with low bandwidth, keeping sockets open; SYN flood sends massive packet rates.",
        "relevant_document_ids": ["mitre_attack_T1499"],
        "relevant_passage_ids": ["mitre-T1499.001"],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Differentiate low-and-slow Layer 7 from high-rate Layer 4."
    },
    {
        "question_id": "EBE-014",
        "task_category": "Evidence-Based Explanation",
        "question": "Explain the mechanism of faster-than-light subspace transceiver packet exploitation.",
        "expected_answer": "Sci-fi concept; no valid evidence or security standard supports this phenomenon.",
        "relevant_document_ids": [],
        "relevant_passage_ids": [],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Trigger verification abstention on ungrounded concepts."
    },
    {
        "question_id": "EBE-015",
        "task_category": "Evidence-Based Explanation",
        "question": "How does Reciprocal Rank Fusion (RRF) combine dense and sparse rankings?",
        "expected_answer": "RRF computes the sum of reciprocal ranks 1/(k + r) across individual retrievers, eliminating score distribution scale disparities.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-rrf"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Cite RRF formula with k=60."
    },

    # --- TASK 4: DEFENSIVE RESPONSE RECOMMENDATIONS (10 Questions) ---
    {
        "question_id": "DRR-001",
        "task_category": "Defensive Response",
        "question": "What are the recommended containment actions for an ongoing volumetric TCP SYN flood targeting port 80?",
        "expected_answer": "Deploy edge rate-limiting, activate SYN cookies, enable BGP Flowspec filtering, and redirect ingress traffic to scrubbing centers.",
        "relevant_document_ids": ["cisa_guidance_ddos", "mitre_mitigation_M1037"],
        "relevant_passage_ids": ["cisa-aa20-205a", "mitre-m1037"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Enforce Human-in-the-Loop authorization before firewall changes."
    },
    {
        "question_id": "DRR-002",
        "task_category": "Defensive Response",
        "question": "What remediation is required for CISA KEV CVE-2023-34362 (MOVEit)?",
        "expected_answer": "Apply vendor security patches immediately, block external HTTP/HTTPS traffic to MOVEit if unpatched, and audit database accounts.",
        "relevant_document_ids": ["cisa_kev_cve_2023_34362"],
        "relevant_passage_ids": ["cisa-cve-2023-34362"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Cite CISA Known Exploited Vulnerability deadline."
    },
    {
        "question_id": "DRR-003",
        "task_category": "Defensive Response",
        "question": "Why is Human-in-the-Loop approval strictly enforced in ThreatRAG defensive recommendations?",
        "expected_answer": "Automated mitigation without analyst oversight risks severe self-inflicted denial of service and misconfiguration of production infrastructure.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-governance"],
        "difficulty": "Easy",
        "expected_behavior_under_insufficient_evidence": "Emphasize ethical governance and supervisory AI role."
    },
    {
        "question_id": "DRR-004",
        "task_category": "Defensive Response",
        "question": "What immediate mitigation should be applied when internal port scanning (T1046) is detected?",
        "expected_answer": "Isolate the originating internal IP/host on the local VLAN, inspect active processes, and capture volatile memory.",
        "relevant_document_ids": ["mitre_mitigation_M1035"],
        "relevant_passage_ids": ["mitre-m1035"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Recommend host-based quarantine."
    },
    {
        "question_id": "DRR-005",
        "task_category": "Defensive Response",
        "question": "What is the operational risk of enacting BGP Flowspec network null-routing during a suspected attack?",
        "expected_answer": "High risk of service disruption if legitimate customer IP traffic is inadvertently included in the null-routed CIDR block.",
        "relevant_document_ids": ["research_methodology"],
        "relevant_passage_ids": ["methodology-operational-risk"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Warn of false-positive service outage."
    },
    {
        "question_id": "DRR-006",
        "task_category": "Defensive Response",
        "question": "What mitigations prevent DNS amplification attacks on recursive resolvers?",
        "expected_answer": "Disable open recursion on public-facing DNS servers and implement Response Rate Limiting (RRL).",
        "relevant_document_ids": ["cisa_guidance_ddos"],
        "relevant_passage_ids": ["cisa-dns-rrl"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Cite CISA DNS defense guidance."
    },
    {
        "question_id": "DRR-007",
        "task_category": "Defensive Response",
        "question": "What steps are required to mitigate remote execution of Log4Shell (CVE-2021-44228)?",
        "expected_answer": "Upgrade Log4j to >= 2.17.1, remove JndiLookup.class from classpath, or set log4j2.formatMsgNoLookups=true.",
        "relevant_document_ids": ["cisa_kev_log4j"],
        "relevant_passage_ids": ["cisa-cve-2021-44228"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Reference CISA Log4j remediation advisory."
    },
    {
        "question_id": "DRR-008",
        "task_category": "Defensive Response",
        "question": "What is the recovery protocol following a ransomware compromise?",
        "expected_answer": "Restore systems from verified offline immutable backups, rotate all directory credentials, and rebuild compromised host images.",
        "relevant_document_ids": ["cisa_guidance_ransomware"],
        "relevant_passage_ids": ["cisa-ransomware-playbook"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Highlight clean offline backup restoration."
    },
    {
        "question_id": "DRR-009",
        "task_category": "Defensive Response",
        "question": "What containment action is recommended when C2 beaconing to a malicious domain is confirmed?",
        "expected_answer": "Sinkhole the destination domain at perimeter DNS resolvers and isolate the internal host for forensic acquisition.",
        "relevant_document_ids": ["mitre_mitigation_M1020"],
        "relevant_passage_ids": ["mitre-m1020"],
        "difficulty": "Medium",
        "expected_behavior_under_insufficient_evidence": "Cite DNS filtering and endpoint isolation."
    },
    {
        "question_id": "DRR-010",
        "task_category": "Defensive Response",
        "question": "What defensive playbook handles planetary shield generator network disruptions?",
        "expected_answer": "Fictional scenario; ThreatRAG acknowledges insufficient ground truth and abstains from recommending production changes.",
        "relevant_document_ids": [],
        "relevant_passage_ids": [],
        "difficulty": "Hard",
        "expected_behavior_under_insufficient_evidence": "Explicitly refuse to generate unsupported containment actions."
    }
]

def main():
    out_dir = "data/evaluation"
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "ai506_test_questions.json")
    csv_path = os.path.join(out_dir, "ai506_test_questions.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, indent=2)
    print(f"[OK] Saved {len(QUESTIONS)} questions to {json_path}")

    fieldnames = [
        "question_id", "task_category", "question", "expected_answer",
        "relevant_document_ids", "relevant_passage_ids", "difficulty",
        "expected_behavior_under_insufficient_evidence"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in QUESTIONS:
            row = dict(q)
            row["relevant_document_ids"] = ";".join(q["relevant_document_ids"])
            row["relevant_passage_ids"] = ";".join(q["relevant_passage_ids"])
            writer.writerow(row)
    print(f"[OK] Saved CSV to {csv_path}")

if __name__ == "__main__":
    main()
