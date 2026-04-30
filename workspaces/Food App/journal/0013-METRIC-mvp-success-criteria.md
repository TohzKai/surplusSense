# METRIC: MVP Success Criteria

**Date**: 2026-04-25
**Type**: METRIC
**Slug**: mvp-success-criteria

## Success Definition

MVP is successful when:

1. **ML Model**: Outperforms simple baselines (Historical Average, Previous Day, Same Weekday Last Week)
2. **Dashboard**: Produces usable recommendations end-to-end without manual fixes
3. **Food-Safety**: Rules block/caution/safe items correctly
4. **Value**: Target merchants (cafés, bakeries) can understand output and see business value

## Exit Criteria for Phase 2

MVP ready for merchant pilots when:

1. Model beats baseline performance (MAE improvement verified)
2. Dashboard runs end-to-end without manual fixes
3. Food-safety rules working
4. Merchants can test workflow using their own sample data

## Current Status

| Criterion             | Status                             |
| --------------------- | ---------------------------------- |
| Model beats baselines | ✅ 74-82% improvement              |
| Dashboard end-to-end  | ✅ Running at localhost:8501       |
| Food-safety rules     | ✅ Working (block/caution/safe)    |
| Merchant value test   | ❌ Requires real merchant feedback |
