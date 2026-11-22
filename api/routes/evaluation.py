import sys
import os
import pandas as pd
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation & Benchmarks"])

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../reports"))
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")


def _read_table(filename: str) -> List[Dict[str, Any]]:
    filepath = os.path.join(TABLES_DIR, filename)
    if not os.path.exists(filepath):
        return []
    df = pd.read_csv(filepath)
    return df.to_dict(orient="records")


@router.get("/retrieval")
async def get_retrieval_benchmark():
    """Returns empirical retrieval performance metrics across baselines E2-E5."""
    try:
        return _read_table("retrieval_benchmark.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generation")
async def get_generation_evaluation():
    """Returns generation quality, faithfulness, and citation metrics for E1-E5."""
    try:
        return _read_table("generation_evaluation.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents")
async def get_agent_performance():
    """Returns agent completion, latency, cost, and safety metrics."""
    try:
        return _read_table("agent_performance.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classification")
async def get_classification_results():
    """Returns ML classification performance and calibration metrics (ECE, Brier)."""
    try:
        return _read_table("classification_results.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ablation")
async def get_ablation_study():
    """Returns component ablation study results demonstrating individual contributions."""
    try:
        return _read_table("ablation_study.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_evaluation_summary():
    """Returns a unified summary of all experimental benchmarks."""
    return {
        "retrieval_benchmark": _read_table("retrieval_benchmark.csv"),
        "generation_evaluation": _read_table("generation_evaluation.csv"),
        "agent_performance": _read_table("agent_performance.csv"),
        "classification_results": _read_table("classification_results.csv"),
        "ablation_study": _read_table("ablation_study.csv")
    }
