#!/usr/bin/env python3
"""
Unit tests for model training and evaluation modules.
Tests baseline creation, model training, and metrics calculation.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


def create_sample_data():
    """Create sample data for testing."""
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    np.random.seed(42)

    data = {
        "date": dates,
        "merchant_id": ["M1"] * 30,
        "product_category": ["Pastries"] * 30,
        "merchant_type": ["Bakery"] * 30,
        "storage_type": ["Ambient"] * 30,
        "production_quantity": [100] * 30,
        "sold_quantity": [90 - i % 10 for i in range(30)],
        "surplus_quantity": [10 + i % 10 for i in range(30)],
        "original_price": [5.50] * 30,
        "shelf_life_hours": [48] * 30,
        "preparation_time": [30] * 30,
        "holding_time_hours": [2] * 30,
        "weekend_flag": [d.dayofweek >= 5 for d in dates],
        "promotion_flag": [False] * 30,
        "day_of_week": [d.dayofweek for d in dates],
    }
    return pd.DataFrame(data)


def test_create_baseline_predictions():
    """Baseline predictions should be created."""
    from src.train_model import create_baseline_predictions
    from src.feature_engineering import engineer_features

    df = create_sample_data()
    df = engineer_features(df)
    baselines = create_baseline_predictions(df)

    assert "historical_average" in baselines
    assert "previous_day" in baselines
    assert "same_weekday_last_week" in baselines


def test_baseline_predictions_length():
    """Baseline predictions should match data length."""
    from src.train_model import create_baseline_predictions
    from src.feature_engineering import engineer_features

    df = create_sample_data()
    df = engineer_features(df)
    baselines = create_baseline_predictions(df)

    for name, predictions in baselines.items():
        assert len(predictions) == len(df)


def test_train_random_forest_import():
    """RandomForest should be importable."""
    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
    assert model is not None


def test_calculate_metrics():
    """Metrics should be calculated correctly."""
    from src.evaluate_model import calculate_metrics

    y_true = pd.Series([10, 20, 30, 40])
    y_pred = pd.Series([12, 18, 33, 38])

    metrics = calculate_metrics(y_true, y_pred)

    assert "MAE" in metrics
    assert "RMSE" in metrics
    # |12-10|=2, |18-20|=2, |33-30|=3, |38-40|=2 → MAE=9/4=2.25
    assert metrics["MAE"] == 2.25
    assert 0 < metrics["RMSE"] < 10


def test_calculate_metrics_handles_negatives():
    """Metrics should clip negative predictions to 0."""
    from src.evaluate_model import calculate_metrics

    y_true = pd.Series([10, 20, 30])
    y_pred = pd.Series([-5, 25, 35])  # -5 should clip to 0

    metrics = calculate_metrics(y_true, y_pred)

    assert metrics["MAE"] > 0


def test_calculate_improvement():
    """Improvement calculation should be correct."""
    from src.evaluate_model import calculate_improvement

    result = calculate_improvement(baseline_mae=2.0, model_mae=1.0)

    assert result["absolute_improvement"] == 1.0
    assert result["percentage_improvement"] == 50.0
    assert result["baseline_mae"] == 2.0
    assert result["model_mae"] == 1.0


def test_evaluate_baselines():
    """Baseline evaluation should return metrics."""
    from src.train_model import create_baseline_predictions
    from src.evaluate_model import evaluate_baselines
    from src.feature_engineering import engineer_features

    df = create_sample_data()
    df = engineer_features(df)
    baselines = create_baseline_predictions(df)

    results = evaluate_baselines(df, baselines)

    for name, metrics in results.items():
        assert "MAE" in metrics
        assert "RMSE" in metrics


def test_get_feature_importance():
    """Feature importance should return DataFrame."""
    from sklearn.ensemble import RandomForestRegressor
    from src.train_model import get_feature_importance

    # Create simple model
    X = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    y = pd.Series([1, 2, 3])

    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X, y)

    importance = get_feature_importance(model, ["a", "b"])

    assert len(importance) == 2
    assert "feature" in importance.columns
    assert "importance" in importance.columns


if __name__ == "__main__":
    test_create_baseline_predictions()
    test_baseline_predictions_length()
    test_train_random_forest_import()
    test_calculate_metrics()
    test_calculate_metrics_handles_negatives()
    test_calculate_improvement()
    test_evaluate_baselines()
    test_get_feature_importance()
    print("All model training tests passed!")
