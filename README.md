# SurplusSense: Decision Intelligence for F&B Merchants

A decision-support product that helps food merchants decide what to discount, donate, hold, or discard before unsold inventory becomes waste — combining ML-assisted surplus prediction with transparent rule-based recommendation logic.

---

## Individual Assignment Grading Guide

Primary grading artefacts for MGMT655 Individual Assignment:

1. **Working product**: `app/streamlit_app.py`
2. **Executive report, max 4 pages**: `docs/EXECUTIVE_REPORT.pdf`
3. **COC decision log**: `COC_DECISION_LOG.md`
4. **Test and model evidence**:
   - `tests/unit/` — 75 passing unit tests
   - `outputs/model_comparison.csv` — official temporal holdout metrics (XGBoost MAE 0.6355)
   - `outputs/model_results.csv` — baseline comparison

SurplusSense is a **pilot-ready decision-support cockpit** for F&B merchants. It is not merely a forecasting dashboard: the ML layer estimates surplus risk, while the business layer translates that risk into merchant actions such as hold, monitor, discount, deep-discount, donate, or discard. The product is designed for pilot validation before production deployment.

**Supplementary artefact**: `docs/INDIVIDUAL_REPORT.pdf` is an extended stakeholder handover report for three audiences — business manager, app user, and fellow developer. The official executive report for grading is `docs/EXECUTIVE_REPORT.pdf`.

---

## Reproducible Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/unit/ -q
streamlit run app/streamlit_app.py
```

> **Note:** `pyproject.toml` is retained for project metadata only. The authoritative setup path is `pip install -r requirements.txt`.

---

## For Grading — Start Here

| File                             | Purpose                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------- |
| `app/streamlit_app.py`           | **Working interactive product** — run with `streamlit run app/streamlit_app.py` |
| `docs/INDIVIDUAL_REPORT.md`     | Individual assignment report — 4–8 pages, three-audience structure              |
| `COC_DECISION_LOG.md`            | Prototype-to-product decision journey and judgment evidence                     |
| `src/`                           | Reproducible ML pipeline with 75 passing unit tests                             |

**Private repository:** https://github.com/TohzKai/surplusSense

Prof. Jack Hong has been invited as a collaborator for grading. The repository will remain private and access will be removed after grading, as instructed.

### How to Run

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### ML Technique Family

SurplusSense uses **supervised regression with XGBoost** — predicting surplus units as a continuous value. This differs from the team project, WanderLess, which uses **recommender systems and optimization** (hybrid tourist-guide matching, TruncatedSVD collaborative filtering, and itinerary optimization).

### Test Command

```bash
python -m pytest tests/unit/ -q
# Result: 75 passed
```

### Official Model Metric

XGBoost temporal holdout MAE: **0.6355** (from `outputs/model_comparison.csv` — temporal holdout on last 20% of dates). The model improves over the Historical Average baseline by **57%**.

---

## Final Professor Review Path

Recommended review order:

1. `docs/EXECUTIVE_REPORT.md` — executive summary, business case, and results
2. `app/streamlit_app.py` — working interactive product
3. `COC_DECISION_LOG.md` — decision journey and final decision audit
4. `workspaces/SurplusSense/01-analysis/04-final-positioning.md` — why the product narrowed from marketplace to merchant cockpit
5. `workspaces/SurplusSense/02-plans/01-implementation-plan.md` — final MVP scope and implementation plan
6. `workspaces/SurplusSense/03-user-flows/01-merchant-flows.md` — final merchant decision flow
7. `workspaces/SurplusSense/04-validate/grading-self-assessment-v6-final.md` — final validation and supersession of older assessments
8. `workspaces/SurplusSense/briefs/01-product-brief.md` — final product definition
9. `workspaces/SurplusSense/journal/0030-DECISION-final-scope-and-assessment-alignment.md` — final scope decision
10. `workspaces/SurplusSense/todos/completed/008-final-assessment-alignment.md` — final assessment-alignment closure

---

## Product Overview

SurplusSense is not an ML dashboard. It is a **decision-support product** that translates surplus-risk predictions into specific merchant actions.

The product delivers five decision-support capabilities:

1. **Surplus prediction** — estimates expected waste units (XGBoost model, 31 raw features → 47 model input columns after one-hot encoding)
2. **Action recommendation** — suggests HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD based on quantity and time pressure
3. **Discount tier guidance** — maps surplus and shelf life to a specific discount intensity (20–70%)
4. **Food safety screening** — checks shelf life, holding time, storage type, and pickup window; returns SAFE / CAUTION / BLOCK
5. **Recovery value estimation** — calculates estimated revenue recovery vs potential loss

The output is a **recommended business action** — not a prediction score.

---

## Who It Is For

- Bakeries, cafés, and small F&B operators with 5–50 daily surplus units
- Singapore-based, SFA-licensed food operators
- Food retailers, supermarket fresh-food sections, prepared-food operators

The product is designed for merchants who already know they have a surplus problem and need structured guidance on what to do about it.

---

## Why SurplusSense Is Not Just an ML Dashboard

Most F&B tech products show prediction scores. This product shows decisions.

The prediction layer (XGBoost) estimates _what will happen_. The downstream layers decide _what to do about it_. This distinction matters:

- A merchant with 11 surplus units of Ciabatta needs to know: **50% discount, list now, SGD 35 recovered** — not just "MAE 0.68"
- The rule-based recommendation and safety layers convert the prediction into an action the merchant can take immediately
- Cold-start merchants (no historical data) receive category-benchmark estimates, so the product is useful from day one

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic training data (one-time)
python data/generate_synthetic_data.py

# Train model and evaluate (saves to outputs/)
python src/train_model.py

# Run the decision-support dashboard
streamlit run app/streamlit_app.py
```

