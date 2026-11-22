"""
models/calibration.py
=====================
Confidence Calibration Engine for ThreatRAG.

Implements:
1. Expected Calibration Error (ECE) across M equal-frequency or equal-width bins.
2. Brier Score (Mean Squared Error in probability space).
3. Post-hoc Platt Scaling (Logistic Sigmoid Calibration).
4. Post-hoc Isotonic Regression (Non-parametric Pair-Adjacent Violators).
5. Reliability diagram data generation.
"""

import numpy as np
from typing import Dict, Any, Tuple, List
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

def calculate_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> Dict[str, Any]:
    """
    Computes Expected Calibration Error (ECE), Maximum Calibration Error (MCE),
    and bin-level accuracy/confidence statistics.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_prob = np.asarray(y_prob, dtype=float)
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    mce = 0.0
    bin_data = []

    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (y_prob > bin_lower) & (y_prob <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_prob[in_bin])
            abs_diff = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            ece += abs_diff * prop_in_bin
            mce = max(mce, abs_diff)

            bin_data.append({
                "bin_range": f"{bin_lower:.1f}-{bin_upper:.1f}",
                "confidence": float(avg_confidence_in_bin),
                "accuracy": float(accuracy_in_bin),
                "count": int(np.sum(in_bin)),
                "weight": float(prop_in_bin)
            })
        else:
            bin_data.append({
                "bin_range": f"{bin_lower:.1f}-{bin_upper:.1f}",
                "confidence": float((bin_lower + bin_upper) / 2.0),
                "accuracy": 0.0,
                "count": 0,
                "weight": 0.0
            })

    return {
        "ece": float(ece),
        "mce": float(mce),
        "bin_details": bin_data
    }

def evaluate_calibration_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> Dict[str, Any]:
    """Computes comprehensive calibration and probabilistic quality metrics."""
    ece_stats = calculate_ece(y_true, y_prob, n_bins=10)
    brier = float(brier_score_loss(y_true, y_prob))
    
    return {
        "ece": round(ece_stats["ece"], 4),
        "mce": round(ece_stats["mce"], 4),
        "brier_score": round(brier, 4),
        "mean_confidence": round(float(np.mean(y_prob)), 4),
        "bin_details": ece_stats["bin_details"]
    }

class PostHocCalibrator:
    """Wraps scikit-learn models with Platt Scaling or Isotonic Regression."""
    def __init__(self, base_estimator, method: str = "sigmoid"):
        self.method = method  # 'sigmoid' for Platt, 'isotonic' for Isotonic
        self.calibrated_model = CalibratedClassifierCV(
            estimator=base_estimator,
            method=self.method,
            cv="prefit"
        )

    def fit(self, X_cal: np.ndarray, y_cal: np.ndarray):
        self.calibrated_model.fit(X_cal, y_cal)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.calibrated_model.predict_proba(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.calibrated_model.predict(X)
