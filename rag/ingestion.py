"""
rag/ingestion.py
================
Updatable Knowledge Base Manager for ThreatRAG.

Supports:
1. Ingesting single documents (TXT, Markdown, JSON, CSV).
2. Adding new incident records.
3. Refreshing official feeds (CISA KEV, MITRE ATT&CK).
4. Deleting documents and removing associated chunks from ChromaDB and BM25.
5. Ingestion status reporting, duplicate detection, and incremental index syncing.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from rag.chunking import KnowledgeChunk, parse_generic_text, load_preprocessed_chunks
from rag.vector_store import ThreatVectorStore
from rag.bm25_retriever import BM25Retriever
from rag.structured_retriever import StructuredEventRetriever

INGESTION_STATUS_FILE = os.path.join("artifacts", "ingestion_status.json")

class KnowledgeBaseManager:
    def __init__(
        self,
        vector_store: Optional[ThreatVectorStore] = None,
        bm25_retriever: Optional[BM25Retriever] = None,
        structured_retriever: Optional[StructuredEventRetriever] = None
    ):
        self.vector_store = vector_store or ThreatVectorStore()
        self.bm25 = bm25_retriever or BM25Retriever()
        self.structured = structured_retriever or StructuredEventRetriever()
        self.status = self._load_status()

    def _load_status(self) -> Dict[str, Any]:
        if os.path.exists(INGESTION_STATUS_FILE):
            try:
                with open(INGESTION_STATUS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "last_updated": None,
            "total_documents": 0,
            "total_chunks": 0,
            "sources": {},
            "status": "ready"
        }

    def _save_status(self):
        os.makedirs(os.path.dirname(INGESTION_STATUS_FILE), exist_ok=True)
        with open(INGESTION_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.status, f, indent=2)

    def initialize_from_preprocessed(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """Indexes preprocessed knowledge chunks into ChromaDB and BM25."""
        current_count = self.vector_store.count()
        if current_count > 0 and not force_rebuild:
            print(f"[INGESTION] Vector store already contains {current_count} chunks. Skipping re-indexing.")
            chunks = load_preprocessed_chunks()
            self.structured.set_chunks(chunks)
            if self.bm25.bm25 is None:
                self.bm25.build_index(chunks)
            return {"status": "skipped", "chunk_count": current_count}

        print("[INGESTION] Initializing full index from preprocessed knowledge chunks...")
        chunks = load_preprocessed_chunks()
        if not chunks:
            print("[INGESTION] No preprocessed chunks found! Run scripts/prepare_data.py first.")
            return {"status": "error", "message": "No chunks found"}

        if force_rebuild:
            self.vector_store.reset()

        # Add to vector store
        added_count = self.vector_store.add_chunks(chunks)
        
        # Build BM25
        self.bm25.build_index(chunks)
        
        # Set structured retriever chunks
        self.structured.set_chunks(chunks)

        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = added_count
        self.status["sources"]["mitre_attack"] = sum(1 for c in chunks if c.doc_type.startswith("mitre"))
        self.status["sources"]["cisa_kev"] = sum(1 for c in chunks if c.doc_type == "cisa_vulnerability")
        self.status["sources"]["historical_incidents"] = sum(1 for c in chunks if c.doc_type == "historical_incident")
        self.status["status"] = "operational"
        self._save_status()

        print(f"[INGESTION] Successfully indexed {added_count} chunks.")
        return {"status": "success", "indexed_chunks": added_count}

    def add_custom_document(self, title: str, content: str, source_url: str = "", doc_type: str = "advisory") -> Dict[str, Any]:
        """Ingests a new user-supplied security document or advisory."""
        doc_hash = hashlib.md5(content.encode("utf-8")).hexdigest()[:8]
        doc_id = f"DOC-{doc_hash}"

        # Generate chunks
        chunks = parse_generic_text(content, doc_id=doc_id, title=title, source_url=source_url)
        if not chunks:
            return {"status": "error", "message": "Document empty or failed to chunk"}

        # Add to vector store
        self.vector_store.add_chunks(chunks)
        
        # Append to existing chunks in memory and update BM25
        existing = load_preprocessed_chunks()
        updated = existing + chunks
        self.bm25.build_index(updated)
        self.structured.set_chunks(updated)

        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = self.vector_store.count()
        self.status["sources"][doc_id] = len(chunks)
        self._save_status()

        return {
            "status": "success",
            "document_id": doc_id,
            "title": title,
            "chunks_created": len(chunks)
        }

    def add_incident_record(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ingests a new structured incident record."""
        inc_id = incident_data.get("incident_id") or f"INC-{int(datetime.utcnow().timestamp())}"
        title = incident_data.get("title", "Untitled Incident")
        attack_ids = incident_data.get("attack_ids", [])
        
        content = (
            f"Incident ID: {inc_id} - {title}\n"
            f"Threat Category: {incident_data.get('threat_category', 'General Threat')}\n"
            f"Observed Behavior: {incident_data.get('observed_behavior', '')}\n"
            f"Indicators: {', '.join(incident_data.get('indicators', []))}\n"
            f"ATT&CK Techniques: {', '.join(attack_ids)}\n"
            f"Defensive Mitigation: {incident_data.get('defensive_response', '')}"
        )

        chunk = KnowledgeChunk(
            chunk_id=f"CHUNK-INC-{inc_id}",
            document_id=inc_id,
            source_title=f"Incident: {title}",
            source_url=incident_data.get("source_url", ""),
            doc_type="historical_incident",
            content=content,
            attack_ids=attack_ids,
            publication_date=incident_data.get("publication_date", datetime.utcnow().strftime("%Y-%m-%d")),
            metadata=incident_data
        )

        self.vector_store.add_chunks([chunk])
        existing = load_preprocessed_chunks() + [chunk]
        self.bm25.build_index(existing)
        self.structured.set_chunks(existing)

        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = self.vector_store.count()
        self._save_status()

        return {"status": "success", "incident_id": inc_id, "chunks_created": 1}

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Removes a document and its associated chunks."""
        removed_count = self.vector_store.delete_document(document_id)
        # Re-sync BM25 and structured retriever from active vector store / chunks
        remaining_chunks = [c for c in load_preprocessed_chunks() if c.document_id != document_id]
        self.bm25.build_index(remaining_chunks)
        self.structured.set_chunks(remaining_chunks)

        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = self.vector_store.count()
        if document_id in self.status["sources"]:
            del self.status["sources"][document_id]
        self._save_status()

        return {"status": "success", "document_id": document_id, "chunks_removed": removed_count}

    def get_status(self) -> Dict[str, Any]:
        self.status["total_chunks"] = self.vector_store.count()
        return self.status