The dashboard opens at `http://localhost:8501`.

---

## How to Use the Dashboard

1. **Open the app** — streamlit dashboard launches at localhost:8501
2. **Select or enter merchant context** — merchant type, product category, storage type, preparation time
3. **Enter item details** — original price, shelf life, current holding time
4. **Review the recommendation** — the app shows:
   - Predicted surplus quantity (XGBoost model)
   - Recommended action (DISCOUNT / MONITOR / HOLD / etc.)
   - Recommended discount tier (20–70%)
   - Food safety status (SAFE / CAUTION / BLOCK)
   - Estimated revenue recovery vs potential loss
   - Why this recommendation was made (reasoning displayed)
5. **Adjust inputs** — rerun with different parameters to compare scenarios

---

## Reproducibility

All pipelines use `RANDOM_SEED=42` for deterministic results.

```bash
python data/generate_synthetic_data.py   # Regenerate training data
python src/train_model.py                # Retrain model, save to outputs/surplus_model.pkl
python src/evaluate_model.py             # Display official temporal holdout metrics from outputs/model_comparison.csv
pytest tests/unit/ -q                   # Run unit tests (75 passing)
```

**Test results:** 75 unit tests across 5 modules — all passing.
**Model outputs:** `outputs/model_results.csv`, `outputs/metrics_summary.csv`
**Trained model:** `outputs/surplus_model.pkl`

---

## Assignment Deliverables

This submission includes all required deliverables:

| Deliverable                    | File                             | Description                                                                                                     |
| ------------------------------ | -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Working interactive product    | `app/streamlit_app.py`           | Streamlit dashboard with full decision workflow                                                                 |
| Executive report (max 4 pages) | `docs/EXECUTIVE_REPORT.md`       | Business case, worked example, model results                                                                    |
| COC decision log               | `COC_DECISION_LOG.md`            | Prototype-to-product decision journey                                                                           |
| Supporting deck                | `DIGITAL_TRANSFORMATION_DECK.md` | 8-slide executive presentation                                                                                  |
| Pilot validation plan          | `PILOT_VALIDATION_PLAN.md`       | Proposed 4-week merchant pilot: recovery value, adoption, safety exceptions, and willingness-to-pay assumptions |

---

## Key Files for Grading

| Category                  | File                             | What It Shows                                                    |
| ------------------------- | -------------------------------- | ---------------------------------------------------------------- |
| **Working product**       | `app/streamlit_app.py`           | Interactive decision-support dashboard                           |
| **ML pipeline**           | `src/train_model.py`             | XGBoost training, temporal 80/20 holdout                         |
| **Feature engineering**   | `src/feature_engineering.py`     | 31 raw features → 47 model input columns; temporal, lag, rolling, expanding-window aggregates |
| **Recommendation engine** | `src/recommendation_engine.py`   | 10-tier discount logic, recovery calculation                     |
| **Safety rules**          | `src/food_safety_rules.py`       | 5 safety checks: BLOCK/CAUTION/SAFE                              |
| **Cold-start**            | `src/recommendation_engine.py`   | Category benchmark fallback for new merchants                    |
| **Model evaluation**      | `src/evaluate_model.py` + `outputs/model_comparison.csv` | Official temporal holdout evaluation; diagnostic broader-dataset evaluation available with --diagnostic |
| **Tests**                 | `tests/unit/`                    | 75 passing unit tests                                            |
| **Model outputs**         | `outputs/model_comparison.csv`  | XGBoost MAE 0.6355 (temporal holdout) vs baseline 1.49          |
| **Executive report**      | `docs/EXECUTIVE_REPORT.md`       | 4-page business document                                         |
| **Decision log**          | `COC_DECISION_LOG.md`            | Decision journey, judgment evidence                              |
| **Deck**                  | `DIGITAL_TRANSFORMATION_DECK.md` | 8-slide executive presentation                                   |

