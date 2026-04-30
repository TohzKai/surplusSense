# Cold Start Merchant Profile Form

**Priority**: HIGH
**Status**: TODO
**Type**: Product Gap

## Task

Add or document a merchant profile input form for cold-start predictions.

## Requirement

New merchants without history should be able to input:

- Merchant type (café, bakery, small F&B)
- Product categories
- Typical production quantities
- Operating hours
- Storage capabilities

The system should use category benchmarks + profile inputs to generate initial predictions labeled as "starter estimates."

## Files to Update

- `app/streamlit_app.py` - Already has merchant/category selectors (can be enhanced)
- `docs/product_hardening_plan.md` §1.5 - Already documented

## Notes

Can use existing selectors as proxy. Enhancement is nice-to-have for presentation.
