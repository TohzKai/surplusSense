#!/usr/bin/env python3
"""
SurplusSense Model Training
============================
Trains baseline models and supervised ML model (Random Forest) for surplus prediction.

Baselines:
- Historical average surplus
- Previous day surplus
- Same weekday last week surplus

Supervised Model:
- Random Forest Regressor

Features are engineered via feature_engineering.py
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
from typing import Dict, Any, Tuple
from datetime import datetime

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from scipy.stats import randint, uniform
from xgboost import XGBRegressor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.feature_engineering import (
    engineer_features,
    get_feature_columns,
    get_target_column,
    prepare_features_for_model,
)


def calculate_cv_metrics(y_true, y_pred):
    """Compute evaluation metrics for a single CV fold."""
    from sklearn.metrics import mean_absolute_error, mean_squared_error

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


def run_cross_validation(X, y, n_splits=5, n_estimators=100, max_depth=15, random_state=42):
    """
    Run k-fold time-series cross-validation.

    Uses TimeSeriesSplit — each fold trains on expanding window,
    validates on the next contiguous block.

    Returns dict with fold-level metrics and summary statistics.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)

    fold_results = []
    fold_models = []

    print(f"\nRunning {n_splits}-fold TimeSeriesSplit CV...")

    for fold_idx, (train_idx, val_idx) in enumerate(tscv.split(X), start=1):
        X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
        y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]

        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=5,
            random_state=random_state,
            n_jobs=-1,
        )
        model.fit(X_train_fold, y_train_fold)

        y_pred_fold = model.predict(X_val_fold)
        metrics = calculate_cv_metrics(y_val_fold, y_pred_fold)
        metrics["fold"] = fold_idx
        metrics["train_size"] = len(train_idx)
        metrics["val_size"] = len(val_idx)
        fold_results.append(metrics)
        fold_models.append(model)

        print(f"  Fold {fold_idx}: MAE={metrics['MAE']:.4f}, RMSE={metrics['RMSE']:.4f}, "
              f"MAPE={metrics['MAPE']:.2f}%, R²={metrics['R2']:.4f}")

    metric_names = ["MAE", "RMSE", "MAPE", "SMAPE", "R2", "MedAE"]
    summary = {}
    for metric in metric_names:
        values = [r[metric] for r in fold_results]
        summary[metric] = {
            "mean": round(np.mean(values), 4),
            "std": round(np.std(values), 4),
            "min": round(np.min(values), 4),
            "max": round(np.max(values), 4),
        }

    print(f"\nCV Summary ({n_splits} folds):")
    for metric in metric_names:
        m = summary[metric]
        print(f"  {metric}: {m['mean']:.4f} ± {m['std']:.4f} "
              f"[{m['min']:.4f} — {m['max']:.4f}]")

    return {
        "fold_results": fold_results,
        "summary": summary,
        "models": fold_models,
        "n_splits": n_splits,
    }


