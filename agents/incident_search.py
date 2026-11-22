"""
agents/incident_search.py
=========================
Agent 2: Historical Incident Similarity and Case-Based Retrieval.

Responsibilities:
1. Extracts key incident indicators, attack vectors, and target characteristics.
2. Executes hybrid retrieval and cross-encoder reranking over historical incident profiles.
3. Returns top-ranked historical incident matches with explicit retrieval similarity scores.
4. Explains shared characteristics, attack patterns, and crucial operational differences.
"""

from typing import Dict, Any, List, Optional
from rag.hybrid_retriever import AdaptiveHybridRetriever
from rag.citation_validator import CitationValidator

class IncidentSearchAgent:
    def __init__(
        self,
        retriever: Optional[AdaptiveHybridRetriever] = None,
        validator: Optional[CitationValidator] = None
    ):
        self.retriever = retriever or AdaptiveHybridRetriever()
        self.validator = validator or CitationValidator()

    def run(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Convenience method aligning with agent testing & API schemas."""
        res = self.search_similar_incidents(incident_description=query, top_k=k)
        matches = []
        for c in res.get("similar_incidents", []):
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
        return {
            "query": query,
            "historical_matches": matches,
            "summary_comparison": res.get("comparative_analysis_summary", "")
        }

    def search_similar_incidents(
        self,
        incident_description: str,
        structured_indicators: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieves and compares historically documented cyber incidents against the active case.
        """
        # Sanitize query
        clean_desc, is_safe, detected_flags = self.validator.sanitize_input(incident_description)

        # Formulate query focused on historical incidents
        query = f"Historical Incident breach case study: {clean_desc}"
        
        # Retrieval with intent routing
        retrieval_res = self.retriever.retrieve(
            query=query,
            structured_data=structured_indicators,
            top_k=top_k,
            enable_reranking=True
        )

        raw_results = retrieval_res["results"]

        # Parse incident comparison details
        similar_cases = []
        for rank, item in enumerate(raw_results, 1):
            cid = item["chunk_id"]
            title = item.get("source_title", "Unknown Case")
            score = item.get("rerank_score", item.get("score", 0.0))
            content = item.get("content", "")

            # Analyze shared attributes vs differences
            shared = []
            differences = []

            if "ddos" in clean_desc.lower() and "ddos" in content.lower():
                shared.append("High-volume network denial-of-service / packet saturation signature")
            elif "ransomware" in clean_desc.lower() and "ransomware" in content.lower():
                shared.append("Cryptographic extortion behavior and lateral movement")
            elif "rce" in clean_desc.lower() or "exploit" in clean_desc.lower():
                shared.append("Remote code execution via public-facing service vulnerability")
            else:
                shared.append("Corroborated adversarial tactic and technique indicators")

            if "log4j" in content.lower() and "log4j" not in clean_desc.lower():
                differences.append("Historical case leveraged Java JNDI lookups; current case lacks explicit JNDI artifacts.")
            elif "sunburst" in content.lower() and "supply chain" not in clean_desc.lower():
                differences.append("Historical case involved deep supply chain DLL trojanization.")
            else:
                differences.append("Target environment infrastructure and operational victim sector differ.")

            similar_cases.append({
                "rank": rank,
                "incident_id": item.get("document_id", cid),
                "title": title,
                "retrieval_similarity_score": round(float(score), 4),
                "score_type": "Normalized Cross-Encoder Retrieval Score (Not Threat Probability)",
                "source_url": item.get("source_url", ""),
                "citation_tag": f"[{cid}]",
                "attack_ids": item.get("attack_ids", []),
                "shared_characteristics": shared,
                "key_differences": differences,
                "snippet": content[:300] + ("..." if len(content) > 300 else "")
            })

        summary = (
            f"Evaluated {len(similar_cases)} historically documented incidents. "
            f"Top match: {similar_cases[0]['title']} (Retrieval Score: {similar_cases[0]['retrieval_similarity_score']:.4f}) "
            f"{similar_cases[0]['citation_tag']}. "
            f"Primary shared pattern: {similar_cases[0]['shared_characteristics'][0]}."
        ) if similar_cases else "No statistically significant historical matches retrieved."

        return {
            "agent": "IncidentSearchAdvisor",
            "query": clean_desc,
            "total_matches": len(similar_cases),
            "top_incident_id": similar_cases[0]["incident_id"] if similar_cases else None,
            "top_match_title": similar_cases[0]["title"] if similar_cases else None,
            "top_match_score": similar_cases[0]["retrieval_similarity_score"] if similar_cases else 0.0,
            "similar_incidents": similar_cases,
            "similarity_summary": summary,
            "evidence_citations": [c["citation_tag"] for c in similar_cases]
        }
