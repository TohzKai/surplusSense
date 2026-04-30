#!/usr/bin/env python3
"""
SurplusSense Recommendation Engine
==================================
Rule-based discount recommendation engine for surplus items.

Outputs:
- predicted_surplus: ML-predicted surplus quantity
- recommended_discount_pct: discount percentage to recommend
- recommended_listing_time: when to list the item
- recommended_pickup_window: pickup window for consumers
- estimated_recovery: estimated revenue recovery
- recommendation_explanation: human-readable explanation
- safety_status: whether item is safe to list
"""

import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta


def _round_surplus(value: float) -> float:
    """Round surplus to 1 decimal place using exact decimal arithmetic.

    Avoids floating-point artifacts like round(7.184..., 1) → 7.1999...
    Also handles numpy scalar types (np.float32, np.float64) correctly by
    converting to Python float before Decimal(), which prevents str()-truncation
    artifacts from numpy's string representation of float32 values.
    """
    d = Decimal(str(float(value)))
    return float(d.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

# Discount tiers based on surplus quantity and remaining shelf life
# STRICTEST time limits first within each surplus bucket (remaining <= 0 before <= 2 before <= 4)
DISCOUNT_TIERS = [
    # (max_surplus_qty, min_shelflife_hours, discount_pct)
    # Small surplus (surplus <= 5): stricter time limits first
    (5, 0, 0.30),   # Small surplus, at limit (0h) -> 30% off
    (5, 2, 0.20),   # Small surplus, time pressure (≤2h) -> 20% off
    # Medium surplus (5 < surplus <= 10): stricter time limits first
    (10, 0, 0.50),  # Medium surplus, at limit (0h) -> 50% off
    (10, 2, 0.40),  # Medium surplus, time pressure (≤2h) -> 40% off
    (10, 4, 0.30),  # Medium surplus, good time (≤4h) -> 30% off
    # Large surplus (10 < surplus <= 20): stricter time limits first
    (20, 0, 0.60),  # Large surplus, at limit (0h) -> 60% off
    (20, 2, 0.50),  # Large surplus, time pressure (≤2h) -> 50% off
    (20, 4, 0.40),  # Large surplus, good time (≤4h) -> 40% off
    # Very large surplus (surplus > 20): stricter time limits first
    (999, 0, 0.70), # Very large surplus, at limit (0h) -> 70% off
    (999, 4, 0.50), # Very large surplus, good time (≤4h) -> 50% off
]

# Maximum pickup windows by storage type (hours)
MAX_PICKUP_WINDOW = {
    "Ambient": 4,
    "Refrigerated": 8,
    "Frozen": 24,
}

# Optimal listing times by product category (hours before end of day)
OPTIMAL_LISTING_HOURS = {
    "Coffee & Beverages": 6,
    "Pastries": 8,
    "Sandwiches": 5,
    "Salads": 6,
    "Desserts": 8,
    "Bread": 10,
    "Cakes": 12,
    "Cookies": 24,
    "Tarts": 8,
    "Rice Dishes": 4,
    "Noodle Dishes": 4,
    "Bento Sets": 5,
    "Soup & Sides": 6,
}

# Category emoji for display
CATEGORY_EMOJI = {
    "Coffee & Beverages": "☕",
    "Pastries": "🥐",
    "Sandwiches": "🥪",
    "Salads": "🥗",
    "Desserts": "🍰",
    "Bread": "🍞",
    "Cakes": "🎂",
    "Cookies": "🍪",
    "Tarts": "🥧",
    "Rice Dishes": "🍚",
    "Noodle Dishes": "🍜",
    "Bento Sets": "🍱",
    "Soup & Sides": "🍲",
}


def determine_discount_tier(
    surplus_qty: int,
    shelf_life_hours: float,
    holding_time_hours: float,
) -> Tuple[float, str]:
    """
    Determine appropriate discount tier based on surplus quantity and time pressure.

    Time pressure is measured by remaining shelf life ratio:
    remaining_shelf_life = shelf_life_hours - holding_time_hours

    Returns:
        (discount_percentage, tier_description)
    """
    remaining_life = shelf_life_hours - holding_time_hours

    for max_qty, min_life_hours, discount in DISCOUNT_TIERS:
        if surplus_qty <= max_qty and remaining_life <= min_life_hours:
            # Find the best matching tier
            return discount, f"Surplus: {surplus_qty} units, Remaining shelf life: {remaining_life:.1f}h"

    # Default to highest reasonable discount
    return 0.50, f"Surplus: {surplus_qty} units, Standard discount applied"


def calculate_recovery_value(
    original_price: float,
    surplus_qty: int,
    discount_pct: float,
) -> Dict[str, float]:
    """
    Calculate revenue recovery from discount strategy.

    Returns:
        Dict with original_value, discount_amount, estimated_recovery
    """
    original_value = original_price * surplus_qty
    discounted_price = original_price * (1 - discount_pct)
    estimated_recovery = discounted_price * surplus_qty
    discount_amount = original_value - estimated_recovery

    return {
        "original_value": round(original_value, 2),
        "discount_amount": round(discount_amount, 2),
        "discounted_price": round(discounted_price, 2),
        "estimated_recovery": round(estimated_recovery, 2),
        "recovery_rate": round(estimated_recovery / original_value * 100, 1) if original_value > 0 else 0,
    }


def determine_listing_time(
    category: str,
    shelf_life_hours: float,
    holding_time_hours: float,
    current_time: str = "10:00",
) -> Dict[str, Any]:
    """
    Determine optimal listing time for surplus item.

    Returns:
        Dict with recommended_time, latest_pickup, and reason
    """
    # Parse current time
    current_hour, current_min = map(int, current_time.split(":"))
    current_total_minutes = current_hour * 60 + current_min

    # Calculate optimal listing lead time
    optimal_lead_time = OPTIMAL_LISTING_HOURS.get(category, 6)
    remaining_shelf = shelf_life_hours - holding_time_hours

    # If shelf life is low, recommend immediate listing
    if remaining_shelf <= 2:
        recommended_time = "Immediately"
        reason = f"Critical shelf life ({remaining_shelf:.1f}h remaining) - list now"
    elif remaining_shelf <= optimal_lead_time:
        recommended_time = "ASAP"
        reason = f"Limited shelf life ({remaining_shelf:.1f}h remaining) - list within {remaining_shelf:.0f}h"
    else:
        # Calculate actual time
        optimal_minutes = optimal_lead_time * 60
        recommended_dt = datetime.now() + timedelta(minutes=optimal_minutes)
        recommended_time = recommended_dt.strftime("%H:%M")
        reason = f"Optimal listing {optimal_lead_time}h before pickup deadline"

    # Calculate latest pickup time
    latest_pickup_hours = min(MAX_PICKUP_WINDOW.get("Refrigerated", 8), remaining_shelf * 0.8)
    latest_pickup = f"{latest_pickup_hours:.0f}h from now"

    return {
        "recommended_time": recommended_time,
        "latest_pickup": latest_pickup,
        "reason": reason,
        "pickup_window_hours": latest_pickup_hours,
    }


def generate_recommendation(
    merchant_id: str,
    merchant_type: str,
    product_category: str,
    product_name: str,
    original_price: float,
    predicted_surplus: float,
    shelf_life_hours: float,
    preparation_time: int,
    storage_type: str,
    holding_time_hours: float,
    current_time: str = "10:00",
    safety_status: str = "SAFE",
    safety_flags: list = None,
) -> Dict[str, Any]:
    """
    Generate complete recommendation for a surplus item.

    Parameters:
        merchant_id: Merchant identifier
        merchant_type: Type of merchant (Café, Bakery, Small F&B)
        product_category: Product category
        product_name: Product name
        original_price: Original price in SGD
        predicted_surplus: ML-predicted surplus quantity
        shelf_life_hours: Total shelf life in hours
        preparation_time: Prep time in minutes
        storage_type: Storage condition (Ambient/Refrigerated/Frozen)
        holding_time_hours: Hours already held
        current_time: Current time (HH:MM format)
        safety_status: Safety check result
        safety_flags: List of safety warnings

    Returns:
        Dict with all recommendation details
    """
    if safety_flags is None:
        safety_flags = []

    # Normalize to 1 decimal place — all downstream text/calculations use this value
    # Use decimal arithmetic to avoid float artifacts (round(7.184..., 1) → 7.1999...)
    predicted_surplus = _round_surplus(predicted_surplus)

    # Determine discount
    discount_pct, tier_desc = determine_discount_tier(
        predicted_surplus, shelf_life_hours, holding_time_hours
    )

    # Calculate recovery
    recovery = calculate_recovery_value(original_price, predicted_surplus, discount_pct)

    # Determine listing time
    listing = determine_listing_time(
        product_category, shelf_life_hours, holding_time_hours, current_time
    )

    # Build recommendation explanation
    emoji = CATEGORY_EMOJI.get(product_category, "🍽️")

    explanation_parts = [
        f"{emoji} **{product_name}** at {merchant_id}",
        f"Predicted surplus: **{predicted_surplus:.0f} units**",
        f"Recommended discount: **{discount_pct*100:.0f}%** ({tier_desc})",
        f"Estimated recovery: **SGD {recovery['estimated_recovery']:.2f}** "
        f"(vs potential loss of SGD {recovery['original_value']:.2f})",
        f"Listing time: **{listing['recommended_time']}** - {listing['reason']}",
        f"Pickup window: **{listing['latest_pickup']}**",
    ]

    if safety_flags:
        explanation_parts.append(f"\n⚠️ Safety flags: {', '.join(safety_flags)}")

    recommendation = {
        "merchant_id": merchant_id,
        "merchant_type": merchant_type,
        "product_category": product_category,
        "product_name": product_name,
        "original_price": original_price,
        "predicted_surplus": round(predicted_surplus, 1),
        "recommended_discount_pct": discount_pct,
        "discounted_price": recovery["discounted_price"],
        "recommended_listing_time": listing["recommended_time"],
        "recommended_pickup_window": f"{listing['pickup_window_hours']:.0f} hours",
        "latest_pickup_time": listing["latest_pickup"],
        "estimated_merchant_recovery": recovery["estimated_recovery"],
        "original_value": recovery["original_value"],
        "recovery_rate_pct": recovery["recovery_rate"],
        "safety_status": safety_status,
        "safety_flags": safety_flags,
        "recommendation_explanation": "\n".join(explanation_parts),
        "tier_description": tier_desc,
    }

    return recommendation


def generate_batch_recommendations(
    df: pd.DataFrame,
    model,
    feature_names: list,
    current_time: str = "10:00",
) -> pd.DataFrame:
    """
    Generate recommendations for a batch of items.

    Parameters:
        df: DataFrame with engineered features
        model: Trained Random Forest model
        feature_names: List of feature names
        current_time: Current time

    Returns:
        DataFrame with recommendations
    """
    from src.food_safety_rules import check_item_safety

    recommendations = []

    # Get encoded features
    df_pred = df.copy()
    categorical_cols = ["product_category", "merchant_type", "storage_type"]
    for col in categorical_cols:
        if col in df_pred.columns:
            dummies = pd.get_dummies(df_pred[col], prefix=col)
            df_pred = pd.concat([df_pred, dummies], axis=1)

    # Ensure all feature columns exist
    X = df_pred[[c for c in feature_names if c in df_pred.columns]].fillna(0)

    # Predict surplus
    predictions = model.predict(X)

    # Generate recommendation for each row
    for idx, row in df.iterrows():
        if idx >= len(predictions):
            break

        pred_surplus = max(0, predictions[idx - df.index[0]] if idx >= df.index[0] else predictions[idx])

        # Check safety
        safety_result = check_item_safety(
            product_category=row.get("product_category", ""),
            preparation_time=row.get("preparation_time", 0),
            holding_time_hours=row.get("holding_time_hours", 0),
            storage_type=row.get("storage_type", "Ambient"),
            shelf_life_hours=row.get("shelf_life_hours", 24),
        )

        rec = generate_recommendation(
            merchant_id=row.get("merchant_id", ""),
            merchant_type=row.get("merchant_type", ""),
            product_category=row.get("product_category", ""),
            product_name=row.get("product_name", ""),
            original_price=row.get("original_price", 0),
            predicted_surplus=pred_surplus,
            shelf_life_hours=row.get("shelf_life_hours", 24),
            preparation_time=row.get("preparation_time", 0),
            storage_type=row.get("storage_type", "Ambient"),
            holding_time_hours=row.get("holding_time_hours", 0),
            current_time=current_time,
            safety_status=safety_result["status"],
            safety_flags=safety_result["flags"],
        )

        recommendations.append(rec)

    return pd.DataFrame(recommendations)


# Cold-start: cluster centroid lookup (synthetic data structure)
# In real deployment, sub-cluster variation within merchant types would be more informative.
# Merchant type is used as a proxy for cluster assignment during cold-start.
_CLUSTER_CENTROIDS = {
    0: {"avg_daily_production": 90.35, "avg_daily_surplus": 11.13, "avg_surplus_ratio": 0.1247,
        "surplus_std": 4.06, "median_shelf_life": 27.55, "weekend_surplus_ratio": 1.2144},
    1: {"avg_daily_production": 141.0, "avg_daily_surplus": 24.80, "avg_surplus_ratio": 0.1778,
        "surplus_std": 8.23, "median_shelf_life": 66.8, "weekend_surplus_ratio": 1.071},
    2: {"avg_daily_production": 119.30, "avg_daily_surplus": 17.92, "avg_surplus_ratio": 0.1509,
        "surplus_std": 6.03, "median_shelf_life": 16.45, "weekend_surplus_ratio": 1.1426},
}

_CLUSTER_NAMES = {
    0: "Weekend-Surge, Lean Operations",
    1: "High-Volume, Predictable Surplus",
    2: "Mid-Volume, Fast-Paced Perishable",
}

# Mapping derived from synthetic data clustering.
# In real data this mapping would be learned from actual merchant patterns.
_MERCHANT_TYPE_CLUSTER = {
    "Café": 0,
    "Bakery": 1,
    "Small F&B": 2,
}


def predict_surplus_cold_start(
    merchant_type: str,
    product_category: str,
    avg_daily_production: Optional[float] = None,
    dominant_storage: str = "Refrigerated",
    is_weekend: bool = False,
) -> Dict[str, Any]:
    """
    Cold-start surplus prediction for merchants without historical data.

    Assigns the merchant to the nearest operational cluster based on merchant_type
    (derived from synthetic data clustering; in real data, sub-cluster variation
    within types would be more informative). Returns a cluster-centroid-based
    starter prediction labeled as a 'starter estimate'.

    Parameters:
        merchant_type: Café | Bakery | Small F&B
        product_category: Product category for category-level adjustment
        avg_daily_production: Known average daily production (optional; uses cluster
            centroid production if not provided)
        dominant_storage: Storage type (Refrigerated / Ambient / Frozen)
        is_weekend: Whether the prediction is for a weekend day

    Returns:
        Dict with starter surplus prediction and confidence metadata
    """
    cluster_id = _MERCHANT_TYPE_CLUSTER.get(merchant_type, 0)
    centroid = _CLUSTER_CENTROIDS[cluster_id]

    # Base prediction: use provided production or centroid production
    base_production = avg_daily_production if avg_daily_production is not None else centroid["avg_daily_production"]
    base_surplus = base_production * centroid["avg_surplus_ratio"]

    # Weekend adjustment
    weekend_multiplier = centroid["weekend_surplus_ratio"] if is_weekend else 1.0
    predicted_surplus = base_surplus * weekend_multiplier

    cluster_name = _CLUSTER_NAMES[cluster_id]

    return {
        "predicted_surplus": round(predicted_surplus, 1),
        "surplus_ratio_used": centroid["avg_surplus_ratio"],
        "production_used": round(base_production, 1),
        "weekend_adjustment": round(weekend_multiplier, 3),
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "confidence_label": "starter estimate",
        "cold_start_note": (
            "Based on cluster-centroid surplus ratio calibrated against merchants "
            "with similar operating patterns. Refines as merchant-specific data accumulates."
        ),
        "synthetic_data_note": (
            "Cluster assignments derived from synthetic training data. "
            "In real data, sub-cluster variation within merchant types would be more informative."
        ),
    }


if __name__ == "__main__":
    # Test recommendation engine
    print("Testing recommendation engine...")

    test_rec = generate_recommendation(
        merchant_id="CAF001",
        merchant_type="Café",
        product_category="Pastries",
        product_name="Croissant",
        original_price=5.50,
        predicted_surplus=8,
        shelf_life_hours=48,
        preparation_time=5,
        storage_type="Ambient",
        holding_time_hours=6,
        current_time="10:00",
    )

    print("\n" + "=" * 60)
    print("Sample Recommendation")
    print("=" * 60)
    for key, value in test_rec.items():
        if key != "recommendation_explanation":
            print(f"{key}: {value}")

    print("\n" + test_rec["recommendation_explanation"])