def run_hyperparameter_search(
    X,
    y,
    n_iter=30,
    n_splits=5,
    random_state=42,
):
    """
    RandomizedSearchCV for Random Forest hyperparameters.

    Uses TimeSeriesSplit and negative MAE as scoring metric.
    Saves results to outputs/tuning_results.csv.
    """
    print(f"\nRunning RandomizedSearchCV ({n_iter} combos, {n_splits}-fold TimeSeriesSplit)...")

    param_dist = {
        "n_estimators": randint(50, 300),
        "max_depth": randint(5, 30),
        "min_samples_split": randint(2, 30),
        "min_samples_leaf": randint(1, 15),
        "max_features": ["sqrt", "log2", None],
        "bootstrap": [True, False],
    }

    base_model = RandomForestRegressor(random_state=random_state, n_jobs=-1)
    tscv = TimeSeriesSplit(n_splits=n_splits)

    search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_dist,
        n_iter=n_iter,
        scoring="neg_mean_absolute_error",
        cv=tscv,
        random_state=random_state,
        return_train_score=True,
        verbose=0,
    )

    search.fit(X, y)

    print(f"  Best MAE: {-search.best_score_:.4f}")
    print(f"  Best params: {search.best_params_}")

    # Build results dataframe
    cv_results = pd.DataFrame(search.cv_results_)
    results_df = cv_results[[
        "param_n_estimators", "param_max_depth", "param_min_samples_split",
        "param_min_samples_leaf", "param_max_features", "param_bootstrap",
        "mean_test_score", "std_test_score",
        "mean_train_score", "rank_test_score",
    ]].copy()
    results_df["mean_test_score"] = -results_df["mean_test_score"]
    results_df["mean_train_score"] = -results_df["mean_train_score"]
    results_df.columns = [
        "n_estimators", "max_depth", "min_samples_split",
        "min_samples_leaf", "max_features", "bootstrap",
        "val_MAE_mean", "val_MAE_std", "train_MAE_mean", "rank",
    ]
    results_df = results_df.sort_values("rank")
    results_df.to_csv("outputs/tuning_results.csv", index=False)
    print(f"  Saved {len(results_df)} configs to outputs/tuning_results.csv")

    return {
        "best_params": search.best_params_,
        "best_score": -search.best_score_,
        "best_estimator": search.best_estimator_,
        "results_df": results_df,
    }


def run_xgboost_search(X, y, n_iter=30, n_splits=5, random_state=42):
    """
    RandomizedSearchCV for XGBoost hyperparameters.

    Uses TimeSeriesSplit and negative MAE as scoring metric.
    Saves results to outputs/xgb_tuning_results.csv.
    """
    print(f"\nRunning XGBoost RandomizedSearchCV ({n_iter} combos, {n_splits}-fold TimeSeriesSplit)...")

    param_dist = {
        "n_estimators": randint(50, 300),
        "max_depth": randint(3, 20),
        "learning_rate": uniform(0.01, 0.29),
        "min_child_weight": randint(1, 15),
        "subsample": uniform(0.6, 0.4),
        "colsample_bytree": uniform(0.6, 0.4),
        "gamma": uniform(0, 5),
        "reg_alpha": uniform(0, 2),
        "reg_lambda": uniform(0, 5),
    }

    base_model = XGBRegressor(random_state=random_state, n_jobs=-1, verbosity=0)
    tscv = TimeSeriesSplit(n_splits=n_splits)

    search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_dist,
        n_iter=n_iter,
        scoring="neg_mean_absolute_error",
        cv=tscv,
        random_state=random_state,
        return_train_score=True,
        verbose=0,
    )

    search.fit(X, y)

    print(f"  XGB Best MAE: {-search.best_score_:.4f}")
    print(f"  XGB Best params: {search.best_params_}")

    cv_results = pd.DataFrame(search.cv_results_)
    cols = [
        "param_n_estimators", "param_max_depth", "param_learning_rate",
        "param_min_child_weight", "param_subsample", "param_colsample_bytree",
        "param_gamma", "param_reg_alpha", "param_reg_lambda",
        "mean_test_score", "std_test_score", "rank_test_score",
    ]
    results_df = cv_results[[c for c in cols if c in cv_results.columns]].copy()
    results_df["mean_test_score"] = -results_df["mean_test_score"]
    results_df = results_df.sort_values("rank_test_score")
    results_df.to_csv("outputs/xgb_tuning_results.csv", index=False)
    print(f"  Saved {len(results_df)} configs to outputs/xgb_tuning_results.csv")

    return {
        "best_params": search.best_params_,
        "best_score": -search.best_score_,
        "best_estimator": search.best_estimator_,
        "results_df": results_df,
    }


