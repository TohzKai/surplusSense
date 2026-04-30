# GAP: Synthetic Data MVP Limitations

**Date**: 2026-04-25
**Type**: GAP
**Slug**: synthetic-data-mvp-limitations

## Finding

The MVP uses synthetic data generated via a controlled random process. This is appropriate for demonstrating the ML pipeline but creates specific limitations:

1. **No real merchant patterns**: Actual surplus depends on weather, events, staff behavior, supplier delays - not in synthetic data
2. **No seasonal calibration**: 90-day window cannot capture CNY, Ramadan, Deepavali patterns
3. **No demand validation**: Cannot prove consumers actually buy predicted surplus
4. **No merchant feedback**: No way to calibrate predictions against actual outcomes

## Impact

- Cannot claim real-world predictive accuracy
- Model may behave differently with real merchant data
- Requires pilot with actual merchant data before production

## Resolution

Documented in:

- `docs/product_hardening_plan.md` §1.1
- `docs/executive_report_notes.md` Limitations section
- COC decision log

**Positioning**: Synthetic data is an MVP development tool, not real-world validation.

## Next Steps

1. Conduct merchant pilot with real (anonymized) surplus data
2. Compare predicted vs actual surplus during pilot
3. Calibrate model weights based on real outcomes
4. Extend training window to 12-24 months for seasonality
