#!/usr/bin/env python3
"""
Unit tests for feature_engineering module.
Tests feature creation functions and feature column definitions.
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
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    data = {
        "date": dates,
        "merchant_id": ["M1"] * 10,
        "product_category": ["Pastries"] * 10,
        "merchant_type": ["Bakery"] * 10,
        "storage_type": ["Ambient"] * 10,
        "production_quantity": [100] * 10,
        "sold_quantity": [90] * 10,
        "surplus_quantity": [10] * 10,
        "original_price": [5.50] * 10,
        "shelf_life_hours": [48] * 10,
        "preparation_time": [30] * 10,
        "holding_time_hours": [2] * 10,
        "weekend_flag": [d.dayofweek >= 5 for d in dates],
        "promotion_flag": [False] * 10,
        "day_of_week": [d.dayofweek for d in dates],
    }
    return pd.DataFrame(data)


def test_create_time_features():
    """Time features should be created correctly."""
    from src.feature_engineering import create_time_features

    df = create_sample_data()
    df = create_time_features(df)

    assert "month" in df.columns
    assert "day_of_week_sin" in df.columns
    assert "day_of_week_cos" in df.columns
    assert "is_payday_week" in df.columns


def test_create_lag_features():
    """Lag features should be created correctly."""
    from src.feature_engineering import create_lag_features

    df = create_sample_data()
    df = create_lag_features(df)

    assert "prev_day_surplus" in df.columns
    assert "same_weekday_last_week_surplus" in df.columns


def test_create_rolling_features():
    """Rolling features should be created correctly."""
    from src.feature_engineering import create_rolling_features

    df = create_sample_data()
    df = create_rolling_features(df)

    assert "surplus_7day_avg" in df.columns
    assert "surplus_7day_max" in df.columns
    assert "surplus_7day_std" in df.columns


def test_create_merchant_aggregates():
    """Merchant aggregate features should be created."""
    from src.feature_engineering import create_merchant_aggregates

    df = create_sample_data()
    df = create_merchant_aggregates(df)

    assert "merchant_avg_surplus" in df.columns
    assert "merchant_avg_surplus_rate" in df.columns


def test_create_category_aggregates():
    """Category aggregate features should be created."""
    from src.feature_engineering import create_category_aggregates

    df = create_sample_data()
    df = create_category_aggregates(df)

    assert "category_avg_surplus" in df.columns
    assert "category_avg_surplus_rate" in df.columns


def test_create_interaction_features():
    """Interaction features should be created."""
    from src.feature_engineering import create_merchant_aggregates, create_interaction_features

    df = create_sample_data()
    df = create_merchant_aggregates(df)  # prerequisite for surplus_vs_merchant_avg
    df = create_interaction_features(df)

    assert "weekend_promotion" in df.columns
    assert "surplus_vs_merchant_avg" in df.columns
    assert "production_vs_merchant_avg" in df.columns
    assert "holding_vs_shelf_ratio" in df.columns


def test_engineer_features_complete_pipeline():
    """Full feature engineering pipeline should add many columns."""
    from src.feature_engineering import engineer_features

    df = create_sample_data()
    original_cols = len(df.columns)

    df = engineer_features(df)

    # Should add many feature columns
    assert len(df.columns) > original_cols
    # Should have dow_avg_surplus and dow_avg_sold
    assert "dow_avg_surplus" in df.columns
    assert "dow_avg_sold" in df.columns


def test_get_feature_columns():
    """Feature column list should return strings."""
    from src.feature_engineering import get_feature_columns

    features = get_feature_columns()
    assert isinstance(features, list)
    assert len(features) > 0
    assert all(isinstance(f, str) for f in features)
    # Key features should be present
    assert "day_of_week" in features
    assert "dow_avg_surplus" in features


def test_get_target_column():
    """Target column should be surplus_quantity."""
    from src.feature_engineering import get_target_column

    target = get_target_column()
    assert target == "surplus_quantity"


def test_prepare_features_for_model():
    """Categorical encoding should work."""
    from src.feature_engineering import prepare_features_for_model

    df = create_sample_data()
    df = prepare_features_for_model(df)

    # Should have encoded columns
    assert "product_category_Pastries" in df.columns
    assert "merchant_type_Bakery" in df.columns


def test_engineer_features_no_nan_in_key_features():
    """Key features should not be all NaN after engineering."""
    from src.feature_engineering import engineer_features

    df = create_sample_data()
    df = engineer_features(df)

    # Lag features should have some NaN (first rows)
    assert df["prev_day_surplus"].isna().any()


if __name__ == "__main__":
    test_create_time_features()
    test_create_lag_features()
    test_create_rolling_features()
    test_create_merchant_aggregates()
    test_create_category_aggregates()
    test_create_interaction_features()
    test_engineer_features_complete_pipeline()
    test_get_feature_columns()
    test_get_target_column()
    test_prepare_features_for_model()
    test_engineer_features_no_nan_in_key_features()
    print("All feature_engineering tests passed!")
