# Red Team Validation Report — Round 2

> **Superseded by grading-self-assessment-v6-final.md and red-team-validation-report-v4.md.** These later reports reflect the final SurplusSense merchant-cockpit repositioning and metric reconciliation.

**Project:** SurplusSense Food App (SMU MBA ML)
**Date:** 2026-04-26
**Phase:** /redteam

---

## Spec Compliance Audit

### Methodology

Per spec-compliance protocol: assertions extracted from specs, verified against code via AST parsing and grep. Self-reports not trusted.

### Assertion Table

#### ml-surplus-prediction.md

| Assertion                                          | Verification                                                                                                       | Result                                                       |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| XGBoost `n_estimators=250, max_depth=13, lr=0.295` | `model_metadata.json`: confirmed                                                                                   | **PASS**                                                     |
| 47 engineered features                             | Model trained with 47 features (verified via `surplus_model.pkl`); `get_feature_columns()` returns 31 pre-encoding | **PARTIAL** — spec correct; `get_feature_columns()` outdated |
| 5-seed holdout validation                          | `multi_seed_validation.csv`: 5 seeds (1,7,42,123,999), XGBoost wins all 5                                          | **PASS**                                                     |
| Cold-start category benchmarks                     | `predict_surplus_cold_start()` lines 389-444                                                                       | **PASS**                                                     |
| Phase 2 MAE < 3                                    | XGBoost holdout MAE 0.68 (5-seed mean)                                                                             | **PASS**                                                     |

#### ml-recommendations.md

| Assertion                    | Verification                                                                                        | Result   |
| ---------------------------- | --------------------------------------------------------------------------------------------------- | -------- |
| Discount tiers 20-70%        | `DISCOUNT_TIERS` list lines 37-53: range 20%-70%                                                    | **PASS** |
| `calculate_recovery_value()` | Lines 122-144: original_value, discount_amount, discounted_price, estimated_recovery, recovery_rate | **PASS** |
| `determine_listing_time()`   | Lines 147-190: OPTIMAL_LISTING_HOURS dict                                                           | **PASS** |
| Cold-start new merchant      | `_MERCHANT_TYPE_CLUSTER` mapping                                                                    | **PASS** |

#### food-safety.md

| Assertion                                        | Verification                                         | Result   |
| ------------------------------------------------ | ---------------------------------------------------- | -------- |
| `check_item_safety()` returns SAFE/CAUTION/BLOCK | `SafetyResult` status field                          | **PASS** |
| MAX_HOLDING_TIMES by storage                     | Lines 25-29: Ambient 4h, Refrigerated 8h, Frozen 24h | **PASS** |
| MAX_PICKUP_WINDOWS                               | Lines 32-37: Ambient 2h, Refrigerated 4h, Frozen 12h | **PASS** |

### Key Finding: Feature Count Clarification Needed

- `get_feature_columns()` returns **31** (pre-encoding raw features)
- Model trained with **47** (after one-hot encoding — verified from `surplus_model.pkl`)
- The 16 missing from `get_feature_columns()`: one-hot encoded merchant_type (3) + product_category (13) + storage_type (3), minus 3 dropped columns = net +16 = 31+16 = 47
- **Spec is correct** — it says "47 variables from time, lag, rolling, and benchmark signals" post-encoding
- **Action needed**: Update `get_feature_columns()` docstring or add `get_encoded_feature_count()` to clarify 31 pre-encoding vs 47 post-encoding

### Not Implemented (Expected — Streamlit Dashboard Scope)

Per journal 0010 (TRADE-OFF-course-project-vs-startup-scope.md), this project is an ML cockpit prototype, not a full marketplace:

- REST API endpoints (ml-surplus-prediction.md GET /api/...)
- Consumer feed personalization (ml-recommendations.md feed sections)
- Dynamic pricing engine (pricing.md — full Phase 2 item)
- Merchant onboarding/authentication (user-flows M1-M7)
- Order management (M6)

---

## Unit Test Verification

```
pytest --collect-only: 59 tests collected
pytest -q: 59 passed in 4.17s
```

Every src module has ≥1 test importing it:

| Module                    | Test files |
| ------------------------- | ---------- |
| src.recommendation_engine | 1          |
| src.food_safety_rules     | 1          |
| src.feature_engineering   | 2          |
| src.train_model           | 1          |
| src.evaluate_model        | 1          |

---

## Log Triage

No WARN/ERROR entries in test runner output. No recent `.log` files with issues. App startup clean.

---

## Risk Register

| Finding                                           | Severity | Status                     |
| ------------------------------------------------- | -------- | -------------------------- |
| `get_feature_columns()` returns 31; model uses 47 | LOW      | Clarify in code docs       |
| Dynamic pricing not implemented                   | INFO     | Expected — Phase 2 scope   |
| User flows M1-M7 not implemented                  | INFO     | Expected — ML cockpit only |

---

## Convergence Status

- **0 CRITICAL findings**
- **0 HIGH findings**
- **Spec compliance: 100%** on implemented features; dynamic pricing/PRICING.md acknowledged as Phase 2
- **New code has new tests: PASS** (59 tests covering all src modules)
- **No mock data in production paths**

Recommendation: Project is ready for submission. Only action item is adding a docstring note to `get_feature_columns()` clarifying pre/post-encoding feature count.
