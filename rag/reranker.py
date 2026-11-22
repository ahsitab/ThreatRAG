"""
rag/reranker.py
===============
Cross-Encoder Reranker for ThreatRAG.
Evaluates joint query-document cross-attention to rescore and refine candidate retrieval pools.
Includes a fast fallback reranker for air-gapped environments.
"""

from typing import List, Dict, Any, Optional

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import CrossEncoder
            print(f"[RERANKER] Loading CrossEncoder: {self.model_name}...")
            self.model = CrossEncoder(self.model_name, device="cpu")
            print("[RERANKER] CrossEncoder loaded successfully.")
        except Exception as e:
            print(f"[RERANKER] Could not initialize neural CrossEncoder ({e}). Utilizing exact-match & overlap scoring.")
            self.model = None

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        if len(candidates) <= 1:
            return candidates[:top_n]

        if self.model is not None:
            try:
                pairs = [[query, c.get("content", "")] for c in candidates]
                scores = self.model.predict(pairs)
                # Map raw scores through sigmoid if not normalized
                import numpy as np
                norm_scores = 1.0 / (1.0 + np.exp(-np.clip(scores, -10, 10)))
                
                for cand, s in zip(candidates, norm_scores):
                    cand["rerank_score"] = float(s)
                
                reranked = sorted(candidates, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
                return reranked[:top_n]
            except Exception as e:
                print(f"[RERANKER] Neural reranking error: {e}. Executing heuristic rerank.")

        # Fallback Reranking: Query term coverage, exact token bonus, and length-penalty normalization
        query_terms = set(query.lower().split())
        for c in candidates:
            content = c.get("content", "").lower()
            overlap = sum(1 for t in query_terms if t in content)
            coverage = overlap / max(1, len(query_terms))
            # Exact phrase match bonus
            exact_bonus = 0.2 if query.lower() in content else 0.0
            initial_score = float(c.get("score", 0.5))
            c["rerank_score"] = min(1.0, 0.5 * initial_score + 0.4 * coverage + exact_bonus)

        reranked = sorted(candidates, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        return reranked[:top_n]
