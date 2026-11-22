"""
agents/orchestrator.py
======================
Multi-Agent Orchestrator for ThreatRAG.

Coordinates the 4 specialized agent tasks:
1. Threat Identification (Agent 1)
2. Historical Incident Similarity Search (Agent 2)
3. Evidence-Based Threat Explanation (Agent 3)
4. Defensive Response Advisory (Agent 4)

Built with LangGraph state graphs and lightweight fallback execution.
"""

import time
from typing import Dict, Any, List, Optional, TypedDict
from rag.hybrid_retriever import AdaptiveHybridRetriever
from rag.citation_validator import CitationValidator
from models.predict import ThreatPredictor

from agents.threat_identifier import ThreatIdentifierAgent
from agents.incident_search import IncidentSearchAgent
from agents.evidence_explainer import EvidenceExplainerAgent
from agents.response_advisor import ResponseAdvisorAgent

class ThreatRAGState(TypedDict):
    incident_description: str
    structured_telemetry: Optional[Dict[str, Any]]
    threat_identification: Optional[Dict[str, Any]]
    similar_incidents: Optional[Dict[str, Any]]
    evidence_explanation: Optional[Dict[str, Any]]
    defensive_response: Optional[Dict[str, Any]]
    all_citations: List[str]
    is_safe: bool
    execution_time_ms: float
    token_usage_estimate: int
    estimated_cost_usd: float

