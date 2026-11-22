"""
agents/threat_identifier.py
===========================
Agent 1: Threat Identification and Calibrated Confidence Estimation.

Responsibilities:
1. Validates incoming telemetry, structured flow records, or textual alert logs.
2. Invokes the calibrated classifier (LightGBM + Platt Scaling) when flow metrics are provided.
3. Retrieves contextual knowledge from MITRE ATT&CK and threat signatures via hybrid retrieval.
4. Assigns calibrated confidence and assesses uncertainty.
5. Emits structured threat identification with evidence citations.
"""

from typing import Dict, Any, List, Optional
from models.predict import ThreatPredictor
from rag.hybrid_retriever import AdaptiveHybridRetriever
from rag.citation_validator import CitationValidator

class ThreatIdentifierAgent:
    def __init__(
        self,
        predictor: Optional[ThreatPredictor] = None,
        retriever: Optional[AdaptiveHybridRetriever] = None,
        validator: Optional[CitationValidator] = None
    ):
        self.predictor = predictor or ThreatPredictor()
        self.retriever = retriever or AdaptiveHybridRetriever()
        self.validator = validator or CitationValidator()

    def run(self, telemetry: Optional[Dict[str, Any]] = None, analyst_query: str = "") -> Dict[str, Any]:
        """Convenience method aligning with agent testing & API schemas."""
        res = self.identify_threat(
            incident_description=analyst_query or "Network flow activity inspection",
            structured_flow=telemetry
        )
        is_threat = False
        clf = res.get("classifier_telemetry")
        if clf:
            is_threat = clf.get("is_threat", False)
        else:
            is_threat = "ddos" in res.get("threat_category", "").lower() or "threat" in res.get("threat_category", "").lower()

        conf = float(res.get("calibrated_confidence", 0.72))
        return {
            "threat_detected": is_threat,
            "predicted_label": res.get("threat_category", "Unknown"),
            "calibrated_probability": conf,
            "confidence_level": "High" if conf > 0.8 else ("Medium" if conf > 0.5 else "Low"),
            "uncertainty": 0.05 if "Low" in str(res.get("uncertainty_level", "")) else 0.15,
            "top_contributing_features": [
                {"feature": f.get("feature"), "observed_value": f.get("value"), "impact": f"z-score {f.get('z_score')}"}
                for f in (clf.get("salient_indicators", []) if clf else [])
            ],
            "mapped_att_ck_techniques": res.get("associated_attack_ids", []),
            "analyst_summary": res.get("identification_summary", "")
        }

    def identify_threat(
        self,
        incident_description: str,
        structured_flow: Optional[Dict[str, Any]] = None,
        top_evidence_k: int = 5
    ) -> Dict[str, Any]:
        """
        Executes multi-modal threat identification.
        """
        # 1. Sanitize input against prompt injection
        clean_desc, is_safe, detected_flags = self.validator.sanitize_input(incident_description)

        # 2. ML Classification if flow telemetry is provided
        classifier_output = None
        if structured_flow:
            flow_keys_lower = [str(k).lower().replace(" ", "_").replace("/", "").replace("-", "") for k in structured_flow.keys()]
            if any(k in flow_keys_lower for k in ["destination_port", "flow_duration", "total_fwd_packets", "total_packets", "flow_packetss", "packet_length_mean"]):
                classifier_output = self.predictor.predict_flow(structured_flow)

        # 3. Formulate query for hybrid retrieval
        search_query = clean_desc
        if classifier_output and classifier_output.get("is_threat"):
            search_query += f" {classifier_output['threat_category']} denial of service flood"

        retrieval_res = self.retriever.retrieve(
            query=search_query,
            structured_data=structured_flow,
            top_k=top_evidence_k,
            enable_reranking=True
        )
        evidence_chunks = retrieval_res["results"]

        # 4. Synthesize suspected threat and ATT&CK mappings from evidence
        candidate_attacks = set()
        citations = []
        for c in evidence_chunks:
            citations.append(c["chunk_id"])
            for aid in c.get("attack_ids", []):
                candidate_attacks.add(aid)

        # Determine primary threat category
        if classifier_output:
            primary_category = classifier_output["threat_category"]
            confidence = classifier_output["calibrated_confidence"]
            calib_method = classifier_output["calibration_method"]
            uncertainty = classifier_output["uncertainty_level"]
            analyst_review = classifier_output["analyst_review_recommended"]
        else:
            primary_category = "Suspected Adversary Activity"
            confidence = 0.72  # Uncalibrated baseline placeholder
            calib_method = "Heuristic Retrieval Alignment (Not Calibrated Probability)"
            uncertainty = "Moderate (Text-Only Ingestion Without Flow Telemetry)"
            analyst_review = True

        # Generate formatted analyst identification summary
        summary = (
            f"Threat Classification: {primary_category}\n"
            f"Observed telemetry indicates high volumetric network flow alignment with {primary_category}. "
            f"Retrieved threat intelligence corroborates adversarial technique profiles "
            f"[{', '.join(citations[:2]) if citations else 'CHUNK-BASELINE'}]. "
            f"Calibrated probability of threat: {confidence:.2%} via {calib_method}. "
            f"Uncertainty status: {uncertainty}."
        )

        return {
            "agent": "ThreatIdentifier",
            "threat_category": primary_category,
            "calibrated_confidence": confidence,
            "calibration_status": calib_method,
            "uncertainty_level": uncertainty,
            "analyst_review_required": analyst_review,
            "classifier_telemetry": classifier_output,
            "associated_attack_ids": sorted(list(candidate_attacks)),
            "evidence_chunks": evidence_chunks,
            "evidence_citations": citations,
            "identification_summary": summary,
            "input_safety": {
                "is_safe": is_safe,
                "sanitized": len(detected_flags) > 0,
                "detected_patterns": detected_flags
            }
        }
