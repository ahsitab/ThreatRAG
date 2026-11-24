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
6. Full document catalog retrieval for UI and API management.
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
            "documents": {},
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

    def add_document(
        self,
        title: str,
        content: str,
        source_type: str = "advisory",
        source_url: str = "manual://upload",
        att_ck_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingests a new user-supplied cybersecurity document or advisory
        and synchronizes vector and BM25 indices.
        """
        doc_hash = hashlib.md5(content.encode("utf-8")).hexdigest()[:8]
        doc_id = f"DOC-{doc_hash}"

        # Generate chunks
        attack_ids = [att_ck_id.strip()] if att_ck_id and att_ck_id.strip() else []
        chunks = parse_generic_text(content, doc_id=doc_id, title=title, source_url=source_url)
        if not chunks:
            chunks = [
                KnowledgeChunk(
                    chunk_id=f"{doc_id}-chunk-0",
                    document_id=doc_id,
                    source_title=title,
                    source_url=source_url,
                    doc_type=source_type,
                    content=content.strip(),
                    attack_ids=attack_ids,
                    metadata={"chunk_index": 0}
                )
            ]

        for c in chunks:
            if attack_ids and not c.attack_ids:
                c.attack_ids = attack_ids
            c.doc_type = source_type

        # Add to vector store
        self.vector_store.add_chunks(chunks)
        
        # Append to existing chunks in memory and update BM25
        existing = load_preprocessed_chunks()
        updated = existing + chunks
        self.bm25.build_index(updated)
        self.structured.set_chunks(updated)

        # Update metadata catalog
        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = self.vector_store.count()
        if "documents" not in self.status:
            self.status["documents"] = {}
        self.status["documents"][doc_id] = {
            "document_id": doc_id,
            "title": title,
            "source_type": source_type,
            "source_url": source_url,
            "attack_ids": attack_ids,
            "chunks_created": len(chunks),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        self.status["sources"][doc_id] = len(chunks)
        self._save_status()

        return {
            "status": "success",
            "document_id": doc_id,
            "title": title,
            "chunks_created": len(chunks)
        }

    def add_custom_document(self, title: str, content: str, source_url: str = "", doc_type: str = "advisory") -> Dict[str, Any]:
        """Backward-compatible wrapper for add_document."""
        return self.add_document(title=title, content=content, source_type=doc_type, source_url=source_url)

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
        if "documents" not in self.status:
            self.status["documents"] = {}
        self.status["documents"][inc_id] = {
            "document_id": inc_id,
            "title": title,
            "source_type": "historical_incident",
            "source_url": incident_data.get("source_url", ""),
            "attack_ids": attack_ids,
            "chunks_created": 1,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        self._save_status()

        return {"status": "success", "incident_id": inc_id, "chunks_created": 1}

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        Returns a structured catalog of all indexed documents and knowledge assets
        suitable for Streamlit tables and API endpoints.
        """
        docs_map: Dict[str, Dict[str, Any]] = {}

        # 1. Inspect existing preprocessed knowledge chunks
        try:
            chunks = load_preprocessed_chunks()
            for c in chunks:
                doc_id = c.document_id
                if doc_id not in docs_map:
                    docs_map[doc_id] = {
                        "document_id": str(doc_id),
                        "title": str(c.source_title),
                        "category": str(c.doc_type),
                        "chunks": 1,
                        "source_url": str(c.source_url or ""),
                        "attack_ids": ", ".join(c.attack_ids) if c.attack_ids else "N/A"
                    }
                else:
                    docs_map[doc_id]["chunks"] += 1
                    if c.attack_ids:
                        existing_ids = [x.strip() for x in docs_map[doc_id]["attack_ids"].split(",") if x.strip() and x != "N/A"]
                        combined = sorted(list(set(existing_ids + c.attack_ids)))
                        docs_map[doc_id]["attack_ids"] = ", ".join(combined)
        except Exception as e:
            print(f"[INGESTION] Warning: Failed to parse chunks for list_documents: {e}")

        # 2. Merge dynamically ingested documents from status tracking
        dynamic_docs = self.status.get("documents", {})
        for doc_id, meta in dynamic_docs.items():
            if doc_id not in docs_map:
                attack_ids_val = meta.get("attack_ids", [])
                if isinstance(attack_ids_val, list):
                    attack_str = ", ".join(attack_ids_val) if attack_ids_val else "N/A"
                else:
                    attack_str = str(attack_ids_val)

                docs_map[doc_id] = {
                    "document_id": str(doc_id),
                    "title": str(meta.get("title", doc_id)),
                    "category": str(meta.get("source_type", "advisory")),
                    "chunks": int(meta.get("chunks_created", 1)),
                    "source_url": str(meta.get("source_url", "")),
                    "attack_ids": attack_str
                }

        return list(docs_map.values())

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Removes a document and its associated chunks from vector and sparse indices."""
        removed_count = self.vector_store.delete_document(document_id)
        
        # Re-sync BM25 and structured retriever from remaining chunks
        remaining_chunks = [c for c in load_preprocessed_chunks() if c.document_id != document_id]
        self.bm25.build_index(remaining_chunks)
        self.structured.set_chunks(remaining_chunks)

        self.status["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.status["total_chunks"] = self.vector_store.count()
        if document_id in self.status.get("sources", {}):
            del self.status["sources"][document_id]
        if "documents" in self.status and document_id in self.status["documents"]:
            del self.status["documents"][document_id]
        self._save_status()

        return {
            "status": "success",
            "document_id": document_id,
            "chunks_removed": removed_count
        }

    def refresh_index(self) -> Dict[str, Any]:
        """Re-indexes and synchronizes BM25 and ChromaDB vector indices."""
        res = self.initialize_from_preprocessed(force_rebuild=True)
        return {
            "status": "success",
            "total_chunks": self.vector_store.count(),
            "details": res
        }

    def get_status(self) -> Dict[str, Any]:
        """Returns the operational status, document counts, and indexing paths."""
        total_chunks = self.vector_store.count()
        try:
            chunks = load_preprocessed_chunks()
            doc_ids = set(c.document_id for c in chunks)
            if "documents" in self.status:
                doc_ids.update(self.status["documents"].keys())
            total_docs = len(doc_ids)
        except Exception:
            total_docs = len(self.status.get("sources", {}))

        return {
            "status": self.status.get("status", "operational"),
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "vector_dimension": 384,
            "last_updated": self.status.get("last_updated") or datetime.utcnow().isoformat() + "Z",
            "vector_index_path": getattr(self.vector_store, "persist_dir", "artifacts/chroma_db"),
            "bm25_index_path": "artifacts/bm25_index.pkl",
            "sources": self.status.get("sources", {})
        }
