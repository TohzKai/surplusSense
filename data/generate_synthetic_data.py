#!/usr/bin/env python3
"""
SurplusSense Synthetic F&B Data Generator
==========================================
Generates realistic synthetic data for cafés, bakeries, and small F&B operators.
Used for MVP demonstration of the ML pipeline and decision-support workflow.

NOTE: This data is SYNTHETIC and does not represent real merchant transactions.
It is designed to demonstrate the ML pipeline, feature logic, evaluation approach,
and decision-support workflow in a controlled environment.
"""

import random
import hashlib
from datetime import datetime, timedelta
import csv
from typing import List, Dict, Any

# Seed for reproducibility (can be changed for different datasets)
RANDOM_SEED = 42

# Merchant configurations for MVP beachhead segment
MERCHANTS = {
    "Café": {
        "merchant_ids": ["CAF001", "CAF002", "CAF003", "CAF004", "CAF005"],
        "product_categories": ["Coffee & Beverages", "Pastries", "Sandwiches", "Salads", "Desserts"],
        "products": {
            "Coffee & Beverages": ["Cappuccino", "Latte", "Americano", "Matcha Latte", "Cold Brew"],
            "Pastries": ["Croissant", "Almond Croissant", "Blueberry Muffin", "Cinnamon Roll", "Banana Bread"],
            "Sandwiches": ["Turkey Sandwich", "Chicken Avocado Wrap", "Veggie Panini", "Tuna Melt", "BLT"],
            "Salads": ["Caesar Salad", "Greek Salad", "Chicken Grain Bowl", "Quinoa Power Bowl", "Garden Fresh"],
            "Desserts": ["Tiramisu", "Cheesecake", "Chocolate Cake", "Carrot Cake", "Brownie"],
        },
        "base_surplus_rate": 0.12,
        "weekend_surplus_multiplier": 1.3,
    },
    "Bakery": {
        "merchant_ids": ["BAK001", "BAK002", "BAK003", "BAK004", "BAK005"],
        "product_categories": ["Bread", "Pastries", "Cakes", "Cookies", "Tarts"],
        "products": {
            "Bread": ["Sourdough Loaf", "Whole Wheat Loaf", "Baguette", "Ciabatta", "Focaccia"],
            "Pastries": ["Pain au Chocolat", "Danish Pastry", "Apple Turnover", "Cheese Danish", "Almond Twist"],
            "Cakes": ["Victoria Sponge", "Carrot Cake", "Lemon Drizzle", "Chocolate Fudge", "Coffee Cake"],
            "Cookies": ["Chocolate Chip", "Oatmeal Raisin", "Double Chocolate", "White Choc Macadamia", "Snickerdoodle"],
            "Tarts": ["Fruit Tart", "Lemon Tart", "Pecan Tart", "Chocolate Tart", "Bakewell Tart"],
        },
        "base_surplus_rate": 0.18,
        "weekend_surplus_multiplier": 1.1,
    },
    "Small F&B": {
        "merchant_ids": ["FNB001", "FNB002", "FNB003", "FNB004", "FNB005"],
        "product_categories": ["Rice Dishes", "Noodle Dishes", "Bento Sets", "Soup & Sides", "Desserts"],
        "products": {
            "Rice Dishes": ["Hainanese Chicken Rice", "Teriyaki Don", "Curry Rice", "Fried Rice", "Bibimbap"],
            "Noodle Dishes": ["Laksa", "Wanton Noodles", "Pad Thai", "Beef Noodles", "Miso Ramen"],
            "Bento Sets": ["Teriyaki Bento", "Tempura Bento", "Katsu Don", "Yakitori Set", "Sushi Set"],
            "Soup & Sides": ["Miso Soup", "Edamame", "Gyoza", "Takoyaki", "Korokke"],
            "Desserts": ["Mochi Ice Cream", "Dorayaki", "Taiyaki", "Matcha Parfait", "Red Bean Soup"],
        },
        "base_surplus_rate": 0.15,
        "weekend_surplus_multiplier": 1.2,
    },
}