def train_and_compare_models(
    X_train, X_test, y_train, y_test,
    rf_params, xgb_params, random_state=42,
):
    """
    Train both Random Forest and XGBoost with tuned hyperparameters,
    evaluate on hold-out test set, save comparison to outputs/model_comparison.csv.

    Returns dict of model_name -> metrics.
    """
    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

    results = {}

    # --- Random Forest (tuned params) ---
    rf_model = RandomForestRegressor(**rf_params, random_state=random_state, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = np.maximum(rf_model.predict(X_test), 0)
    rf_metrics = calculate_cv_metrics(y_test, rf_pred)
    results["Random Forest (Tuned)"] = rf_metrics
    print(f"\nRandom Forest (Tuned): MAE={rf_metrics['MAE']:.4f}, "
          f"RMSE={rf_metrics['RMSE']:.4f}, R²={rf_metrics['R2']:.4f}")

    # --- XGBoost (tuned params) ---
    xgb_model = XGBRegressor(**xgb_params, random_state=random_state, n_jobs=-1, verbosity=0)
    xgb_model.fit(X_train, y_train)
    xgb_pred = np.maximum(xgb_model.predict(X_test), 0)
    xgb_metrics = calculate_cv_metrics(y_test, xgb_pred)
    results["XGBoost"] = xgb_metrics
    print(f"XGBoost: MAE={xgb_metrics['MAE']:.4f}, "
          f"RMSE={xgb_metrics['RMSE']:.4f}, R²={xgb_metrics['R2']:.4f}")

    # --- Save comparison ---
    rows = []
    for name, m in results.items():
        rows.append({**{"model": name}, **{k: v for k, v in m.items()}})
    comp_df = pd.DataFrame(rows)
    comp_df.to_csv("outputs/model_comparison.csv", index=False)
    print(f"\nSaved model comparison to outputs/model_comparison.csv")

    return results


def load_data(filepath: str = "data/synthetic_fnb_data.csv") -> pd.DataFrame:
    """Load synthetic F&B data."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df


def create_baseline_predictions(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    Create baseline predictions using simple business rules.

    Baselines:
    1. Historical average: mean surplus for this merchant+category
    2. Previous day surplus: lag 1
    3. Same weekday last week: lag 7

    Returns:
        Dict of baseline_name -> predictions
    """
    df = df.copy()

    baselines = {}

    # Baseline 1: Historical average surplus (merchant + category)
    # Use expanding mean to avoid look-ahead bias
    df = df.sort_values(["merchant_id", "product_category", "date"])
    df["cum_sum"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].cumsum()
    df["cum_count"] = df.groupby(["merchant_id", "product_category"]).cumcount() + 1
    df["historical_avg_baseline"] = np.where(
        df["cum_count"] > 1, df["cum_sum"] / df["cum_count"], df["surplus_quantity"]
    )
    baselines["historical_average"] = df["historical_avg_baseline"]

    # Baseline 2: Previous day surplus (lag 1)
    # Already have prev_day_surplus from feature engineering
    baselines["previous_day"] = df["prev_day_surplus"].fillna(
        df["merchant_avg_surplus"]
    ).fillna(df["surplus_quantity"].mean())

    # Baseline 3: Same weekday last week (lag 7)
    baselines["same_weekday_last_week"] = df["same_weekday_last_week_surplus"].fillna(
        df["merchant_avg_surplus"]
    ).fillna(df["surplus_quantity"].mean())

    return baselines


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    max_depth: int = 15,
    min_samples_split: int = 5,
    random_state: int = 42,
) -> RandomForestRegressor:
    """
    Train a Random Forest model for surplus prediction.

    Parameters:
        X_train: Feature matrix
        y_train: Target variable (surplus_quantity)
        n_estimators: Number of trees
        max_depth: Maximum tree depth
        min_samples_split: Minimum samples to split a node
        random_state: Random seed for reproducibility

    Returns:
        Trained RandomForestRegressor
    """
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)
    print(f"Random Forest trained with {n_estimators} trees, max_depth={max_depth}")

    return model


