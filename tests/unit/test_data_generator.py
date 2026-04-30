#!/usr/bin/env python3
"""
Unit tests for data_generator module.
Tests synthetic data generation functions.
"""

import sys
import os
# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


def test_generate_records_returns_list():
    """generate_records should return a list."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)
    assert isinstance(records, list)


def test_generate_records_length():
    """generate_records should return a non-empty list of expected size."""
    from src.data_generator import generate_records

    num_days = 7
    records_per_day = 3

    records = generate_records(
        num_days=num_days,
        records_per_day_per_merchant=records_per_day,
    )

    # With 3 merchant types x 5 merchants x ~3 records/day x 7 days = ~315 records
    # Allow range due to random selection
    assert len(records) > 200
    assert isinstance(records, list)


def test_generate_records_has_required_fields():
    """Generated records should have all required fields."""
    from src.data_generator import generate_records

    records = generate_records(num_days=3, records_per_day_per_merchant=1)

    required_fields = [
        "date", "merchant_id", "merchant_type", "product_category",
        "product_name", "storage_type", "original_price",
        "production_quantity", "sold_quantity", "surplus_quantity",
        "shelf_life_hours", "preparation_time", "holding_time_hours",
    ]

    for record in records[:5]:  # Check first 5 records
        for field in required_fields:
            assert field in record, f"Missing field: {field}"


def test_generate_records_surplus_calculation():
    """Surplus should equal production minus sold."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    for record in records:
        expected_surplus = record["production_quantity"] - record["sold_quantity"]
        assert record["surplus_quantity"] == expected_surplus


def test_generate_records_valid_categories():
    """Records should have valid product categories."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    valid_categories = [
        "Coffee & Beverages", "Pastries", "Sandwiches", "Salads",
        "Desserts", "Bread", "Cakes", "Cookies", "Tarts",
        "Rice Dishes", "Noodle Dishes", "Bento Sets", "Soup & Sides",
    ]

    for record in records:
        assert record["product_category"] in valid_categories


def test_generate_records_valid_storage():
    """Records should have valid storage types."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    valid_storage = ["Ambient", "Refrigerated", "Frozen"]

    for record in records:
        assert record["storage_type"] in valid_storage


def test_generate_records_prices_positive():
    """Original prices should be positive."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    for record in records:
        assert record["original_price"] > 0


def test_generate_records_quantities_non_negative():
    """Production, sold, and surplus quantities should be non-negative."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    for record in records:
        assert record["production_quantity"] >= 0
        assert record["sold_quantity"] >= 0
        assert record["surplus_quantity"] >= 0


def test_generate_records_holding_within_shelf_life():
    """Holding time should not exceed shelf life."""
    from src.data_generator import generate_records

    records = generate_records(num_days=7, records_per_day_per_merchant=2)

    for record in records:
        assert record["holding_time_hours"] <= record["shelf_life_hours"]


if __name__ == "__main__":
    test_generate_records_returns_list()
    test_generate_records_length()
    test_generate_records_has_required_fields()
    test_generate_records_surplus_calculation()
    test_generate_records_valid_categories()
    test_generate_records_valid_storage()
    test_generate_records_prices_positive()
    test_generate_records_quantities_non_negative()
    test_generate_records_holding_within_shelf_life()
    print("All data_generator tests passed!")
