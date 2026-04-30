#!/usr/bin/env python3
"""
SurplusSense Feature Engineering
================================
Creates features for surplus prediction ML pipeline.

Features created:
- Time-based features (day of week, weekend, month, week of year)
- Lag features (previous day surplus, same weekday last week)
- Rolling statistics (7-day avg surplus, 7-day surplus std)
- Merchant-level aggregates (avg production, avg surplus rate)
- Category-level aggregates
- Interaction features
- Demand indicators
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features from date."""
    df = df.copy()

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Basic time features
    df["month"] = df["date"].dt.month
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["day_of_month"] = df["date"].dt.day

    # Cyclical encoding for day of week (captures weekly patterns)
    df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    # Is it early/late in the month (paycheck effects)
    df["is_payday_week"] = (df["day_of_month"] <= 10).astype(int)

    return df


def create_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create lag features for time-series prediction."""
    df = df.copy()
    df = df.sort_values(["merchant_id", "product_category", "date"])

    # Previous day surplus (lag 1)
    df["prev_day_surplus"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].shift(1)

    # Same weekday last week (lag 7)
    df["same_weekday_last_week_surplus"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].shift(7)

    # Same weekday two weeks ago (lag 14)
    df["same_weekday_2weeks_ago_surplus"] = df.groupby(
        ["merchant_id", "product_category"]
    )["surplus_quantity"].shift(14)

    return df


def create_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create rolling window statistics."""
    df = df.copy()
    df = df.sort_values(["merchant_id", "product_category", "date"])

    # 7-day rolling average surplus
    df["surplus_7day_avg"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].transform(lambda x: x.shift(1).rolling(window=7, min_periods=1).mean())

    # 7-day rolling max surplus
    df["surplus_7day_max"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].transform(lambda x: x.shift(1).rolling(window=7, min_periods=1).max())

    # 7-day surplus std (volatility)
    df["surplus_7day_std"] = df.groupby(["merchant_id", "product_category"])[
        "surplus_quantity"
    ].transform(lambda x: x.shift(1).rolling(window=7, min_periods=1).std()).fillna(0)

    # 7-day total production
    df["production_7day_avg"] = df.groupby(["merchant_id", "product_category"])[
        "production_quantity"
    ].transform(lambda x: x.shift(1).rolling(window=7, min_periods=1).mean())

    # 7-day surplus rate
    df["surplus_rate_7day"] = np.where(
        df["production_7day_avg"] > 0,
        df["surplus_7day_avg"] / df["production_7day_avg"],
        0,
    )

    return df


def create_merchant_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Create merchant-level aggregate features."""
    df = df.copy()

    # Merchant-level average surplus rate (historical)
    merchant_stats = df.groupby("merchant_id").agg(
        merchant_avg_surplus=("surplus_quantity", "mean"),
        merchant_avg_production=("production_quantity", "mean"),
        merchant_surplus_std=("surplus_quantity", "std"),
    ).reset_index()

    merchant_stats["merchant_avg_surplus_rate"] = (
        merchant_stats["merchant_avg_surplus"] / merchant_stats["merchant_avg_production"]
    )
    merchant_stats["merchant_surplus_std"] = merchant_stats["merchant_surplus_std"].fillna(0)

    df = df.merge(merchant_stats[["merchant_id", "merchant_avg_surplus", "merchant_avg_production", "merchant_avg_surplus_rate", "merchant_surplus_std"]], on="merchant_id", how="left")

    return df


def create_category_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Create product-category-level aggregate features."""
    df = df.copy()

    # Category-level average surplus
    category_stats = df.groupby("product_category").agg(
        category_avg_surplus=("surplus_quantity", "mean"),
        category_avg_production=("production_quantity", "mean"),
    ).reset_index()

    category_stats["category_avg_surplus_rate"] = (
        category_stats["category_avg_surplus"] / category_stats["category_avg_production"]
    )

    df = df.merge(
        category_stats[["product_category", "category_avg_surplus", "category_avg_surplus_rate"]],
        on="product_category",
        how="left",
    )

    return df


