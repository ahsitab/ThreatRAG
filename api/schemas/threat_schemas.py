from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TelemetryInput(BaseModel):
    Destination_Port: Optional[float] = Field(default=80.0, description="Destination port number")
    Flow_Duration: Optional[float] = Field(default=1000.0, description="Flow duration in microseconds")
    Total_Fwd_Packets: Optional[float] = Field(default=10.0, description="Total forward packets")
    Total_Backward_Packets: Optional[float] = Field(default=5.0, description="Total backward packets")
    Flow_Bytes_s: Optional[float] = Field(default=50000.0, description="Flow bytes per second")
    Flow_Packets_s: Optional[float] = Field(default=100.0, description="Flow packets per second")
    Packet_Length_Mean: Optional[float] = Field(default=500.0, description="Mean packet length")
    raw_features: Optional[Dict[str, float]] = Field(default=None, description="Full dictionary of flow features")


class AnalyzeRequest(BaseModel):
    query: str = Field(..., description="Analyst query or description of observed security event")
    telemetry: Optional[TelemetryInput] = Field(default=None, description="Optional network flow telemetry features")
    k: int = Field(default=5, description="Number of candidate chunks to retrieve")
    top_k_rerank: int = Field(default=3, description="Number of top chunks after cross-encoder reranking")


class ThreatIdentificationResponse(BaseModel):
    threat_detected: bool
    predicted_label: str
    calibrated_probability: float
    confidence_level: str
    uncertainty: float
    top_contributing_features: List[Dict[str, Any]]
    mapped_att_ck_techniques: List[str]
    analyst_summary: str


class IncidentSearchRequest(BaseModel):
    query: str = Field(..., description="Query or incident description to match against historical repository")
    k: int = Field(default=3, description="Number of historical incidents to retrieve")


class SimilarIncidentResult(BaseModel):
    incident_id: str
    title: str
    similarity_score: float
    threat_category: str
    att_ck_mappings: List[str]
    observed_behavior: str
    shared_characteristics: List[str]
    differences: List[str]
    defensive_response: str
    source_url: str


class IncidentSearchResponse(BaseModel):
    query: str
    historical_matches: List[SimilarIncidentResult]
    summary_comparison: str


class ExplainRequest(BaseModel):
    threat_type: str = Field(..., description="Identified threat or anomaly type")
    observations: List[str] = Field(default_factory=list, description="Empirical observations and telemetry signals")
    telemetry: Optional[Dict[str, Any]] = Field(default=None, description="Structured telemetry dictionary")


class ExplainResponse(BaseModel):
    threat_type: str
    explanation: str
    grounded_att_ck_techniques: List[str]
    empirical_evidence: List[str]
    hypotheses: List[str]
    citations: List[Dict[str, Any]]
    citation_audit: Dict[str, Any]


class RecommendRequest(BaseModel):
    threat_type: str = Field(..., description="Identified threat or attack type")
    severity: str = Field(default="High", description="Threat severity level (Critical, High, Medium, Low)")
    affected_assets: List[str] = Field(default_factory=lambda: ["Web Server", "Database"], description="Affected asset identifiers")


class RecommendedAction(BaseModel):
    step: int
    phase: str
    action: str
    rationale: str
    cisa_guidance: Optional[str]
    operational_risk: str


class RecommendResponse(BaseModel):
    threat_type: str
    severity: str
    actions: List[RecommendedAction]
    cisa_references: List[str]
    operational_impact_summary: str
    human_approval_required: bool
    approval_notice: str


class FullPipelineResponse(BaseModel):
    status: str
    query: str
    threat_identification: Optional[Dict[str, Any]]
    incident_search: Optional[Dict[str, Any]]
    evidence_explanation: Optional[Dict[str, Any]]
    defensive_recommendations: Optional[Dict[str, Any]]
    retrieved_chunks: List[Dict[str, Any]]
    citation_audit: Dict[str, Any]
    execution_metrics: Dict[str, Any]


class DocumentUploadRequest(BaseModel):
    title: str = Field(..., description="Title of the cybersecurity document or advisory")
    content: str = Field(..., description="Raw text or markdown content of the document")
    source_type: str = Field(default="advisory", description="Document type: advisory, incident, report, technique")
    source_url: Optional[str] = Field(default="manual://upload", description="Source URL or reference")
    att_ck_id: Optional[str] = Field(default=None, description="Optional associated ATT&CK ID")


class DocumentUploadResponse(BaseModel):
    status: str
    document_id: str
    title: str
    chunks_created: int
    message: str


class KnowledgeStatusResponse(BaseModel):
    status: str
    total_documents: int
    total_chunks: int
    vector_dimension: int
    last_updated: str
    vector_index_path: str
    bm25_index_path: str
