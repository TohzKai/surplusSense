# Seasonal Features Roadmap

**Priority**: MEDIUM
**Status**: TODO
**Type**: Technical Gap

## Task

Document seasonal feature requirements for production.

## Requirement

The 90-day synthetic dataset cannot capture annual seasonality. Production needs:

1. **12-24 months of historical data** for annual patterns
2. **External calendar features**:
   - Public holidays (CNY, Ramadan, Deepavali, Christmas)
   - School holidays
   - Payday cycles
   - Local events (Marathon, F1, concerts)
3. **Weather integration** (rain affects foot traffic)

## Documentation

- `docs/product_hardening_plan.md` §1.2
- Technical design for Phase 3

## Notes

Roadmap item, not MVP requirement.
