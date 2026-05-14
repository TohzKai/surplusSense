# Executive Report: SurplusSense Decision Support

**SMU MBA Machine Learning — Individual Project | April 2026**

---

## 1. Executive Summary

SurplusSense helps food merchants convert end-of-day surplus uncertainty into faster, safer, and more margin-aware decisions. It is a decision-support product — not a dashboard — that translates surplus predictions into specific recommended actions under food-safety guardrails. The product is pilot-ready; commercial deployment requires a structured merchant pilot with 3–5 outlets.

Singapore generated 784,000 tonnes of food waste in 2024 (National Environment Agency). The merchant-side surplus decision — hold, monitor, discount, deep discount, donate, or discard — is where value is lost or recovered. Existing platforms help consumers discover discounted surplus; none help merchants decide what to discount, at what intensity, or when. SurplusSense fills this gap.

---

## 2. Problem Worth Solving

For F&B merchants — bakeries, cafés, and prepared-food outlets — the problem is a daily operational decision at 4pm: **what do I do with unsold inventory?**

The decision is genuinely hard:

- **Time pressure**: shelf life is already running down
- **Margin trade-off**: deeper discounts recover more revenue but erode margin on items that would have sold at full price
- **Safety risk**: items past safe holding times cannot be listed
- **Labour constraints**: staff must decide under operating pressure
- **Inconsistent judgment**: the same surplus item may receive different decisions across shifts

The monetisable gap is narrower than "food waste" broadly: small F&B merchants often know they may have surplus, but lack a structured way to decide what action to take before the item loses value. The key decision happens late in the operating day. This is not only a forecasting problem — it is a time-sensitive trade-off between revenue recovery, food safety, staff workload, brand risk, and customer experience.

**Target buyer**: Singapore-based bakery, café, or prepared-food outlet with recurring end-of-day surplus and enough daily volume for recovered value to exceed SGD 99–299 monthly subscription.

---

## 3. Product Approach

SurplusSense is a **decision-support product** — it translates surplus-risk predictions into specific merchant actions. The six-step workflow:

| Step                           | What happens                                                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **1 — Enter context**          | Merchant selects product category, storage type, holding time, shelf life                                        |
| **2 — Predict surplus**        | XGBoost model estimates expected surplus units from 46 leakage-aware features                                    |
| **3 — Recommend action**       | Rule engine maps surplus quantity and shelf life to HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD |
| **4 — Screen for safety**      | Five deterministic checks return SAFE / CAUTION / BLOCKED                                                        |
| **5 — Estimate recovery**      | System calculates discounted revenue recovery vs potential loss                                                  |
| **6 — Explain recommendation** | Merchant sees the specific reason for the recommended action                                                     |

**Design choice: rules over learning.** Recommendations are rule-based because food safety cannot be entrusted to an opaque learned policy. A merchant who lists an unsafe item creates liability that no accuracy metric offsets. Rule-based logic is fully explainable — every recommendation traces to a specific rule.

---

## 4. ML/AI Architecture and Results

### Why This Is an ML Decision-Support Product, Not a Dashboard

Most F&B tech products show prediction scores. This product shows decisions. The distinction matters:

- A merchant with 11 surplus units of Ciabatta needs to know: **50% discount, list now, SGD 35 recovered** — not "MAE 0.64"
- The prediction layer (XGBoost) estimates _what will happen_; the downstream layers decide _what to do about it_
- Cold-start merchants (no historical data) receive category-benchmark estimates, so the product is useful from day one

The architecture deliberately separates prediction from prescription: **the model estimates what may happen; the rule and safety layers decide what action is permissible and commercially sensible.**

**Architecture layers:**