# Realistic price ranges (SGD)
PRICE_RANGES = {
    "Coffee & Beverages": (4.50, 8.00),
    "Pastries": (3.50, 7.50),
    "Sandwiches": (7.00, 12.00),
    "Salads": (9.00, 14.00),
    "Desserts": (6.00, 12.00),
    "Bread": (4.00, 9.00),
    "Cakes": (7.00, 15.00),
    "Cookies": (2.50, 5.00),
    "Tarts": (4.50, 8.50),
    "Rice Dishes": (8.00, 15.00),
    "Noodle Dishes": (9.00, 16.00),
    "Bento Sets": (12.00, 20.00),
    "Soup & Sides": (4.00, 8.00),
}

# Storage types and their characteristics
STORAGE_TYPES = ["Ambient", "Refrigerated", "Frozen"]
STORAGE_PROBS = [0.3, 0.5, 0.2]

# Shelf life ranges (hours) by category type
SHELF_LIFE_RANGES = {
    "Coffee & Beverages": (4, 8),
    "Pastries": (24, 72),
    "Sandwiches": (6, 24),
    "Salads": (12, 48),
    "Desserts": (24, 72),
    "Bread": (24, 96),
    "Cakes": (48, 120),
    "Cookies": (168, 336),  # 1-2 weeks
    "Tarts": (24, 72),
    "Rice Dishes": (4, 12),
    "Noodle Dishes": (4, 12),
    "Bento Sets": (6, 24),
    "Soup & Sides": (12, 48),
}

# Preparation time ranges (minutes)
PREP_TIME_RANGES = {
    "Coffee & Beverages": (2, 5),
    "Pastries": (0, 5),  # Pre-made
    "Sandwiches": (5, 15),
    "Salads": (8, 20),
    "Desserts": (10, 30),
    "Bread": (0, 10),
    "Cakes": (15, 45),
    "Cookies": (5, 15),
    "Tarts": (10, 25),
    "Rice Dishes": (15, 30),
    "Noodle Dishes": (10, 25),
    "Bento Sets": (20, 40),
    "Soup & Sides": (5, 15),
}

# Promotion patterns (higher on weekends, some weekday specials)
PROMOTION_PROB_BASE = 0.08
PROMOTION_PROB_WEEKEND = 0.25

# Production quantities by merchant type
PRODUCTION_QUANTITY_RANGES = {
    "Café": (10, 50),
    "Bakery": (15, 80),
    "Small F&B": (20, 60),
}


def get_day_characteristics(date: datetime) -> Dict[str, Any]:
    """Calculate day characteristics for realistic surplus patterns."""
    day_of_week = date.weekday()
    is_weekend = day_of_week >= 5

    # Singapore F&B patterns
    # Weekends have different consumption patterns
    if day_of_week == 6:  # Sunday
        pattern = "sunday"
        base_demand = 0.85
    elif day_of_week == 5:  # Saturday
        pattern = "saturday"
        base_demand = 0.90
    elif day_of_week in [0, 4]:  # Monday, Friday - lighter
        pattern = "transition"
        base_demand = 0.95
    else:  # Tuesday, Wednesday, Thursday - steady
        pattern = "midweek"
        base_demand = 1.0

    # Special events (simplified - public holidays, festive periods)
    # In production, this would be calendar-based
    is_holiday_period = False  # Simplified

    return {
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "pattern": pattern,
        "base_demand": base_demand,
        "is_holiday_period": is_holiday_period,
    }


