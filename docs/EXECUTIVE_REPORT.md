# Executive Report: SurplusSense Decision Support

**SMU MBA Machine Learning — Individual Project | April 2026**

---

## 1. Executive Summary

SurplusSense helps food merchants convert end-of-day surplus uncertainty into faster, safer, and more margin-aware decisions. It is a merchant-side decision-support cockpit — not a consumer marketplace — that translates surplus predictions into specific recommended actions (hold, monitor, discount, deep discount, donate, discard) under food-safety guardrails. Singapore generated 784,000 tonnes of food waste in 2024 (NEA); the merchant-side decision at 4pm is where that value is lost or recovered. No existing platform helps merchants decide what to discount, at what intensity, or when. SurplusSense fills this gap. The product is pilot-ready; commercial deployment requires a structured 4–6 week merchant pilot with 2–5 outlets.

---

## 2. Problem Worth Solving

For F&B merchants — bakeries, cafés, and prepared-food outlets — the problem is a daily operational decision at 4pm: **what do I do with unsold inventory?**

The decision is genuinely hard:
- **Time pressure**: shelf life is already running down
- **Margin trade-off**: deeper discounts recover more revenue but erode margin on items that would have sold at full price
- **Safety risk**: items past safe holding times cannot be listed
- **Labour constraints**: staff must decide under operating pressure
- **Inconsistent judgment**: the same surplus item may receive different decisions across shifts

The monetisable gap is narrower than "food waste" broadly: merchants often know they may have surplus, but lack a structured way to decide what action to take before the item loses value. This is not only a forecasting problem — it is a time-sensitive trade-off between revenue recovery, food safety, staff workload, and customer experience.

**Target buyer**: Singapore-based bakery, café, or prepared-food outlet with recurring end-of-day surplus and enough daily volume for recovered value to exceed SGD 99–299 monthly subscription.

---

## 3. Product Approach

SurplusSense is a **decision-support product** — it translates surplus-risk predictions into specific merchant actions. The six-step workflow:

| Step | What happens |
|------|-------------|
| **1 — Enter context** | Merchant selects product category, storage type, holding time, shelf life |
| **2 — Predict surplus** | XGBoost model estimates expected surplus units from 47 engineered features |
| **3 — Recommend action** | Rule engine maps surplus quantity and shelf life to HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD |
| **4 — Screen for safety** | Five deterministic checks return SAFE / CAUTION / BLOCKED |
| **5 — Estimate recovery** | System calculates discounted revenue recovery vs potential loss |
| **6 — Explain recommendation** | Merchant sees the specific reason for the recommended action |

**Why rules over learning**: Food safety cannot be entrusted to an opaque learned policy. A merchant who lists an unsafe item creates liability that no accuracy metric offsets. Rule-based logic is fully explainable — every recommendation traces to a specific rule. The model estimates what *may* happen; the rule and safety layers decide what action is *permissible and commercially sensible*.

---

## 4. ML Architecture and Results

**Architecture:**

| Layer | Component | Role |
|-------|-----------|------|
| Input | Merchant/item context | 31 raw features: temporal, lag, rolling, expanding-window, product |
| Feature engineering | Expanding-window aggregates with shift(1) | Prevents target leakage; no future information in aggregates |
| Prediction | XGBoost | Estimates surplus units |
| Validation | Temporal 80/20 holdout + TimeSeriesSplit CV | Forward-looking evaluation; simulates real deployment |
| Decision | Rule-based recommendation engine | Converts surplus prediction into action |
| Governance | Food-safety rules | BLOCK/CAUTION/SAFE overrides commercial optimisation |
| Output | Merchant decision cockpit | Recommended action + recovery estimate + explanation |

**Key design decisions:**

| Decision | Choice | Why |
|----------|--------|-----|
| Train/test split | Temporal holdout | Random split would inflate accuracy using future information |
| Feature aggregation | Expanding-window with shift(1) | Prevents target leakage; each row only uses data before its date |
| Recommendation logic | Transparent rule engine | Food safety requires explainable logic; black-box learned policy rejected |
| New merchant handling | Category benchmark fallback | Makes product usable from day one without historical data |
| Output format | Recommended action + recovery value | Matches real merchant decision workflow, not a prediction score |

**Model results** (synthetic data, 4,027 records, 15 merchants, 13 categories, 90-day window):

| Model | Temporal Holdout MAE | vs Historical Average |
|-------|---------------------:|-|
| Historical Average | 1.49 | — |
| Previous Day | 2.01 | −35% |
| **XGBoost (Tuned)** | **0.6355** | **−57%** |

5-fold TimeSeriesSplit CV MAE: 1.38 ± 1.22 (higher variance reflects distributional shift across temporal folds).

---

## 5. Business Case and Pilot Validation

**Who pays**: Bakeries, cafés, and small F&B operators with 5–50 daily surplus units in Singapore.

**Why they pay**: Recovered surplus value plus avoided disposal costs could exceed SGD 99–299 per month per outlet, subject to pilot validation. Even SGD 6–12 daily recovery can justify the entry subscription tier if staff use the system consistently.

**Merchant unit economics:**

| Scenario | Daily recovered value | Monthly (26 operating days) | Supports pricing |
|----------|--------------------:|---------------------------:|-----------------|
| Conservative | SGD 6/day | SGD 156/month | Entry plan SGD 99/month |
| Base case | SGD 12/day | SGD 312/month | Mid plan SGD 199/month |
| Strong case | SGD 20/day | SGD 520/month | SGD 299/month + transaction fee |

**Proposed pricing**: Monthly SaaS SGD 99–299 per outlet (predictable recurring revenue); 15% recovered-value fee (aligns SurplusSense revenue with merchant benefit); ESG/reporting module for chains.

**Pilot design** (required before commercial deployment claims):
- **Duration**: 4–6 weeks with 2–5 merchant outlets
- **Data**: Daily sales, inventory, discount, donation, and disposal records from merchant POS/inventory systems
- **Success metrics**: Recommendation acceptance rate ≥ 60%; surplus reduction 10–15% vs baseline; recovered value ≥ SGD 200/outlet/month; zero safety incidents

---

_SurplusSense is a pilot-ready decision-support prototype. It is not SFA-validated and not commercially live. All performance metrics are from synthetic data and require validation with merchant POS/inventory data before commercial deployment claims._

**Source note**: Singapore generated 784,000 tonnes of food waste in 2024 (NEA waste statistics). Business impact estimates are derived from synthetic pilot data and model outputs; real merchant pilot data is required before commercial rollout.
