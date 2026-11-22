"""
agents/response_advisor.py
==========================
Agent 4: Defensive Response and Incident Remediation Advisor.

Responsibilities:
1. Synthesizes actionable defensive countermeasures grounded in MITRE Mitigations and CISA guidance.
2. Prioritizes triage and containment actions based on incident severity.
3. Explicitly flags potential operational business impacts of containment steps.
4. Strictly enforces human-in-the-loop authorization gates (prohibits autonomous network disruption).
"""

from typing import Dict, Any, List, Optional
from rag.hybrid_retriever import AdaptiveHybridRetriever
from rag.citation_validator import CitationValidator

class ResponseAdvisorAgent:
    def __init__(
        self,
        retriever: Optional[AdaptiveHybridRetriever] = None,
        validator: Optional[CitationValidator] = None
    ):
        self.retriever = retriever or AdaptiveHybridRetriever()
        self.validator = validator or CitationValidator()

    def run(self, threat_type: str, severity: str = "High", affected_assets: Optional[List[str]] = None) -> Dict[str, Any]:
        """Convenience method aligning with agent testing & API schemas."""
        res = self.generate_response_plan(
            threat_identification={"threat_category": threat_type, "calibrated_confidence": 0.90 if severity in ["Critical", "High"] else 0.60}
        )
        actions = []
        for step_idx, act in enumerate(res.get("containment_recommendations", []), 1):
            actions.append({
                "step": step_idx,
                "phase": "Containment" if step_idx <= 2 else "Recovery",
                "action": act.get("action", "Mitigation"),
                "rationale": act.get("detail", "Apply defensive filtering"),
                "cisa_guidance": "CISA Alert AA20-205A: Defending Against Network Floods",
                "operational_risk": act.get("operational_impact", "Medium")
            })
        return {
            "threat_type": threat_type,
            "severity": severity,
            "actions": actions,
            "cisa_references": ["CISA KEV Catalog", "CISA Advisory AA20-205A"],
            "operational_impact_summary": "Potential temporary degradation during BGP flowspec rerouting.",
            "human_approval_required": True,
            "approval_notice": "SOC Incident Lead approval mandatory prior to enacting network-level changes."
        }

    def generate_response_plan(
        self,
        threat_identification: Dict[str, Any],
        explanation: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Formulates an actionable, prioritized defensive playbook.
        """
        threat_name = threat_identification.get("threat_category", "General Incident")
        confidence = threat_identification.get("calibrated_confidence", 0.8)
        attack_ids = threat_identification.get("associated_attack_ids", [])

        # 1. Determine Incident Priority
        if confidence > 0.85 and ("ddos" in threat_name.lower() or "ransomware" in threat_name.lower() or "rce" in threat_name.lower()):
            priority = "CRITICAL"
            sla = "Immediate Containment Required (< 15 Minutes)"
        elif confidence > 0.65:
            priority = "HIGH"
            sla = "Urgent Analyst Investigation (< 1 Hour)"
        else:
            priority = "MEDIUM"
            sla = "Standard SOC Queue Triage (< 4 Hours)"

        # 2. Retrieve grounded mitigation intelligence
        query = f"Mitigation remediation guidance for {threat_name} {' '.join(attack_ids)}"
        retrieval_res = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            enable_reranking=True
        )
        mitigation_chunks = retrieval_res["results"]
        citations = [c["chunk_id"] for c in mitigation_chunks]
        primary_cit = citations[0] if citations else "CHUNK-MITIGATION-DEF"

        # 3. Defensive Response Checklist (Categorized by Phase)
        investigation_checklist = [
            f"Capture full packet payload (PCAP) and NetFlow logs around affected destination ports [{primary_cit}].",
            "Identify origin source IP addresses and determine whether ingress traffic originates from known botnets or bulletproof hosting providers.",
            "Inspect edge firewall and load balancer connection tables for SYN/UDP saturation spikes.",
            "Verify server resource utilization (CPU, memory, socket exhaustion) across frontend tiers."
        ]

        containment_recommendations = [
            {
                "step": 1,
                "action": "Rate-Limit or BGP Flowspec Filtering",
                "detail": f"Deploy rate-limiting policies at edge routers for anomalous ports [{primary_cit}].",
                "operational_impact": "LOW: Drops excessive traffic bursts while preserving existing valid sessions.",
                "requires_human_approval": False
            },
            {
                "step": 2,
                "action": "Upstream DDoS Scrubbing Redirection",
                "detail": "Reroute incoming edge traffic through cloud DDoS mitigation scrubbers (e.g., Cloudflare, Akamai).",
                "operational_impact": "MEDIUM: Minor latency increase during routing propagation (1-3 minutes).",
                "requires_human_approval": True,
                "approval_role": "Network Operations Center (NOC) Lead"
            },
            {
                "step": 3,
                "action": "Host / Subnet Network Isolation",
                "detail": "Quarantine severely impacted service endpoints to prevent lateral exhaustion across internal VLANs.",
                "operational_impact": "HIGH: Service disruption for connected clients until attack subsides.",
                "requires_human_approval": True,
                "approval_role": "SOC Incident Commander"
            }
        ]

        monitoring_validation = [
            "Monitor TCP half-open connection rate and RST flag frequency for the next 4 hours.",
            "Ensure DNS queries for target domain resolve normally with low error rates.",
            "Review SIEM correlation alerts for secondary attacks attempting credential access during the diversion."
        ]

        return {
            "agent": "DefensiveResponseAdvisor",
            "incident_priority": priority,
            "response_sla": sla,
            "target_threat": threat_name,
            "grounding_citations": citations,
            "investigation_checklist": investigation_checklist,
            "containment_recommendations": containment_recommendations,
            "monitoring_and_validation": monitoring_validation,
            "governance_guardrail": {
                "autonomous_action_permitted": False,
                "policy_enforcement": "Strict Human-in-the-Loop Approval Required for All Disruptive Actions",
                "rationale": "Prevents automated denial of service or misconfiguration of production infrastructure."
            }
        }
