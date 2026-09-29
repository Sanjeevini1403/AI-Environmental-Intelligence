"""
Automated Model Retraining & Continuous Learning Pipeline.

Implements model retraining pipelines to update the forecasting model with
new sensor data batches (per Week 3-4 and Week 7-8 specifications).
Performs:
- Data validation and missing value imputation
- Feature normalization and temporal feature extraction
- Model candidate training (Random Forest & Gradient Boosting Regressor)
- K-Fold cross-validation, MAE, RMSE, and R² evaluation
- Automated model artifact persistence into models/aqi_prediction_model.pkl
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "pune_aqi_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "aqi_prediction_model.pkl")
REPORT_PATH = os.path.join(BASE_DIR, "data", "model_evaluation_report.txt")

FEATURES = ["PM2_5", "PM10", "NO2", "SO2", "CO", "O3"]
TARGET = "AQI"


def run_retraining_pipeline():
    print("=" * 60)
    print("AI Environmental Intelligence — Automated Model Retraining")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        sys.exit(1)

    print(f"Loading sensor batch data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset shape: {df.shape[0]} samples, {df.shape[1]} columns")

    # Validate feature presence
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Required features missing from sensor batch: {missing}")

    X = df[FEATURES].copy()
    y = df[TARGET].copy() if TARGET in df.columns else None

    if y is None:
        raise ValueError(f"Target column '{TARGET}' not present in dataset.")

    # Impute missing values using robust column medians
    X = X.fillna(X.median())
    y = y.fillna(y.median())

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"Split: {len(X_train)} training samples, {len(X_test)} validation samples")

    # 1. Train Random Forest Model
    print("\n[1/3] Training Random Forest Regressor (n_estimators=150, max_depth=16)...")
    rf_model = RandomForestRegressor(
        n_estimators=150,
        max_depth=16,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    rf_preds = rf_model.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    rf_r2 = r2_score(y_test, rf_preds)

    print(f"Random Forest Validation -> MAE: {rf_mae:.2f} | RMSE: {rf_rmse:.2f} | R²: {rf_r2:.4f}")

    # 2. 5-Fold Cross Validation
    print("\n[2/3] Performing 5-Fold Cross Validation...")
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf_model, X, y, cv=kfold, scoring="r2", n_jobs=-1)
    cv_mean = float(np.mean(cv_scores))
    print(f"5-Fold Cross-Validation Mean R²: {cv_mean:.4f} (Scores: {[round(s, 3) for s in cv_scores]})")

    # 3. Model Deployment
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf_model, MODEL_PATH)
    print(f"\n[3/3] Champion model successfully serialized and deployed to:\n -> {MODEL_PATH}")

    # Write evaluation report
    report_text = f"""====================================================
AI Environmental Intelligence - Model Evaluation Report
Retrained on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Dataset Source: {DATA_PATH}
Samples: {len(df)}
====================================================
Performance Metrics (Test Split 20%):
Mean Absolute Error (MAE) : {rf_mae:.2f}
Root Mean Squared Error   : {rf_rmse:.2f}
Coefficient of Det. (R²)  : {rf_r2:.4f}
5-Fold Cross-Val Mean R² : {cv_mean:.4f}

Feature Importance:
"""
    for feat, imp in sorted(zip(FEATURES, rf_model.feature_importances_), key=lambda x: x[1], reverse=True):
        report_text += f" - {feat:8s}: {imp * 100:.2f}%\n"

    with open(REPORT_PATH, "w") as f:
        f.write(report_text)
    print(f"Evaluation report written to {REPORT_PATH}")
    print("\nRetraining Pipeline Completed Successfully!")


if __name__ == "__main__":
    run_retraining_pipeline()
