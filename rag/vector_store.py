"""
rag/vector_store.py
===================
Persistent ChromaDB vector index manager for ThreatRAG.
Handles vector indexing, similarity search, metadata filtering, and incremental updates.
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from rag.chunking import KnowledgeChunk
from rag.embeddings import EmbeddingManager

class ThreatVectorStore:
    def __init__(self, persist_dir: str = "artifacts/chroma_db", collection_name: str = "threatrag_knowledge", embedding_manager: Optional[EmbeddingManager] = None):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        os.makedirs(self.persist_dir, exist_ok=True)
        
        self.embedding_manager = embedding_manager or EmbeddingManager()
        
        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def count(self) -> int:
        return self.collection.count()

    def add_chunks(self, chunks: List[KnowledgeChunk], batch_size: int = 64) -> int:
        if not chunks:
            return 0

        total_added = 0
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            ids = [c.chunk_id for c in batch]
            documents = [c.content for c in batch]
            
            # Prepare metadata (ensure values are primitive types for ChromaDB)
            metadatas = []
            for c in batch:
                meta = {
                    "document_id": str(c.document_id),
                    "source_title": str(c.source_title),
                    "source_url": str(c.source_url or ""),
                    "doc_type": str(c.doc_type),
                    "publication_date": str(c.publication_date or ""),
                    "attack_ids": ",".join(c.attack_ids) if c.attack_ids else ""
                }
                metadatas.append(meta)

            # Generate embeddings
            embeddings = self.embedding_manager.encode(documents, batch_size=batch_size)
            
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )
            total_added += len(batch)

        return total_added

    def query(self, query_text: str, top_k: int = 5, where_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.count() == 0:
            return []

        query_emb = self.embedding_manager.encode(query_text)
        
        kwargs = {
            "query_embeddings": query_emb.tolist(),
            "n_results": min(top_k, self.count()),
            "include": ["documents", "metadatas", "distances"]
        }
        if where_filter:
            kwargs["where"] = where_filter

        results = self.collection.query(**kwargs)
        
        hits = []
        if results and "ids" in results and results["ids"]:
            ids = results["ids"][0]
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for chunk_id, doc, meta, dist in zip(ids, docs, metas, dists):
                # Cosine distance to similarity: similarity = 1 - distance
                similarity = max(0.0, 1.0 - float(dist))
                attack_ids = [a.strip() for a in meta.get("attack_ids", "").split(",") if a.strip()]
                hits.append({
                    "chunk_id": chunk_id,
                    "content": doc,
                    "document_id": meta.get("document_id"),
                    "source_title": meta.get("source_title"),
                    "source_url": meta.get("source_url"),
                    "doc_type": meta.get("doc_type"),
                    "publication_date": meta.get("publication_date"),
                    "attack_ids": attack_ids,
                    "score": float(similarity)
                })

        return hits

    def delete_document(self, document_id: str) -> int:
        """Deletes all chunks associated with a document_id."""
        initial_count = self.count()
        self.collection.delete(where={"document_id": document_id})
        return initial_count - self.count()

    def reset(self):
        """Resets the collection."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
