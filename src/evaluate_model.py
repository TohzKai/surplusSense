#!/usr/bin/env python3
"""
SurplusSense Model Evaluation
=============================
Displays the official temporal holdout evaluation results from the training run.

The official model metric is the temporal holdout MAE recorded in
`outputs/model_comparison.csv`, which is generated at training time using the
same temporal 80/20 split (last 20% of dates, sorted chronologically) used
to train the model.

A separate diagnostic evaluation over the broader engineered dataset is also
available in this script (run with --diagnostic) but is NOT used as the
official assignment metric because it evaluates on a larger, non-holdout
sample and can overstate performance.

Official reported metric:
    XGBoost MAE = 0.6355 (temporal holdout, last 20% of dates)
    Improvement vs Historical Average baseline: ~57%

Usage:
    python src/evaluate_model.py              # Display official temporal holdout metrics
    python src/evaluate_model.py --diagnostic # Run diagnostic broader-dataset evaluation
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import mean_absolute_error, mean_squared_error


# ─────────────────────────────────────────────────────────────────────────────
# Utility functions (kept for backward compatibility with tests)
# ─────────────────────────────────────────────────────────────────────────────

def calculate_improvement(baseline_mae: float, model_mae: float) -> dict:
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
    df: pd.DataFrame, baselines: dict, target_col: str = "surplus_quantity"
) -> dict:
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
        metrics = calculate_metrics(y_true, predictions.fillna(y_true.mean()))
        results[name] = metrics
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Official temporal holdout display
# ─────────────────────────────────────────────────────────────────────────────

def display_official_holdout_metrics():
    """
    Load and display the official temporal holdout evaluation results.

    These results are computed during model training (src/train_model.py) using
    an 80/20 temporal split on the last 20% of dates. The metrics are saved
    to outputs/model_comparison.csv at training time.

    This is the defensible, reported assignment metric.
    """
    comparison_path = "outputs/model_comparison.csv"
    results_path = "outputs/model_results.csv"

    print("=" * 60)
    print("SurplusSense Model Evaluation")
    print("=" * 60)
    print()
    print("Evaluation type: Temporal holdout evaluation")
    print("Official metric source: outputs/model_comparison.csv")
    print("  (Generated at training time using last 20% of dates as holdout)")
    print()

    if not os.path.exists(comparison_path):
        print(f"ERROR: {comparison_path} not found.")
        print("Please run `python src/train_model.py` first to generate the model and metrics.")
        return None

    comp_df = pd.read_csv(comparison_path)

    # Load model_results.csv for baseline comparison
    if os.path.exists(results_path):
        results_df = pd.read_csv(results_path)
        baselines = results_df[results_df["is_baseline"] == True]
        if len(baselines) > 0:
            # Use historical_average as the primary baseline
            hist_base = baselines[baselines["model"] == "historical_average"]
            if len(hist_base) > 0:
                baseline_mae = hist_base["MAE"].iloc[0]
            else:
                baseline_mae = baselines.iloc[baselines["MAE"].idxmin()]["MAE"]
        else:
            baseline_mae = None
    else:
        baseline_mae = None

    print("-" * 60)
    print(f"{'Model':<30} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
    print("-" * 60)

    for _, row in comp_df.iterrows():
        print(f"{row['model']:<30} {row['MAE']:>8.4f} {row['RMSE']:>8.4f} {row['R2']:>8.4f}")

    print("-" * 60)

    # Highlight XGBoost result
    xgb_row = comp_df[comp_df["model"] == "XGBoost"]
    if len(xgb_row) > 0:
        xgb_mae = xgb_row["MAE"].iloc[0]
        xgb_rmse = xgb_row["RMSE"].iloc[0]
        xgb_r2 = xgb_row["R²"].iloc[0] if "R²" in xgb_row.columns else xgb_row["R2"].iloc[0]
        print()
        print(f"Official reported metric — XGBoost temporal holdout:")
        print(f"  MAE  = {xgb_mae:.4f}")
        print(f"  RMSE = {xgb_rmse:.4f}")
        print(f"  R²   = {xgb_r2:.4f}")

        if baseline_mae is not None:
            improvement_pct = (baseline_mae - xgb_mae) / baseline_mae * 100
            print()
            print(f"Improvement vs Historical Average baseline (MAE {baseline_mae:.4f}):")
            print(f"  MAE reduction: {baseline_mae - xgb_mae:.4f}")
            print(f"  Improvement:     {improvement_pct:.1f}%")
        else:
            # Fallback: use 1.49 from model comparison if available
            if "historical_average" in comp_df["model"].values:
                ha_row = comp_df[comp_df["model"] == "historical_average"]
                if len(ha_row) > 0:
                    ha_mae = ha_row["MAE"].iloc[0]
                    improvement_pct = (ha_mae - xgb_mae) / ha_mae * 100
                    print()
                    print(f"Improvement vs Historical Average baseline (MAE {ha_mae:.4f}):")
                    print(f"  MAE reduction: {ha_mae - xgb_mae:.4f}")
                    print(f"  Improvement:     {improvement_pct:.1f}%")

    print()
    print("=" * 60)
    print("NOTE: The official reported metric is the temporal holdout MAE")
    print("      from outputs/model_comparison.csv, computed at training time")
    print("      using the last 20% of dates as the holdout set.")
    print()
    print("      A diagnostic broader-dataset evaluation is available with:")
    print("      python src/evaluate_model.py --diagnostic")
    print()
    print("      The diagnostic MAE (e.g. ~0.47) is NOT the official metric")
    print("      because it evaluates on a larger, non-holdout sample and can")
    print("      overstate model performance.")
    print("=" * 60)

    return comp_df


# ─────────────────────────────────────────────────────────────────────────────
# Diagnostic broader-dataset evaluation
# ─────────────────────────────────────────────────────────────────────────────

def calculate_metrics(y_true, y_pred):
    """Compute evaluation metrics."""
    y_pred = np.maximum(y_pred, 0)
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)

    mae = mean_absolute_error(y_true_arr, y_pred_arr)
    rmse = np.sqrt(mean_squared_error(y_true_arr, y_pred_arr))

    median_ae = np.median(np.abs(y_true_arr - y_pred_arr))

    epsilon = 1e-6
    mape_arr = np.abs((y_true_arr - y_pred_arr) / (y_true_arr + epsilon))
    mape = np.mean(mape_arr) * 100

    denominator = np.abs(y_true_arr) + np.abs(y_pred_arr) + epsilon
    smape = np.mean(2.0 * np.abs(y_true_arr - y_pred_arr) / denominator) * 100

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


def create_baseline_predictions(df):
    """Create baseline predictions using expanding-window logic."""
    df = df.copy()

    baselines = {}

    # Historical average baseline (expanding mean, no lookahead)
    df = df.sort_values(["merchant_id", "product_category", "date"])
    df["cum_sum"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].cumsum()
    df["cum_count"] = df.groupby(["merchant_id", "product_category"]).cumcount() + 1
    df["historical_avg_baseline"] = np.where(
        df["cum_count"] > 1, df["cum_sum"] / df["cum_count"], df["surplus_quantity"]
    )
    baselines["historical_average"] = df["historical_avg_baseline"]

    # Previous day baseline
    baselines["previous_day"] = df["prev_day_surplus"].fillna(
        df["merchant_avg_surplus"]
    ).fillna(df["surplus_quantity"].mean())

    # Same weekday last week baseline
    baselines["same_weekday_last_week"] = df["same_weekday_last_week_surplus"].fillna(
        df["merchant_avg_surplus"]
    ).fillna(df["surplus_quantity"].mean())

    return baselines


def run_diagnostic_evaluation():
    """
    Run diagnostic evaluation over the broader engineered dataset.

    WARNING: This is NOT the official assignment metric.
    This evaluation is over the full engineered dataset (after dropping rows
    without valid lag features) rather than the temporal holdout set.
    The diagnostic MAE (~0.47) is lower than the official holdout MAE (0.6355)
    because it includes rows from throughout the time series, not just the
    forward-looking holdout period. Do NOT report this as the model accuracy.
    """
    print()
    print("=" * 60)
    print("DIAGNOSTIC EVALUATION (NOT the official assignment metric)")
    print("=" * 60)
    print()
    print("WARNING: This evaluation runs over the broader engineered dataset")
    print("         (full dataset after dropping rows without lag features).")
    print("         It is NOT the same as the temporal holdout evaluation")
    print("         used for the official reported metric.")
    print()
    print("         Diagnostic MAE (~0.47) will be lower than the official")
    print("         holdout MAE (0.6355) because it includes easier cases")
    print("         from the earlier part of the time series.")
    print()
    print("         For the official metric, run without --diagnostic:")
    print("         python src/evaluate_model.py")
    print()

    # Import here to keep diagnostic isolated
    from src.feature_engineering import engineer_features

    # Load data
    data_path = "data/synthetic_fnb_data.csv"
    model_path = "outputs/surplus_model.pkl"

    if not os.path.exists(data_path):
        print(f"ERROR: {data_path} not found.")
        return

    if not os.path.exists(model_path):
        print(f"ERROR: {model_path} not found. Run `python src/train_model.py` first.")
        return

    print("-" * 60)
    print("Loading data and engineering features...")
    print("-" * 60)

    df = pd.read_csv(data_path)
    df = engineer_features(df)

    # Create baseline predictions
    baselines = create_baseline_predictions(df)
    y_true_all = df["surplus_quantity"]

    print("\nBaseline metrics (full engineered dataset):")
    for name, preds in baselines.items():
        m = calculate_metrics(y_true_all, preds.fillna(y_true_all.mean()))
        print(f"  {name}: MAE={m['MAE']:.4f}, RMSE={m['RMSE']:.4f}")

    # Filter to valid rows for model prediction
    df_eval = df.dropna(subset=["prev_day_surplus", "same_weekday_last_week_surplus"]).copy()

    # Encode categoricals the same way as training
    import pickle
    with open(model_path, "rb") as f:
        model_metadata = pickle.load(f)

    model = model_metadata["model"]
    feature_names = model_metadata["feature_names"]

    categorical_cols = ["product_category", "merchant_type", "storage_type"]
    for col in categorical_cols:
        if col in df_eval.columns:
            dummies = pd.get_dummies(df_eval[col], prefix=col)
            df_eval = pd.concat([df_eval, dummies], axis=1)

    X_eval = df_eval[[c for c in feature_names if c in df_eval.columns]].fillna(0)

    print(f"\nDiagnostic evaluation on {len(X_eval)} rows (full engineered dataset):")

    y_pred_diag = model.predict(X_eval)
    diag_metrics = calculate_metrics(df_eval["surplus_quantity"], y_pred_diag)

    print(f"\n  XGBoost (diagnostic):")
    print(f"    MAE  = {diag_metrics['MAE']:.4f}")
    print(f"    RMSE = {diag_metrics['RMSE']:.4f}")
    print(f"    R²   = {diag_metrics['R2']:.4f}")

    # Compare to official
    print()
    print(f"  For comparison — official temporal holdout MAE: 0.6355")
    print(f"  This diagnostic MAE:                          {diag_metrics['MAE']:.4f}")
    print()
    print("  The diagnostic MAE is lower because it evaluates on the full")
    print("  time series, not the forward-looking holdout period.")
    print()
    print("=" * 60)
    print("END OF DIAGNOSTIC EVALUATION")
    print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SurplusSense Model Evaluation")
    parser.add_argument(
        "--diagnostic",
        action="store_true",
        help="Run diagnostic broader-dataset evaluation (NOT the official metric)",
    )
    args = parser.parse_args()

    if args.diagnostic:
        run_diagnostic_evaluation()
    else:
        display_official_holdout_metrics()


if __name__ == "__main__":
    main()
