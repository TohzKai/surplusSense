# Analysis Remediation: Critical and Major Gap Fixes

**Date**: 2026-04-17
**Trigger**: Red team reports 01-analysis-gaps.md (39 findings) and 02-spec-gaps.md (48 findings)

---

## Decision 1: Timeline Reconciliation (GAP-M01, GAP-X01)

**Problem**: ML architecture proposes 14-20 weeks of ML work. Implementation plan allocates 4 weeks. These directly contradict.

**Decision**: The project is a **10-week SMU MBA ML individual project**. The ML architecture describes the full production system; the implementation plan describes what's achievable in 10 weeks. We adopt a **"demonstrate the ML pipeline, don't build production ML"** approach.

**Revised ML scope for 10-week project**:

| Capability         | Course Project Scope                                              | Production Roadmap                                         |
| ------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| Surplus Prediction | XGBoost on synthetic data, demonstrated pipeline                  | Full ensemble with Prophet + per-merchant tuning           |
| Recommendations    | Content-based filtering on synthetic data, demo personalized feed | Hybrid with collaborative filtering + contextual bandit    |
| Dynamic Pricing    | Rule-based time-decay with configurable parameters                | Multi-armed bandit → RL (requires 10K+ real transactions)  |
| Waste Analytics    | Descriptive + pattern detection (clustering) on synthetic data    | Full prescriptive with anomaly detection + recommendations |

**Rationale**: Four ML capabilities are kept, but each is scoped to its simplest viable demonstration. The architecture document serves as the "production blueprint" while the implementation plan reflects what gets built.

---

## Decision 2: Synthetic Data Strategy (GAP-M02)

**Problem**: Platform has zero users. ML models need historical data. No data generation strategy exists.

**Strategy**: Generate realistic synthetic F&B data based on Singapore research benchmarks.

### Synthetic Data Design

**Merchant profiles** (20-30 synthetic merchants):

- Distribution: 8 restaurants, 6 cafes, 5 bakeries, 4 grocery stores, 3 hawker stalls
- Each has 3-8 food categories with realistic batch sizes and prices
- Locations distributed across Singapore (CBD, residential, mixed)
- Operating hours based on establishment type

**Transaction history** (6 months, ~180 days per merchant):

- Daily sales per category generated with:
  - Day-of-week patterns (weekday lunch vs. weekend dinner)
  - Weather correlation (rain = lower foot traffic for pickup)
  - Holiday effects (Chinese New Year, National Day, etc.)
  - Random noise (normal distribution, σ = 15% of mean)
  - Trend component (slight growth or decline per merchant)
- Surplus = batch_size - sales, floored at 0, with realistic waste rates (5-25% depending on category)

**Consumer interactions** (500-1000 synthetic consumers):

- Cuisine preferences, dietary tags, location, budget ranges
- 6 months of browsing/purchase/rating history
- Generated with realistic engagement distributions (most users casual, few power users)

**Data generation scripts**:

```python
# Data generator structure
src/ml/synthetic/
  generate_merchants.py     # Merchant profiles with categories
  generate_transactions.py  # 6 months of daily sales/surplus data
  generate_consumers.py     # Consumer profiles with preferences
  generate_interactions.py  # Browse/purchase/rating history
  config.py                 # Distributions, noise levels, parameters
```

**Validation**: Synthetic data statistics compared against Singapore F&B research benchmarks:

- Average waste rate: 10-20% (matches research)
- Day-of-week variation: ±30% (realistic for F&B)
- Price distribution: S$3-12 range (matches Singapore F&B pricing)
- Consumer engagement: Power-law distribution (realistic for marketplace apps)

---

## Decision 3: Cold Start Approach (GAP-G01)

**Problem**: Two-sided marketplace with ML needs both sides active before ML adds value.

**Approach for the course project**:

1. **Synthetic data** provides the "warm start" for all ML models
2. **Demo scenario**: Pre-loaded app with synthetic history, user interacts with live ML predictions
3. **Honest framing**: "Here's what the platform would look like after 6 months of operation"
4. **Incremental value path documented**: Month 1 (rules) → Month 3 (basic ML) → Month 6 (full ML) → Month 12 (data moat)

For the startup exploration aspect:

- Months 1-3: Manual marketplace with rule-based features, recruiting 20-50 merchants manually
- Months 3-6: ML features begin activating as merchant-specific data accumulates
- Months 6-12: Full ML features active, data moat beginning to compound
- This phased approach is documented in the business case, not just the technical plan

---

## Decision 4: Hawker Positioning (GAP-X02)

**Problem**: Hawker stalls claimed as differentiator but never concretely planned; economics may not work.

**Decision**: **Hawkers excluded from MVP, included as Phase 3 expansion target.**

