# Developer Handover — SurplusSense

**Product:** SurplusSense — AI Decision Cockpit for F&B Merchants
**Repository:** https://github.com/TohzKai/surplusSense
**ML Technique:** Supervised regression with XGBoost
**Status:** Pilot-ready; synthetic data only — real merchant pilot required before commercial deployment

---

## Repository Structure

```
surplusSense/
├── app/
│   └── streamlit_app.py          # Main product — Streamlit decision cockpit
├── src/
│   ├── train_model.py             # XGBoost training pipeline + temporal 80/20 holdout
│   ├── feature_engineering.py     # 31 raw features → 47 model input columns after one-hot encoding
│   ├── recommendation_engine.py   # 10-tier discount logic + cold-start fallback
│   ├── food_safety_rules.py       # 5 safety check functions (BLOCK/CAUTION/SAFE)
│   ├── evaluate_model.py          # Holdout evaluation + baseline comparison
│   └── data_generator.py          # Synthetic data generation
├── data/
│   ├── generate_synthetic_data.py # Data generator
│   └── synthetic_fnb_data.csv     # Training data (4,027 rows, 15 merchants)
├── outputs/
│   ├── surplus_model.pkl          # Trained XGBoost model (primary artifact)
│   ├── model_comparison.csv       # Temporal holdout results — XGBoost MAE 0.6355
│   ├── model_results.csv          # All model metrics (baselines + XGBoost)
│   ├── metrics_summary.csv        # Full metrics table
│   ├── cv_results.csv             # 5-fold TimeSeriesSplit CV results
│   ├── feature_importance.csv     # XGBoost feature importance ranking
│   ├── tuning_results.csv         # Random Forest hyperparameter search
│   └── xgb_tuning_results.csv     # XGBoost hyperparameter search
├── tests/
│   └── unit/                      # 75 passing unit tests
│       ├── test_data_generator.py
│       ├── test_feature_engineering.py
│       ├── test_food_safety_rules.py
│       ├── test_recommendation_engine.py
│       ├── test_model_training.py
│       └── test_leakage_awareness.py
├── docs/
│   ├── INDIVIDUAL_REPORT.md       # Individual assignment report (this package)
│   ├── DEVELOPER_HANDOVER.md      # This document
│   ├── USER_GUIDE.md              # End-user guide
│   └── EXECUTIVE_REPORT.md        # Executive summary (4-page)
├── COC_DECISION_LOG.md            # Prototype-to-product decision journey
├── FINAL_SUBMISSION_PACKAGE.md    # Submission package overview
├── README.md                      # Product overview
└── PILOT_VALIDATION_PLAN.md       # 4-week merchant pilot design
```

---

## Environment Setup

### Requirements

```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.6.0
streamlit>=1.25.0
plotly>=5.15.0
```

### Install

```bash
pip install -r requirements.txt
```

No external API keys are required. The app uses only synthetic data and local model files.

---

## How to Run the App

```bash
# 1. Generate training data (one-time)
python data/generate_synthetic_data.py

# 2. Train model (one-time; saves to outputs/surplus_model.pkl)
python src/train_model.py

# 3. Launch the dashboard
streamlit run app/streamlit_app.py
```

Dashboard opens at `http://localhost:8501`.

---

## How to Run Tests

```bash
python -m pytest tests/unit/ -q
# Result: 75 passed
```

To run with verbose output:
```bash
python -m pytest tests/unit/ -v
```

---

## How to Retrain or Evaluate the Model

### Retrain Model

```bash
python src/train_model.py
```

This will:
1. Load `data/synthetic_fnb_data.csv`
2. Engineer features via `src/feature_engineering.py`
3. Run 5-fold TimeSeriesSplit CV for Random Forest and XGBoost
4. Perform hyperparameter search (30 iterations each)
5. Train on temporal 80/20 split (last 20% of dates as holdout)
6. Compare RF vs XGBoost on holdout
7. Save best model to `outputs/surplus_model.pkl`
8. Save comparison to `outputs/model_comparison.csv`

### Evaluate Model

```bash
python src/evaluate_model.py
```

This command displays the official temporal holdout evaluation results from `outputs/model_comparison.csv`. These metrics are generated at training time using the last 20% of dates as the temporal holdout set — the same split used to train the model.

**Official reported metric:**
- XGBoost MAE: 0.6355 (temporal holdout)
- Improvement vs Historical Average baseline (MAE 1.49): 57%

A diagnostic broader-dataset evaluation is available with:
```bash
python src/evaluate_model.py --diagnostic
```
The diagnostic mode evaluates the model on the full engineered dataset (after dropping rows without lag features), producing a lower MAE (~0.47). This is **not** the official assignment metric because it evaluates on a non-holdout sample and can overstate performance.

---

## Key Files and What Each Does

### `src/feature_engineering.py`

The feature engineering pipeline. Creates 31 raw feature fields from the raw data, which are then one-hot encoded into 47 model input columns.

Key functions:
- `engineer_features()` — applies all feature engineering steps
- `get_feature_columns()` — returns the 31 raw feature names
- `prepare_features_for_model()` — one-hot encodes categoricals

