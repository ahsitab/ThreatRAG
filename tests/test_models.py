import pytest
import numpy as np
import os
import sys
from sklearn.metrics import brier_score_loss

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.predict import ThreatPredictor
from models.calibration import calculate_ece, evaluate_calibration_metrics


def test_threat_predictor_loading_and_inference():
    predictor = ThreatPredictor()
    assert predictor.is_ready()

    # Test benign flow features
    benign_flow = {
        "Destination_Port": 443.0,
        "Flow_Duration": 1500000.0,
        "Total_Fwd_Packets": 15.0,
        "Total_Backward_Packets": 20.0,
        "Flow_Bytes_s": 10000.0,
        "Flow_Packets_s": 25.0,
        "Packet_Length_Mean": 450.0
    }
    result_benign = predictor.predict_flow(benign_flow)
    assert "threat_detected" in result_benign
    assert "calibrated_probability" in result_benign
    assert 0.0 <= result_benign["calibrated_probability"] <= 1.0
    assert 0.0 <= result_benign["uncertainty"] <= 1.0

    # Test DDoS flood features (high packet rate, low length)
    ddos_flow = {
        "Destination_Port": 80.0,
        "Flow_Duration": 5000.0,
        "Total_Fwd_Packets": 200.0,
        "Total_Backward_Packets": 2.0,
        "Flow_Bytes_s": 800000.0,
        "Flow_Packets_s": 95000.0,
        "Packet_Length_Mean": 15.0
    }
    result_ddos = predictor.predict_flow(ddos_flow)
    assert result_ddos["threat_detected"] is True
    assert result_ddos["calibrated_probability"] > 0.5
    assert len(result_ddos["top_contributing_features"]) > 0


def test_calibration_metrics_ece_and_brier():
    # Perfectly calibrated synthetic probabilities
    y_true = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])
    
    ece_dict = calculate_ece(y_true, y_prob, n_bins=5)
    brier = float(brier_score_loss(y_true, y_prob))

    assert 0.0 <= ece_dict["ece"] <= 1.0
    assert 0.0 <= brier <= 1.0
    assert ece_dict["ece"] < 0.2
    assert brier < 0.15

    eval_dict = evaluate_calibration_metrics(y_true, y_prob)
    assert "ece" in eval_dict
    assert "brier_score" in eval_dict
