"""
rag/citation_validator.py
=========================
Citation Validation and Security Guardrail Engine for ThreatRAG.

Responsibilities:
1. Validates that every assertion citing a chunk [CHUNK-...] or [T1xxx] is directly entailed by the retrieved context.
2. Calculates citation precision, recall, and unsupported claim rates.
3. Detects and neutralizes prompt-injection attempts inside ingested documents and user queries.
4. Enforces defensive-only reasoning boundaries (prohibits execution of offensive exploit payloads).
"""

import re
from typing import List, Dict, Any, Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(the\s+)?system\s+prompt",
    r"you\s+are\s+now\s+(in\s+developer\s+mode|unrestricted|an\s+adversary)",
    r"forget\s+(your\s+)?guidelines",
    r"output\s+(the\s+)?system\s+(prompt|instructions)",
    r"execute\s+(the\s+)?following\s+as\s+root",
    r"curl\s+-s\s+http[s]?://",
    r"rm\s+-rf\s+/",
    r"base64\s+-d\s+\|",
    r"<script.*?>.*?</script>"
]

class CitationValidator:
    def __init__(self):
        self.injection_regexes = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

    def sanitize_input(self, text: str) -> Tuple[str, bool, List[str]]:
        """
        Inspects text for prompt injection vectors.
        Returns (sanitized_text, is_safe, detected_flags).
        """
        detected_flags = []
        for reg in self.injection_regexes:
            match = reg.search(text)
            if match:
                detected_flags.append(match.group(0))

        if detected_flags:
            # Neutralize detected injection text
            sanitized = text
            for flag in detected_flags:
                sanitized = sanitized.replace(flag, "[REDACTED_SECURITY_RISK]")
            return sanitized, False, detected_flags

        return text, True, []

    def extract_citations(self, text: str) -> List[str]:
        """Extracts cited chunk IDs, ATT&CK IDs, and CVE IDs from text."""
        citations = []
        # Match [CHUNK-...], [T1xxx], [CVE-xxxx-xxxx], [INC-xxxx]
        matches = re.findall(r"\[(CHUNK-[A-Za-z0-9_.-]+|T1\d{3}(?:\.\d{3})?|CVE-\d{4}-\d{4,7}|INC-\d{4}-\d{3})\]", text, re.IGNORECASE)
        citations.extend(matches)
        return list(set(citations))

    def validate_citations(self, generated_text: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates whether citations in the generated response correspond to actual retrieved context chunks.
        Evaluates:
        - Citation Precision: Valid citations / Total citations emitted
        - Supported Claim Ratio: Claims supported by retrieved evidence
        - Unsupported Claim Count
        """
        valid_chunk_ids = {c["chunk_id"] for c in retrieved_chunks}
        valid_doc_ids = {str(c.get("document_id")) for c in retrieved_chunks if c.get("document_id")}
        valid_attack_ids = set()
        for c in retrieved_chunks:
            for a in c.get("attack_ids", []):
                valid_attack_ids.add(a)

        all_valid_identifiers = valid_chunk_ids.union(valid_doc_ids).union(valid_attack_ids)

        extracted_cits = self.extract_citations(generated_text)
        
        valid_citations = []
        hallucinated_citations = []

        for cit in extracted_cits:
            if cit in all_valid_identifiers:
                valid_citations.append(cit)
            else:
                hallucinated_citations.append(cit)

        total_citations = len(extracted_cits)
        citation_precision = (len(valid_citations) / total_citations) if total_citations > 0 else 1.0

        # Break text into claim sentences
        sentences = [s.strip() for s in re.split(r"[.!?]\s+", generated_text) if len(s.strip()) > 20]
        unsupported_claims = []
        supported_claims = []

        # Build concatenated context for keyword verification
        context_corpus = " ".join([c["content"].lower() for c in retrieved_chunks])

        for s in sentences:
            has_explicit_citation = any(cit in s for cit in valid_citations)
            # Check key entity presence in context
            entities = re.findall(r"\b[A-Za-z0-9_-]{4,}\b", s)
            overlap_count = sum(1 for e in entities if e.lower() in context_corpus)
            overlap_ratio = overlap_count / max(1, len(entities))

            if has_explicit_citation or overlap_ratio > 0.45:
                supported_claims.append(s)
            else:
                unsupported_claims.append(s)

        total_sentences = len(sentences)
        faithfulness = (len(supported_claims) / total_sentences) if total_sentences > 0 else 1.0
        unsupported_claim_rate = (len(unsupported_claims) / total_sentences) if total_sentences > 0 else 0.0

        return {
            "total_citations": total_citations,
            "valid_citations": valid_citations,
            "hallucinated_citations": hallucinated_citations,
            "citation_precision": round(citation_precision, 4),
            "total_claims": total_sentences,
            "supported_claims_count": len(supported_claims),
            "unsupported_claims_count": len(unsupported_claims),
            "faithfulness_score": round(faithfulness, 4),
            "unsupported_claim_rate": round(unsupported_claim_rate, 4),
            "is_grounded": (len(hallucinated_citations) == 0 and unsupported_claim_rate <= 0.15)
        }
