"""
evaluation/evaluate_retrieval.py
================================
Retrieval Benchmark for ThreatRAG.

Evaluates configurations:
- E2: Dense Only
- E3: Dense + BM25 Hybrid (Fixed weights)
- E4: Hybrid + Cross-Encoder Reranking
- E5: Adaptive Hybrid RAG (Proposed tri-modal with query routing)

Calculates:
- Recall@1
- Recall@5
- Precision@5
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (nDCG@5)
"""

import os
import sys
import math
import numpy as np
import pandas as pd
from typing import List, Dict, Any

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rag.hybrid_retriever import AdaptiveHybridRetriever

# Standard Ground-Truth Evaluation Benchmark Queries
BENCHMARK_QUERIES = [
    {
        "query": "PowerShell command execution adversary technique T1059.001",
        "ground_truth_ids": ["CHUNK-ATTACK-T1059.001", "T1059.001", "T1059"],
        "telemetry": None
    },
    {
        "query": "Remote code execution in Apache Log4j JNDI lookup CVE-2021-44228",
        "ground_truth_ids": ["CHUNK-INC-INC-2021-003", "CHUNK-CISA-CVE-2021-44228", "CVE-2021-44228"],
        "telemetry": {"destination_port": 389, "protocol": "TCP"}
    },
    {
        "query": "Supply chain compromise trojanized Orion DLL Cozy Bear SolarWinds",
        "ground_truth_ids": ["CHUNK-INC-INC-2020-001", "CHUNK-ATTACK-T1195.002", "T1195.002"],
        "telemetry": {"destination_port": 443}
    },
    {
        "query": "Colonial pipeline ransomware extortion external remote services DarkSide",
        "ground_truth_ids": ["CHUNK-INC-INC-2021-002", "CHUNK-ATTACK-T1133", "T1133"],
        "telemetry": {"destination_port": 443}
    },
    {
        "query": "EternalBlue SMBv1 exploitation WannaCry self propagating worm",
        "ground_truth_ids": ["CHUNK-INC-INC-2017-005", "CHUNK-ATTACK-T1210", "T1210"],
        "telemetry": {"destination_port": 445, "protocol": "TCP"}
    },
    {
        "query": "MOVEit Transfer pre-auth SQL injection human2.aspx web shell CL0P",
        "ground_truth_ids": ["CHUNK-INC-INC-2023-004", "CHUNK-CISA-CVE-2023-34362", "CHUNK-ATTACK-T1505.003"],
        "telemetry": {"destination_port": 443}
    },
    {
        "query": "High packet volume UDP/TCP SYN flood denial of service traffic",
        "ground_truth_ids": ["CHUNK-ATTACK-T1498", "CHUNK-ATTACK-T1499", "CHUNK-INC-INC-2017-005"],
        "telemetry": {"destination_port": 80, "flow_duration": 1500000, "total_fwd_packets": 250}
    },
    {
        "query": "OS credential dumping from LSASS memory Mimikatz T1003.001",
        "ground_truth_ids": ["CHUNK-ATTACK-T1003.001", "T1003.001", "CHUNK-INC-INC-2017-006"],
        "telemetry": None
    },
    {
        "query": "NotPetya disk wipe destructive malware M.E.Doc supply chain",
        "ground_truth_ids": ["CHUNK-INC-INC-2017-006", "CHUNK-ATTACK-T1561.002", "T1561.002"],
        "telemetry": {"destination_port": 445}
    },
    {
        "query": "Exploit Public-Facing Application initial access vulnerability T1190",
        "ground_truth_ids": ["CHUNK-ATTACK-T1190", "T1190"],
        "telemetry": {"destination_port": 80}
    }
]

def calculate_ndcg(retrieved_ids: List[str], ground_truth: List[str], k: int = 5) -> float:
    dcg = 0.0
    for i, cid in enumerate(retrieved_ids[:k]):
        rel = 1.0 if any(gt in cid for gt in ground_truth) else 0.0
        dcg += rel / math.log2(i + 2)

    # Ideal DCG
    ideal_hits = min(len(ground_truth), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    return (dcg / idcg) if idcg > 0 else 0.0

def evaluate_retrieval_suite() -> pd.DataFrame:
    print("=" * 70)
    print("Evaluating Retrieval Configurations across Benchmark Suite")
    print("=" * 70)

    retriever = AdaptiveHybridRetriever()

    configs = {
        "E2: Dense Only": {"strategy_override": "dense_only", "enable_rerank": False},
        "E3: Dense + BM25 Hybrid": {"strategy_override": "no_rerank", "enable_rerank": False},
        "E4: Hybrid + Cross-Encoder": {"strategy_override": None, "enable_rerank": True},
        "E5: Proposed Adaptive Hybrid": {"strategy_override": None, "enable_rerank": True}
    }

    metrics_rows = []

    for cfg_name, cfg_params in configs.items():
        recalls_1 = []
        recalls_5 = []
        precisions_5 = []
        mrrs = []
        ndcgs_5 = []

        for item in BENCHMARK_QUERIES:
            q = item["query"]
            gt = item["ground_truth_ids"]
            tel = item["telemetry"] if "Adaptive" in cfg_name else None

            res = retriever.retrieve(
                query=q,
                structured_data=tel,
                top_k=5,
                enable_reranking=cfg_params["enable_rerank"],
                strategy_override=cfg_params["strategy_override"]
            )
            hit_ids = [c["chunk_id"] for c in res["results"]]

            # Check matches
            matches_at_1 = 1 if hit_ids and any(g in hit_ids[0] for g in gt) else 0
            matches_at_5 = [1 if any(g in hid for g in gt) else 0 for hid in hit_ids[:5]]

            r1 = matches_at_1
            r5 = 1.0 if sum(matches_at_5) > 0 else 0.0
            p5 = sum(matches_at_5) / 5.0

            # MRR
            first_rank = 0
            for idx, m in enumerate(matches_at_5, 1):
                if m == 1:
                    first_rank = idx
                    break
            mrr = (1.0 / first_rank) if first_rank > 0 else 0.0
            ndcg5 = calculate_ndcg(hit_ids, gt, k=5)

            recalls_1.append(r1)
            recalls_5.append(r5)
            precisions_5.append(p5)
            mrrs.append(mrr)
            ndcgs_5.append(ndcg5)

        metrics_rows.append({
            "configuration": cfg_name,
            "recall@1": round(float(np.mean(recalls_1)), 4),
            "recall@5": round(float(np.mean(recalls_5)), 4),
            "precision@5": round(float(np.mean(precisions_5)), 4),
            "mrr": round(float(np.mean(mrrs)), 4),
            "ndcg@5": round(float(np.mean(ndcgs_5)), 4)
        })

    df = pd.DataFrame(metrics_rows)
    os.makedirs(os.path.join("reports", "tables"), exist_ok=True)
    out_path = os.path.join("reports", "tables", "retrieval_benchmark.csv")
    df.to_csv(out_path, index=False)
    print(df.to_string(index=False))
    print(f"\n[SAVED] Benchmark metrics written to {out_path}")
    print("=" * 70)
    return df

if __name__ == "__main__":
    evaluate_retrieval_suite()