def calculate_surplus(
    production_qty: int,
    day_char: Dict[str, Any],
    merchant_type: str,
    category: str,
    promotion_flag: bool,
    prev_day_surplus: int = None,
    same_weekday_prev_surplus: int = None,
) -> int:
    """Calculate realistic surplus based on operating conditions."""
    base_rate = MERCHANTS[merchant_type]["base_surplus_rate"]
    weekend_mult = MERCHANTS[merchant_type]["weekend_surplus_multiplier"]

    # Adjust surplus rate based on conditions
    adjusted_rate = base_rate

    # Weekend effect
    if day_char["is_weekend"]:
        adjusted_rate *= weekend_mult

    # Midweek dip
    if day_char["pattern"] == "midweek":
        adjusted_rate *= 0.95

    # Promotion reduces surplus (increases sales)
    if promotion_flag:
        adjusted_rate *= 0.75

    # Add some noise
    noise = random.gauss(1.0, 0.1)
    adjusted_rate *= max(0.5, min(1.5, noise))  # Clamp to reasonable range

    # Calculate base surplus
    base_surplus = production_qty * adjusted_rate

    # If we have historical data, add some correlation
    if prev_day_surplus is not None:
        base_surplus = 0.6 * base_surplus + 0.3 * prev_day_surplus + 0.1 * random.gauss(production_qty * base_rate, 2)

    # Ensure non-negative and reasonable
    surplus = max(0, round(base_surplus))
    surplus = min(surplus, production_qty)  # Can't surplus more than produced

    return surplus


def generate_records(
    num_days: int = 90,
    records_per_day_per_merchant: int = 3,
) -> List[Dict[str, Any]]:
    """Generate synthetic F&B surplus records."""
    random.seed(RANDOM_SEED)

    records = []
    start_date = datetime(2026, 1, 6)  # Start from a Monday
    merchant_types = list(MERCHANTS.keys())

    # Historical surplus tracking for baselines
    surplus_history: Dict[str, List[int]] = {}  # merchant_id -> list of daily surpluses

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        day_char = get_day_characteristics(current_date)

        # Generate records for each merchant
        for merchant_type in merchant_types:
            merchant_config = MERCHANTS[merchant_type]

            for merchant_id in merchant_config["merchant_ids"]:
                # Initialize surplus history if needed
                if merchant_id not in surplus_history:
                    surplus_history[merchant_id] = []

                # Determine how many products for this merchant today
                num_products = random.randint(
                    records_per_day_per_merchant - 1,
                    records_per_day_per_merchant + 1,
                )

                # Select random categories for this merchant
                categories = random.sample(
                    merchant_config["product_categories"],
                    min(num_products, len(merchant_config["product_categories"])),
                )

                for category in categories:
                    # Select a product from this category
                    product = random.choice(merchant_config["products"][category])

                    # Determine price
                    price_min, price_max = PRICE_RANGES.get(category, (5.0, 15.0))
                    original_price = round(random.uniform(price_min, price_max), 2)

                    # Determine production quantity
                    qty_min, qty_max = PRODUCTION_QUANTITY_RANGES[merchant_type]
                    production_quantity = random.randint(qty_min, qty_max)

                    # Promotion flag
                    promo_prob = (
                        PROMOTION_PROB_WEEKEND
                        if day_char["is_weekend"]
                        else PROMOTION_PROB_BASE
                    )
                    promotion_flag = random.random() < promo_prob

                    # Storage type
                    storage_type = random.choices(STORAGE_TYPES, weights=STORAGE_PROBS)[0]

                    # Shelf life
                    shelf_min, shelf_max = SHELF_LIFE_RANGES.get(category, (24, 72))
                    shelf_life_hours = random.randint(shelf_min, shelf_max)

                    # Preparation time
                    prep_min, prep_max = PREP_TIME_RANGES.get(category, (5, 20))
                    preparation_time = random.randint(prep_min, prep_max)

                    # Current time (when decision is made - morning for most items)
                    # Simulate decision time between 6 AM and 10 AM
                    hour = random.choices(
                        [6, 7, 8, 9, 10],
                        weights=[0.15, 0.25, 0.30, 0.20, 0.10],
                    )[0]
                    current_time = current_date.replace(
                        hour=hour, minute=random.randint(0, 59), second=0
                    )

                    # Calculate holding time (hours since production)
                    # Assume production was 2-4 hours before decision time
                    holding_time_hours = round(random.uniform(1.0, 4.0), 1)

                    # Get previous day surplus for this merchant
                    prev_day_surplus = None
                    same_weekday_prev_surplus = None

                    if len(surplus_history[merchant_id]) >= 1:
                        prev_day_surplus = surplus_history[merchant_id][-1]

                    # Same weekday last week (7 days back)
                    history_len = len(surplus_history[merchant_id])
                    if history_len >= 7:
                        same_weekday_prev_surplus = surplus_history[merchant_id][-7]

                    # Calculate surplus
                    sold_quantity = production_quantity  # Start with no surplus assumption

                    surplus_quantity = calculate_surplus(
                        production_quantity,
                        day_char,
                        merchant_type,
                        category,
                        promotion_flag,
                        prev_day_surplus,
                        same_weekday_prev_surplus,
                    )

                    # Sold is production minus surplus
                    sold_quantity = production_quantity - surplus_quantity

                    # Create record
                    record = {
                        "merchant_id": merchant_id,
                        "merchant_type": merchant_type,
                        "product_category": category,
                        "product_name": product,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "day_of_week": day_char["day_of_week"],
                        "weekend_flag": 1 if day_char["is_weekend"] else 0,
                        "promotion_flag": 1 if promotion_flag else 0,
                        "original_price": original_price,
                        "production_quantity": production_quantity,
                        "sold_quantity": sold_quantity,
                        "surplus_quantity": surplus_quantity,
                        "shelf_life_hours": shelf_life_hours,
                        "preparation_time": preparation_time,
                        "storage_type": storage_type,
                        "current_time": current_time.strftime("%H:%M"),
                        "holding_time_hours": holding_time_hours,
                        # Derived features for ML
                        "day_pattern": day_char["pattern"],
                        "is_holiday_period": 1 if day_char["is_holiday_period"] else 0,
                    }

                    records.append(record)

                    # Update history
                    surplus_history[merchant_id].append(surplus_quantity)

                    # Keep only last 14 days of history per merchant
                    if len(surplus_history[merchant_id]) > 14:
                        surplus_history[merchant_id] = surplus_history[merchant_id][-14:]

    return records


