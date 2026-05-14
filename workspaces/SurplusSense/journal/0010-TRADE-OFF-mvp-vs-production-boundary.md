# TRADE-OFF: MVP vs Production Architecture

**Date**: 2026-04-25
**Type**: TRADE-OFF
**Slug**: mvp-vs-production-boundary

## Finding

The gap analysis revealed many production requirements not in the MVP scope. This trade-off document clarifies the boundary.

## Scope Decision

| Component              | MVP             | Production          |
| ---------------------- | --------------- | ------------------- |
| Data                   | CSV/SQLite      | PostgreSQL          |
| Auth                   | None            | Email/password, MFA |
| API                    | None            | FastAPI             |
| Model versioning       | Simple file     | MLflow              |
| CI/CD                  | None            | Full pipeline       |
| Notifications          | None            | Multi-channel       |
| Consumer side          | Mock preview    | Full marketplace    |
| SFA compliance         | Not claimed     | Required            |
| Food-safety validation | Prototype rules | Expert review       |

## Rationale

The MVP demonstrates the **core AI/ML decision-support logic**:

- Surplus prediction
- Discount recommendation
- Recovery estimation
- Food-safety screening

Production features are **acknowledged but deferred** to later phases.

## Documented In

- `docs/product_hardening_plan.md` - Full gap analysis
- `docs/executive_report_notes.md` - Limitations section
- `docs/coc_decision_log.md` - Decision rationale

## Key Principle

> "The strongest product is not the one with the most features, but the one with the clearest user, sharpest decision problem, most defensible ML logic, and most honest implementation boundary."
