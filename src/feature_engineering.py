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
    """
    Create merchant-level aggregate features using expanding-window logic.

    Sorts by merchant_id and date in-place (preserving original index).
    Uses cumulative expanding mean of surplus_quantity shifted by 1 period,
    ensuring that for each row at date D, only surplus values from dates
    strictly before D contribute to the aggregate — preventing target lookahead.
    """
    # Sort in-place but keep original index for alignment
    df.sort_values(["merchant_id", "date"], inplace=True)

    # Expanding-window merchant average: cumulative mean of surplus up to (but not including) current row.
    # shift(1) ensures the current row's surplus is excluded.
    grp = df.groupby("merchant_id")["surplus_quantity"]
    df["merchant_avg_surplus"] = grp.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["merchant_avg_surplus"] = df["merchant_avg_surplus"].fillna(0)

    # Expanding-window production average
    grp_prod = df.groupby("merchant_id")["production_quantity"]
    df["merchant_avg_production"] = grp_prod.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["merchant_avg_production"] = df["merchant_avg_production"].fillna(df["production_quantity"].mean())

    # Surplus rate
    df["merchant_avg_surplus_rate"] = np.where(
        df["merchant_avg_production"] > 0,
        df["merchant_avg_surplus"] / df["merchant_avg_production"],
        0,
    )

    # Expanding-window surplus std (shift(1), then expanding std of lagged values)
    df["merchant_surplus_std"] = (
        df.groupby("merchant_id")["surplus_quantity"]
        .transform(lambda x: x.shift(1).expanding().std())
    ).fillna(0)

    return df


def create_category_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create product-category-level aggregate features using expanding-window logic.

    Sorts by product_category and date in-place (preserving original index).
    Uses cumulative expanding mean of surplus_quantity shifted by 1 period per category.
    """
    df.sort_values(["product_category", "date"], inplace=True)

    grp = df.groupby("product_category")["surplus_quantity"]
    grp_prod = df.groupby("product_category")["production_quantity"]
    df["category_avg_surplus"] = grp.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["category_avg_surplus"] = df["category_avg_surplus"].fillna(0)

    df["category_avg_production"] = grp_prod.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["category_avg_production"] = df["category_avg_production"].fillna(df["production_quantity"].mean())

    df["category_avg_surplus_rate"] = np.where(
        df["category_avg_production"] > 0,
        df["category_avg_surplus"] / df["category_avg_production"],
        0,
    )

    return df


def create_merchant_type_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create merchant-type-level aggregate features using expanding-window logic.

    Sorts by merchant_type and date in-place (preserving original index).
    Uses cumulative expanding mean shifted by 1 period per merchant type.
    """
    df.sort_values(["merchant_type", "date"], inplace=True)

    grp = df.groupby("merchant_type")["surplus_quantity"]
    grp_prod = df.groupby("merchant_type")["production_quantity"]
    df["type_avg_surplus"] = grp.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["type_avg_surplus"] = df["type_avg_surplus"].fillna(0)

    df["type_avg_production"] = grp_prod.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["type_avg_production"] = df["type_avg_production"].fillna(df["production_quantity"].mean())

    df["type_avg_surplus_rate"] = np.where(
        df["type_avg_production"] > 0,
        df["type_avg_surplus"] / df["type_avg_production"],
        0,
    )

    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction features between variables.

    NOTE: surplus_vs_merchant_avg has been removed.
    The prior version used surplus_quantity (the target) to compute
    surplus_vs_merchant_avg = surplus_quantity - merchant_avg_surplus.
    This was a current-row target leakage risk: the feature included the
    current row's own target value, giving the model direct access to the
    label during training. This is removed in the current implementation.
    """
    df = df.copy()

    # Weekend × Promotion interaction
    df["weekend_promotion"] = df["weekend_flag"] * df["promotion_flag"]

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
    """
    Create features indicating demand patterns using expanding-window logic.

    dow_avg_sold and dow_avg_surplus are computed using only data before
    the current row's date within each merchant+category+day_of_week group.
    """
    df.sort_values(["merchant_id", "product_category", "day_of_week", "date"], inplace=True)

    grp = df.groupby(["merchant_id", "product_category", "day_of_week"])
    df["dow_avg_sold"] = grp["sold_quantity"].cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["dow_avg_sold"] = df["dow_avg_sold"].fillna(0)

    df["dow_avg_surplus"] = grp["surplus_quantity"].cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
    df["dow_avg_surplus"] = df["dow_avg_surplus"].fillna(0)

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.

    All aggregate features (merchant/category/type-level averages and
    demand features) are computed using expanding-window logic that excludes
    the current row's target value, preventing target lookahead leakage.
    Lag and rolling features use shift(1) before aggregation, ensuring
    only historical data contributes.

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
    """Return raw feature names (31 pre-encoding; 46 post one-hot
    encoding for categorical variables — what the trained model
    actually uses).

    Note: surplus_vs_merchant_avg has been removed from this list
    because it used the current row's surplus_quantity (the target)
    as a feature input — a form of current-row target leakage.
    All aggregate features (merchant_avg_surplus, category_avg_surplus,
    type_avg_surplus, dow_avg_sold, dow_avg_surplus) are now computed
    using expanding-window logic that excludes the current row's target.
    """
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
        # Merchant features (expanding-window aggregates — no future leakage)
        "merchant_type",
        "merchant_avg_surplus",
        "merchant_avg_surplus_rate",
        "merchant_surplus_std",
        # Category features (expanding-window aggregates)
        "category_avg_surplus",
        "category_avg_surplus_rate",
        # Type features (expanding-window aggregates)
        "type_avg_surplus",
        "type_avg_surplus_rate",
        # Lag features (point-in-time, clean)
        "prev_day_surplus",
        "same_weekday_last_week_surplus",
        # Rolling features (shift(1) before rolling — clean)
        "surplus_7day_avg",
        "surplus_7day_max",
        "surplus_7day_std",
        "production_7day_avg",
        "surplus_rate_7day",
        # Interaction features (surplus_vs_merchant_avg removed — current-row target leakage)
        "weekend_promotion",
        "production_vs_merchant_avg",
        # Demand features (expanding-window aggregates)
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
