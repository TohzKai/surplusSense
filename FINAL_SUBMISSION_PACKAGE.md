# Final Submission Package — SurplusSense

**Course:** SMU MGMT655 Machine Learning
**Individual Assignment**

---

## Product

SurplusSense is a merchant-side F&B surplus decision-support cockpit — not a consumer marketplace. It helps bakeries, cafés, and prepared-food outlets decide whether to hold, monitor, discount, deep discount, donate, or discard surplus inventory.

The product combines XGBoost surplus prediction with deterministic recommendation rules, food-safety gating, and recovery-value estimation.

---

## Evidence Map

| MGMT655 Requirement            | Evidence File                                                             | Key Evidence                                                                                |
| ------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Working interactive product    | `app/streamlit_app.py`                                                    | Streamlit decision cockpit — run with `streamlit run app/streamlit_app.py`                  |
| Executive report (max 4 pages) | `docs/EXECUTIVE_REPORT.md`                                                | 197 lines — problem, product, worked example, model results, business case                  |
| COC decision log               | `COC_DECISION_LOG.md`                                                     | 12 sections — prototype-to-product journey, rejected alternatives, human-judgment audit     |
| Problem worth solving          | `docs/EXECUTIVE_REPORT.md` §1                                             | Merchant-side surplus decision at end of day                                                |
| ML/AI depth                    | `src/train_model.py` + `src/feature_engineering.py`                       | XGBoost, 46 features, temporal 80/20 holdout, leakage-aware expanding-window aggregates     |
| Temporal validation            | `src/feature_engineering.py`                                              | `shift(1)` on all aggregate features; no target lookahead                                   |
| Business case                  | `PILOT_VALIDATION_PLAN.md`                                                | Recovery value, willingness-to-pay, pilot design                                            |
| Not a default COC demo         | `COC_DECISION_LOG.md` §11                                                 | Human-judgment decision audit — documented rejected alternatives                            |
| Different ML technique family  | README.md + COC_DECISION_LOG.md                                           | SurplusSense: supervised XGBoost regression. WanderLess: recommender systems + optimization |
| User flows                     | `workspaces/SurplusSense/03-user-flows/01-merchant-flows.md`              | Final merchant decision flow; Phase 2 flows documented separately                           |
| Validation                     | `workspaces/SurplusSense/04-validate/grading-self-assessment-v6-final.md` | 93–94/100 self-assessment; 63 unit tests; all requirements met                              |
| Process trail                  | `workspaces/SurplusSense/journal/`                                        | 29 journal entries; scope evolution documented                                              |

---

## Test Command

```bash
python -m pytest tests/unit/ -q
```

**Result: 63 passed**

---

## Run the Product

```bash
# Install dependencies
pip install -r requirements.txt

# Generate training data (one-time)
python data/generate_synthetic_data.py

# Train model
python src/train_model.py

# Launch dashboard
streamlit run app/streamlit_app.py
```

Dashboard opens at `http://localhost:8501`.

---

## Key Model Metrics

| Model               | Temporal Holdout MAE | Notes                                    |
| ------------------- | -------------------- | ---------------------------------------- |
| Historical Average  | 1.49                 | Baseline                                 |
| **XGBoost (Tuned)** | **0.64**             | Primary metric; 57% better than baseline |

Primary metric sourced from `outputs/model_results.csv`. Temporal holdout (last 20% of dates) is the primary evaluation — not random split.

---

## WanderLess Technique Family Declaration

SurplusSense uses **supervised machine learning** (XGBoost surplus prediction). The team project, WanderLess, uses **recommender systems and optimization** (hybrid tourist-guide matching, TruncatedSVD collaborative filtering, content-based compatibility scoring, itinerary optimization). These are different ML technique families.

---

## Quick Professor Review Path

1. **Open the app** — `streamlit run app/streamlit_app.py`
2. **Read the executive report** — `docs/EXECUTIVE_REPORT.md` (4 pages)
3. **Review the decision log** — `COC_DECISION_LOG.md`
4. **Check the self-assessment** — `workspaces/SurplusSense/04-validate/grading-self-assessment-v6-final.md`
5. **Run the tests** — `pytest tests/unit/ -q` (63 passed)

---

## Include in Final ZIP

The following files constitute the final submission package:

```
README.md
docs/EXECUTIVE_REPORT.md
COC_DECISION_LOG.md
PILOT_VALIDATION_PLAN.md
DEMO_SCRIPT.md
DIGITAL_TRANSFORMATION_DECK.md
FINAL_SUBMISSION_PACKAGE.md
SUBMISSION_CHECKLIST.md
app/
src/
data/
models/
outputs/
tests/unit/
pytest.ini
requirements.txt
pyproject.toml
workspaces/SurplusSense/
```

---

## Exclude from Final ZIP

The following are local settings, caches, SDK/template artifacts, and historical Phase 2 exploration files that are not part of the final MVP submission:

```
# Version control and local settings
.git/
.env
.env.example
.session-notes

# AI tool and IDE settings
.claude/
.DS_Store

# Build and cache artifacts
.pytest_cache/
__pycache__/
__MACOSX/
*.pyc

# SDK/template tests (not SurplusSense product tests)
tests/sdk/

# Deployment infrastructure (not part of MVP)
deploy/
Dockerfile
.dockerignore
.coc-sync-marker

# SDK MCP and CI configs
mcp-configs/
.github/

# Kailash SDK scripts (not SurplusSense product scripts)
scripts/

# Template workspace
workspaces/_template/

# Phase 2 / historical marketplace exploration
specs/
```

---

## Why These Are Excluded

- `.env` and `.session-notes` may contain local secrets or session-specific paths
- `.claude/` and local settings are AI-tool configuration, not assessment evidence
- `tests/sdk/` contains Kailash SDK template tests — not SurplusSense product tests
- `specs/` contains historical marketplace, payment, consumer, and delivery planning that predates the final merchant-cockpit MVP scope
- `deploy/`, `scripts/`, `mcp-configs/`, `.github/` are SDK infrastructure — not part of the MGMT655 submission
- `.git/` is useful for version history but creates a large, noisy ZIP for eLearn submission
- `__pycache__/` and `.pytest_cache/` are build artifacts — they make the package look uncurated

---

## Clean ZIP Command

From the repository root, run:

```bash
zip -r SurplusSense_FINAL.zip \
  README.md \
  docs/EXECUTIVE_REPORT.md \
  COC_DECISION_LOG.md \
  PILOT_VALIDATION_PLAN.md \
  DEMO_SCRIPT.md \
  DIGITAL_TRANSFORMATION_DECK.md \
  FINAL_SUBMISSION_PACKAGE.md \
  SUBMISSION_CHECKLIST.md \
  app \
  src \
  data \
  models \
  outputs \
  tests/unit \
  pytest.ini \
  requirements.txt \
  pyproject.toml \
  workspaces/SurplusSense \
  -x "*/__pycache__/*" \
     "*/.pytest_cache/*" \
     "*/.DS_Store" \
     "*/__MACOSX/*" \
     ".git/*" \
     ".env" \
     ".env.example" \
     ".session-notes" \
     ".claude/*" \
     "tests/sdk/*" \
     "deploy/*" \
     "Dockerfile" \
     ".dockerignore" \
     ".coc-sync-marker" \
     "mcp-configs/*" \
     ".github/*" \
     "scripts/*" \
     "specs/*" \
     "workspaces/_template/*"
```

This produces `SurplusSense_FINAL.zip` containing only the assessment-relevant files.