def prepare_training_data(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    min_records: int = 2,
) -> Tuple[pd.DataFrame, pd.Series, pd.Index]:
    """
    Prepare data for model training.

    Parameters:
        df: DataFrame with engineered features
        feature_cols: List of feature column names
        target_col: Target column name
        min_records: Minimum records required per merchant+category

    Returns:
        X: Feature matrix (filtered)
        y: Target series (filtered)
        valid_indices: Index of valid rows
    """
    df = df.copy()

    # Remove rows with insufficient history (need at least 2 records for lag features)
    df = df.dropna(subset=["prev_day_surplus", "same_weekday_last_week_surplus"])

    # Ensure all feature columns exist
    available_features = [c for c in feature_cols if c in df.columns]

    # Handle categorical columns that need encoding
    categorical_cols = ["product_category", "merchant_type", "storage_type"]
    encoded_features = []

    for col in categorical_cols:
        if col in df.columns:
            # Create dummy variables
            dummies = pd.get_dummies(df[col], prefix=col)
            encoded_features.extend(dummies.columns.tolist())
            df = pd.concat([df, dummies], axis=1)

    # Combine available numeric features with encoded categoricals
    numeric_features = [c for c in available_features if c not in categorical_cols]
    all_features = numeric_features + encoded_features

    # Filter to only available features
    all_features = [c for c in all_features if c in df.columns]

    X = df[all_features].copy()
    y = df[target_col].copy()

    # Fill any remaining NaN values
    X = X.fillna(0)

    print(f"Training data: {len(X)} samples, {len(all_features)} features")

    return X, y, X.index


