# SurplusSense COC Decision Log

**Project:** SurplusSense - AI Decision Cockpit for F&B Merchants
**Date:** 2026-04-25
**Framework:** Kailash COC (Cognitive Orchestration for Codegen)
**Assignment:** SMU MBA Machine Learning Individual Project

---

## Executive Summary

This document records the key product decisions made during the development of SurplusSense MVP. Each decision follows the COC framework of explicitly accepting, rejecting, deferring, or modifying proposals based on analysis, not AI-generated suggestions.

---

## Decision 1: Narrowed Product Scope (Marketplace → Merchant Cockpit)

### Decision

**ACCEPTED** - Narrowed from two-sided food marketplace to merchant-facing AI decision cockpit.

### Rationale

The original concept of a full consumer marketplace faced several structural challenges:

- **Chicken-and-egg problem**: Requires both merchants and consumers to join simultaneously
- **Trust建立**: New marketplace has no transaction history to demonstrate reliability
- **Resource constraints**: MVP timeline cannot support both demand (consumer acquisition) and supply (merchant onboarding) sides
- **Competitive intensity**: Consumer-facing food discount space has established players (Treatsure, Yindii, Too Good To Go)

### Why Merchant-First

- Merchants have a clearer, more immediate pain point (unsold surplus → financial loss)
- Single-sided acquisition (merchants only)
- AI decision-support creates defensible value before marketplace effects
- SaaS-like monetisation path (subscription for insights) doesn't require consumer adoption

### Impact

- Product: SurplusSense (not a marketplace)
- Target user: Café, bakery, small F&B operators
- Core value: Predict surplus, recommend discounts, estimate recovery

---

## Decision 2: Synthetic Data for MVP

### Decision

**ACCEPTED** - Use synthetic data for MVP demonstration.

### Rationale

- **No real merchant data available**: MVP development began without merchant partnerships or data sharing agreements
- **Controlled environment**: Synthetic data allows demonstration of ML pipeline, feature logic, evaluation approach
- **Privacy**: No real merchant business data exposed
- **Reproducibility**: Known random seed allows consistent results for demo purposes

### Constraints Acknowledged

- Cannot claim real-world predictive accuracy
- Cannot validate against actual merchant outcomes
- Evaluation framework demonstrates methodology, not proven performance

### Positioned As

> "A controlled environment to demonstrate the ML pipeline, feature logic, evaluation approach, and decision-support workflow."

---

## Decision 3: Rejection of Reinforcement Learning for MVP

### Decision

**REJECTED** - Reinforcement learning removed from MVP scope.

### Rationale

- **Live transaction feedback required**: RL needs continuous reward signals (actual consumer purchases)
- **Cold-start problem**: New marketplace has no transaction history to learn from
- **Sample efficiency**: RL typically requires thousands of interactions to learn effectively
- **Complexity**: Adds significant implementation complexity without clear MVP value
- **Evaluation difficulty**: Hard to benchmark RL against baselines without live system

### Future Path

RL may be appropriate in Phase 3 after:

- Sufficient transaction volume accumulated
- Clear reward signals established
- Baseline policies learned from historical data

---

## Decision 4: Consumer Recommender Moved to Roadmap

### Decision

**DEFERRED** - Consumer-side recommendation moved to future roadmap.

### Original Proposal

Consumer-facing personalised recommendations for discounted items.

### Why Deferred

- **No user-item interaction data**: Cannot build collaborative filtering without purchase history
- **Consumer acquisition not MVP focus**: Targeting merchants first
- **Recommender complexity**: Would require significant additional ML work
- **Positioning confusion**: "Recommendation" means different things for merchants vs consumers

### Redefined for MVP

"Recommendation" = merchant-side operational recommendations:

- Which item to discount
- When to list
- What recovery value to expect

---

## Decision 5: MVP Segment Selection (Cafés, Bakeries, Small F&B)

### Decision

**ACCEPTED** - Target cafés, bakeries, and small F&B operators as beachhead segment.

### Rationale

| Factor                | Cafés/Bakeries                  | Hawkers                | Restaurants     |
| --------------------- | ------------------------------- | ---------------------- | --------------- |
| Surplus patterns      | Predictable (daily baked goods) | Variable               | Highly variable |
| Digital readiness     | High (POS systems)              | Medium                 | High            |
| Recovery value        | High                            | Low                    | High            |
| Onboarding complexity | Medium                          | High                   | Medium          |
| Regulatory compliance | Standard F&B                    | Special considerations | Standard F&B    |

### Why NOT Hawkers for MVP

- Lower average transaction values
- More complex onboarding ( hawker culture, collective decision-making)
- Less predictable surplus patterns
- Different regulatory considerations in Singapore

### Why Cafés/Bakeries First

- Clear, predictable surplus cycles (end of day)
- Strong digital infrastructure
- Higher recovery value per transaction
- More willing to pay for decision support (vs price-sensitive consumers)

---

## Decision 6: Food-Safety Rules as Product Feature

### Decision

**ACCEPTED** - Food-safety rule layer added as core product feature, not just legal disclaimer.

### Rationale

- **Safety is non-negotiable**: Foodborne illness risks are severe (reputational and legal)
- **Trust building**: Merchants need to trust the system before acting on recommendations
- **Differentiation**: Competitors may not have explicit safety checks
- **Liability protection**: Clear safety rules reduce platform liability

