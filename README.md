# SurplusSense Food App

SurplusSense is a merchant-facing AI decision cockpit for F&B surplus reduction. It predicts daily surplus quantities per product category using a supervised XGBoost regression model, recommends tiered discount pricing (20-70% off) based on shelf life and category rules, calculates estimated revenue recovery, and screens listings against food safety thresholds. The Streamlit dashboard is the primary interface; merchants input today's product mix and receive a ranked recommendation within seconds. The ML pipeline uses supervised regression (XGBoost with 5-seed holdout validation) and is evaluated against three baseline models.

---

## Quick Start

```bash
pip install -r requirements.txt
python data/generate_synthetic_data.py
python src/train_model.py
streamlit run app/streamlit_app.py
```

---

## Project Structure

```
app/                    Streamlit dashboard (merchant UI, prediction, recommendations)
src/                    ML pipeline modules
  train_model.py        XGBoost training, RandomizedSearchCV, model serialization
  feature_engineering.py 47-feature engineering (temporal, lag, rolling, aggregates)
  recommendation_engine.py  Tiered discount pricing, revenue recovery calculation
  food_safety_rules.py  SAFE/CAUTION/BLOCK screening rules
  evaluate_model.py      Holdout evaluation, metrics computation
data/                   Synthetic F&B data (4,027 rows, 15 merchants, 13 categories)
docs/                   Executive report, specifications
outputs/                Trained model (.pkl), CSVs, EDA figures
tests/unit/             59 unit tests (pytest)
specs/                  Domain specifications (ML, food safety, pricing, UX)
journal/                Design decision log (22 entries)
models/                 Model metadata (hyperparameters, feature names, validation results)
scripts/                Figure generation script
```

---

## Reproducibility

All pipelines use `RANDOM_SEED=42`. Regenerate everything:

```bash
python data/generate_synthetic_data.py     # Regenerate data/synthetic_fnb_data.csv
python src/train_model.py                  # Retrain model, save to outputs/surplus_model.pkl
python scripts/generate_report_figures.py   # Regenerate EDA figures and workflow diagram
```

---

## Documentation

- `docs/EXECUTIVE_REPORT.md` — Executive report (4 pages, 3 figures)
- `journal/` — 22 journal entries: scoping decisions, model trade-offs, implementation rationale
- `models/model_metadata.json` — XGBoost hyperparameters, feature names, 5-seed validation results
- `specs/` — Domain specifications (ML surplus prediction, recommendations, food safety, pricing)

---

## Testing

```bash
pytest tests/unit/ -q
```

59 tests, all passing. Tests cover: feature engineering, recommendation engine, food safety screening, model evaluation.

---

## Docker

```bash
docker build -t surplussense .
docker run -p 8501:8501 surplussense
```

Docker build was not verified locally (Docker not installed). The Dockerfile follows standard Python image conventions and has been reviewed for correctness.

---

## Limitations

- Synthetic data only — results are based on generated F&B patterns, not real merchant data; pilot validation required before deployment
- Food safety rules are advisory prototype — not validated against SFA regulations; merchant assumes responsibility for listing decisions
- Single-tenant Streamlit MVP — no multi-merchant support, no auth, no MLOps pipeline; Phase 2 requires production infrastructure
- PDPA compliance deferred — no consent flows or data handling procedures implemented; required before real merchant data
- No video demo — live dashboard walkthrough not recorded
