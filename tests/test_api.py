import pytest
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app

client = TestClient(app)


def test_health_endpoints():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ThreatRAG" in data["service"]


def test_knowledge_status_endpoint():
    response = client.get("/api/knowledge/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_chunks" in data
    assert data["total_chunks"] >= 1000
    assert data["vector_dimension"] == 384


def test_evaluation_endpoints():
    resp_ret = client.get("/api/evaluation/retrieval")
    assert resp_ret.status_code == 200
    assert isinstance(resp_ret.json(), list)

    resp_gen = client.get("/api/evaluation/generation")
    assert resp_gen.status_code == 200

    resp_clf = client.get("/api/evaluation/classification")
    assert resp_clf.status_code == 200

    resp_sum = client.get("/api/evaluation/summary")
    assert resp_sum.status_code == 200
    data = resp_sum.json()
    assert "retrieval_benchmark" in data
    assert "ablation_study" in data


def test_api_threat_identify():
    payload = {
        "query": "SYN flood surge on port 80",
        "telemetry": {
            "Destination_Port": 80.0,
            "Flow_Packets_s": 95000.0,
            "Flow_Bytes_s": 850000.0,
            "Packet_Length_Mean": 20.0
        }
    }
    response = client.post("/api/threats/identify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["threat_detected"] is True
    assert data["calibrated_probability"] > 0.5


def test_api_incident_search():
    payload = {
        "query": "Mirai botnet volumetric DNS attack",
        "k": 2
    }
    response = client.post("/api/incidents/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["historical_matches"]) > 0


def test_api_recommend():
    payload = {
        "threat_type": "DDoS",
        "severity": "High",
        "affected_assets": ["Web Server", "Load Balancer"]
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["human_approval_required"] is True
    assert len(data["actions"]) >= 3