def train_model(
    data_path: str = "data/synthetic_fnb_data.csv",
    model_output_path: str = "outputs/surplus_model.pkl",
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[RandomForestRegressor, Dict[str, Any]]:
    """
    Main training pipeline.

    Parameters:
        data_path: Path to synthetic data
        model_output_path: Path to save trained model
        test_size: Fraction of data for testing
        random_state: Random seed

    Returns:
        (trained_model, metadata)
    """
    print("=" * 60)
    print("SurplusSense Model Training")
    print("=" * 60)

    # Load data
    df = load_data(data_path)

    # Engineer features
    print("\nEngineering features...")
    df = engineer_features(df)

    # Get feature columns
    feature_cols = get_feature_columns()
    target_col = get_target_column()

    # Prepare training data
    X, y, valid_indices = prepare_training_data(df, feature_cols, target_col)

    # Run cross-validation on full dataset (before hold-out split)
    cv_results = run_cross_validation(X, y, n_splits=5, n_estimators=100, max_depth=15, random_state=random_state)

    # Save CV results to CSV
    cv_output_path = "outputs/cv_results.csv"
    os.makedirs(os.path.dirname(cv_output_path), exist_ok=True)
    cv_rows = []
    for r in cv_results["fold_results"]:
        row = {"fold": r["fold"], "train_size": r["train_size"], "val_size": r["val_size"]}
        for metric in ["MAE", "RMSE", "MAPE", "SMAPE", "R2", "MedAE"]:
            row[metric] = r[metric]
        cv_rows.append(row)
    cv_df = pd.DataFrame(cv_rows)

    # Add summary row
    summary_row = {"fold": "mean", "train_size": "", "val_size": ""}
    for metric in ["MAE", "RMSE", "MAPE", "SMAPE", "R2", "MedAE"]:
        m = cv_results["summary"][metric]
        summary_row[metric] = f"{m['mean']:.4f} ± {m['std']:.4f}"
    cv_df = pd.concat([cv_df, pd.DataFrame([summary_row])], ignore_index=True)
    cv_df.to_csv(cv_output_path, index=False)
    print(f"\nCV results saved to {cv_output_path}")

    # Hyperparameter search - Random Forest
    tune_results = run_hyperparameter_search(X, y, n_iter=30, n_splits=5, random_state=random_state)
    best_params = tune_results["best_params"]

    # Hyperparameter search - XGBoost
    xgb_results = run_xgboost_search(X, y, n_iter=30, n_splits=5, random_state=random_state)
    xgb_best_params = xgb_results["best_params"]

    # Split data — temporal split (last 20% of sorted dates as holdout)
    # This is more realistic for time-series surplus prediction than random split
    df_sorted = df.loc[valid_indices].sort_values("date")
    split_idx = int(len(df_sorted) * (1 - test_size))
    train_dates = df_sorted.iloc[:split_idx]["date"]
    test_dates = df_sorted.iloc[split_idx:]["date"]

    train_mask = X.index.isin(X.index[X.index.isin(df[df["date"].isin(train_dates)].index)])
    test_mask = X.index.isin(X.index[X.index.isin(df[df["date"].isin(test_dates)].index)])

    X_train = X[train_mask]
    X_test = X[test_mask]
    y_train = y[train_mask]
    y_test = y[test_mask]

    # Train and compare RF vs XGBoost
    comparison = train_and_compare_models(
        X_train, X_test, y_train, y_test,
        rf_params=best_params,
        xgb_params=xgb_best_params,
    )

    # Select best model by holdout MAE
    best_name = min(comparison, key=lambda k: comparison[k]["MAE"])
    best_metrics = comparison[best_name]

    print(f"\n{'='*60}")
    print(f"BEST MODEL: {best_name}")
    print(f"  MAE={best_metrics['MAE']:.4f}, RMSE={best_metrics['RMSE']:.4f}, "
          f"MAPE={best_metrics['MAPE']:.2f}%, SMAPE={best_metrics['SMAPE']:.2f}%, "
          f"R²={best_metrics['R2']:.4f}, MedAE={best_metrics['MedAE']:.4f}")
    print(f"{'='*60}")

    # Train final model with best params and full training data
    if "XGBoost" in best_name:
        final_model = XGBRegressor(
            n_estimators=xgb_best_params.get("n_estimators", 100),
            max_depth=xgb_best_params.get("max_depth", 6),
            learning_rate=xgb_best_params.get("learning_rate", 0.1),
            min_child_weight=xgb_best_params.get("min_child_weight", 1),
            subsample=xgb_best_params.get("subsample", 0.8),
            colsample_bytree=xgb_best_params.get("colsample_bytree", 0.8),
            random_state=random_state,
            n_jobs=-1,
            verbosity=0,
        )
        final_model.fit(X_train, y_train)
        model_type_label = "XGBoost"
    else:
        final_model = RandomForestRegressor(
            n_estimators=best_params.get("n_estimators", 100),
            max_depth=best_params.get("max_depth", 15),
            min_samples_split=best_params.get("min_samples_split", 5),
            min_samples_leaf=best_params.get("min_samples_leaf", 1),
            max_features=best_params.get("max_features", "sqrt"),
            bootstrap=best_params.get("bootstrap", True),
            random_state=random_state,
            n_jobs=-1,
        )
        final_model.fit(X_train, y_train)
        model_type_label = "Random Forest"

    # Save model
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

    model_metadata = {
        "model": final_model,
        "model_type": model_type_label,
        "feature_names": list(X.columns),
        "train_date": datetime.now().isoformat(),
        "n_train_samples": len(X_train),
        "n_test_samples": len(X_test),
        "best_params": best_params if "Forest" in best_name else xgb_best_params,
        "rf_cv_best_score": tune_results["best_score"],
        "xgb_cv_best_score": xgb_results["best_score"],
        "comparison": comparison,
        "selected_model": best_name,
        "selected_metrics": best_metrics,
    }

    with open(model_output_path, "wb") as f:
        pickle.dump(model_metadata, f)

    print(f"\nModel saved to {model_output_path}")

    return final_model, model_metadata


def get_feature_importance(model: RandomForestRegressor, feature_names: list) -> pd.DataFrame:
    """
    Extract feature importance from trained Random Forest.

    Returns DataFrame sorted by importance.
    """
    importances = model.feature_importances_

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    return importance_df


if __name__ == "__main__":
    # Run training
    model, metadata = train_model()
    print("\nTraining complete!")
    print(f"Feature importance saved via evaluate_model.py")
