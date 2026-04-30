#!/usr/bin/env python3
"""
Unit tests for food_safety_rules module.
Tests safety check functions: check_holding_time, check_remaining_shelf_life,
check_pickup_window, check_storage_type_appropriateness, check_preparation_time.
"""

import sys
import os
# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


def test_check_holding_time_ambient_safe():
    """Ambient holding within 4h limit should pass."""
    from src.food_safety_rules import check_holding_time

    result = check_holding_time(holding_time_hours=2.0, storage_type="Ambient")
    assert result.passed is True
    assert result.severity == "INFO"


def test_check_holding_time_ambient_caution():
    """Ambient holding approaching 4h limit (75%+) should caution."""
    from src.food_safety_rules import check_holding_time

    result = check_holding_time(holding_time_hours=3.5, storage_type="Ambient")
    assert result.severity == "CAUTION"


def test_check_holding_time_ambient_block():
    """Ambient holding exceeding 4h limit should block."""
    from src.food_safety_rules import check_holding_time

    result = check_holding_time(holding_time_hours=5.0, storage_type="Ambient")
    assert result.passed is False
    assert result.severity == "BLOCK"


def test_check_holding_time_refrigerated_safe():
    """Refrigerated holding within 8h limit should pass."""
    from src.food_safety_rules import check_holding_time

    result = check_holding_time(holding_time_hours=6.0, storage_type="Refrigerated")
    assert result.passed is True
    # 6.0 is not > 8*0.75=6.0, so it's INFO (below CAUTION threshold)
    assert result.severity == "INFO"


def test_check_remaining_shelf_life_expired():
    """Expired shelf life should block."""
    from src.food_safety_rules import check_remaining_shelf_life

    result = check_remaining_shelf_life(
        shelf_life_hours=4.0, holding_time_hours=6.0, product_category="Pastries"
    )
    assert result.passed is False
    assert result.severity == "BLOCK"


def test_check_remaining_shelf_life_insufficient():
    """Insufficient remaining shelf life should block."""
    from src.food_safety_rules import check_remaining_shelf_life

    # Pastries require 4h minimum, but only 2h remaining
    result = check_remaining_shelf_life(
        shelf_life_hours=6.0, holding_time_hours=5.0, product_category="Pastries"
    )
    assert result.passed is False
    assert result.severity == "BLOCK"


def test_check_remaining_shelf_life_adequate():
    """Sufficient remaining shelf life should pass."""
    from src.food_safety_rules import check_remaining_shelf_life

    result = check_remaining_shelf_life(
        shelf_life_hours=48.0, holding_time_hours=2.0, product_category="Pastries"
    )
    assert result.passed is True


def test_check_pickup_window_ambient_too_long():
    """Ambient pickup window exceeding 2h should block."""
    from src.food_safety_rules import check_pickup_window

    result = check_pickup_window(pickup_window_hours=3.0, storage_type="Ambient")
    assert result.passed is False
    assert result.severity == "BLOCK"


def test_check_pickup_window_ambient_ok():
    """Ambient pickup window within 2h should pass."""
    from src.food_safety_rules import check_pickup_window

    result = check_pickup_window(pickup_window_hours=1.5, storage_type="Ambient")
    assert result.passed is True


def test_check_storage_type_sandwiches_refrigerated():
    """Sandwiches require Refrigerated storage."""
    from src.food_safety_rules import check_storage_type_appropriateness

    result = check_storage_type_appropriateness(
        product_category="Sandwiches", storage_type="Refrigerated"
    )
    assert result.passed is True


def test_check_storage_type_sandwiches_ambient_warning():
    """Sandwiches should warn for Ambient storage."""
    from src.food_safety_rules import check_storage_type_appropriateness

    result = check_storage_type_appropriateness(
        product_category="Sandwiches", storage_type="Ambient"
    )
    assert result.passed is False
    assert result.severity == "CAUTION"


def test_check_preparation_time_normal():
    """Normal prep time (<60min) should pass."""
    from src.food_safety_rules import check_preparation_time

    result = check_preparation_time(product_category="Pastries", preparation_time=30)
    assert result.passed is True
    assert result.severity == "INFO"


def test_check_preparation_time_long():
    """Long prep time (>60min) should caution."""
    from src.food_safety_rules import check_preparation_time

    result = check_preparation_time(product_category="Pastries", preparation_time=90)
    assert result.severity == "CAUTION"


def test_check_item_safety_safe():
    """Fresh pastry with comfortable pickup window should be SAFE."""
    from src.food_safety_rules import check_item_safety

    # Use a 1h pickup window (well under the 2h Ambient max and below 1.4h caution threshold)
    result = check_item_safety(
        product_category="Pastries",
        preparation_time=5,
        holding_time_hours=2,
        storage_type="Ambient",
        shelf_life_hours=48,
        pickup_window_hours=1.0,  # Comfortable window
    )
    assert result.status == "SAFE"


def test_check_item_safety_caution():
    """Rice dish with tight pickup window should be CAUTION."""
    from src.food_safety_rules import check_item_safety

    # Holding time within limit but pickup window tight
    result = check_item_safety(
        product_category="Rice Dishes",
        preparation_time=20,
        holding_time_hours=3,  # Within 4h Ambient limit
        storage_type="Ambient",
        shelf_life_hours=8,
        pickup_window_hours=2,  # At the max for Ambient
    )
    # Should be CAUTION due to tight pickup window
    assert result.status == "CAUTION"


def test_check_item_safety_block():
    """Expired sandwich should be BLOCK."""
    from src.food_safety_rules import check_item_safety

    result = check_item_safety(
        product_category="Sandwiches",
        preparation_time=10,
        holding_time_hours=10,
        storage_type="Refrigerated",
        shelf_life_hours=12,
        pickup_window_hours=4,
    )
    assert result.status == "BLOCK"


def test_format_safety_display():
    """Format function should return markdown string."""
    from src.food_safety_rules import check_item_safety, format_safety_display

    result = check_item_safety(
        product_category="Pastries",
        preparation_time=5,
        holding_time_hours=2,
        storage_type="Ambient",
        shelf_life_hours=48,
        pickup_window_hours=2,
    )
    formatted = format_safety_display(result)
    assert isinstance(formatted, str)
    assert "SAFE" in formatted or "CAUTION" in formatted or "BLOCK" in formatted


if __name__ == "__main__":
    # Run tests manually for verification
    test_check_holding_time_ambient_safe()
    test_check_holding_time_ambient_caution()
    test_check_holding_time_ambient_block()
    test_check_holding_time_refrigerated_safe()
    test_check_remaining_shelf_life_expired()
    test_check_remaining_shelf_life_insufficient()
    test_check_remaining_shelf_life_adequate()
    test_check_pickup_window_ambient_too_long()
    test_check_pickup_window_ambient_ok()
    test_check_storage_type_sandwiches_refrigerated()
    test_check_storage_type_sandwiches_ambient_warning()
    test_check_preparation_time_normal()
    test_check_preparation_time_long()
    test_check_item_safety_safe()
    test_check_item_safety_caution()
    test_check_item_safety_block()
    test_format_safety_display()
    print("All food_safety_rules tests passed!")
