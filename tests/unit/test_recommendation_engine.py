#!/usr/bin/env python3
"""
Unit tests for recommendation_engine module.
Tests discount tier determination, recovery calculation, and recommendation generation.
"""

import sys
import os
# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


def test_determine_discount_tier_small_surplus_time_pressure():
    """Small surplus with time pressure = 20% discount."""
    from src.recommendation_engine import determine_discount_tier

    # Small surplus (3) with 1h remaining (critical time pressure)
    # Tier: (5, 2, 0.20) means surplus<=5 AND remaining<=2h → 20%
    discount, desc = determine_discount_tier(
        surplus_qty=3, shelf_life_hours=5, holding_time_hours=4
    )
    assert discount == 0.20


def test_determine_discount_tier_small_surplus_low_time():
    """Small surplus with very low shelf life = 30% discount."""
    from src.recommendation_engine import determine_discount_tier

    # Small surplus (3), remaining=0h (at limit)
    discount, desc = determine_discount_tier(
        surplus_qty=3, shelf_life_hours=3, holding_time_hours=3
    )
    assert discount == 0.30


def test_determine_discount_tier_medium_surplus_good_time():
    """Medium surplus with no time pressure = 50% discount (default)."""
    from src.recommendation_engine import determine_discount_tier

    # Medium surplus (8) with plenty of time (46h remaining)
    discount, desc = determine_discount_tier(
        surplus_qty=8, shelf_life_hours=48, holding_time_hours=2
    )
    # Falls to default 50% when no time pressure
    assert discount == 0.50


def test_determine_discount_tier_medium_surplus_time_pressure():
    """Medium surplus with time pressure = 40% discount."""
    from src.recommendation_engine import determine_discount_tier

    # Medium surplus (8), remaining=2h (at pressure threshold)
    discount, desc = determine_discount_tier(
        surplus_qty=8, shelf_life_hours=6, holding_time_hours=4
    )
    assert discount == 0.40


def test_determine_discount_tier_large_surplus():
    """Large surplus with time pressure = 50% discount."""
    from src.recommendation_engine import determine_discount_tier

    # Large surplus (15), remaining=2h (at pressure threshold)
    discount, desc = determine_discount_tier(
        surplus_qty=15, shelf_life_hours=6, holding_time_hours=4
    )
    assert discount == 0.50


def test_calculate_recovery_value():
    """Test revenue recovery calculation."""
    from src.recommendation_engine import calculate_recovery_value

    result = calculate_recovery_value(
        original_price=5.50, surplus_qty=8, discount_pct=0.50
    )
    assert result["original_value"] == 44.00
    assert result["discounted_price"] == 2.75
    assert result["estimated_recovery"] == 22.00
    assert result["recovery_rate"] == 50.0


def test_calculate_recovery_value_no_discount():
    """No discount = full recovery."""
    from src.recommendation_engine import calculate_recovery_value

    result = calculate_recovery_value(
        original_price=10.00, surplus_qty=5, discount_pct=0.0
    )
    assert result["original_value"] == 50.00
    assert result["estimated_recovery"] == 50.00
    assert result["recovery_rate"] == 100.0


def test_calculate_recovery_value_zero_price():
    """Zero original price should not divide by zero."""
    from src.recommendation_engine import calculate_recovery_value

    result = calculate_recovery_value(
        original_price=0.0, surplus_qty=5, discount_pct=0.0
    )
    assert result["recovery_rate"] == 0


def test_determine_listing_time_immediate():
    """Critical shelf life should list immediately."""
    from src.recommendation_engine import determine_listing_time

    result = determine_listing_time(
        category="Rice Dishes",
        shelf_life_hours=4,
        holding_time_hours=3,
    )
    assert result["recommended_time"] == "Immediately"


def test_determine_listing_time_asap():
    """Limited shelf life should list ASAP."""
    from src.recommendation_engine import determine_listing_time

    # remaining_shelf = 6 - 3 = 3h, which is <= 8 (Pastries optimal lead)
    # but > 2, so it returns ASAP not Immediately
    result = determine_listing_time(
        category="Pastries",
        shelf_life_hours=6,
        holding_time_hours=3,
    )
    assert result["recommended_time"] == "ASAP"


def test_generate_recommendation_returns_dict():
    """generate_recommendation should return a complete dict."""
    from src.recommendation_engine import generate_recommendation

    rec = generate_recommendation(
        merchant_id="TEST001",
        merchant_type="Bakery",
        product_category="Pastries",
        product_name="Croissant",
        original_price=5.50,
        predicted_surplus=8,
        shelf_life_hours=48,
        preparation_time=5,
        storage_type="Ambient",
        holding_time_hours=6,
    )

    # Check required keys exist
    assert "merchant_id" in rec
    assert "product_category" in rec
    assert "recommended_discount_pct" in rec
    assert "discounted_price" in rec
    assert "estimated_merchant_recovery" in rec
    assert "safety_status" in rec
    assert "recommendation_explanation" in rec


def test_generate_recommendation_discount_values():
    """Verify discount calculation in recommendation."""
    from src.recommendation_engine import generate_recommendation

    rec = generate_recommendation(
        merchant_id="TEST001",
        merchant_type="Bakery",
        product_category="Pastries",
        product_name="Croissant",
        original_price=5.50,
        predicted_surplus=8,
        shelf_life_hours=48,
        preparation_time=5,
        storage_type="Ambient",
        holding_time_hours=6,
    )

    # Verify discounted price calculation
    expected_discounted = 5.50 * (1 - rec["recommended_discount_pct"])
    assert abs(rec["discounted_price"] - expected_discounted) < 0.01


def test_category_emoji_mapping():
    """Verify category emoji constants exist."""
    from src.recommendation_engine import CATEGORY_EMOJI

    assert "Pastries" in CATEGORY_EMOJI
    assert "Rice Dishes" in CATEGORY_EMOJI
    assert "Coffee & Beverages" in CATEGORY_EMOJI


def test_discount_tiers_complete():
    """All major surplus scenarios should have a discount tier."""
    from src.recommendation_engine import determine_discount_tier

    test_cases = [
        (3, 48, 2),  # Small, plenty
        (3, 4, 2),   # Small, low
        (8, 48, 2),  # Medium, plenty
        (8, 6, 4),   # Medium, pressure
        (15, 48, 2), # Large, plenty
        (15, 4, 2),  # Large, critical
        (25, 48, 2), # Very large, plenty
        (25, 4, 2),  # Very large, critical
    ]

    for surplus, shelf, holding in test_cases:
        discount, desc = determine_discount_tier(surplus, shelf, holding)
        assert 0.20 <= discount <= 0.70, f"Discount {discount} out of range for case {surplus},{shelf},{holding}"


if __name__ == "__main__":
    test_determine_discount_tier_small_surplus_time_pressure()
    test_determine_discount_tier_small_surplus_low_time()
    test_determine_discount_tier_medium_surplus_good_time()
    test_determine_discount_tier_medium_surplus_time_pressure()
    test_determine_discount_tier_large_surplus()
    test_calculate_recovery_value()
    test_calculate_recovery_value_no_discount()
    test_calculate_recovery_value_zero_price()
    test_determine_listing_time_immediate()
    test_determine_listing_time_asap()
    test_generate_recommendation_returns_dict()
    test_generate_recommendation_discount_values()
    test_category_emoji_mapping()
    test_discount_tiers_complete()
    print("All recommendation_engine tests passed!")
