# Merchant Feedback Mechanism

**Priority**: MEDIUM
**Status**: TODO
**Type**: Product Gap

## Task

Add or document a merchant feedback mechanism for predictions.

## Requirement

Merchants should be able to indicate:

- Prediction accuracy: Too high / Too low / Accurate
- Recommendation usefulness: Useful / Not useful
- Item availability: Available / Not available

## Implementation

Simple approach:

- Add "Was this prediction useful?" thumbs up/down
- Add "Actual surplus quantity" input field
- Store feedback for future model improvement

## Files to Update

- `app/streamlit_app.py` - Enhancement opportunity
- `docs/product_hardening_plan.md` §6.2 - Already documented

## Notes

MVP can demonstrate the concept; full feedback loop needs database.
