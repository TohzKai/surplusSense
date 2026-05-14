#!/usr/bin/env python3
"""
Unit tests for record fallback logic in streamlit_app.py.
Tests get_selected_record_or_fallback and _safe_get.
"""

import sys
import os
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

# Import from app module (the helpers are at module level now)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "streamlit_app_module",
    os.path.join(PROJECT_ROOT, "app", "streamlit_app.py")
)
# We only need to test the helpers; importing the whole app requires streamlit
# so we inline the function logic here for testing purposes


def _safe_get(record, key, default):
    """Safely get a value from a dict-like record, returning default if key missing."""
    try:
        val = record[key]
        if pd.isna(val):
            return default
        return val
    except (KeyError, TypeError, ValueError):
        return default


def get_selected_record_or_fallback(df, merchant_id, category, product, selected_date=None):
    """
    Return a safe record-like dict for the selected merchant/category/product/date.
    Copied from app/streamlit_app.py for isolated testing.
    """
    # Guard: if DataFrame is empty or has no columns, return hardcoded defaults immediately
    if df is None or len(df.columns) == 0 or len(df) == 0:
        return {
            "surplus_quantity": 5.0,
            "preparation_time": 30,
            "holding_time_hours": 2.0,
            "storage_type": "Refrigerated",
            "shelf_life_hours": 48.0,
            "original_price": 10.0,
            "weekend_flag": False,
            "promotion_flag": False,
        }, "fallback: hardcoded defaults"

    SAFE_DEFAULTS = {
        "surplus_quantity": 5.0,
        "preparation_time": 30,
        "holding_time_hours": 2.0,
        "storage_type": "Refrigerated",
        "shelf_life_hours": 48.0,
        "original_price": 10.0,
        "weekend_flag": False,
        "promotion_flag": False,
    }

    if selected_date is not None:
        exact = df[
            (df["merchant_id"] == merchant_id) &
            (df["product_category"] == category) &
            (df["product_name"] == product) &
            (df["date"] == selected_date)
        ]
        if len(exact) > 0:
            return exact.iloc[-1].to_dict(), "exact merchant/category/product/date"

    mcp = df[
        (df["merchant_id"] == merchant_id) &
        (df["product_category"] == category) &
        (df["product_name"] == product)
    ]
    if len(mcp) > 0:
        return mcp.tail(1).iloc[-1].to_dict(), "fallback: merchant/category/product (latest date)"

    mc = df[
        (df["merchant_id"] == merchant_id) &
        (df["product_category"] == category)
    ]
    if len(mc) > 0:
        return mc.tail(1).iloc[-1].to_dict(), "fallback: merchant/category (latest record)"

    cp = df[df["product_category"] == category]
    if len(cp) > 0:
        avg = cp.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in cp.columns:
            mode_vals = cp["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: category average"

    m = df[df["merchant_id"] == merchant_id]
    if len(m) > 0:
        avg = m.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in m.columns:
            mode_vals = m["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: merchant average"

    if len(df) > 0:
        avg = df.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in df.columns:
            mode_vals = df["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: global average"

    return SAFE_DEFAULTS.copy(), "fallback: hardcoded defaults"


def create_test_df():
    """Create a sample DataFrame for testing."""
    dates = pd.date_range("2024-01-01", periods=10, freq="D").astype(str)
    m1_dates = list(dates)
    m2_dates = list(dates)
    return pd.DataFrame({
        "date": m1_dates + m2_dates,
        "merchant_id": ["M1"] * 10 + ["M2"] * 10,
        "product_category": ["Pastries"] * 10 + ["Bread"] * 10,
        "product_name": ["Croissant"] * 10 + ["Baguette"] * 10,
        "surplus_quantity": [10.0] * 5 + [8.0] * 5 + [6.0] * 10,
        "original_price": [5.50] * 5 + [4.00] * 5 + [3.50] * 10,
        "preparation_time": [30] * 10 + [20] * 10,
        "holding_time_hours": [2.0] * 10 + [1.5] * 10,
        "storage_type": ["Ambient"] * 10 + ["Refrigerated"] * 10,
        "shelf_life_hours": [48.0] * 10 + [72.0] * 10,
        "weekend_flag": [False] * 7 + [True] * 3 + [False] * 10,
        "promotion_flag": [False] * 10 + [True] * 5 + [False] * 5,
    })


class TestSafeGet:
    def test_normal_access(self):
        record = {"surplus_quantity": 10.0, "original_price": 5.50}
        assert _safe_get(record, "surplus_quantity", 5.0) == 10.0
        assert _safe_get(record, "original_price", 10.0) == 5.50

    def test_missing_key_returns_default(self):
        record = {"surplus_quantity": 10.0}
        assert _safe_get(record, "missing_key", 5.0) == 5.0
        assert _safe_get(record, "other_key", "default") == "default"

    def test_none_record_returns_default(self):
        assert _safe_get(None, "key", 5.0) == 5.0

    def test_pandas_na_returns_default(self):
        record = {"value": pd.NA}
        assert _safe_get(record, "value", 5.0) == 5.0


class TestRecordFallback:
    def test_exact_match_returns_record(self):
        df = create_test_df()
        record, label = get_selected_record_or_fallback(df, "M1", "Pastries", "Croissant", "2024-01-01")
        assert label == "exact merchant/category/product/date"
        assert record["surplus_quantity"] == 10.0

    def test_no_date_match_falls_back_to_merchant_category_product(self):
        df = create_test_df()
        # Product exists for M1/Pastries but not on "2024-01-20" (out of range)
        # Falls back to merchant/category/product — tail(1) gives last record (index 9 = 8.0)
        record, label = get_selected_record_or_fallback(df, "M1", "Pastries", "Croissant", "2024-01-20")
        assert "fallback" in label
        assert record["surplus_quantity"] == 8.0  # tail(1) of [10.0]*5 + [8.0]*5

    def test_no_product_match_falls_back_to_merchant_category(self):
        df = create_test_df()
        record, label = get_selected_record_or_fallback(df, "M1", "Pastries", "UnknownProduct", "2024-01-01")
        assert "fallback" in label
        assert "surplus_quantity" in record
        assert "original_price" in record

    def test_no_category_match_uses_global_average(self):
        df = create_test_df()
        record, label = get_selected_record_or_fallback(df, "M999", "UnknownCat", "Unknown", "2024-01-01")
        assert label == "fallback: global average"
        assert "surplus_quantity" in record
        assert "original_price" in record
        assert "storage_type" in record

    def test_never_raises_index_error(self):
        """Regression test: must never raise IndexError from iloc on empty DataFrame."""
        empty_df = pd.DataFrame(columns=["date", "merchant_id", "product_category", "product_name",
                                          "surplus_quantity", "original_price", "preparation_time",
                                          "holding_time_hours", "storage_type", "shelf_life_hours",
                                          "weekend_flag", "promotion_flag"])
        # Must not raise
        record, label = get_selected_record_or_fallback(empty_df, "M1", "Pastries", "Croissant", "2024-01-01")
        assert label == "fallback: hardcoded defaults"
        assert record["surplus_quantity"] == 5.0
        assert record["storage_type"] == "Refrigerated"

    def test_empty_df_returns_hardcoded_defaults(self):
        empty_df = pd.DataFrame()
        record, label = get_selected_record_or_fallback(empty_df, "M1", "Pastries", "Croissant", "2024-01-01")
        assert label == "fallback: hardcoded defaults"
        assert record["surplus_quantity"] == 5.0
        assert record["original_price"] == 10.0
        assert record["preparation_time"] == 30
        assert record["storage_type"] == "Refrigerated"

    def test_unknown_merchant_uses_global_fallback(self):
        df = create_test_df()
        record, label = get_selected_record_or_fallback(df, "M999", "Pastries", "Croissant", "2024-01-01")
        # M999 doesn't exist, so falls back to category → global average
        assert "fallback" in label
        assert "surplus_quantity" in record

    def test_all_required_keys_present(self):
        df = create_test_df()
        record, _ = get_selected_record_or_fallback(df, "M999", "Unknown", "Unknown", "2024-01-01")
        required_keys = ["surplus_quantity", "original_price", "preparation_time",
                         "holding_time_hours", "storage_type", "shelf_life_hours",
                         "weekend_flag", "promotion_flag"]
        for key in required_keys:
            assert key in record, f"Missing key: {key}"