---

## Model Performance

| Model               | Temporal Holdout MAE | vs Historical Average |
| ------------------- | -------------------- | --------------------: |
| Historical Average  | 1.49                 |                     — |
| **XGBoost (Tuned)** | **0.6355**           |              **−57%** |

Temporal holdout MAE (0.6355) is the primary metric — it reflects forward-looking prediction on the last 20% of dates, sorted chronologically. 5-fold TimeSeriesSplit CV MAE: 1.38 ± 1.22 (higher variance reflects distributional shift across temporal folds). Results from `outputs/model_comparison.csv`.

---

## ML Architecture

### Problem Type

Supervised regression: predict surplus units per item per day.

### Model

XGBoost regressor, tuned via 5-fold TimeSeriesSplit CV. Compared against Historical Average and Previous Day baselines.

### Feature Categories (31 raw fields → 47 model input columns after one-hot encoding)

| Category                   | Examples                                                              |
| -------------------------- | --------------------------------------------------------------------- |
| Merchant/outlet            | merchant type, category, storage type                                 |
| Product                    | original price, shelf life, preparation time                          |
| Temporal                   | day of week, weekend flag, month, sin/cos encodings                   |
| Lag                        | prev_day_surplus, same_weekday_last_week_surplus                      |
| Rolling                    | surplus_7day_avg, surplus_7day_max, surplus_7day_std                  |
| Expanding-window aggregate | merchant_avg_surplus, category_avg_surplus, dow_avg_surplus           |
| Derived                    | holding_vs_shelf_ratio, surplus_rate_7day, production_vs_merchant_avg |

### Validation

- **Temporal 80/20 holdout** (last 20% of dates as holdout, sorted by date) — primary metric
- **5-fold TimeSeriesSplit CV** — additional validation

Random split is NOT used as the primary evaluation method because real deployment predicts future surplus from past data; random split would allow future information to inflate accuracy estimates.

### Leakage Control

All aggregate features use **expanding-window logic with shift(1)**:

```python
grp = df.groupby("merchant_id")["surplus_quantity"]
df["merchant_avg_surplus"] = grp.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
```

For each row at date D, aggregates use only data from dates strictly before D. Rolling features use `.shift(1)` before `.rolling()`. The `surplus_vs_merchant_avg` interaction feature (which used current-row target) was removed entirely.

### Output

The model outputs a **predicted surplus quantity**. Downstream layers convert this into:

- Recommended action (HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD)
- Discount tier (20–70%)
- Food-safety status (SAFE / CAUTION / BLOCKED)
- Estimated recovery value

### Architecture Flow

```
Input data → Feature engineering → XGBoost surplus prediction
→ Recommendation rules → Food-safety gate → Recovery-value estimate
→ Merchant decision cockpit
```

---

## Why This Is Not a Default COC Demo

SurplusSense goes beyond a default COC-generated prototype in five ways:

1. **Leakage-aware temporal validation** — temporal holdout and TimeSeriesSplit, not generic random split
2. **Prediction → action conversion** — XGBoost output feeds a rule engine, not a dashboard
3. **Food-safety gating** — commercial optimisation does not override safety
4. **Recovery-value estimation** — ML output linked to business value, not just accuracy metrics
5. **Pilot validation plan** — usage, recovery, safety, and willingness-to-pay metrics defined

---

## Final MVP Scope

**Included:**
- Streamlit merchant cockpit
- Supervised ML surplus prediction with XGBoost
- Temporal validation and leakage-aware feature engineering
- Deterministic recommendation rules
- Food-safety gating
- Recovery-value estimation
- Explanation layer
- Unit tests
- Executive report
- COC decision log
- Process evidence trail

**Not included:**
- Consumer marketplace
- Payments
- QR pickup / collection
- Delivery logistics
- POS integration
- Real merchant deployment

## Limitations (Honestly Stated)

