# DISCOVERY: food-app-pricing.md had ALL discount tiers inverted

**Date:** 2026-04-30
**Type:** DISCOVERY
**Session:** /codify session 2026-04-30

## Finding

The `food-app-pricing.md` skill's discount tier table was the **mirror opposite** of the source code's logic.

**Skill claimed:**

- "≤5 units, >2h remaining → 20% off"
- "≤5 units, ≤2h remaining → 30% off"
  (More time remaining = lower discount)

**Source code (`src/recommendation_engine.py`) implements:**

- `DISCOUNT_TIERS = [(5, 0, 0.30), (5, 2, 0.20), ...]`
- Matching: `surplus_qty <= max_qty AND remaining_life <= min_life_hours`
- For surplus=3: `remaining=0h → 30%`, `remaining=2h → 20%`
  (Less time remaining = higher urgency = higher discount)

## Root Cause

The skill's tier table was authored with intuitive ordering (higher remaining time = higher discount) but the source code uses early-exit matching where **strictest time constraint first** means highest urgency = highest discount. The skill was never verified against source during codification.

## Evidence

Source DISCOUNT_TIERS (strictest-first):

```python
DISCOUNT_TIERS = [
    (5, 0, 0.30),   # ≤0h remaining → 30% (most urgent)
    (5, 2, 0.20),   # ≤2h remaining → 20% (less urgent)
    ...
]
```

Match logic: `if surplus_qty <= max_qty and remaining_life <= min_life_hours`

## Correction Applied

Rewrote tier table in food-app-pricing.md:

- Corrected ordering: ≤0h (at limit) = 30%, ≤2h (limited time) = 20%
- Matched source tier structure and comments
- Added explicit correction note in the skill

## Files Changed

- `.claude/skills/project/food-app-pricing.md` — discount tier table rewritten

## For Discussion

Why did the skill get the logic inverted? Possible contributing factors:

- The tier names in the source ("at limit" vs "time pressure") suggest urgency, but the 30%/20% assignment was counterintuitive
- The skill author may have assumed higher remaining time = higher value to consumer = lower discount needed
- No source-verification step was run during initial codification
