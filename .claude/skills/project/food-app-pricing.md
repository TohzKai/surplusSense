# Food App Pricing

SurplusSense discount recommendation and revenue recovery calculation patterns.

## Discount Tiers

### Tier Structure

Discount is determined by surplus quantity and remaining shelf life:

| Surplus Qty | Shelf Life     | Discount |
| ----------- | -------------- | -------- |
| ≤5 units    | >2h remaining  | 20%      |
| ≤5 units    | ≤2h remaining  | 30%      |
| ≤10 units   | >4h remaining  | 30%      |
| ≤10 units   | 2-4h remaining | 40%      |
| ≤10 units   | ≤2h remaining  | 50%      |
| ≤20 units   | >4h remaining  | 40%      |
| ≤20 units   | 2-4h remaining | 50%      |
| ≤20 units   | ≤2h remaining  | 60%      |
| >20 units   | >4h remaining  | 50%      |
| >20 units   | ≤2h remaining  | 70%      |

### Determining Discount

```python
from src.recommendation_engine import determine_discount_tier

discount_pct, tier_desc = determine_discount_tier(
    surplus_qty=8,
    shelf_life_hours=48,
    holding_time_hours=6,
)
# remaining_life = 48 - 6 = 42h
# 8 <= 10, 42 > 4 → 30% discount
```

## Recovery Calculation

### Formula

```python
def calculate_recovery_value(
    original_price: float,
    surplus_qty: int,
    discount_pct: float,
) -> Dict[str, float]:
    original_value = original_price * surplus_qty
    discounted_price = original_price * (1 - discount_pct)
    estimated_recovery = discounted_price * surplus_qty
    discount_amount = original_value - estimated_recovery
    recovery_rate = (estimated_recovery / original_value) * 100

    return {
        "original_value": original_value,
        "discount_amount": discount_amount,
        "discounted_price": discounted_price,
        "estimated_recovery": estimated_recovery,
        "recovery_rate": recovery_rate,
    }
```

### Example

```
Original: SGD 5.50 × 8 units = SGD 44.00
Discount: 50% → SGD 2.75 × 8 = SGD 22.00
Recovery rate: 50%
```

## Listing Time Recommendations

### Optimal Listing Hours by Category

| Category           | Optimal Lead Time  |
| ------------------ | ------------------ |
| Rice Dishes        | 4h before deadline |
| Noodle Dishes      | 4h                 |
| Bento Sets         | 5h                 |
| Sandwiches         | 5h                 |
| Coffee & Beverages | 6h                 |
| Salads             | 6h                 |
| Soup & Sides       | 6h                 |
| Pastries           | 8h                 |
| Desserts           | 8h                 |
| Tarts              | 8h                 |
| Bread              | 10h                |
| Cakes              | 12h                |
| Cookies            | 24h                |

### Listing Time Logic

```python
def determine_listing_time(category, shelf_life_hours, holding_time_hours):
    remaining_shelf = shelf_life_hours - holding_time_hours

    if remaining_shelf <= 2:
        return "Immediately"  # Critical
    elif remaining_shelf <= optimal_lead_time:
        return "ASAP"  # Limited time
    else:
        return recommended_time  # Calculate based on optimal lead time
```

## Pickup Windows

### Maximum Pickup Windows by Storage

| Storage Type | Max Pickup Window |
| ------------ | ----------------- |
| Ambient      | 4 hours           |
| Refrigerated | 8 hours           |
| Frozen       | 24 hours          |

### Recommended Pickup Calculation

```python
def determine_listing_time(...):
    # Latest pickup is 80% of remaining shelf life, capped at storage max
    latest_pickup_hours = min(
        MAX_PICKUP_WINDOW.get(storage_type, 8),
        remaining_shelf * 0.8
    )
```

## Category Emoji

```python
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
```

## Full Recommendation Example

```python
from src.recommendation_engine import generate_recommendation

rec = generate_recommendation(
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
)
# Returns full recommendation dict
```

## Output Structure

```python
{
    "merchant_id": "CAF001",
    "merchant_type": "Café",
    "product_category": "Pastries",
    "product_name": "Croissant",
    "original_price": 5.50,
    "predicted_surplus": 8.0,
    "recommended_discount_pct": 0.50,
    "discounted_price": 2.75,
    "recommended_listing_time": "ASAP",
    "recommended_pickup_window": "4 hours",
    "latest_pickup_time": "4h from now",
    "estimated_merchant_recovery": 22.00,
    "original_value": 44.00,
    "recovery_rate_pct": 50.0,
    "safety_status": "CAUTION",
    "safety_flags": [...],
    "recommendation_explanation": "...",
}
```
