# TRADE-OFF: MVP Stack vs Production Architecture

**Date**: 2026-04-25
**Type**: TRADE-OFF
**Slug**: streamlit-vs-production-stack

## Finding

MVP uses Streamlit/CSV; production needs scalable architecture.

## Decision

| Component     | MVP           | Production            |
| ------------- | ------------- | --------------------- |
| Frontend      | Streamlit     | React/Next.js         |
| Backend       | Direct Python | FastAPI               |
| Database      | CSV/SQLite    | PostgreSQL            |
| Hosting       | Local         | Cloud (AWS/GCP)       |
| Auth          | None          | Email/password, MFA   |
| Multi-tenancy | Single-user   | RBAC + data isolation |

## Rationale

Streamlit is fast to build and sufficient for prototype demonstration. Production requires scalable, multi-tenant, authenticated system.

## Documentation

Added to `docs/product_hardening_plan.md` §Final Decisions