def create_merchant_type_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Create merchant-type-level aggregate features."""
    df = df.copy()

    # Merchant-type level stats
    type_stats = df.groupby("merchant_type").agg(
        type_avg_surplus=("surplus_quantity", "mean"),
        type_avg_production=("production_quantity", "mean"),
    ).reset_index()

    type_stats["type_avg_surplus_rate"] = (
        type_stats["type_avg_surplus"] / type_stats["type_avg_production"]
    )

    df = df.merge(
        type_stats[["merchant_type", "type_avg_surplus", "type_avg_surplus_rate"]],
        on="merchant_type",
        how="left",
    )

    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create interaction features between variables."""
    df = df.copy()

    # Weekend × Promotion interaction
    df["weekend_promotion"] = df["weekend_flag"] * df["promotion_flag"]

    # Surplus deviation from merchant average
    df["surplus_vs_merchant_avg"] = df["surplus_quantity"] - df["merchant_avg_surplus"]

    # Production relative to merchant average
    df["production_vs_merchant_avg"] = (
        df["production_quantity"] / df["merchant_avg_production"]
    )

    # Holding time relative to shelf life (critical for safety)
    df["holding_vs_shelf_ratio"] = df["holding_time_hours"] / df["shelf_life_hours"]

    # Demand indicator: sold vs expected
    df["demand_fill_rate"] = np.where(
        df["production_quantity"] > 0,
        df["sold_quantity"] / df["production_quantity"],
        1.0,
    )

    return df


def create_demand_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features indicating demand patterns."""
    df = df.copy()

    # Historical demand pattern for this day of week
    dow_demand = df.groupby(["merchant_id", "product_category", "day_of_week"]).agg(
        dow_avg_sold=("sold_quantity", "mean"),
        dow_avg_surplus=("surplus_quantity", "mean"),
    ).reset_index()

    df = df.merge(
        dow_demand[["merchant_id", "product_category", "day_of_week", "dow_avg_sold", "dow_avg_surplus"]],
        on=["merchant_id", "product_category", "day_of_week"],
        how="left",
    )

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.

    Parameters:
        df: Raw DataFrame with columns from synthetic data generator

    Returns:
        DataFrame with all engineered features
    """
    df = df.copy()

    # Apply feature engineering pipeline
    df = create_time_features(df)
    df = create_lag_features(df)
    df = create_rolling_features(df)
    df = create_merchant_aggregates(df)
    df = create_category_aggregates(df)
    df = create_merchant_type_aggregates(df)
    df = create_interaction_features(df)
    df = create_demand_features(df)

    return df


def get_feature_columns() -> List[str]:
    """Return raw feature names (31 pre-encoding; 47 post one-hot
    encoding for categorical variables — what the trained model
    actually uses)."""
    return [
        # Time features
        "day_of_week",
        "weekend_flag",
        "month",
        "day_of_week_sin",
        "day_of_week_cos",
        # Product features
        "product_category",
        "original_price",
        "shelf_life_hours",
        "preparation_time",
        # Storage and holding
        "storage_type",
        "holding_time_hours",
        "holding_vs_shelf_ratio",
        # Merchant features
        "merchant_type",
        "merchant_avg_surplus",
        "merchant_avg_surplus_rate",
        "merchant_surplus_std",
        # Category features
        "category_avg_surplus",
        "category_avg_surplus_rate",
        # Type features
        "type_avg_surplus",
        "type_avg_surplus_rate",
        # Lag features (key baselines)
        "prev_day_surplus",
        "same_weekday_last_week_surplus",
        # Rolling features
        "surplus_7day_avg",
        "surplus_7day_max",
        "surplus_7day_std",
        "production_7day_avg",
        "surplus_rate_7day",
        # Interaction features
        "weekend_promotion",
        "production_vs_merchant_avg",
        # Demand features
        "dow_avg_sold",
        "dow_avg_surplus",
    ]


def get_target_column() -> str:
    """Return the target column name."""
    return "surplus_quantity"


def prepare_features_for_model(
    df: pd.DataFrame,
    categorical_cols: List[str] = ["product_category", "merchant_type", "storage_type"],
) -> pd.DataFrame:
    """
    Prepare features for ML model by encoding categoricals.

    Parameters:
        df: DataFrame with engineered features
        categorical_cols: List of categorical column names to encode

    Returns:
        DataFrame ready for ML training/prediction
    """
    df = df.copy()

    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    return df_encoded


if __name__ == "__main__":
    # Test feature engineering
    from data.generate_synthetic_data import generate_records

    print("Testing feature engineering...")
    records = generate_records(num_days=30, records_per_day_per_merchant=2)
    df = pd.DataFrame(records)

    print(f"Raw data shape: {df.shape}")
    print(f"Raw columns: {list(df.columns)}")

    df_features = engineer_features(df)
    print(f"\nAfter feature engineering shape: {df_features.shape}")
    print(f"New columns: {[c for c in df_features.columns if c not in df.columns]}")

    feature_cols = get_feature_columns()
    print(f"\nFeature columns ({len(feature_cols)}): {feature_cols}")

    df_prepared = prepare_features_for_model(df_features)
    print(f"\nAfter encoding shape: {df_prepared.shape}")
