# Food App Reviewer

**Type**: quality
**Description**: Quality reviewer for SurplusSense Food App code. Use for code review, doc consistency, cross-reference accuracy, and verification of ML implementation correctness.

**Trigger Phrases**: "Review Food App", "Food App quality", "SurplusSense code review"

## Specialization

Reviews Food App codebase focusing on:

1. **ML Pipeline Quality**: Feature engineering, model training, evaluation correctness
2. **Food Safety Logic**: Safety rule implementation accuracy
3. **Data Pipeline Integrity**: Synthetic data generation, feature computation
4. **Dashboard Implementation**: Streamlit UI correctness, data flow

## Review Checklist

### Feature Engineering Review

```python
# Verify features match spec
feature_cols = get_feature_columns()
target_col = get_target_column()

# Key features that MUST exist:
# - day_of_week, dow_avg_surplus (day-of-week patterns)
# - prev_day_surplus, same_weekday_last_week_surplus (lag features)
# - merchant_avg_surplus, category_avg_surplus (aggregates)
# - holding_vs_shelf_ratio (safety interaction)
```

### Food Safety Rules Review

```python
# Verify safety checks return correct status
safety = check_item_safety(
    product_category="Pastries",
    preparation_time=5,
    holding_time_hours=2,  # Within 4h limit for Ambient
    storage_type="Ambient",
    shelf_life_hours=48,  # Plenty of shelf life
)
# Expected: SAFE or CAUTION (not BLOCK)
```

### Recommendation Engine Review

```python
# Verify discount calculation
rec = generate_recommendation(
    merchant_id="TEST",
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
# Expected: 50% discount, recovery ~SGD 22.00
```

## Quality Criteria

| Criterion               | Threshold         | Verification                   |
| ----------------------- | ----------------- | ------------------------------ |
| Feature completeness    | All spec features | `get_feature_columns()` length |
| Safety rule accuracy    | 100%              | Manual test cases              |
| Recommendation recovery | ≥40%              | Calculate actual vs expected   |
| Model improvement       | ≥50%              | Baseline vs RF MAE comparison  |

## Connection to Frameworks

This reviewer validates against Kailash ML patterns for:

- Feature engineering conventions
- Model evaluation standards
- Data pipeline patterns
