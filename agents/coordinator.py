"""
agents/coordinator.py
=====================
Agent 1: Coordinator / Planner Agent (AI506 Architecture)

Responsibilities:
1. Interprets user query and structured telemetry.
2. Identifies required analytical tasks (Threat ID, Incident Matching, Explanation, Playbook).
3. Selects appropriate specialist agents and determines execution schedule.
4. Maintains shared workflow state across multi-agent handoffs.
5. Manages the verification feedback loop and handles retry budget.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time

@dataclass
class WorkflowPlan:
    query: str
    requires_telemetry_analysis: bool
    requires_incident_search: bool
    requires_att_ck_mapping: bool
    requires_defensive_plan: bool
    selected_specialists: List[str]
    retrieval_strategy: str
    max_feedback_retries: int = 2

class CoordinatorAgent:
    def __init__(self, max_feedback_retries: int = 2):
        self.agent_name = "Coordinator / Planner"
        self.max_feedback_retries = max_feedback_retries

    def plan(self, query: str, telemetry: Optional[Dict[str, Any]] = None) -> WorkflowPlan:
        """
        Decomposes query and telemetry into task plan and schedules specialists.
        """
        has_telemetry = bool(telemetry and len(telemetry) > 0)
        q_lower = query.lower()

        # Task identification
        req_threat_id = has_telemetry or any(w in q_lower for w in ["threat", "attack", "ddos", "detect", "anomaly", "scan", "packet", "port", "surge"])
        req_incident = any(w in q_lower for w in ["incident", "precedent", "historical", "history", "mirai", "solarwinds", "moveit", "case", "breach"])
        req_explanation = any(w in q_lower for w in ["explain", "why", "evidence", "att&ck", "technique", "t1", "fact", "observation", "hypothesis"])
        req_defense = any(w in q_lower for w in ["defend", "mitigate", "remediate", "playbook", "response", "cisa", "contain", "recovery", "action"])

        # Default to full triage if broad or general query
        if not (req_threat_id or req_incident or req_explanation or req_defense):
            req_threat_id = True
            req_incident = True
            req_explanation = True
            req_defense = True

        specialists = []
        if req_threat_id:
            specialists.append("Cybersecurity Retrieval Specialist")
            specialists.append("Security Reasoning Specialist (Threat Identifier)")
        if req_incident:
            specialists.append("Security Reasoning Specialist (Incident Comparator)")
        if req_explanation:
            specialists.append("Security Reasoning Specialist (Evidence Explainer)")
        if req_defense:
            specialists.append("Security Reasoning Specialist (Defense Advisor)")
        
        # Verification Specialist is always active
        specialists.append("Evidence Verification Specialist")

        strategy = "adaptive_hybrid_tri_modal" if has_telemetry else "hybrid_dense_bm25"

        return WorkflowPlan(
            query=query,
            requires_telemetry_analysis=req_threat_id,
            requires_incident_search=req_incident,
            requires_att_ck_mapping=req_explanation or req_threat_id,
            requires_defensive_plan=req_defense,
            selected_specialists=list(dict.fromkeys(specialists)),
            retrieval_strategy=strategy,
            max_feedback_retries=self.max_feedback_retries
        )

    def evaluate_feedback(
        self,
        verification_report: Dict[str, Any],
        current_retry_count: int
    ) -> Dict[str, Any]:
        """
        Decides whether to trigger a re-retrieval feedback loop or finalize response.
        """
        is_grounded = verification_report.get("is_grounded", True)
        faithfulness = verification_report.get("faithfulness_score", 1.0)
        insufficient_evidence = verification_report.get("insufficient_evidence", False)

        should_retry = False
        reason = "Verification Passed"

        if (not is_grounded or faithfulness < 0.70 or insufficient_evidence) and current_retry_count < self.max_feedback_retries:
            should_retry = True
            reason = f"Verification failure (Faithfulness: {faithfulness:.2f}, Insufficient: {insufficient_evidence}). Triggering Feedback Loop {current_retry_count + 1}/{self.max_feedback_retries}."
        elif current_retry_count >= self.max_feedback_retries and (not is_grounded or insufficient_evidence):
            reason = f"Maximum feedback retries ({self.max_feedback_retries}) reached. Qualifying response with explicit uncertainty warnings."

        return {
            "should_retry": should_retry,
            "retry_count": current_retry_count + (1 if should_retry else 0),
            "reason": reason,
            "qualify_response": not should_retry and (not is_grounded or insufficient_evidence)
        }
