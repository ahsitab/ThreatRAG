"""
agents/retrieval_agent.py
========================
Agent 2: Cybersecurity Retrieval Specialist (AI506 Architecture)

Responsibilities:
1. Executes adaptive hybrid retrieval over ChromaDB vector store and BM25 sparse index.
2. Performs structured network flow matching against known attack telemetry profiles.
3. Retrieves historical incident precedents with source URLs and provenance tags.
4. Handles feedback loop re-retrieval requests by reformulating queries with expanded synonyms and relaxed thresholds.
"""

from typing import Dict, Any, List, Optional
from rag.hybrid_retriever import AdaptiveHybridRetriever

class CybersecurityRetrievalAgent:
    def __init__(self, retriever: Optional[AdaptiveHybridRetriever] = None):
        self.agent_name = "Cybersecurity Retrieval Specialist"
        self.retriever = retriever or AdaptiveHybridRetriever()

    def retrieve_evidence(
        self,
        query: str,
        structured_telemetry: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        feedback_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves candidate evidence chunks. Supports feedback-loop query expansion.
        """
        active_query = query
        if feedback_context:
            # Query expansion for feedback re-retrieval
            active_query = f"{query} {feedback_context} mitigation technique remediation detection"

        res = self.retriever.retrieve(
            query=active_query,
            structured_data=structured_telemetry,
            top_k=top_k,
            enable_reranking=True
        )

        results = res.get("results", [])
        retrieval_metadata = {
            "retriever": self.agent_name,
            "raw_query": query,
            "expanded_query": active_query if feedback_context else None,
            "strategy": res.get("routing_strategy", "adaptive_rrf"),
            "candidate_count": len(results),
            "top_chunks": [
                {
                    "chunk_id": r.get("chunk_id"),
                    "title": r.get("source_title"),
                    "score": float(r.get("rerank_score", r.get("score", 0.0))),
                    "source_url": r.get("source_url"),
                    "attack_ids": r.get("attack_ids", []),
                    "content_preview": r.get("content", "")[:200]
                }
                for r in results
            ]
        }

        return {
            "evidence_chunks": results,
            "retrieval_metadata": retrieval_metadata
        }
