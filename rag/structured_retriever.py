"""
rag/structured_retriever.py
===========================
Structured Security Event Matcher for ThreatRAG.
Matches incident telemetry (network flow metrics, protocol, destination port,
alert categories, and ATT&CK IDs) against documented threat baselines and historical incident patterns.
Avoids arbitrary IP address equality by focusing on behavioral and structural signatures.
"""

import os
import math
from typing import List, Dict, Any, Optional
from rag.chunking import KnowledgeChunk

class StructuredEventRetriever:
    def __init__(self, chunks: Optional[List[KnowledgeChunk]] = None):
        self.chunks: List[KnowledgeChunk] = chunks or []

    def set_chunks(self, chunks: List[KnowledgeChunk]):
        self.chunks = chunks

    def compute_similarity(self, event_features: Dict[str, Any], chunk: KnowledgeChunk) -> float:
        score = 0.0
        total_weight = 0.0

        content_lower = chunk.content.lower()

        # 1. Destination Port / Service Matching (Weight: 2.0)
        dst_port = event_features.get("destination_port") or event_features.get("dst_port")
        if dst_port is not None:
            total_weight += 2.0
            port_str = str(dst_port)
            if f"port {port_str}" in content_lower or f":{port_str}" in content_lower:
                score += 2.0
            elif int(dst_port) in [80, 443, 8080] and ("web" in content_lower or "http" in content_lower):
                score += 1.5
            elif int(dst_port) in [445, 139] and ("smb" in content_lower or "eternalblue" in content_lower):
                score += 2.0
            elif int(dst_port) in [389, 636, 1389] and ("ldap" in content_lower or "jndi" in content_lower or "log4j" in content_lower):
                score += 2.0

        # 2. Protocol Matching (Weight: 1.0)
        protocol = event_features.get("protocol") or event_features.get("proto")
        if protocol:
            total_weight += 1.0
            proto_str = str(protocol).lower()
            if proto_str in content_lower:
                score += 1.0

        # 3. Flow Volumetric Characteristics (Duration, Packet Count) (Weight: 2.0)
        flow_duration = event_features.get("flow_duration")
        total_packets = event_features.get("total_fwd_packets") or event_features.get("total_packets")
        
        if total_packets is not None:
            total_weight += 2.0
            packets = float(total_packets)
            # High-packet volume characteristic of DoS/DDoS or scan
            if packets > 50:
                if "dos" in content_lower or "ddos" in content_lower or "flood" in content_lower or "amplification" in content_lower:
                    score += 2.0
            elif packets <= 3:
                if "scan" in content_lower or "probe" in content_lower or "reconnaissance" in content_lower:
                    score += 1.5

        # 4. ATT&CK ID overlap (Weight: 3.0)
        target_attack_ids = event_features.get("attack_ids", [])
        if target_attack_ids:
            total_weight += 3.0
            overlap = set(target_attack_ids).intersection(set(chunk.attack_ids))
            if overlap:
                score += 3.0 * (len(overlap) / len(target_attack_ids))

        # 5. Alert Category / Threat Label (Weight: 2.0)
        alert_category = event_features.get("alert_category") or event_features.get("threat_category") or event_features.get("label")
        if alert_category:
            total_weight += 2.0
            cat_lower = str(alert_category).lower()
            if cat_lower in content_lower or (cat_lower == "ddos" and "denial of service" in content_lower):
                score += 2.0

        if total_weight == 0.0:
            return 0.0
        return min(1.0, score / total_weight)

    def query(self, event_features: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.chunks or not event_features:
            return []

        scored_chunks = []
        for c in self.chunks:
            sim = self.compute_similarity(event_features, c)
            if sim > 0.15:
                scored_chunks.append({
                    "chunk_id": c.chunk_id,
                    "content": c.content,
                    "document_id": c.document_id,
                    "source_title": c.source_title,
                    "source_url": c.source_url,
                    "doc_type": c.doc_type,
                    "publication_date": c.publication_date,
                    "attack_ids": c.attack_ids,
                    "score": float(sim),
                    "match_type": "structured_telemetry"
                })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]