| Layer               | Component                                 | Role                                                        |
| ------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| Input               | Merchant/item context                     | Merchant enters product and outlet details                  |
| Feature engineering | 46 features                               | Lag, rolling, expanding-window, temporal, category features |
| Prediction          | XGBoost                                   | Estimates surplus units                                     |
| Validation          | Temporal holdout + TimeSeriesSplit        | Forward-looking evaluation                                  |
| Leakage control     | Expanding-window aggregates with shift(1) | Prevents future-information lookahead                       |
| Decision            | Rule-based recommendation engine          | Converts surplus prediction into action                     |
| Governance          | Food-safety rules                         | BLOCK/CAUTION/SAFE overrides commercial optimisation        |
| Output              | Merchant decision cockpit                 | Recommended action + recovery estimate + explanation        |

**Design decisions:**

| Design decision       | Option rejected          | Final choice                              | Why it matters                                         |
| --------------------- | ------------------------ | ----------------------------------------- | ------------------------------------------------------ |
| Train/test split      | Random split             | Temporal holdout                          | Prevents inflated accuracy from future information     |
| Feature aggregation   | Full-dataset averages    | Expanding-window aggregates with shift(1) | Prevents target leakage                                |
| Recommendation logic  | Learned black-box policy | Transparent rule engine                   | Safer for food handling; easier for merchants to trust |
| New merchant handling | Require historical data  | Category benchmark fallback               | Makes product usable from day one                      |
| Output format         | Prediction score         | Recommended action + recovery value       | Matches real merchant decision workflow                |

**Model results** (synthetic training data, 4,027 records, 15 merchants, 13 categories, 90-day window):

| Model               | Temporal Holdout MAE | vs Historical Average |
| ------------------- | -------------------: | --------------------- |
| Historical Average  |                 1.49 | —                     |
| Previous Day        |                 2.01 | −35%                  |
| **XGBoost (Tuned)** |             **0.64** | **−57%**              |

5-fold TimeSeriesSplit CV MAE: 1.38 ± 1.22 (higher variance reflects distributional shift in synthetic data).

**Validation caveat:** Results are from synthetic/prototype data. They indicate technical feasibility and feature-signal logic, not production accuracy. Aggregate features use expanding-window logic to prevent target leakage. Real merchant pilot data is required before commercial deployment.

---

## 5. Business Case

**Who pays:** Bakeries, cafés, and small F&B operators with 5–50 daily surplus units in Singapore.

**Why they pay:** Recovered surplus value plus avoided disposal costs could exceed SGD 99–299 per month per outlet, subject to pilot validation.

**Merchant unit economics:**

| Scenario     | Daily recovered value | Monthly recovered value (26 operating days) | Supports pricing                     |
| ------------ | --------------------: | ------------------------------------------: | ------------------------------------ |
| Conservative |             SGD 6/day |                               SGD 156/month | Entry plan at SGD 99/month           |
| Base case    |            SGD 12/day |                               SGD 312/month | Mid plan at SGD 199/month            |
| Strong case  |            SGD 20/day |                               SGD 520/month | SGD 299/month plan + transaction fee |

The commercial case does not require every surplus decision to generate large savings. Even SGD 6–12 daily recovery can justify the low-to-mid subscription tier if staff use the system consistently.

**Proposed pricing** (pilot-stage hypothesis):

| Revenue stream                      | Rationale                                                          |
| ----------------------------------- | ------------------------------------------------------------------ |
| Monthly SaaS: SGD 99–299 per outlet | Predictable recurring revenue; easier for merchants to budget      |
| 15% recovered-value fee             | Aligns SurplusSense revenue with merchant benefit                  |
| Future marketplace integration fee  | Phase 2 if product connects surplus items to consumer channels     |
| ESG/reporting module                | Additional value for chains needing waste reporting across outlets |

**Buyer-validation table:**

