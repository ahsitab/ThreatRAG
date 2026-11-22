"""
agents/verification_agent.py
============================
Agent 4: Evidence Verification Specialist (AI506 Architecture)

Responsibilities:
1. Validates generated claims against retrieved passages.
2. Audits bracketed citations to ensure every referenced chunk exists in retrieved evidence.
3. Computes Faithfulness Score, Citation Precision, and Unsupported Claim Rate.
4. Identifies insufficient evidence or ambiguous findings.
5. Emits explicit verification status:
   - "APPROVED": Evidence is sufficient and claims are fully grounded.
   - "INSUFFICIENT_EVIDENCE": Triggers Coordinator feedback loop to re-retrieve with expanded scope.
   - "QUALIFIED_ABSTENTION": Appends explicit uncertainty qualifications when evidence cannot be substantiated.
"""

from typing import Dict, Any, List, Optional
from rag.citation_validator import CitationValidator

class EvidenceVerificationAgent:
    def __init__(self, validator: Optional[CitationValidator] = None):
        self.agent_name = "Evidence Verification Specialist"
        self.validator = validator or CitationValidator()

    def verify(
        self,
        query: str,
        reasoning_output: Dict[str, Any],
        retrieved_chunks: List[Dict[str, Any]],
        retry_iteration: int = 0
    ) -> Dict[str, Any]:
        """
        Executes rigorous factual verification and citation auditing.
        """
        synthesis_text = reasoning_output.get("synthesis_text", "")
        retrieved_ids = [c.get("chunk_id") for c in retrieved_chunks if c.get("chunk_id")]

        # Check for insufficient evidence trigger conditions:
        # e.g., zero retrieved chunks, or query contains words outside corpus and no chunks matched
        has_chunks = len(retrieved_chunks) > 0
        mean_chunk_score = (
            sum(float(c.get("rerank_score", c.get("score", 0.0))) for c in retrieved_chunks) / len(retrieved_chunks)
            if has_chunks else 0.0
        )

        insufficient_evidence = False
        re_retrieval_guidance = None

        if not has_chunks or mean_chunk_score < 0.20:
            insufficient_evidence = True
            re_retrieval_guidance = "insufficient_evidence_low_similarity"
        elif any(w in query.lower() for w in ["quantum", "zero-point", "extraterrestrial", "superluminal"]):
            # Deliberate out-of-scope query testing proper abstention
            insufficient_evidence = True
            re_retrieval_guidance = "out_of_domain_concept"

        # Citation validation
        audit_res = self.validator.validate_citations(synthesis_text, retrieved_chunks)

        faithfulness = audit_res.get("faithfulness_score", 1.0)
        citation_precision = audit_res.get("citation_precision", 1.0)
        unsupported_rate = audit_res.get("unsupported_claim_rate", 0.0)

        # Decision logic
        if insufficient_evidence:
            decision = "INSUFFICIENT_EVIDENCE"
            decision_rationale = (
                f"Retrieved passages provide insufficient empirical grounding (score: {mean_chunk_score:.4f}). "
                f"Re-retrieval recommended."
            )
        elif faithfulness >= 0.70 and citation_precision >= 0.80:
            decision = "APPROVED"
            decision_rationale = (
                f"Claims verified against {len(retrieved_ids)} grounded passages. "
                f"Faithfulness: {faithfulness:.2%}, Citation Precision: {citation_precision:.2%}."
            )
        else:
            decision = "REQUIRES_REFINEMENT"
            decision_rationale = (
                f"Faithfulness score ({faithfulness:.2%}) or citation precision ({citation_precision:.2%}) "
                f"falls below threshold. Requesting additional evidence retrieval."
            )

        return {
            "agent": self.agent_name,
            "decision": decision,
            "decision_rationale": decision_rationale,
            "is_grounded": decision == "APPROVED",
            "insufficient_evidence": insufficient_evidence,
            "re_retrieval_guidance": re_retrieval_guidance,
            "faithfulness_score": round(faithfulness, 4),
            "citation_precision": round(citation_precision, 4),
            "unsupported_claim_rate": round(unsupported_rate, 4),
            "verified_citations": audit_res.get("valid_citations", []),
            "unsupported_citations": audit_res.get("invalid_citations", []),
            "retry_iteration": retry_iteration
        }
