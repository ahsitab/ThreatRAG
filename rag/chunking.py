"""
rag/chunking.py
===============
Metadata-aware chunking and document parsing for cybersecurity intelligence.
Supports: JSON, CSV, TXT, Markdown, STIX JSON, and structured security event logs.
"""

import os
import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class KnowledgeChunk:
    chunk_id: str
    document_id: str
    source_title: str
    source_url: str
    doc_type: str  # 'mitre_technique', 'cisa_vulnerability', 'historical_incident', 'security_log', 'advisory'
    content: str
    attack_ids: List[str] = field(default_factory=list)
    publication_date: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeChunk":
        return cls(**data)

def security_aware_tokenize(text: str) -> List[str]:
    """
    Tokenizes text while preserving cybersecurity entities:
    - CVE identifiers: CVE-2023-34362
    - MITRE ATT&CK IDs: T1059, T1059.001
    - IPv4 addresses and port strings: 192.168.1.1, 8080/TCP
    - Registry keys / file extensions: .exe, .dll, HKLM\\Software
    """
    pattern = r"[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*|\S"
    tokens = re.findall(pattern, text.lower())
    return [t for t in tokens if len(t) > 1 or t.isalnum()]

def parse_generic_text(content: str, doc_id: str, title: str, source_url: str = "", chunk_size: int = 500, overlap: int = 50) -> List[KnowledgeChunk]:
    """Splits plain text or markdown into overlapping chunks preserving sentence boundaries."""
    paragraphs = content.split("\n\n")
    chunks = []
    current_text = ""
    chunk_idx = 0

    # Extract ATT&CK IDs
    attack_ids = list(set(re.findall(r"\bT1\d{3}(?:\.\d{3})?\b", content, re.IGNORECASE)))

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(current_text) + len(p) <= chunk_size:
            current_text += "\n\n" + p if current_text else p
        else:
            if current_text:
                c_id = f"{doc_id}-chunk-{chunk_idx}"
                chunks.append(KnowledgeChunk(
                    chunk_id=c_id,
                    document_id=doc_id,
                    source_title=f"{title} (Part {chunk_idx+1})",
                    source_url=source_url,
                    doc_type="advisory",
                    content=current_text.strip(),
                    attack_ids=attack_ids,
                    metadata={"chunk_index": chunk_idx}
                ))
                chunk_idx += 1
            current_text = p

    if current_text:
        c_id = f"{doc_id}-chunk-{chunk_idx}"
        chunks.append(KnowledgeChunk(
            chunk_id=c_id,
            document_id=doc_id,
            source_title=f"{title} (Part {chunk_idx+1})",
            source_url=source_url,
            doc_type="advisory",
            content=current_text.strip(),
            attack_ids=attack_ids,
            metadata={"chunk_index": chunk_idx}
        ))

    return chunks

def load_preprocessed_chunks(filepath: str = "data/processed/knowledge_chunks/chunks.json") -> List[KnowledgeChunk]:
    """Loads pre-compiled knowledge chunks from disk."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [KnowledgeChunk.from_dict(d) for d in data]