**Rationale**:

- Hawker food at S$3-6 with 50% discount = S$1.50-3. Platform commission (15%) = S$0.23-0.45 per transaction. This does not justify merchant onboarding effort.
- Hawker digital adoption barriers (one-person operations, older demographics) require dedicated onboarding resources.
- Hawker food already affordable — the value proposition is weaker than for restaurants/cafes/bakeries.

**Impact on documents**:

- Competitive analysis: Hawker gap reframed as Phase 3 opportunity, not MVP differentiator
- USPs: Remove hawker from "Singapore-First Design" USP; replace with "Bakery and cafe surplus focus"
- Platform model: Hawker stalls moved to "Phase 3 expansion" section
- ML architecture: No hawker-specific ML patterns needed for MVP

**MVP target merchants**: Restaurants, cafes, bakeries, grocery stores — establishments with S$8-20 price points where 50% discount creates meaningful consumer savings (S$4-10) and merchant revenue (S$3-8 after commission).

---

## Decision 5: Unit Economics Correction (GAP-P01)

**Problem**: Unit economics optimistic by 2-4x.

**Corrected economics**:

| Metric                                                  | Optimistic | Moderate | Pessimistic |
| ------------------------------------------------------- | ---------- | -------- | ----------- |
| Avg deal value                                          | S$6        | S$4      | S$3         |
| Transactions/merchant/week                              | 15         | 8        | 3           |
| Revenue/merchant/week (at 15% commission)               | S$13.50    | S$4.80   | S$1.35      |
| Consumer acquisition cost                               | S$5        | S$10     | S$15        |
| Merchants for break-even (at S$2K/month operating cost) | 50         | 100      | 370+        |

**Key insight**: Break-even is achievable under moderate assumptions with 100 merchants. This is realistic within 12-18 months of operation. The optimistic scenario understates the challenge; the pessimistic scenario shows the business is still viable with patience.

---

## Decision 6: Failure Mode and Liability (GAP-G03)

**Key failure modes and mitigations**:

| Failure Mode                           | Likelihood | Impact   | Mitigation                                                                                                                                                                           |
| -------------------------------------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Consumer food poisoning                | Low        | Critical | Platform disclaims liability (merchant is food provider); merchant ToS requires food safety compliance; recommend merchants carry food liability insurance; SFA license verification |
| Prediction wrong, merchant loses money | Medium     | Medium   | Merchant always reviews and approves listings; prediction presented with confidence score; merchant can override; platform does not guarantee prediction accuracy                    |
| Dynamic pricing too aggressive         | Medium     | Medium   | Merchant sets price floor; pricing mode is merchant-configurable; A/B testing on small % before full rollout                                                                         |
| Consumer claims food quality poor      | High       | Low      | Review and rating system; refund policy for legitimate complaints; merchant response mechanism                                                                                       |
| Merchant lists past use-by food        | Low        | Critical | System auto-validates use-by dates; 30-minute monitoring checks; merchant suspended on violation                                                                                     |
| Platform used for money laundering     | Very Low   | Critical | Stripe handles payment compliance; transaction monitoring; suspicious activity reporting                                                                                             |

**Liability framework**: Platform is a marketplace connecting merchants and consumers. Merchants are responsible for food safety and quality. Platform is responsible for listing accuracy, payment processing, and fair dispute resolution. This mirrors the GrabFood/foodpanda liability model in Singapore.

---

## Decision 7: Right-Sized Infrastructure (GAP-M06)

**Course project infrastructure**:

| Component       | Course Project                   | Production              |
| --------------- | -------------------------------- | ----------------------- |
| Database        | SQLite or PostgreSQL (local)     | PostgreSQL (managed)    |
| Caching         | Python dict / in-memory          | Redis                   |
| Model storage   | File system (joblib/pickle)      | Model registry (MLflow) |
| Task scheduling | Simple Python cron / manual      | APScheduler + Celery    |
| Deployment      | Local or single Docker container | Docker Compose / K8s    |
| Monitoring      | Print statements + notebooks     | Prometheus + Grafana    |

The ML architecture document describes the production system. The implementation plan builds the simpler version.

---

## Spec Fixes Applied

The following spec files have been updated to address critical spec gaps:

1. **data-model.md**: Added missing tables (Notification, NotificationPreference, FCMToken, SavedListing, MerchantPayout, MerchantBankAccount, Badge, UserBadge)
2. **API conflicts resolved**: Surplus prediction uses GET (spec is authority), Order status "collected" is terminal (no "completed" state)
3. **Error response format and pagination**: Added to marketplace spec
4. **Payment methods**: Standardized to Stripe-supported methods (Card, Apple Pay, Google Pay); PayNow deferred to Phase 2