### Implementation

Safety checks validate:

- preparation_time
- holding_time
- storage_type
- shelf_life
- pickup_window

Items can be BLOCKED or flagged CAUTION before recommendation.

### Why Not ML for Safety?

- Rule-based is more transparent and explainable
- Food safety is not a prediction problem (physics, not patterns)
- Regulations are deterministic (hard rules, not probabilities)
- Merchants can understand and trust explicit rules

---

## Decision 7: Business Model Beyond Transaction Commission

### Decision

**ACCEPTED** - Multiple monetisation paths, not just transaction commission.

### Why Not Commission-Only Early

- **Chicken-and-egg**: Need volume before commission is meaningful
- **Merchant resistance**: Commission on already-discounted items reduces merchant margin
- **Value misalignment**: Commission creates incentive to push more discounts, not optimize

### Revenue Paths Identified

| Path                       | Timing      | Rationale                              |
| -------------------------- | ----------- | -------------------------------------- |
| Merchant SaaS subscription | Early (MVP) | Predictable revenue, aligns incentives |
| Transaction commission     | Mid-term    | Once volume builds                     |
| Data insights              | Future      | Anonymised industry trends             |
| Premium features           | Future      | Advanced analytics, forecasting        |

### Positioning

> "Merchant SaaS or freemium decision support as a stronger early monetisation path."

---

## Decision 8: Simplified Technical Stack

### Decision

**ACCEPTED** - MVP uses: Streamlit, Python, CSV/SQLite, scikit-learn, local storage.

### Not Included in MVP (Future Roadmap)

- Redis (caching)
- Docker (containerisation)
- Model registry (MLflow, etc.)
- Automated retraining pipelines
- Drift monitoring
- Full MLOps infrastructure

### Rationale

- **Speed to demo**: Focus on working product, not infrastructure
- **Complexity management**: Fewer dependencies = easier to explain
- **Assignment fit**: Demonstrates ML concepts without requiring DevOps expertise

---

## Decision 9: Baseline Comparisons for Evaluation

### Decision

**ACCEPTED** - Compare ML model against simple business rule baselines.

### Baselines Implemented

1. Historical average surplus (merchant + category)
2. Previous day surplus (lag 1)
3. Same weekday last week surplus (lag 7)

### Why These Baselines

- **Business relevance**: Merchants already use intuition similar to these rules
- **Interpretability**: Easy to explain to non-technical stakeholders
- **Low implementation cost**: Simple to compute, no ML required
- **Defensible improvement**: Model must beat simple rules to show value

### Evaluation Criteria

Focus on improvement over baselines, not just prediction existence:

- MAE improvement %
- RMSE improvement %
- Business value of better predictions

---

## Decision 10: Rule-Based Discount Engine

### Decision

**ACCEPTED** - Rule-based discount recommendation instead of learned policy.

### Why Not Learned Policy

- **Transparency**: Merchants need to understand why a discount is recommended
- **Trust**: Black-box recommendations may not be acted upon
- **Stability**: Rule outputs are consistent and explainable
- **No feedback loop**: Need consumer response data to learn optimal discounts

### Rule Structure

Discount tiers based on:

- Surplus quantity (more surplus → higher discount)
- Remaining shelf life (less time → higher discount)
- Category-specific considerations

---

## Summary Table

| Decision                       | Status   | Key Reason                                         |
| ------------------------------ | -------- | -------------------------------------------------- |
| Marketplace → Merchant Cockpit | ACCEPTED | Focus, differentiation, simpler acquisition        |
| Synthetic data                 | ACCEPTED | No real data available                             |
| RL removed                     | REJECTED | Cold start, complexity, no feedback loop           |
| Consumer recommender deferred  | DEFERRED | No interaction data, wrong focus                   |
| Cafés/bakeries as beachhead    | ACCEPTED | Predictable patterns, digital ready, high recovery |
| Food-safety rules              | ACCEPTED | Safety non-negotiable, differentiation             |
| Non-commission revenue         | ACCEPTED | Aligns incentives, earlier revenue                 |
| Simplified stack               | ACCEPTED | Speed to demo, assignment fit                      |
| Baseline comparisons           | ACCEPTED | Business relevance, defensible value               |
| Rule-based discounts           | ACCEPTED | Transparency, trust, no feedback data              |

---

## Lessons Learned

1. **Narrow scope creates focus**: Restricting to merchant-side only made the product coherent
2. **Simplicity scales**: Rule-based systems are maintainable and explainable
3. **Evaluation against baselines is crucial**: Proving improvement over simple rules validates ML value
4. **Safety cannot be afterthought**: Food safety as feature builds trust
5. **Business model clarity**: Multiple paths reduce early-stage risk

---

## Future Roadmap Items (Not MVP)

- [ ] Real merchant data partnerships
- [ ] Consumer-facing mobile app
- [ ] Payment/PayNow integration
- [ ] Hawker segment expansion
- [ ] Collaborative filtering for consumers
- [ ] Reinforcement learning for discount optimisation
- [ ] Automated model retraining
- [ ] Drift monitoring
- [ ] Advanced MLOps infrastructure

---

_Document generated as part of COC methodology. Each decision reflects deliberate product thinking, not AI-generated suggestions._