- **Data:** Results based on synthetic F&B data. Pilot validation with real merchant data required before production deployment.
- **Safety rules:** Prototype advisory only — not SFA-validated. Merchant assumes responsibility for listing decisions.
- **Cold-start:** New merchants use category benchmarks. Accuracy improves as merchant-specific data accumulates.
- **No POS integration:** Manual item entry required in Phase 1. Automated input planned for Phase 2.
- **Single-tenant:** Phase 1 runs on a single-merchant basis. Multi-tenant infrastructure for Phase 2.

---

## Project Structure

```
app/
  streamlit_app.py          # Decision-support dashboard
src/
  train_model.py            # XGBoost training + temporal 80/20 holdout
  feature_engineering.py    # 31 raw features → 47 model input columns; expanding-window aggregates
  recommendation_engine.py  # 10-tier discount engine + cold-start
  food_safety_rules.py     # 5 safety check functions
  evaluate_model.py         # Display official temporal holdout metrics (use --diagnostic for broader-dataset evaluation)
data/
  generate_synthetic_data.py # Synthetic F&B data generator
  synthetic_fnb_data.csv    # Training data (4,027 rows, 15 merchants)
outputs/
  surplus_model.pkl        # Trained XGBoost model
  model_results.csv        # Evaluation metrics
  metrics_summary.csv      # MAE/RMSE/MAPE/R² by model
tests/unit/
  test_data_generator.py
  test_feature_engineering.py
  test_food_safety_rules.py
  test_recommendation_engine.py
  test_model_training.py
```

---

## Technology Stack

- **Backend:** Python, scikit-learn, XGBoost
- **Dashboard:** Streamlit (interactive UI)
- **Data:** Pandas, NumPy
- **Evaluation:** Temporal 80/20 holdout + 5-fold TimeSeriesSplit CV
- **Testing:** pytest (75 unit tests)
- **Random seed:** 42 (all pipelines)

---

_SurplusSense was developed iteratively with structured validation at each stage. All product decisions reflect deliberate business reasoning — not automated defaults._

---

## GitHub Submission Note

This repository is curated for GitHub-link submission. Local AI-tool settings, cache files, SDK/template tests, deployment files, scripts, and old marketplace/payment specs have been removed or ignored so the professor can focus on the final product and COC decision evidence.

Previous workspace files that used the early "Food App" working title are retained in `workspaces/SurplusSense/journal/` with explicit historical-notes headers explaining they predate the final SurplusSense repositioning.

## ML Technique Family Declaration

SurplusSense foregrounds **supervised machine learning** through XGBoost surplus prediction, combined with deterministic recommendation and food-safety rules. This differs from the team project, WanderLess, which foregrounds recommender systems and optimization through hybrid tourist-guide matching, TruncatedSVD collaborative filtering, content-based compatibility scoring, and itinerary optimization.

The supervised regression approach (XGBoost predicting surplus units as a continuous value) was chosen for temporal holdout performance, explainability, and safety-critical applicability.

---

## Final Assessment Evidence Map

| MGMT655 Requirement           | Evidence in Repository                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Working interactive product   | `app/streamlit_app.py` — Streamlit decision cockpit                                                                 |
| Executive report max 4 pages  | `docs/EXECUTIVE_REPORT.md` (~197 lines)                                                                             |
| COC decision log              | `COC_DECISION_LOG.md` — 12 sections, human-judgment audit                                                           |
| Problem worth solving         | `docs/EXECUTIVE_REPORT.md` §2; `workspaces/SurplusSense/01-analysis/04-final-positioning.md`                        |
| ML/AI depth                   | `README.md` ML Architecture; `src/feature_engineering.py`; `models/model_metadata.json`                             |
| Business case                 | `docs/EXECUTIVE_REPORT.md` §5; `PILOT_VALIDATION_PLAN.md`                                                           |
| User flows                    | `workspaces/SurplusSense/03-user-flows/01-merchant-flows.md`                                                        |
| Validation                    | `workspaces/SurplusSense/04-validate/grading-self-assessment-v6-final.md`                                           |
| Process journal               | `workspaces/SurplusSense/journal/` — 29 entries                                                                     |
| Execution todos               | `workspaces/SurplusSense/todos/completed/`                                                                          |
| Not a default COC demo        | `COC_DECISION_LOG.md` §11 — human-judgment decision audit                                                           |
| Different ML technique family | Supervised XGBoost regression; differs from team project WanderLess which uses recommender systems and optimization |

### Recommended Validation Command

```bash
python -m pytest -q
```

Result: **75 passed** — all SurplusSense product unit tests. `pytest.ini` at repository root restricts discovery to `tests/unit/`.
