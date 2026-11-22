import sys
import os
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.schemas.threat_schemas import (
    DocumentUploadRequest,
    DocumentUploadResponse,
    KnowledgeStatusResponse
)
from rag.ingestion import KnowledgeBaseManager

router = APIRouter(prefix="/api", tags=["Knowledge Base Management"])

_kb_manager: Optional[KnowledgeBaseManager] = None

def get_kb_manager() -> KnowledgeBaseManager:
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KnowledgeBaseManager()
    return _kb_manager


@router.get("/knowledge/status", response_model=KnowledgeStatusResponse)
async def get_knowledge_status():
    """Returns current vector store, BM25 index, and document statistics."""
    try:
        kb = get_kb_manager()
        status = kb.get_status()
        return KnowledgeStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve knowledge status: {str(e)}")


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(request: DocumentUploadRequest):
    """
    Ingests a new cybersecurity document or advisory into the active
    ChromaDB and BM25 index incrementally without rebuilding from scratch.
    """
    try:
        kb = get_kb_manager()
        result = kb.add_document(
            title=request.title,
            content=request.content,
            source_type=request.source_type,
            source_url=request.source_url or "manual://upload",
            att_ck_id=request.att_ck_id
        )
        return DocumentUploadResponse(
            status="success",
            document_id=result.get("document_id", "doc_unknown"),
            title=request.title,
            chunks_created=result.get("chunks_created", 0),
            message="Document successfully processed and indexed."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")


@router.post("/documents/upload-file", response_model=DocumentUploadResponse)
async def upload_document_file(
    file: UploadFile = File(...),
    source_type: str = Form("advisory"),
    att_ck_id: Optional[str] = Form(None)
):
    """Ingests a file (TXT, MD, JSON, CSV) directly into the knowledge base."""
    try:
        content_bytes = await file.read()
        try:
            content_text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content_text = content_bytes.decode("latin-1")

        kb = get_kb_manager()
        result = kb.add_document(
            title=file.filename or "Uploaded Document",
            content=content_text,
            source_type=source_type,
            source_url=f"file://{file.filename}",
            att_ck_id=att_ck_id
        )
        return DocumentUploadResponse(
            status="success",
            document_id=result.get("document_id", "doc_unknown"),
            title=file.filename or "Uploaded File",
            chunks_created=result.get("chunks_created", 0),
            message=f"File {file.filename} parsed and indexed into knowledge base."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File ingestion failed: {str(e)}")


@router.get("/documents", response_model=List[Dict[str, Any]])
async def list_documents():
    """Lists all tracked documents in the knowledge base catalog."""
    try:
        kb = get_kb_manager()
        return kb.list_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Removes a document and its associated chunks from vector and sparse indices."""
    try:
        kb = get_kb_manager()
        deleted = kb.delete_document(document_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Document ID {document_id} not found.")
        return {"status": "success", "message": f"Document {document_id} deleted successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")


@router.post("/knowledge/refresh")
async def refresh_knowledge_base():
    """Refreshes and synchronizes BM25 and vector indices with all processed chunks."""
    try:
        kb = get_kb_manager()
        result = kb.refresh_index()
        return {"status": "success", "refreshed_chunks": result.get("total_chunks", 0)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Index refresh failed: {str(e)}")
