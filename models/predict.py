"""
models/predict.py
=================
Inference module for lightweight threat classification and calibrated confidence.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional

ARTIFACTS_DIR = "artifacts"

class ThreatPredictor:
    def __init__(self, artifacts_dir: str = ARTIFACTS_DIR):
        self.artifacts_dir = artifacts_dir
        self.model = None
        self.scaler = None
        self.feature_names = []
        self._load_artifacts()

    def _load_artifacts(self):
        model_path = os.path.join(self.artifacts_dir, "threat_classifier.joblib")
        scaler_path = os.path.join(self.artifacts_dir, "flow_scaler.joblib")
        features_path = os.path.join(self.artifacts_dir, "feature_names.json")

        if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(features_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                with open(features_path, "r", encoding="utf-8") as f:
                    self.feature_names = json.load(f)
                print(f"[PREDICTOR] Loaded calibrated model and scaler with {len(self.feature_names)} features.")
            except Exception as e:
                print(f"[PREDICTOR] Error loading model artifacts: {e}")
                self.model = None

    def is_ready(self) -> bool:
        return self.model is not None and self.scaler is not None

    def predict_flow(self, flow_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw or structured flow features, scales them, and computes calibrated threat prediction.
        """
        if not self.is_ready():
            return {
                "error": "Classifier model artifacts not loaded. Run models/train.py first.",
                "is_threat": False,
                "confidence": 0.5,
                "uncertainty": "High (Model Unloaded)"
            }

        # Build feature vector matching feature_names
        vec = []
        feature_contributions = []

        # Normalize input flow features to lowercase alphanumeric for robust lookup
        clean_input = {}
        for k, v in flow_features.items():
            norm_k = k.lower().replace(" ", "_").replace("/", "").replace("-", "")
            clean_input[norm_k] = v
            clean_input[k.lower()] = v

        for fname in self.feature_names:
            norm_fname = fname.lower().replace(" ", "_").replace("/", "").replace("-", "")
            val = clean_input.get(fname, clean_input.get(norm_fname, clean_input.get(fname.lower(), 0.0)))
            try:
                val_float = float(val) if val is not None else 0.0
            except (ValueError, TypeError):
                val_float = 0.0
            vec.append(val_float)

        X = np.array([vec], dtype=np.float32)
        X_scaled = self.scaler.transform(X)

        # Calibrated probability
        probs = self.model.predict_proba(X_scaled)[0]
        p_threat = float(probs[1]) if len(probs) > 1 else float(probs[0])
        pred_label = int(p_threat >= 0.5)

        # Class name
        threat_name = "DDoS / Denial of Service" if pred_label == 1 else "Benign Network Flow"

        # Uncertainty estimation
        distance_from_boundary = abs(p_threat - 0.5)
        if distance_from_boundary >= 0.35:
            uncertainty = "Low (Highly Decisive)"
            review_recommended = False
        elif distance_from_boundary >= 0.15:
            uncertainty = "Moderate (Acceptable Confidence)"
            review_recommended = False
        else:
            uncertainty = "High (Near Decision Boundary - Analyst Triage Mandatory)"
            review_recommended = True

        # Extract top anomalous or influential features
        for fname, raw_v, s_v in zip(self.feature_names, vec, X_scaled[0]):
            if abs(s_v) > 1.5:  # more than 1.5 standard deviations from training mean
                feature_contributions.append({
                    "feature": fname,
                    "value": raw_v,
                    "z_score": round(float(s_v), 2)
                })
        
        feature_contributions.sort(key=lambda x: abs(x["z_score"]), reverse=True)

        return {
            "threat_category": threat_name,
            "is_threat": bool(pred_label == 1),
            "calibrated_confidence": round(p_threat if pred_label == 1 else (1.0 - p_threat), 4),
            "threat_probability": round(p_threat, 4),
            "calibration_method": "Platt Scaling (Logistic Sigmoid)",
            "uncertainty_level": uncertainty,
            "analyst_review_recommended": review_recommended,
            "salient_indicators": feature_contributions[:6]
        }
