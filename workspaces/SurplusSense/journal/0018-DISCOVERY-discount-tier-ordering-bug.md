# DISCOVERY: Discount Tier Ordering Bug

**Date:** 2026-04-26
**Type:** DISCOVERY

## Finding

The `DISCOUNT_TIERS` list in `src/recommendation_engine.py` was ordered incorrectly — tiers within the same surplus bucket were sorted from loosest time constraint to strictest. This caused early-exit matching to apply wrong discounts.

**Example:** surplus=3, remaining=0h should match `(5, 0, 0.30)` → 30%, but `(5, 2, 0.20)` matched first because it appeared earlier in the list.

## Root Cause

The condition `surplus_qty <= max_qty AND remaining_life <= min_life_hours` means both conditions must be true. For surplus=3, remaining=0:

- `(5, 2, 0.20)` → 3≤5 ✓ AND 0≤2 ✓ → matched (wrong tier!)
- `(5, 0, 0.30)` → 3≤5 ✓ AND 0≤0 ✓ → would also match but wasn't reached

The fix is to sort tiers **strictest first within each surplus bucket**, so that the most restrictive time limit matches before the less restrictive ones.

## Corrected Ordering

Within each surplus bucket, sort by `min_shelflife_hours` ascending (most restrictive first):

```
# Small surplus (≤5): remaining=0 → 30%, remaining≤2 → 20%
(5, 0, 0.30)   ← at limit
(5, 2, 0.20)   ← time pressure

# Medium surplus (6-10): remaining=0 → 50%, remaining≤2 → 40%, remaining≤4 → 30%
(10, 0, 0.50)
(10, 2, 0.40)
(10, 4, 0.30)

# Large surplus (11-20): remaining=0 → 60%, remaining≤2 → 50%, remaining≤4 → 40%
(20, 0, 0.60)
(20, 2, 0.50)
(20, 4, 0.40)
```

## Implication

Any rule-based system with tiered conditions (surplus + time) must sort tiers strictest-first to avoid early-exit matching errors.

## Files Changed

- `src/recommendation_engine.py` — DISCOUNT_TIERS reordered
- `tests/unit/test_recommendation_engine.py` — test expectations corrected
