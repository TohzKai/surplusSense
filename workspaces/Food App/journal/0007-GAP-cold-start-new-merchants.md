# GAP: Cold Start Problem for New Merchants

**Date**: 2026-04-25
**Type**: GAP
**Slug**: cold-start-new-merchants

## Finding

The Random Forest model requires historical data (lag features, rolling averages) to make predictions. New merchants without history cannot benefit from accurate predictions.

## Impact

- New merchants receive lower-confidence predictions
- May reduce initial value proposition
- Onboarding experience depends on guesswork

## Resolution

**Cold-start approach** (documented in `docs/product_hardening_plan.md` §1.5):

1. Use merchant profile + category benchmarks as initial prediction
2. Label as "starter estimate" not high-confidence
3. Gradually shift to merchant-specific as data accumulates
4. Use similar-merchant benchmarks (same type, category, location)

## Next Steps

1. Implement merchant profile input form
2. Build category-level baseline predictions
3. Add confidence scoring to predictions
4. Track time-to-accuracy for new merchants