def save_to_csv(records: List[Dict[str, Any]], filepath: str) -> None:
    """Save records to CSV file."""
    if not records:
        print("No records to save.")
        return

    fieldnames = list(records[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records -> {filepath}")


def main():
    """Generate synthetic F&B data for SurplusSense MVP."""
    print("=" * 60)
    print("SurplusSense Synthetic Data Generator")
    print("=" * 60)
    print(f"Note: This is SYNTHETIC data for MVP demonstration.")
    print(f"      It does NOT represent real merchant transactions.")
    print("=" * 60)

    # Generate 90 days of data for 15 merchants (5 of each type)
    # Each merchant generates ~3 products per day
    # Expected: 90 days * 15 merchants * 3 products = ~4,050 records
    records = generate_records(num_days=90, records_per_day_per_merchant=3)

    # Save to data directory
    output_path = "data/synthetic_fnb_data.csv"
    save_to_csv(records, output_path)

    # Print summary statistics
    print("\n" + "=" * 60)
    print("Dataset Summary")
    print("=" * 60)

    # Group by merchant type
    by_type = {}
    for r in records:
        mt = r["merchant_type"]
        if mt not in by_type:
            by_type[mt] = []
        by_type[mt].append(r)

    for mt, recs in by_type.items():
        total_surplus = sum(r["surplus_quantity"] for r in recs)
        total_production = sum(r["production_quantity"] for r in recs)
        avg_surplus_rate = total_surplus / total_production if total_production > 0 else 0
        print(f"\n{mt}:")
        print(f"  Records: {len(recs)}")
        print(f"  Merchants: {len(set(r['merchant_id'] for r in recs))}")
        print(f"  Total Production: {total_production}")
        print(f"  Total Surplus: {total_surplus}")
        print(f"  Avg Surplus Rate: {avg_surplus_rate:.1%}")

    print("\n" + "=" * 60)
    print("Data generation complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
