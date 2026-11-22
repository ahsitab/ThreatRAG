import sys
import os
import time
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends

# Ensure workspace root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.schemas.threat_schemas import (
    AnalyzeRequest,
    FullPipelineResponse,
    IncidentSearchRequest,
    IncidentSearchResponse,
    SimilarIncidentResult,
    ExplainRequest,
    ExplainResponse,
    RecommendRequest,
    RecommendResponse,
    RecommendedAction,
    ThreatIdentificationResponse
)
from agents.orchestrator import ThreatRAGOrchestrator
from agents.threat_identifier import ThreatIdentifierAgent
from agents.incident_search import IncidentSearchAgent
from agents.evidence_explainer import EvidenceExplainerAgent
from agents.response_advisor import ResponseAdvisorAgent
from rag.hybrid_retriever import AdaptiveHybridRetriever

router = APIRouter(prefix="/api", tags=["Threat Analysis"])

# Global orchestrator cache
_orchestrator: Optional[ThreatRAGOrchestrator] = None

def get_orchestrator() -> ThreatRAGOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ThreatRAGOrchestrator()
    return _orchestrator


@router.post("/analyze", response_model=FullPipelineResponse)
async def analyze_full_pipeline(request: AnalyzeRequest):
    """
    Executes the full ThreatRAG multi-agent pipeline:
    1. Threat Identification & Calibrated ML Inference
    2. Historical Incident Retrieval & Difference Analysis
    3. Evidence-Grounded Explanation & ATT&CK Mapping
    4. Defensive Action Recommendation with Human Approval Gate
    5. Citation Audit & Verification
    """
    try:
        orchestrator = get_orchestrator()
        telemetry_dict = None
        if request.telemetry:
            if request.telemetry.raw_features:
                telemetry_dict = request.telemetry.raw_features
            else:
                telemetry_dict = request.telemetry.model_dump(exclude={"raw_features"})

        result = orchestrator.run(
            query=request.query,
            telemetry=telemetry_dict
        )
        return FullPipelineResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")


@router.post("/threats/identify", response_model=ThreatIdentificationResponse)
async def identify_threat(request: AnalyzeRequest):
    """
    Invokes Agent 1 (Threat Identifier) to validate telemetry,
    perform calibrated ML classification, map to MITRE ATT&CK,
    and estimate predictive uncertainty.
    """
    try:
        orchestrator = get_orchestrator()
        telemetry_dict = None
        if request.telemetry:
            if request.telemetry.raw_features:
                telemetry_dict = request.telemetry.raw_features
            else:
                telemetry_dict = request.telemetry.model_dump(exclude={"raw_features"})

        result = orchestrator.threat_identifier.run(
            telemetry=telemetry_dict,
            analyst_query=request.query
        )
        return ThreatIdentificationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Threat identification error: {str(e)}")


@router.post("/incidents/search", response_model=IncidentSearchResponse)
async def search_similar_incidents(request: IncidentSearchRequest):
    """
    Invokes Agent 2 (Incident Search) to find similar historical incidents
    using adaptive hybrid retrieval, scoring similarity, and comparing differences.
    """
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.incident_search.run(
            query=request.query,
            k=request.k
        )
        matches = [SimilarIncidentResult(**item) for item in result.get("historical_matches", [])]
        return IncidentSearchResponse(
            query=result.get("query", request.query),
            historical_matches=matches,
            summary_comparison=result.get("summary_comparison", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Incident search error: {str(e)}")


@router.post("/explain", response_model=ExplainResponse)
async def explain_evidence(request: ExplainRequest):
    """
    Invokes Agent 3 (Evidence Explainer) to construct an evidence-grounded
    explanation separating empirical observations from hypotheses, with
    MITRE ATT&CK technique tags and citation tracking.
    """
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.evidence_explainer.run(
            threat_type=request.threat_type,
            observations=request.observations,
            telemetry=request.telemetry
        )
        return ExplainResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evidence explanation error: {str(e)}")


@router.post("/recommend", response_model=RecommendResponse)
async def recommend_defensive_actions(request: RecommendRequest):
    """
    Invokes Agent 4 (Defensive Response Advisor) to generate prioritized
    containment, mitigation, and recovery actions grounded in CISA KEV
    guidance, enforcing human-in-the-loop authorization.
    """
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.response_advisor.run(
            threat_type=request.threat_type,
            severity=request.severity,
            affected_assets=request.affected_assets
        )
        actions = [RecommendedAction(**item) for item in result.get("actions", [])]
        return RecommendResponse(
            threat_type=result.get("threat_type", request.threat_type),
            severity=result.get("severity", request.severity),
            actions=actions,
            cisa_references=result.get("cisa_references", []),
            operational_impact_summary=result.get("operational_impact_summary", ""),
            human_approval_required=result.get("human_approval_required", True),
            approval_notice=result.get("approval_notice", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Defensive recommendation error: {str(e)}")