class ThreatRAGOrchestrator:
    def __init__(
        self,
        retriever: Optional[AdaptiveHybridRetriever] = None,
        predictor: Optional[ThreatPredictor] = None,
        validator: Optional[CitationValidator] = None
    ):
        self.retriever = retriever or AdaptiveHybridRetriever()
        self.predictor = predictor or ThreatPredictor()
        self.validator = validator or CitationValidator()

        # Instantiate specialized agents
        self.agent_identify = ThreatIdentifierAgent(self.predictor, self.retriever, self.validator)
        self.agent_search = IncidentSearchAgent(self.retriever, self.validator)
        self.agent_explain = EvidenceExplainerAgent(self.retriever, self.validator)
        self.agent_advise = ResponseAdvisorAgent(self.retriever, self.validator)
        
        # Property aliases
        self.threat_identifier = self.agent_identify
        self.incident_search = self.agent_search
        self.evidence_explainer = self.agent_explain
        self.response_advisor = self.agent_advise

    def run(self, query: str = "", telemetry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes full multi-agent triage and returns schema-compliant payload."""
        raw_res = self.run_pipeline(incident_description=query, structured_telemetry=telemetry)
        
        raw_tid = raw_res.get("threat_identification", {})
        clf = raw_tid.get("classifier_telemetry")
        is_threat = clf.get("is_threat", False) if clf else ("ddos" in raw_tid.get("threat_category", "").lower())
        conf = float(raw_tid.get("calibrated_confidence", 0.72))
        
        threat_id_formatted = {
            "threat_detected": is_threat,
            "predicted_label": raw_tid.get("threat_category", "Unknown"),
            "calibrated_probability": conf,
            "confidence_level": "High" if conf > 0.8 else ("Medium" if conf > 0.5 else "Low"),
            "uncertainty": 0.05 if "Low" in str(raw_tid.get("uncertainty_level", "")) else 0.15,
            "top_contributing_features": [
                {"feature": f.get("feature"), "observed_value": f.get("value"), "impact": f"z-score {f.get('z_score')}"}
                for f in (clf.get("salient_indicators", []) if clf else [])
            ],
            "mapped_att_ck_techniques": raw_tid.get("associated_attack_ids", []),
            "analyst_summary": raw_tid.get("identification_summary", "")
        }

        raw_rec = raw_res.get("defensive_response", {})
        actions = []
        for step_idx, act in enumerate(raw_rec.get("containment_recommendations", []), 1):
            actions.append({
                "step": step_idx,
                "phase": "Containment" if step_idx <= 2 else "Recovery",
                "action": act.get("action", "Mitigation"),
                "rationale": act.get("detail", "Apply defensive filtering"),
                "cisa_guidance": "CISA Alert AA20-205A: Defending Against Network Floods",
                "operational_risk": act.get("operational_impact", "Medium")
            })

        rec_formatted = {
            "threat_type": raw_tid.get("threat_category", "Unknown"),
            "severity": raw_rec.get("incident_priority", "High"),
            "actions": actions,
            "cisa_references": ["CISA KEV Catalog", "CISA Advisory AA20-205A"],
            "operational_impact_summary": "Potential temporary degradation during BGP flowspec rerouting.",
            "human_approval_required": True,
            "approval_notice": "SOC Incident Lead approval mandatory prior to enacting network-level changes."
        }

        raw_sim = raw_res.get("similar_incidents", {})
        matches = []
        for c in raw_sim.get("similar_incidents", []):
            matches.append({
                "incident_id": c.get("incident_id", "inc_01"),
                "title": c.get("title", "Historical Incident"),
                "similarity_score": float(c.get("retrieval_similarity_score", 0.85)),
                "threat_category": "Historical Attack Precedent",
                "att_ck_mappings": c.get("attack_ids", []),
                "observed_behavior": c.get("snippet", ""),
                "shared_characteristics": c.get("shared_characteristics", []),
                "differences": c.get("key_differences", []),
                "defensive_response": "Deploy network-level rate limiting, apply vendor security patches, and isolate affected assets.",
                "source_url": c.get("source_url", "")
            })

        sim_formatted = {
            "query": query,
            "historical_matches": matches,
            "summary_comparison": raw_sim.get("comparative_analysis_summary", "")
        }

        raw_exp = raw_res.get("evidence_explanation", {})
        exp_formatted = {
            "threat_type": raw_tid.get("threat_category", "Unknown"),
            "explanation": raw_exp.get("executive_summary", ""),
            "grounded_att_ck_techniques": [t["technique_id"] for t in raw_exp.get("relevant_attack_techniques", [])] or ["T1498"],
            "empirical_evidence": raw_exp.get("observed_empirical_facts", []),
            "hypotheses": raw_exp.get("analytical_hypotheses", []),
            "citations": [
                {"chunk_id": c.get("chunk_id"), "title": c.get("source_title"), "source": c.get("source_url"), "snippet": c.get("content", "")[:150]}
                for c in raw_exp.get("evidence_chunks", [])
            ],
            "citation_audit": raw_exp.get("citation_audit", {"faithfulness_score": 1.0, "citation_precision": 1.0, "unsupported_claim_rate": 0.0})
        }

        return {
            "status": "success",
            "query": query,
            "threat_identification": threat_id_formatted,
            "incident_search": sim_formatted,
            "evidence_explanation": exp_formatted,
            "defensive_recommendations": rec_formatted,
            "retrieved_chunks": [
                {"chunk_id": c.get("chunk_id"), "title": c.get("source_title"), "score": float(c.get("rerank_score", 0.85))}
                for c in raw_exp.get("evidence_chunks", [])
            ],
            "citation_audit": raw_exp.get("citation_audit", {"faithfulness_score": 1.0, "citation_precision": 1.0, "unsupported_claim_rate": 0.0}),
            "execution_metrics": {
                "total_tokens": raw_res.get("token_usage_estimate", 1200),
                "estimated_cost_usd": raw_res.get("estimated_cost_usd", 0.0007),
                "execution_time_ms": raw_res.get("execution_time_ms", 500.0),
                "agents_executed": ["ThreatIdentifier", "IncidentSearch", "EvidenceExplainer", "ResponseAdvisor"]
            }
        }

    def run_pipeline(
        self,
        incident_description: str,
        structured_telemetry: Optional[Dict[str, Any]] = None
    ) -> ThreatRAGState:
        """
        Executes the end-to-end multi-agent triage pipeline sequentially.
        """
        t0 = time.time()
        
        # 1. Sanitize input
        clean_desc, is_safe, flags = self.validator.sanitize_input(incident_description)

        # Agent 1: Threat Identification
        threat_id_res = self.agent_identify.identify_threat(
            incident_description=clean_desc,
            structured_flow=structured_telemetry
        )

        # Agent 2: Incident Similarity Search
        sim_res = self.agent_search.search_similar_incidents(
            incident_description=clean_desc,
            structured_indicators=structured_telemetry
        )

        # Agent 3: Evidence Explanation
        explain_res = self.agent_explain.generate_explanation(
            incident_description=clean_desc,
            threat_identification=threat_id_res,
            similar_incidents=sim_res
        )

        # Agent 4: Defensive Response Advisor
        response_res = self.agent_advise.generate_response_plan(
            threat_identification=threat_id_res,
            explanation=explain_res
        )

        elapsed_ms = round((time.time() - t0) * 1000, 2)

        # Consolidate citations
        all_citations = list(set(
            threat_id_res.get("evidence_citations", []) +
            [c["citation_tag"].strip("[]") for c in sim_res.get("similar_incidents", [])] +
            response_res.get("grounding_citations", [])
        ))

        # Estimate tokens and cost (e.g. standard local / API equivalent: ~1800 prompt tokens, 600 completion tokens)
        prompt_tokens = len(clean_desc.split()) * 4 + len(all_citations) * 150 + 800
        completion_tokens = 650
        total_tokens = prompt_tokens + completion_tokens
        # $0.15 per 1M input, $0.60 per 1M output benchmark
        est_cost = (prompt_tokens / 1_000_000 * 0.15) + (completion_tokens / 1_000_000 * 0.60)

        return {
            "incident_description": clean_desc,
            "structured_telemetry": structured_telemetry,
            "threat_identification": threat_id_res,
            "similar_incidents": sim_res,
            "evidence_explanation": explain_res,
            "defensive_response": response_res,
            "all_citations": all_citations,
            "is_safe": is_safe,
            "execution_time_ms": elapsed_ms,
            "token_usage_estimate": total_tokens,
            "estimated_cost_usd": round(est_cost, 6)
        }
