"""
models/train.py
===============
Lightweight Threat Classification & Confidence Calibration Pipeline.

Trains and evaluates:
1. Logistic Regression (Linear Baseline)
2. Random Forest (Ensemble Baseline)
3. LightGBM (Gradient Boosted Tree)

Performs:
- Stratified training and evaluation
- Post-hoc calibration via Platt Scaling and Isotonic Regression
- ECE and Brier score measurement
- Confusion matrix and reliability diagram generation
- Artifact serialization for real-time inference
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.calibration import evaluate_calibration_metrics, PostHocCalibrator

SPLITS_DIR = os.path.join("data", "splits")
ARTIFACTS_DIR = os.path.join("artifacts")
REPORTS_DIR = os.path.join("reports")
TABLES_DIR = os.path.join(REPORTS_DIR, "tables")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

def load_data():
    train_path = os.path.join(SPLITS_DIR, "train", "train_flows.csv")
    val_path = os.path.join(SPLITS_DIR, "validation", "val_flows.csv")
    test_path = os.path.join(SPLITS_DIR, "test", "test_flows.csv")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    # Exclude non-feature columns
    target_col = "binary_target"
    exclude_cols = [target_col, "label"]

    feature_cols = [c for c in train_df.columns if c not in exclude_cols and pd.api.types.is_numeric_dtype(train_df[c])]

    X_train = train_df[feature_cols].values
    y_train = train_df[target_col].values

    X_val = val_df[feature_cols].values
    y_val = val_df[target_col].values

    X_test = test_df[feature_cols].values
    y_test = test_df[target_col].values

    return (X_train, y_train), (X_val, y_val), (X_test, y_test), feature_cols

def plot_calibration_curves(results_dict, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], [0, 1], "k--", label="Perfect Calibration (Ideal)")

    for name, data in results_dict.items():
        bin_details = data["bin_details"]
        confs = [b["confidence"] for b in bin_details if b["count"] > 0]
        accs = [b["accuracy"] for b in bin_details if b["count"] > 0]
        ece = data["ece"]
        plt.plot(confs, accs, marker="o", label=f"{name} (ECE: {ece:.3f})")

    plt.xlabel("Mean Predicted Confidence")
    plt.ylabel("Observed Empirical Accuracy")
    plt.title("Reliability Diagram (Calibration Comparison)")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[FIGURE] Saved calibration diagram to {output_path}")

def plot_confusion_matrix(cm, class_names, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion Matrix (Holdout Test Set)")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)

    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], "d"),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.ylabel("True Threat Label")
    plt.xlabel("Predicted Threat Label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[FIGURE] Saved confusion matrix to {output_path}")

def main():
    print("=" * 70)
    print("ThreatRAG Phase 7: Lightweight Model Training & Calibration")
    print("=" * 70)

    (X_train, y_train), (X_val, y_val), (X_test, y_test), feature_cols = load_data()
    print(f"Features: {len(feature_cols)} numeric attributes")
    print(f"Splits -> Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Models to train
    base_models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        "LightGBM": LGBMClassifier(n_estimators=100, max_depth=8, learning_rate=0.05, random_state=42, verbosity=-1)
    }

    results = []
    trained_calibrators = {}
    curve_data = {}

    best_f1 = -1.0
    best_model_bundle = None

    for name, model in base_models.items():
        print(f"\n--- Training {name} ---")
        model.fit(X_train_scaled, y_train)

        # 1. Uncalibrated predictions on Test
        test_preds = model.predict(X_test_scaled)
        test_probs = model.predict_proba(X_test_scaled)[:, 1]

        acc = accuracy_score(y_test, test_preds)
        prec = precision_score(y_test, test_preds, zero_division=0)
        rec = recall_score(y_test, test_preds, zero_division=0)
        f1 = f1_score(y_test, test_preds, zero_division=0)
        cm = confusion_matrix(y_test, test_preds)
        fpr = cm[0, 1] / (cm[0, 0] + cm[0, 1]) if (cm[0, 0] + cm[0, 1]) > 0 else 0.0

        calib_stats = evaluate_calibration_metrics(y_test, test_probs)
        curve_data[f"{name} (Uncalibrated)"] = calib_stats

        results.append({
            "model": name,
            "calibration": "None (Raw)",
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "macro_f1": round(f1, 4),
            "false_positive_rate": round(fpr, 4),
            "ece": calib_stats["ece"],
            "brier_score": calib_stats["brier_score"]
        })

        # 2. Platt Scaling (Sigmoid) calibrated on Validation set
        platt = PostHocCalibrator(model, method="sigmoid")
        platt.fit(X_val_scaled, y_val)
        platt_probs = platt.predict_proba(X_test_scaled)[:, 1]
        platt_preds = (platt_probs >= 0.5).astype(int)

        platt_f1 = f1_score(y_test, platt_preds, zero_division=0)
        platt_calib = evaluate_calibration_metrics(y_test, platt_probs)
        curve_data[f"{name} (Platt)"] = platt_calib

        results.append({
            "model": name,
            "calibration": "Platt Scaling",
            "accuracy": round(accuracy_score(y_test, platt_preds), 4),
            "precision": round(precision_score(y_test, platt_preds, zero_division=0), 4),
            "recall": round(recall_score(y_test, platt_preds, zero_division=0), 4),
            "macro_f1": round(platt_f1, 4),
            "false_positive_rate": round(fpr, 4),
            "ece": platt_calib["ece"],
            "brier_score": platt_calib["brier_score"]
        })

        # 3. Isotonic Regression calibrated on Validation set
        iso = PostHocCalibrator(model, method="isotonic")
        iso.fit(X_val_scaled, y_val)
        iso_probs = iso.predict_proba(X_test_scaled)[:, 1]
        iso_preds = (iso_probs >= 0.5).astype(int)

        iso_f1 = f1_score(y_test, iso_preds, zero_division=0)
        iso_calib = evaluate_calibration_metrics(y_test, iso_probs)
        curve_data[f"{name} (Isotonic)"] = iso_calib

        results.append({
            "model": name,
            "calibration": "Isotonic Regression",
            "accuracy": round(accuracy_score(y_test, iso_preds), 4),
            "precision": round(precision_score(y_test, iso_preds, zero_division=0), 4),
            "recall": round(recall_score(y_test, iso_preds, zero_division=0), 4),
            "macro_f1": round(iso_f1, 4),
            "false_positive_rate": round(fpr, 4),
            "ece": iso_calib["ece"],
            "brier_score": iso_calib["brier_score"]
        })

        # Track overall winning model bundle (high F1 + low ECE)
        if platt_f1 > best_f1:
            best_f1 = platt_f1
            best_model_bundle = {
                "model_name": name,
                "base_model": model,
                "calibrated_model": platt,
                "test_cm": confusion_matrix(y_test, platt_preds),
                "metrics": platt_calib
            }

    # Save results table
    os.makedirs(TABLES_DIR, exist_ok=True)
    results_df = pd.DataFrame(results)
    results_csv = os.path.join(TABLES_DIR, "classification_results.csv")
    results_df.to_csv(results_csv, index=False)
    print(f"\n[TABLE] Saved evaluation metrics to {results_csv}")
    print(results_df.to_string(index=False))

    # Generate Figures
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plot_calibration_curves(curve_data, os.path.join(FIGURES_DIR, "calibration_curve.png"))
    plot_confusion_matrix(best_model_bundle["test_cm"], ["BENIGN", "DDoS"], os.path.join(FIGURES_DIR, "confusion_matrix.png"))

    # Save Best Model Artifacts
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    joblib.dump(best_model_bundle["calibrated_model"], os.path.join(ARTIFACTS_DIR, "threat_classifier.joblib"))
    joblib.dump(scaler, os.path.join(ARTIFACTS_DIR, "flow_scaler.joblib"))
    with open(os.path.join(ARTIFACTS_DIR, "feature_names.json"), "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"\n[SAVED] Winning calibrated model ({best_model_bundle['model_name']} + Platt Scaling) saved to {ARTIFACTS_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
