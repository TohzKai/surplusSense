# SurplusSense Executive Report Notes

**Project:** SurplusSense - AI Decision Cockpit for F&B Merchants
**Date:** 2026-04-25
**Assignment:** SMU MBA Machine Learning Individual Project

---

## Problem Statement

### The Singapore F&B Surplus Challenge

Singapore's food and beverage industry generates significant food waste annually. The National Environment Agency (NEA) reports that Singapore generates approximately [X] tonnes of food waste daily, with F&B operations contributing a substantial portion.

**Key pain points for F&B merchants:**

- Unsold food at end of day results in direct revenue loss
- Merchants lack tools to predict surplus accurately
- Discount decisions are often reactive, not proactive
- Food safety regulations create liability concerns
- No clear framework for surplus-to-consumer pathways

### Current State

- Merchants rely on intuition and simple rules
- No systematic approach to surplus prediction
- Existing platforms are consumer-facing, not merchant-focused
- Data on surplus patterns is not captured or analysed

---

## Approach

### Product Concept

**SurplusSense** is a merchant-facing AI decision cockpit that helps F&B operators:

1. **Predict** likely surplus quantities before end of day
2. **Recommend** optimal discount actions
3. **Estimate** revenue recovery from discounted sales
4. **Validate** food safety compliance before listing

### Target Segment

**MVP Beachhead:** Cafés, bakeries, and small F&B operators in Singapore

**Why this segment:**

- Predictable surplus patterns (daily cycles)
- Higher digital readiness (POS systems, online ordering)
- Strong recovery value per transaction
- Easier onboarding than hawker stalls

**Not in MVP:** Hawker stalls (Phase 3 expansion), full consumer marketplace

### Technical Approach

**ML Pipeline:**

1. Synthetic data generation (realistic F&B operating variables)
2. Feature engineering (time, lag, rolling, merchant, category features)
3. Baseline models (historical average, previous day, same weekday last week)
4. Supervised model (XGBoost for surplus prediction)
5. Rule-based discount recommendation engine
6. Food-safety rule layer

**Evaluation:**

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- Improvement over baselines

---

## Results

### Model Performance

The XGBoost model demonstrates significant improvement over simple baseline predictors:

| Model                  | Holdout MAE | Notes                                                 |
| ---------------------- | ----------- | ----------------------------------------------------- |
| Historical Average     | 1.39        | Best baseline                                         |
| Previous Day           | 1.95        |                                                       |
| Same Weekday Last Week | 1.93        |                                                       |
| **XGBoost**            | **0.68**    | Wins 5/5 holdout seeds vs RF; mean advantage 0.19 MAE |

**Key findings:**

- XGBoost holdout MAE: **0.6824** (mean across 5 seeds) vs RF holdout MAE: 0.8675
- XGBoost improves over Historical Average baseline by **~51%** in holdout MAE
- XGBoost selected over Random Forest after 5-seed random 80/20 holdout comparison (wins all 5 seeds)
- TimeSeriesSplit CV favored RF (1.07 vs 1.22 MAE) — RF's stronger regularization tolerates temporal shift better; XGBoost wins on i.i.d. holdout

### Feature Importance

Top predictive features:

1. **Day-of-week average surplus** (49.5% importance) - Historical pattern for same weekday
2. **Production vs merchant average** (34.0%) - How current production compares to merchant's typical output
3. **Merchant average surplus rate** (1.4%) - Merchant's historical surplus tendency
4. **Category average surplus rate** (1.2%) - Category-level surplus patterns
5. **Day-of-week average sold** (1.1%) - Historical sales patterns

### Recommendation Engine

The rule-based discount engine produces actionable recommendations:

- Discount tier: Based on surplus quantity and remaining shelf life
- Listing time: Optimal timing for consumer pickup
- Recovery estimate: Revenue recovered vs potential loss

### Food Safety

Safety checks block or flag unsafe items:

- SAFE: Can be listed
- CAUTION: Can be listed with warnings
- BLOCK: Cannot be listed for safety reasons

---

## Business Case

### Unit Economics (Conservative/Based/Optimistic)

| Scenario     | Merchants | Avg Recovery/Merchant/Month | Platform Revenue             |
| ------------ | --------- | --------------------------- | ---------------------------- |
| Conservative | 50        | SGD 200                     | Subscription only            |
| Based        | 150       | SGD 350                     | Subscription + 5% commission |
| Optimistic   | 500       | SGD 500                     | Full platform                |

### Revenue Streams

1. **SaaS Subscription (Early)**
   - Basic: Free tier
   - Pro: SGD 49-99/month per merchant
   - Value: Decision intelligence dashboard

2. **Transaction Commission (Mid-term)**
   - 5-10% on discounted transactions
   - Only viable at scale

3. **Data Insights (Future)**
   - Anonymised industry trends
   - Benchmarking tools

### Why Not Commission-Only?

- Aligns incentives with merchants
- Predictable early revenue
- Doesn't penalise efficient surplus management

---

## Limitations

### Data Limitations

- **Synthetic data**: Results demonstrate methodology, not real-world accuracy. Real merchant pilots required before production deployment.
- **90-day window**: Demonstrates MVP pipeline but insufficient for annual seasonality (CNY, Ramadan, Deepavali)
- **No live feedback**: Cannot validate against actual merchant outcomes

