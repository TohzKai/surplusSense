# SurplusSense: AI Decision Cockpit for F&B Merchants

**SMU MBA Machine Learning — Individual Project**
**April 2026**

---

## 1. The Problem

Singapore generated 755,000 tonnes of food waste in 2023, rising to 784,000 tonnes in 2024 (NEA Waste Statistics, 2024). Food services — restaurants, canteens, and hotels — accounted for 28% of Singapore's food waste in 2022, approximately 211,000 tonnes (NEA, 2022). Singapore imports over 90% of its food supply, which makes food waste a national food-security concern, not just an environmental one (NEA, MSE 2024). The edible portion of this waste represents unrealised value — the Singapore Environment Council estimates the commercial sector loses approximately SGD 342 million annually to food waste.

The core operational problem sits on the **merchant side**, and no current platform addresses it. F&B merchants producing surplus food face three compounding challenges:

- **Surplus is unpredictable.** Without a forecast, merchants either over-produce (direct cost of waste) or under-produce (forgone revenue). Manual intuition does not reliably account for day-of-week patterns, weather, events, or historical trends.
- **Discount decisions are reactive.** When surplus occurs, discounting is ad hoc — a best-guess on price with no systematic recovery calculation.
- **Incumbent platforms ignore merchants.** Treatsure and Yindii are consumer-facing: they help consumers find discounted food, but leave merchants to guess their own surplus quantities and set their own prices. The merchant's core problem — predicting surplus before it happens — is unaddressed.

Singapore's F&B landscape is dominated by small-to-mid operators: bakeries, cafés, and restaurants operating with predictable category mix and 5–50 daily surplus units. This segment is digitally ready, has structured operations, and bears disproportionate waste costs. Hawker stalls, while significant, are deferred to a later phase due to regulatory complexity (journal 0002).

---

## 2. The Solution

SurplusSense is an **upstream operating intelligence platform** — not another consumer marketplace. It predicts surplus before it happens, recommends optimal discount actions, calculates revenue recovery, and screens for food safety. Every transaction improves the model, compounding accuracy over time.

### Three Core Capabilities

**1. Surplus Prediction — XGBoost model**

