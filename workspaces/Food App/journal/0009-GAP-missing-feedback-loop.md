# GAP: Missing Merchant Feedback Loop

**Date**: 2026-04-25
**Type**: GAP
**Slug**: missing-feedback-loop

## Finding

The MVP does not capture merchant feedback on predictions or recommendations. Merchants cannot tell the system when predictions are wrong.

## Impact

1. No signal to improve model accuracy
2. No way to validate predictions against reality
3. Missed learning opportunity

## Resolution

**Feedback mechanism** (documented in `docs/product_hardening_plan.md` §6.2):

Merchants can indicate:

- Prediction: Too high / Too low / Accurate
- Recommendation: Useful / Not useful
- Item: Actually available / Not available
- Discount: Too aggressive / Appropriate / Too conservative
- Safety flag: Too strict / Appropriate / Too lenient

## Outcome Tracking

After each recommendation, record:

- Actual surplus
- Quantity listed, sold, discarded
- Final discount
- Actual recovery value
- Reason for unsold surplus

## Next Steps

1. Add feedback buttons to dashboard
2. Store feedback in database
3. Analyze feedback for patterns
4. Use feedback to prioritize retraining