**Leakage control:** All aggregate features use `shift(1)` expanding-window logic. For each row at date D, aggregates use only data from dates strictly before D. Lag and rolling features also use `shift(1)`.

### `src/train_model.py`

The model training pipeline. Key functions:
- `train_model()` — main entry point; runs full pipeline
- `run_cross_validation()` — 5-fold TimeSeriesSplit CV
- `run_xgboost_search()` — hyperparameter search for XGBoost
- `train_and_compare_models()` — evaluates RF vs XGBoost on temporal holdout

**Temporal holdout:** Uses last 20% of dates as holdout (sorted by date), not random split.

### `src/recommendation_engine.py`

The business rule layer. Key functions:
- `generate_recommendation()` — takes predicted surplus + safety status → returns action, discount tier, recovery estimate
- `predict_surplus_cold_start()` — category-benchmark fallback for new merchants

Recommendation tiers:
- HOLD: surplus < 3 units
- MONITOR: surplus 3–6 units
- DISCOUNT: surplus 6–10 units (20–40%)
- DEEP DISCOUNT: surplus 10+ units (50–70%)
- DONATE: safe + high surplus
- DISCARD: failed safety check

### `src/food_safety_rules.py`

Five safety check functions:
- `check_shelf_life()` — holding time vs. shelf life remaining
- `check_storage_type()` — storage compatibility
- `check_preparation_time()` — prep time vs. recommended holding window
- `check_pickup_window()` — time to list vs. shelf life remaining
- `check_temperature_hazard()` — category-specific temperature risks

Returns `SafetyResult` with status: BLOCK / CAUTION / SAFE.

### `app/streamlit_app.py`

Main product UI. Sections:
- **Decision Workflow header** — 5-step visual workflow
- **Executive Decision Summary** — top-level recommendation at a glance
- **Impact Today** — aggregate KPIs for selected date
- **Surplus Prediction** — predicted surplus with confidence context
- **Merchant Profile** — merchant cluster and operating profile
- **Model Performance** — temporal holdout metrics and baseline comparison
- **Discount Recommendation** — hero card with action, discount tier, recovery estimate
- **Food Safety** — safety status with per-check results
- **Phase 2 Listing Preview** — optional consumer listing preview
- **Revenue Recovery Simulator** — "what-if" discount slider
- **Export** — CSV download of recommendation

---

## Data Assumptions

### Training Data (`data/synthetic_fnb_data.csv`)

- 4,027 rows, 15 synthetic merchants, ~30 days of data
- 14 product categories, 3 merchant types (Bakery, Café, Small F&B)
- Price range: SGD 3–20 per unit
- Surplus generated with realistic merchant-specific variation
- Day-of-week, weekend, and promotional patterns embedded

**Limitation:** Data is synthetic. Real merchant data pilot is required before commercial deployment.

### Feature Engineering

- All aggregate features use **expanding-window logic with shift(1)** — no future leakage
- Lag features: `prev_day_surplus` (lag 1), `same_weekday_last_week_surplus` (lag 7)
- Rolling features: 7-day rolling mean, max, std (all use shift(1))
- Interaction features: `holding_vs_shelf_ratio`, `weekend_promotion`, `production_vs_merchant_avg`

---

## Known Limitations

1. **Synthetic data only** — model accuracy on real merchant data is unknown
2. **Single-tenant MVP** — no merchant authentication or data isolation
3. **Manual data entry** — no POS integration; items entered manually
4. **Food safety rules are advisory** — not SFA-validated; merchant assumes responsibility
5. **Cold-start uses category averages** — less accurate for unusual merchant profiles
6. **No model drift monitoring** — model accuracy may degrade over time without alerting
7. **No multi-merchant support** — app assumes single-merchant context

---

## Future Technical Improvements

### Phase 2 (Post-Pilot)

1. **POS integration** — automate item data entry from Square, Zettle, or iPad POS
2. **Multi-tenant infrastructure** — merchant auth, data isolation, per-merchant model calibration
3. **Real data retraining** — retrain on real merchant data after pilot
4. **Model drift monitoring** — automated alerting when holdout MAE degrades
5. **Consumer marketplace listing** — integrate with Too Good To Go or in-house consumer app
6. **Donation partner API** — automated charity matching for DONATE recommendations

### Post-Phase 2

7. **Reinforcement learning for discount optimization** — learn discount policy from actual merchant feedback (requires feedback loop)
8. **Real-time inventory integration** — connect to inventory management systems for live surplus prediction
9. **NEA waste reporting integration** — automated ESG waste reporting for chain operators
10. **Demand forecasting** — predict tomorrow's expected surplus using today's production data

---

## Random Seed

All pipelines use `RANDOM_SEED=42` for deterministic reproducibility. To change the seed:
1. Edit `data/generate_synthetic_data.py` — `RANDOM_SEED` constant
2. Edit `src/train_model.py` — `random_state=42` parameter
3. Re-run `python data/generate_synthetic_data.py && python src/train_model.py`

---

*This handover document supports the SMU MBA MGMT655 individual assignment requirement that a fellow developer can take over the app. For questions, refer to COC_DECISION_LOG.md for the full decision journey, or docs/INDIVIDUAL_REPORT.md for the executive summary.*
