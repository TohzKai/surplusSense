# RISK: Food Safety Rules Not Expert-Validated

**Date**: 2026-04-25
**Type**: RISK
**Slug**: food-safety-rules-unvalidated

## Finding

The food-safety rule engine implements checks for:

- Holding time vs storage type maximums
- Remaining shelf life vs category minimums
- Pickup window safety
- Storage type appropriateness

These are prototype rules based on general food-safety principles, NOT expert-validated.

## Risk

1. **Incorrect rules could allow unsafe food to be listed**
2. **Overly strict rules could block safe food unnecessarily**
3. **No SFA (Singapore Food Agency) regulatory alignment confirmed**
4. **No legal review of liability implications**

## Mitigation Required

1. **Expert review**: Food-safety specialist must validate rules before production
2. **SFA consultation**: Confirm alignment with Singapore food regulations
3. **Legal review**: Draft liability disclaimer for merchants
4. **Merchant confirmation**: Require explicit storage condition confirmation

## Disposition

Documented in:

- `docs/product_hardening_plan.md` §4
- `docs/executive_report_notes.md` Limitations section

**Disclaimer added**: "Advisory only; merchants remain responsible for food safety compliance"

## Status

OPEN - Requires expert validation before commercial deployment
