# RISK: Model Drift Without Monitoring

**Date**: 2026-04-25
**Type**: RISK
**Slug**: model-drift-without-monitoring

## Finding

The MVP trains a single Random Forest model once. There is no:

- Monitoring of prediction accuracy over time
- Detection of model degradation
- Automated or manual retraining schedule

## Risk

1. **Silent degradation**: Model becomes less accurate without anyone noticing
2. **Concept drift**: Merchant/consumer behavior changes invalidate model assumptions
3. **Feature drift**: Production patterns shift (new menu, different supplier)
4. **Outcome drift**: Sell-through rates change without detection

## Mitigation

**Drift monitoring framework** (documented in `docs/product_hardening_plan.md` §1.3):

1. **Prediction error trend**: actual surplus vs predicted surplus, tracked weekly
2. **Feature drift**: Monitor distribution changes in production_qty, sales, price
3. **Outcome drift**: Track sell-through rate changes

**Threshold**: Flag for retraining when error exceeds baseline by X% for N consecutive days

## Status

OPEN - Production requirement not implemented in MVP
