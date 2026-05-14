#!/usr/bin/env python3
"""
Leakage Awareness Tests for SurplusSense Feature Engineering
=============================================================

These tests document the difference between the current aggregate feature
implementation (full-dataset aggregate) and the production-safe
expanding-window approach that prevents target lookahead.

The tests PASS on the current implementation to confirm the behavior,
but document that PRODUCTION code must use the expanding-window approach.
"""

import pandas as pd
import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.feature_engineering import engineer_features


def _make_synthetic_df_with_surplus_gradient():
    """
    Create a DataFrame where merchant_avg_surplus computed with full-dataset
    aggregate will differ from expanding-window aggregate.

    Merchant M1 has:
      - Days 1-15: surplus_quantity = 5 (low)
      - Days 16-30: surplus_quantity = 15 (high)

    Full-dataset mean = 10
    Expanding-window mean at day 16 = 5 (only days 1-15)
    This creates a measurable difference of 5 units.
    """
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    records = []
    for d in dates:
        surplus = 5 if d.day <= 15 else 15
        records.append({
            "date": d.strftime("%Y-%m-%d"),
            "merchant_id": "M1",
            "merchant_type": "Bakery",
            "product_category": "Bread",
            "product_name": "Sourdough",
            "storage_type": "Ambient",
            "original_price": 8.0,
            "shelf_life_hours": 48,
            "preparation_time": 30,
            "holding_time_hours": 2.0,
            "production_quantity": 50,
            "sold_quantity": 45,
            "surplus_quantity": surplus,
            "day_of_week": d.weekday(),
            "weekend_flag": int(d.weekday() >= 5),
            "promotion_flag": 0,
        })
    return pd.DataFrame(records)


def test_leakage_awareness_expanding_window_now_correct():
    """
    Document: expanding-window aggregate is now correctly implemented.

    The feature engineering now uses expanding-window aggregates (shift(1) cumsum/cumcount)
    so merchant_avg_surplus at day 16 = mean of days 1-15 = 5.

    This test confirms the expanding-window implementation is working:
    merchant_avg_surplus at day 16 should be 5.0 (historical mean only),
    NOT 10.0 (which would include future data from days 16-30).
    """
    df = _make_synthetic_df_with_surplus_gradient()
    df_feat = engineer_features(df.copy())

    # At day 16 (index 15), what is the merchant_avg_surplus?
    row_day16 = df_feat[df_feat["date"] == "2024-01-16"].iloc[0]

    # Expanding-window mean at day 16 = mean of days 1-15 = 5 (NOT 10)
    # This confirms the expanding-window fix is correctly implemented
    assert row_day16["merchant_avg_surplus"] == pytest.approx(5.0, abs=0.01), (
        "Expanding-window aggregate correctly uses only historical data — leakage fixed"
    )


def test_leakage_awareness_expanding_window_excludes_future():
    """
    Document: expanding-window aggregate uses only HISTORICAL data.

    At day 16 (2024-01-16), expanding-window mean = mean of days 1-15 = 5

    This is the PRODUCTION-SAFE approach. The test confirms the
    expanding-window logic produces the correct (non-leaky) value.
    """
    df = _make_synthetic_df_with_surplus_gradient()
    df = df.sort_values(["merchant_id", "date"]).reset_index(drop=True)

    # Expanding-window: cumulative mean of surplus up to (but not including) current row
    df["merchant_avg_surplus_expanding"] = (
        df.groupby("merchant_id")["surplus_quantity"]
        .transform(lambda x: x.shift(1).expanding().mean())
    )

    row_day16 = df[df["date"] == "2024-01-16"].iloc[0]

    # Expanding-window mean at day 16 = mean of days 1-15 = 5 (not 10)
    assert row_day16["merchant_avg_surplus_expanding"] == pytest.approx(5.0, abs=0.01), (
        "Expanding-window aggregate correctly uses only historical data"
    )


def test_leakage_awareness_lag_features_are_point_in_time():
    """
    Lag features (prev_day_surplus, same_weekday_last_week_surplus) are
    constructed using .shift() — they are point-in-time and do NOT include
    future information. This is the production-safe pattern.

    Confirms lag features are clean.
    """
    df = _make_synthetic_df_with_surplus_gradient()
    df_feat = engineer_features(df.copy())

    # prev_day_surplus at day 16 should be surplus at day 15 = 5
    row_day16 = df_feat[df_feat["date"] == "2024-01-16"].iloc[0]
    assert row_day16["prev_day_surplus"] == 5.0, (
        "Lag feature uses previous row only — point-in-time, no lookahead"
    )


def test_leakage_awareness_rolling_features_use_only_past():
    """
    Rolling features use .shift(1) before .rolling() — the window looks
    backward only. This is production-safe.

    Confirms rolling features are clean.
    """
    df = _make_synthetic_df_with_surplus_gradient()
    df_feat = engineer_features(df.copy())

    # surplus_7day_avg at day 16 should be mean of days 9-15 surplus (shifted)
    # Days 9-15 all have surplus = 5, so the rolling mean = 5
    row_day16 = df_feat[df_feat["date"] == "2024-01-16"].iloc[0]
    assert row_day16["surplus_7day_avg"] == pytest.approx(5.0, abs=0.01), (
        "Rolling features use shift(1) — window looks backward only"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
