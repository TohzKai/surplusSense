#!/usr/bin/env python3
"""
SurplusSense Model Evaluation
=============================
Evaluates baseline models and Random Forest model against multiple metrics.

Metrics:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- Improvement over baselines
- Feature importance
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.feature_engineering import engineer_features, get_feature_columns, get_target_column
from src.train_model import load_data, create_baseline_predictions, get_feature_importance


def calculate_metrics(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
    """
    Calculate evaluation metrics for surplus prediction.

    Parameters:
        y_true: Actual surplus values
        y_pred: Predicted surplus values

    Returns:
        Dict of metric_name -> value

    Decision: clip negative predictions to 0 (surplus cannot be negative).
    MAPE/SMAPE epsilon of 1e-6 prevents division by zero when y_true is 0
    (which is a real case — predicting zero waste is valid in this domain).
    """
    # Handle negative predictions (clip to 0)
    y_pred = np.maximum(y_pred, 0)
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)

    mae = mean_absolute_error(y_true_arr, y_pred_arr)
    rmse = np.sqrt(mean_squared_error(y_true_arr, y_pred_arr))

    # Median Absolute Error — robust to outliers, complement to MAE
    median_ae = np.median(np.abs(y_true_arr - y_pred_arr))

    # MAPE with epsilon guard for zero y_true
    epsilon = 1e-6
    mape_arr = np.abs((y_true_arr - y_pred_arr) / (y_true_arr + epsilon))
    mape = np.mean(mape_arr) * 100

    # SMAPE (Symmetric MAPE) — symmetric, bounded [0, 200]
    # SMAPE = 2 * |y_true - y_pred| / (|y_true| + |y_pred| + epsilon)
    denominator = np.abs(y_true_arr) + np.abs(y_pred_arr) + epsilon
    smape = np.mean(2.0 * np.abs(y_true_arr - y_pred_arr) / denominator) * 100

    # R² (coefficient of determination)
    ss_res = np.sum((y_true_arr - y_pred_arr) ** 2)
    ss_tot = np.sum((y_true_arr - np.mean(y_true_arr)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    return {
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "MAPE": round(mape, 4),
        "SMAPE": round(smape, 4),
        "R2": round(r2, 4),
        "MedAE": round(median_ae, 4),
    }


def calculate_improvement(
    baseline_mae: float, model_mae: float
) -> Dict[str, Any]:
    """
    Calculate how much the model improves over baseline.

    Returns:
        Dict with absolute and percentage improvement
    """
    absolute_improvement = baseline_mae - model_mae
    pct_improvement = (absolute_improvement / baseline_mae) * 100 if baseline_mae > 0 else 0

    return {
        "absolute_improvement": absolute_improvement,
        "percentage_improvement": pct_improvement,
        "baseline_mae": baseline_mae,
        "model_mae": model_mae,
    }


def evaluate_baselines(
    df: pd.DataFrame, baselines: Dict[str, pd.Series], target_col: str = "surplus_quantity"
) -> Dict[str, Dict[str, float]]:
    """
    Evaluate all baseline models.

    Parameters:
        df: DataFrame with actual values
        baselines: Dict of baseline_name -> predictions
        target_col: Target column name

    Returns:
        Dict of baseline_name -> metrics
    """
    y_true = df[target_col]

    results = {}
    for name, predictions in baselines.items():
        metrics = calculate_metrics(y_true, predictions)
        results[name] = metrics
        print(f"  {name}: MAE={metrics['MAE']:.4f}, RMSE={metrics['RMSE']:.4f}, "
              f"MAPE={metrics['MAPE']:.2f}%, SMAPE={metrics['SMAPE']:.2f}%, "
              f"R²={metrics['R2']:.4f}, MedAE={metrics['MedAE']:.4f}")

    return results


def evaluate_model(
    model_path: str = "outputs/surplus_model.pkl",
    data_path: str = "data/synthetic_fnb_data.csv",
    output_dir: str = "outputs",
) -> Dict[str, Any]:
    """
    Main evaluation pipeline.

    Parameters:
        model_path: Path to trained model
        data_path: Path to data
        output_dir: Directory for output files

    Returns:
        Dict with all evaluation results
    """
    print("=" * 60)
    print("SurplusSense Model Evaluation")
    print("=" * 60)

    # Load data
    df = load_data(data_path)

    # Engineer features
    print("\nEngineering features...")
    df = engineer_features(df)

    # Create baseline predictions
    print("\nEvaluating baselines...")
    baselines = create_baseline_predictions(df)
    baseline_results = evaluate_baselines(df, baselines)

    # Load trained model
    with open(model_path, "rb") as f:
        model_metadata = pickle.load(f)

    model = model_metadata["model"]
    feature_names = model_metadata["feature_names"]
    model_type = model_metadata.get("model_type", "Random Forest")

    print(f"\nLoading {model_type} model...")

    # Prepare data for model prediction
    # Need to filter to rows with valid lag features
    df_eval = df.dropna(subset=["prev_day_surplus", "same_weekday_last_week_surplus"]).copy()

    # Get encoded features
    categorical_cols = ["product_category", "merchant_type", "storage_type"]
    for col in categorical_cols:
        if col in df_eval.columns:
            dummies = pd.get_dummies(df_eval[col], prefix=col)
            df_eval = pd.concat([df_eval, dummies], axis=1)

    # Ensure all feature columns exist
    X_eval = df_eval[[c for c in feature_names if c in df_eval.columns]].fillna(0)

    # Make predictions
    print("\nMaking model predictions...")
    y_true = df_eval["surplus_quantity"]
    y_pred = model.predict(X_eval)

    # Model metrics
    model_metrics = calculate_metrics(y_true, y_pred)
    print(f"\n{model_type}: MAE={model_metrics['MAE']:.4f}, RMSE={model_metrics['RMSE']:.4f}, "
          f"MAPE={model_metrics['MAPE']:.2f}%, SMAPE={model_metrics['SMAPE']:.2f}%, "
          f"R²={model_metrics['R2']:.4f}, MedAE={model_metrics['MedAE']:.4f}")

    # Calculate improvements over each baseline
    print("\n" + "=" * 60)
    print("Improvement Over Baselines")
    print("=" * 60)

    improvements = {}
    for name, metrics in baseline_results.items():
        improvement = calculate_improvement(metrics["MAE"], model_metrics["MAE"])
        improvements[name] = improvement
        print(f"\n{name}:")
        print(f"  Baseline MAE: {improvement['baseline_mae']:.3f}")
        print(f"  Model MAE: {improvement['model_mae']:.3f}")
        print(f"  Improvement: {improvement['absolute_improvement']:.3f} ({improvement['percentage_improvement']:.1f}%)")

    # Feature importance
    print("\n" + "=" * 60)
    print("Top 15 Feature Importances")
    print("=" * 60)

    importance_df = get_feature_importance(model, feature_names)
    print(importance_df.head(15).to_string(index=False))

    # Save outputs
    os.makedirs(output_dir, exist_ok=True)

    # Save model results
    results_summary = {
        "evaluation_date": datetime.now().isoformat(),
        "n_samples": len(df_eval),
        "baseline_metrics": baseline_results,
        "model_metrics": model_metrics,
        "improvements": improvements,
    }

    # Create results DataFrame
    # Build comprehensive metrics table for all models
    results_rows = []
    for name, metrics in baseline_results.items():
        results_rows.append({
            "model": name,
            "MAE": metrics["MAE"],
            "RMSE": metrics["RMSE"],
            "MAPE": metrics["MAPE"],
            "SMAPE": metrics["SMAPE"],
            "R2": metrics["R2"],
            "MedAE": metrics["MedAE"],
            "is_baseline": True,
        })

    results_rows.append({
        "model": model_type,
        "MAE": model_metrics["MAE"],
        "RMSE": model_metrics["RMSE"],
        "MAPE": model_metrics["MAPE"],
        "SMAPE": model_metrics["SMAPE"],
        "R2": model_metrics["R2"],
        "MedAE": model_metrics["MedAE"],
        "is_baseline": False,
    })

    results_df = pd.DataFrame(results_rows)
    results_df.to_csv(f"{output_dir}/model_results.csv", index=False)

    # Full metrics summary (all models × all metrics)
    metrics_summary_df = results_df.copy()
    metrics_summary_df.to_csv(f"{output_dir}/metrics_summary.csv", index=False)

    # Print clean summary table
    print("\n" + "=" * 80)
    print("METRICS SUMMARY")
    print("=" * 80)
    header = f"{'Model':<30} {'MAE':>8} {'RMSE':>8} {'MAPE%':>8} {'SMAPE%':>8} {'R²':>8} {'MedAE':>8}"
    print(header)
    print("-" * 80)
    for _, row in results_df.iterrows():
        print(f"{row['model']:<30} {row['MAE']:>8.4f} {row['RMSE']:>8.4f} "
              f"{row['MAPE']:>8.2f} {row['SMAPE']:>8.2f} {row['R2']:>8.4f} {row['MedAE']:>8.4f}")
    print("=" * 80)
    print(f"\nSaved metrics_summary.csv and model_results.csv")

    # Save feature importance
    importance_df.to_csv(f"{output_dir}/feature_importance.csv", index=False)
    print(f"Saved feature_importance.csv")

    return {
        "baseline_results": baseline_results,
        "model_metrics": model_metrics,
        "improvements": improvements,
        "feature_importance": importance_df,
        "summary": results_df,
    }


if __name__ == "__main__":
    results = evaluate_model()
    print("\n" + "=" * 60)
    print("Evaluation complete!")
    print("=" * 60)
