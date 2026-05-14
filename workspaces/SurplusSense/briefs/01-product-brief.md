# Product Brief — SurplusSense

## Final Product Definition

SurplusSense is a merchant-side F&B surplus decision cockpit. It helps bakeries, cafés, and prepared-food outlets decide whether to hold, monitor, discount, deep discount, donate, or discard surplus items.

The product uses supervised machine learning to predict expected surplus units, then applies transparent recommendation rules, food-safety gates, and recovery-value estimation to produce an explainable decision for the merchant.

## Target User

The initial user is an outlet manager or staff member at a bakery, café, or prepared-food outlet who must make fast end-of-day decisions about unsold inventory.

## Core Decision

The product supports one recurring operating decision:
"What should I do with this item now, given predicted surplus, remaining shelf life, safety constraints, and potential recovery value?"

## Why This Problem Matters

F&B surplus decisions are time-sensitive. A merchant who delays action loses recovery value; a merchant who discounts too early gives away margin; a merchant who lists unsafe food creates brand and safety risk. SurplusSense turns this trade-off into a structured decision workflow.

## MVP Scope

**Included in final MVP:**

- surplus quantity prediction
- merchant item input
- recommended action (HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD)
- food-safety gate (SAFE / CAUTION / BLOCKED)
- recovery-value estimate
- explanation of recommendation
- category-benchmark cold-start for new merchants
- pilot validation logic

**Not included in final MVP:**

- consumer marketplace
- payment processing
- delivery logistics
- POS integration
- real-time inventory integration
- automated customer notifications

## Scope Decision Rationale

The original concept explored a broader two-sided marketplace. For the individual assignment, I narrowed the final scope to the merchant decision layer because it is more directly aligned with ML decision-making and can be delivered as a working interactive product within the course timeline.

Consumer marketplace integration remains a Phase 2 opportunity.

## Business Model

Initial business model:

- Monthly SaaS fee per outlet (SGD 99–299 proposed, pilot-stage hypothesis)
- Optional recovered-value transaction fee (15% proposed)
- Future marketplace integration fee (Phase 2)
- ESG / waste-reporting module for chains (Phase 2)

## Tech Stack

- Backend: Python, scikit-learn, XGBoost
- Dashboard: Streamlit (interactive UI)
- Data: Pandas, NumPy
- Evaluation: Temporal 80/20 holdout + 5-fold TimeSeriesSplit CV
- Testing: pytest (63 unit tests)
- Random seed: 42

## Assessment Alignment

This brief reflects the final submitted scope of SurplusSense as a merchant-side decision-support cockpit, not a consumer marketplace. The MGMT655 individual assignment is assessed on working AI/ML decision-support products. The merchant cockpit directly demonstrates supervised ML prediction, leakage-aware validation, rule-based recommendation, food-safety governance, explainability, and commercial pilot logic.