| Assumption                           | Current evidence                                      | Validation needed                              | Success metric                  |
| ------------------------------------ | ----------------------------------------------------- | ---------------------------------------------- | ------------------------------- |
| Merchants have surplus pain          | Singapore F&B waste 784k tonnes/year (NEA)            | 4-week pilot with 3–5 merchants                | Waste reduction % per outlet    |
| Recommendation acceptance rate       | Workflow designed for merchant trust signals          | Live pilot observation                         | Acceptance rate ≥ 60%           |
| Recovered value exceeds cost         | Model estimates SGD 6–20/day on prototype             | Pilot measures actual recovered revenue        | Recovered value ≥ SGD 200/month |
| Safety gate prevents unsafe listings | 5 deterministic rules with BLOCK for high-risk        | Rules tested against real operating conditions | Unsafe recommendation rate = 0  |
| Staff use dashboard daily            | Low-friction manual entry; no POS required in Phase 1 | Pilot observes daily active usage              | ≥ 4 sessions/week per outlet    |

---

## 6. Pilot Validation Plan

The next step is a 4-week engagement with 3–5 volunteer bakeries or cafés in Singapore:

- 1–2 daily surplus decision cycles per outlet
- Staff enter item context manually via the dashboard
- Recommendations issued; staff record accept / override / ignore with brief reason

**Success metrics:**

| Metric                         | Target                                                 |
| ------------------------------ | ------------------------------------------------------ |
| Daily active usage             | At least 70% of operating days                         |
| Recommendation acceptance rate | At least 50%                                           |
| Average recovered value        | At least SGD 6–12 per day                              |
| Avoided unsafe listing         | Zero unsafe items recommended for sale                 |
| Staff decision time            | Reduced versus manual process                          |
| Willingness to pay             | At least 2 of 5 outlets willing to pay SGD 99+ monthly |

The pilot produces real-data inputs required before full deployment: POS sales history, inventory snapshots, actual disposal records, safety rule calibration, and willingness-to-pay signals. Because the current product uses synthetic data, the pilot is required before production performance claims.

---

## 7. Why This Is Ready for Assessment

SurplusSense satisfies the individual assignment requirement because it is a **working interactive product**, not a slide concept or notebook. The user can enter merchant and item context, receive a surplus prediction, see a recommended action, review food-safety status, and estimate revenue recovery.

The product demonstrates maturity beyond the weekly prototype in four ways:

1. **Additional decision layers**: prediction is combined with recommendation, food-safety gating, and recovery-value estimation
2. **Improved model discipline**: temporal validation and leakage-aware aggregate features reduce risk of overstated model performance
3. **Improved user experience**: dashboard is organised around merchant decisions rather than technical metrics
4. **Commercial path**: pilot plan defines target buyers, pricing logic, success metrics, and next validation steps

The product is **pilot-ready**: not yet production-validated, but sufficiently complete for a merchant, investor, or company sponsor to evaluate.

---

## 8. Limitations and Next Validation

| Limitation                            | Impact                                             | Mitigation                                                  |
| ------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- |
| **Synthetic training data**           | Model accuracy on real merchant data unknown       | Retrain on pilot merchant data before production            |
| **Food safety rules advisory**        | Not SFA-validated; merchant assumes responsibility | Clear disclaimer in UI; BLOCK/CAUTION/SAFE is guidance only |
| **Single-tenant MVP**                 | No multi-merchant support                          | Phase 2 multi-tenant infrastructure                         |
| **Cold-start uses category averages** | Less accurate for unusual merchants                | Improves as merchant-specific data accumulates              |
| **No POS/inventory integration**      | Manual entry required                              | Phase 2 POS/inventory integration                           |
| **No live pilot conducted**           | No real merchant validation                        | Structured 4-week pilot plan defined                        |

---

## 9. References

- National Environment Agency, Food Waste Management, Singapore, 2024
- SurplusSense Synthetic Data Generator: `data/generate_synthetic_data.py`
- Model and Evaluation Pipeline: `src/train_model.py`, `src/feature_engineering.py`
- SMU MGMT655 Machine Learning for Decision Making — Individual Assignment Requirements
- Yindii, Treatsure, Too Good To Go (Singapore surplus-food platform examples)

---

_SurplusSense is a pilot-ready decision-support prototype. It is not production-deployed, not SFA-validated, and not commercially live. All performance metrics are from synthetic data and require pilot validation before commercial claims._