The model analyses 47 engineered features spanning time patterns (day-of-week, cyclical encoding), lag history (yesterday's surplus, same weekday last week), rolling aggregates (7-day surplus average and variance), merchant-level benchmarks, and category-level benchmarks. Trained on 4,027 synthetic records across 15 merchants and 13 categories, with 5-seed random holdout validation.

XGBoost (n_estimators=250, max_depth=13, learning_rate=0.295) achieves a holdout MAE of **0.68 units** against a Historical Average baseline of 2.40 — a **72% reduction in prediction error**. XGBoost wins all 5 holdout seeds against tuned Random Forest (0.87 MAE).

**2. Discount Recommendation Engine**

A 10-tier rule-based system recommends a discount percentage (20–70% off) based on surplus quantity, remaining shelf life, and category. Every recommendation includes: estimated revenue recovery (discounted price × predicted surplus), optimal listing time, and latest safe pickup window. Merchants see the recovery calculation, not just a price suggestion.

**3. Food Safety Screening**

Five prototype rules check holding time, shelf life remaining, storage type appropriateness, pickup window safety, and preparation time. Items return SAFE (listable), CAUTION (list with warnings), or BLOCK (unsafe to list). _This is an advisory prototype — not SFA-validated. See Limitations._

### The Data Moat

The value compounds: more merchant transactions → better surplus predictions → higher sell-through rates → greater merchant trust → more merchant onboarding → more data. Each prediction cycle improves accuracy, creating a compounding advantage that a new entrant cannot replicate without years of merchant data.

### Competitive Differentiation

|                                  | SurplusSense           | Too Good To Go     | Treatsure          | Yindii             |
| -------------------------------- | ---------------------- | ------------------ | ------------------ | ------------------ |
| **Primary focus**                | Merchant operations    | Consumer discovery | Consumer discovery | Consumer discovery |
| **ML-driven surplus prediction** | Yes                    | No                 | No                 | No                 |
| **Merchant-side value**          | Operating intelligence | None               | None               | None               |
| **Discount recommendation**      | Automated, tiered      | Merchant guess     | Manual             | Manual             |
| **Food safety gating**           | Built-in               | No                 | No                 | No                 |
| **Cold-start handling**          | Category benchmarks    | N/A                | N/A                | N/A                |

---

## 3. Data Exploration

The synthetic dataset (4,027 records, 15 merchants, 13 categories, 90-day window) was explored to validate that simulated F&B surplus patterns match domain expectations before ML training.

![Surplus by category](outputs/eda_surplus_by_category.png)
_Figure 1: Surplus quantity distribution by product category. Bento Sets and Rice Dishes show highest median surplus; bakery categories cluster tightly._

![Day-of-week heatmap](outputs/eda_dow_heatmap.png)
_Figure 2: Mean daily surplus by merchant type and day of week. Bakery merchants show elevated surplus mid-week; Small F&B peaks on weekends._

---

## 4. Approach, Results & Business Model

### ML Methodology

A supervised regression pipeline was built on a synthetic dataset (4,027 rows, 15 merchants, 13 categories, 19 source fields). The training pipeline uses: (1) feature engineering producing 31 raw variables (temporal, lag, rolling-window, merchant aggregates) that expand to 47 model inputs after one-hot encoding of categorical variables (merchant_type, product_category, storage_type); (2) three baseline models (Historical Average, Previous Day, Same Weekday Last Week); (3) hyperparameter tuning via RandomizedSearchCV (30 iterations); (4) XGBoost and Random Forest both trained and compared; (5) 5-seed random 80/20 holdout for headline validation; (6) 5-fold TimeSeriesSplit cross-validation as a production-readiness check.

![Merchant workflow](outputs/workflow_diagram.png)
_Figure 3: End-to-end merchant decision flow with example outputs (BAK001, Ciabatta, 2026-02-10). From input through prediction, recommendation, safety check, and recovery estimate._

As an illustrative example, consider Bakery 001 listing a Ciabatta product on a typical weekday. The pipeline predicts 11 units of surplus, calibrated against four similar bakeries by operating pattern. The recommendation engine evaluates the product's 93-hour shelf life and refrigerated storage, returning a 50% discount tier with a target list price of SGD 3.24 (down from SGD 6.47). Food safety screening confirms the listing is SAFE — holding time of 2 hours is within thresholds for refrigerated storage. Estimated revenue recovery is SGD 34.29 against a potential loss of SGD 68.58, a 50% recovery rate. The full decision takes under 200ms end-to-end on the deployed XGBoost model.

### Model Results

| Model                  | Holdout MAE | RMSE     | MAPE      | R²       |
| ---------------------- | ----------- | -------- | --------- | -------- |
| Historical Average     | 2.40        | 2.85     | 57.7%     | -0.12    |
| Previous Day           | 1.98        | 2.61     | 37.6%     | 0.07     |
| Same Weekday Last Week | 2.06        | 2.72     | 38.8%     | -0.01    |
| Random Forest (Tuned)  | 0.87        | 1.16     | 17.1%     | 0.83     |
| **XGBoost (Tuned)**    | **0.68**    | **0.91** | **12.6%** | **0.89** |

XGBoost wins the i.i.d. holdout decisively (72% improvement vs Historical Average baseline, 66% vs Previous Day baseline). On TimeSeriesSplit CV — which measures performance under temporal distribution shift — Random Forest scores better (RF: 1.07 MAE vs XGBoost: 1.22 MAE). This gap is informative, not disqualifying: gradient boosting captures static patterns powerfully, but RF's stronger regularization tolerates temporal shift more reliably. For pilot deployment, both would be monitored and a drift-aware ensemble considered.

### Business Model: Free Analytics + Transaction Fee

The platform launches with a free tier — surplus prediction and waste analytics dashboard — to break the chicken-and-egg bootstrap problem. No consumers without merchants; no merchants without an immediate reason to join. The analytics tier provides standalone value: merchants reduce waste even without a single consumer transaction, solving the cold-start problem and beginning data collection immediately.

A 15% transaction fee applies when surplus is sold through the marketplace. This rate undercuts Too Good To Go and similar surplus marketplaces, which typically charge 20–30% commission per transaction, is captured at the point of value realization (not upfront), and aligns platform revenue directly with merchant recovery outcomes.

**Illustrative unit economics:** A bakery with SGD 19 in daily surplus, selling 50% of surplus through the platform at an average 35% discount, recovers SGD 6.65 in merchant revenue per day and generates SGD 1.00 in platform fee — approximately SGD 30/month per active merchant during a 30-day month. At 75 active merchants (5% of SAM), monthly recurring platform revenue is SGD 2,250.

**Market sizing (illustrative):** Several thousand SFA-licensed F&B outlets operate across Singapore, with our initial focus on the small-to-mid independent segment (bakeries, cafés, single-location restaurants). TAM — several thousand SFA-licensed F&B outlets (illustrative; precise count to be validated against SFA registry). SAM — approximately 1,000–2,000 (estimated; bakeries, cafés, small restaurants with 5–50 daily surplus units) [footnote: SAM range based on industry segmentation; final figure to be validated against SFA registry pre-pilot]. SOM — 5% Year-1 capture = 50–100 merchants.

---

## 5. Limitations & Decision Trail

**Limitations:** Synthetic data only (pilot validation required). Food safety rules are a prototype (not SFA-validated). Cold-start merchants use category benchmarks. MVP is a single-tenant Streamlit app — Phase 2 requires multi-tenant infrastructure, auth, and MLOps pipeline.

**Roadmap:** Phase 1 — real merchant pilot, food-safety expert review, PDPA consent flows. Phase 2 — production stack (PostgreSQL, FastAPI), drift monitoring, consumer marketplace. Phase 3 — personalised recommender, NEA waste reporting, ASEAN expansion.

**Key decisions:** XGBoost deployed over RF (wins 5/5 holdout seeds, journal 0019). Free analytics tier + 15% transaction fee (solves cold-start, journal 0003). Surplus prediction before marketplace (builds data moat, journal 0001). PDPA and food-safety validation deferred to pilot (journals 0011, 0006).

---

_Per journal 0010: "The strongest product is not the one with the most features, but the one with the clearest user, sharpest decision problem, most defensible ML logic, and most honest implementation boundary."_

### Reproducibility

All pipelines use `RANDOM_SEED=42` for data generation, train/test splitting, and hyperparameter tuning. Multi-seed validation evaluates model stability across five holdout seeds (1, 7, 42, 123, 999). The synthetic dataset (4,027 rows, 15 merchants, 13 categories, 90-day window) is regenerated deterministically by `data/generate_synthetic_data.py`. Model training runs through `src/train_model.py`, which applies RandomizedSearchCV (30 iterations) on 5-fold TimeSeriesSplit for hyperparameter selection, then evaluates final models on a 5-seed random holdout (seeds 1, 7, 42, 123, 999). All embedded figures are regenerated by `scripts/generate_report_figures.py` from the same synthetic data.

**Sources:**

- National Environment Agency (NEA) Waste Statistics 2024
- NEA Food Waste Management 2023 baseline data
- Ministry of Sustainability and the Environment, F&B Sustainability Playbook (2024)
- Singapore Environment Council estimates
- Industry comparisons: Too Good To Go, Treatsure, Yindii public reporting
