"""
rag/hybrid_retriever.py
=======================
Adaptive Tri-Modal Hybrid Retrieval Engine for ThreatRAG.

Fuses:
1. Dense Semantic Retrieval (ChromaDB + Sentence Transformers)
2. Sparse Lexical Retrieval (BM25Okapi)
3. Structured Security Event Matcher (Flow & Telemetry characteristics)
4. Reciprocal Rank Fusion (RRF) with Query-Adaptive Dynamic Weighting
5. Neural Cross-Encoder Reranking
"""

import re
from typing import List, Dict, Any, Optional
from rag.chunking import KnowledgeChunk
from rag.vector_store import ThreatVectorStore
from rag.bm25_retriever import BM25Retriever
from rag.structured_retriever import StructuredEventRetriever
from rag.reranker import CrossEncoderReranker

class AdaptiveHybridRetriever:
    def __init__(
        self,
        vector_store: Optional[ThreatVectorStore] = None,
        bm25_retriever: Optional[BM25Retriever] = None,
        structured_retriever: Optional[StructuredEventRetriever] = None,
        reranker: Optional[CrossEncoderReranker] = None,
        rrf_k: int = 60
    ):
        self.vector_store = vector_store or ThreatVectorStore()
        self.bm25 = bm25_retriever or BM25Retriever()
        self.structured = structured_retriever or StructuredEventRetriever()
        self.reranker = reranker or CrossEncoderReranker()
        self.rrf_k = rrf_k

    def analyze_query_intent(self, query: str, structured_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Classifies incoming query intent to dynamically assign retrieval strategy weights.
        Returns weights for: dense, bm25, structured.
        """
        query_lower = query.lower()
        
        # 1. Pure structured telemetry / network flow
        if structured_data and (structured_data.get("destination_port") or structured_data.get("flow_duration")):
            return {
                "intent": "structured_telemetry",
                "weights": {"dense": 0.3, "bm25": 0.2, "structured": 0.5},
                "use_reranker": True
            }

        # 2. Specific Technique or CVE Lookup (e.g., T1059.001 or CVE-2023-34362)
        if re.search(r"\bT1\d{3}(?:\.\d{3})?\b", query, re.IGNORECASE) or re.search(r"\bCVE-\d{4}-\d{4,7}\b", query, re.IGNORECASE):
            return {
                "intent": "identifier_lookup",
                "weights": {"dense": 0.2, "bm25": 0.7, "structured": 0.1},
                "use_reranker": True
            }

        # 3. Incident Similarity or Case Comparison
        if "incident" in query_lower or "breach" in query_lower or "attack" in query_lower and ("similar" in query_lower or "history" in query_lower):
            return {
                "intent": "incident_similarity",
                "weights": {"dense": 0.45, "bm25": 0.35, "structured": 0.2},
                "use_reranker": True
            }

        # 4. Standard Conceptual / Natural Language Question
        return {
            "intent": "conceptual_qa",
            "weights": {"dense": 0.55, "bm25": 0.45, "structured": 0.0},
            "use_reranker": True
        }

    def retrieve(
        self,
        query: str,
        structured_data: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        candidate_pool_size: int = 20,
        enable_reranking: bool = True,
        strategy_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes adaptive tri-modal retrieval with reciprocal rank fusion and reranking.
        """
        # Analyze intent and obtain weights
        plan = self.analyze_query_intent(query, structured_data)
        if strategy_override == "dense_only":
            weights = {"dense": 1.0, "bm25": 0.0, "structured": 0.0}
            enable_reranking = False
        elif strategy_override == "sparse_only":
            weights = {"dense": 0.0, "bm25": 1.0, "structured": 0.0}
            enable_reranking = False
        elif strategy_override == "no_rerank":
            weights = plan["weights"]
            enable_reranking = False
        else:
            weights = plan["weights"]

        candidate_dict: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}

        # Branch 1: Dense Retrieval
        dense_hits = []
        if weights["dense"] > 0:
            dense_hits = self.vector_store.query(query, top_k=candidate_pool_size)
            for rank, hit in enumerate(dense_hits):
                cid = hit["chunk_id"]
                candidate_dict[cid] = hit
                rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (weights["dense"] / (self.rrf_k + rank + 1))

        # Branch 2: Sparse BM25 Retrieval
        sparse_hits = []
        if weights["bm25"] > 0:
            sparse_hits = self.bm25.query(query, top_k=candidate_pool_size)
            for rank, hit in enumerate(sparse_hits):
                cid = hit["chunk_id"]
                if cid not in candidate_dict:
                    candidate_dict[cid] = hit
                rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (weights["bm25"] / (self.rrf_k + rank + 1))

        # Branch 3: Structured Telemetry Matcher
        structured_hits = []
        if weights["structured"] > 0 and structured_data:
            structured_hits = self.structured.query(structured_data, top_k=candidate_pool_size)
            for rank, hit in enumerate(structured_hits):
                cid = hit["chunk_id"]
                if cid not in candidate_dict:
                    candidate_dict[cid] = hit
                rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (weights["structured"] / (self.rrf_k + rank + 1))

        # Rank candidates by RRF score
        fused_candidates = []
        for cid, score in sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True):
            cand = candidate_dict[cid]
            cand["fused_rrf_score"] = float(score)
            fused_candidates.append(cand)

        # Pre-select top candidates for reranker
        pre_rerank_pool = fused_candidates[:candidate_pool_size]

        # Branch 4: Cross-Encoder Reranking
        final_results = []
        if enable_reranking and self.reranker and len(pre_rerank_pool) > 0:
            final_results = self.reranker.rerank(query, pre_rerank_pool, top_n=top_k)
        else:
            final_results = pre_rerank_pool[:top_k]

        return {
            "query": query,
            "intent": plan["intent"],
            "strategy_weights": weights,
            "reranked": enable_reranking,
            "total_candidates": len(fused_candidates),
            "results": final_results,
            "dense_hit_count": len(dense_hits),
            "sparse_hit_count": len(sparse_hits),
            "structured_hit_count": len(structured_hits)
        }