### Model Limitations

- **Feature scope**: Limited to variables in synthetic dataset
- **Baseline comparisons**: Improvement over simple rules, not proven real-world accuracy
- **Cold start**: New merchants without history use profile-based benchmarks with lower confidence
- **No drift monitoring**: Model may degrade as merchant behavior changes without detection
- **No retraining pipeline**: Manual single training; production needs scheduled + triggered retraining

### Product Limitations

- **No payment integration**: MVP focuses on decision support, not transactions
- **No consumer app**: Merchant-only for MVP; consumer demand is Phase 4 validation
- **No authentication**: No merchant accounts or session persistence
- **No notifications**: Morning alerts not implemented

### Food Safety Limitations

- **Prototype rules only**: Not expert-validated; require food-safety specialist review
- **No SFA integration**: Not claiming Singapore SFA regulatory compliance
- **Storage assumption**: Assumes proper storage; merchants must confirm conditions
- **Liability disclaimer**: "Advisory only. Food safety recommendations are based on general principles and have not been validated by SFA or food safety experts. Merchants remain responsible for food safety compliance, storage, and handling decisions."

### Scope Limitations

- Not a full marketplace
- No real merchant partnerships
- No regulatory compliance certification
- See **docs/product_hardening_plan.md** for detailed gap analysis and phased roadmap

---

## Competitive Landscape

### Existing Platforms

| Platform       | Focus                | SurplusSense Differentiation       |
| -------------- | -------------------- | ---------------------------------- |
| Treatsure      | Consumer discounts   | Upstream merchant intelligence     |
| Yindii         | Consumer discounts   | Decision-support, not just listing |
| Too Good To Go | Consumer marketplace | Merchant-side focus                |
| GrabFood       | Delivery             | Not surplus-focused                |
| foodpanda      | Delivery             | Not surplus-focused                |

### SurplusSense Positioning

> "Existing Singapore surplus-food platforms are primarily consumer-facing. SurplusSense focuses upstream on merchant-side prediction and decision support."

**Differentiation:**

- AI-powered surplus prediction (vs reactive listing)
- Merchant decision intelligence (vs consumer discovery)
- Food-safety integration (safety as feature)
- SaaS monetisation (subscription vs commission)

---

## Roadmap

### Phase 1: Week 9 MVP (Current)

- [x] Synthetic data pipeline
- [x] ML prediction model
- [x] Baseline comparisons (Historical Avg, Prev Day, Same Weekday Last Week)
- [x] Recommendation engine (rule-based discount)
- [x] Food safety rules (block/caution/safe)
- [x] Streamlit dashboard
- [x] COC decision log
- [ ] Real merchant pilot

### Phase 2: Merchant Pilot

- [ ] Real merchant onboarding
- [ ] Actual sales and surplus data
- [ ] Merchant feedback loop
- [ ] Outcome tracking (actual vs predicted)
- [ ] Manual retraining
- [ ] Basic account persistence

### Phase 3: Commercial Platform

- [ ] Authentication (email/password, MFA)
- [ ] Production database (PostgreSQL)
- [ ] API endpoints (FastAPI)
- [ ] Notifications (morning alerts, pickup warnings)
- [ ] Model registry (MLflow)
- [ ] Scheduled + triggered retraining
- [ ] Legal terms of service
- [ ] Subscription pricing

### Phase 4: Marketplace Expansion

- [ ] Consumer listings
- [ ] Payment integration (PayNow, cards, wallets)
- [ ] Consumer demand validation
- [ ] Transaction flow
- [ ] Personalisation

### Phase 5: Advanced Optimisation

- [ ] A/B testing for model versions
- [ ] Drift monitoring
- [ ] Automated retraining
- [ ] POS integration
- [ ] Multi-outlet benchmarking
- [ ] Bandit/RL pricing (future)

See **docs/product_hardening_plan.md** for detailed gap analysis.

---

## Conclusion

### Key Takeaways

1. **Focused scope creates clarity**: Merchant decision-support is a coherent, defensible product
2. **Simple baselines validate ML value**: Proving improvement over rules is crucial
3. **Safety builds trust**: Food-safety integration differentiates and protects
4. **Multiple revenue paths reduce risk**: Subscription model provides early stability
5. **Honest limitations**: Synthetic data, no real merchant data, no consumer app

### The Strongest Product

> "The strongest product is not the one with the most features, but the one with the clearest user, sharpest decision problem, most defensible ML logic, and most honest implementation boundary."

---

## Appendix: Product Decisions Summary

| Feature                 | Status  | Rationale               |
| ----------------------- | ------- | ----------------------- |
| Consumer marketplace    | NOT MVP | Focus on merchant first |
| Payment checkout        | NOT MVP | Decision support focus  |
| Hawker onboarding       | Phase 3 | Beachhead segment first |
| Collaborative filtering | Future  | No interaction data     |
| Reinforcement learning  | Future  | Cold start, complexity  |
| Food-safety rules       | MVP     | Core product feature    |
| Baseline comparisons    | MVP     | Validates ML value      |
| Synthetic data          | MVP     | No real data available  |

---

_Notes prepared for executive report. Some metrics to be filled after model training on actual synthetic data._
