"""
rag/bm25_retriever.py
=====================
BM25 Lexical Retriever for exact keyword, CVE, ATT&CK identifier, and indicator matching.
Uses rank_bm25 (BM25Okapi) with domain-specific tokenization.
"""

import os
import pickle
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from rag.chunking import KnowledgeChunk, security_aware_tokenize

class BM25Retriever:
    def __init__(self, index_path: str = "artifacts/bm25_index.pkl"):
        self.index_path = index_path
        self.bm25: Optional[BM25Okapi] = None
        self.chunks: List[KnowledgeChunk] = []
        self.tokenized_corpus: List[List[str]] = []
        self._load_if_exists()

    def _load_if_exists(self):
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "rb") as f:
                    data = pickle.load(f)
                    self.bm25 = data["bm25"]
                    self.chunks = data["chunks"]
                    self.tokenized_corpus = data["tokenized_corpus"]
            except Exception as e:
                print(f"[BM25] Error loading cached index ({e}). Rebuilding required.")

    def build_index(self, chunks: List[KnowledgeChunk]):
        if not chunks:
            return
        self.chunks = chunks
        self.tokenized_corpus = [security_aware_tokenize(c.content + " " + c.source_title + " " + " ".join(c.attack_ids)) for c in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.save_index()

    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump({
                "bm25": self.bm25,
                "chunks": self.chunks,
                "tokenized_corpus": self.tokenized_corpus
            }, f)

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.bm25 is None or not self.chunks:
            return []

        tokens = security_aware_tokenize(query_text)
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        max_score = max(scores) if len(scores) > 0 and max(scores) > 0 else 1.0

        hits = []
        for idx in top_indices:
            score = float(scores[idx])
            if score <= 0.0:
                continue
            chunk = self.chunks[idx]
            normalized_score = min(1.0, score / max_score)
            hits.append({
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "document_id": chunk.document_id,
                "source_title": chunk.source_title,
                "source_url": chunk.source_url,
                "doc_type": chunk.doc_type,
                "publication_date": chunk.publication_date,
                "attack_ids": chunk.attack_ids,
                "score": float(normalized_score),
                "raw_bm25_score": score
            })

        return hits
