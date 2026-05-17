# Submission Checklist

Complete this checklist before submitting. All items must be verified.

---

## Working Product

- [ ] App runs without errors: `streamlit run app/streamlit_app.py`
- [ ] Interactive decision workflow works end-to-end
- [ ] Prediction, recommendation, safety gate, and recovery estimate all display correctly
- [ ] Revenue Recovery Simulator is functional
- [ ] 75 unit tests pass: `pytest tests/unit/ -q`
- [ ] Python compile check passes: `python -m py_compile app/streamlit_app.py src/*.py`

## Required Deliverables

- [ ] **Working interactive product** — `app/streamlit_app.py` (Streamlit dashboard)
- [ ] **Executive report** — `docs/EXECUTIVE_REPORT.md` (maximum 4 pages equivalent)
- [ ] **COC decision log** — `COC_DECISION_LOG.md` (prototype-to-product journey)
- [ ] **Demo script** — `DEMO_SCRIPT.md` (3–5 minute live demo)
- [ ] **Pilot validation plan** — `PILOT_VALIDATION_PLAN.md` (4-week merchant pilot design)

## Data and Model Integrity

- [ ] Synthetic data limitation disclosed in executive report and COC decision log
- [ ] Model validity caveat disclosed (prototype data, not production-proven)
- [ ] Aggregate feature leakage risk fixed (expanding-window aggregates implemented in `src/feature_engineering.py`)
- [ ] Expanding-window fix documented in COC decision log
- [ ] New leakage-awareness unit test passes: `pytest tests/unit/test_leakage_awareness.py -v`

## Submission Hygiene

- [ ] `.env` NOT committed to repository (contains only placeholders, already in .gitignore)
- [ ] `.claude/` folder NOT tracked (removed from git, added to .gitignore)
- [ ] `.git/` folder NOT in final zip (local .git is preserved for the professor's inspection)
- [ ] `__MACOSX/` folder NOT in final zip
- [ ] `.DS_Store` files NOT in final zip
- [ ] No API keys or secrets in any submitted file
- [ ] `outputs/surplus_model.pkl` included (trained model)
- [ ] `data/synthetic_fnb_data.csv` included (training data)
- [ ] `outputs/model_results.csv` and `outputs/metrics_summary.csv` included

## GitHub Submission

- [ ] `python -m pytest -q` returns `75 passed`
- [ ] `python -m py_compile app/streamlit_app.py src/*.py` passes
- [ ] `git status` is clean (all noisy files removed or ignored)
- [ ] README review path is clear
- [ ] Executive report is under 4 pages when rendered
- [ ] COC decision log exists and shows chosen/rejected options
- [ ] v6 validation is the only final grading self-assessment
- [ ] Team-project technique-family distinction is closed using WanderLess recommender/optimization comparison
- [ ] Final MVP is clearly merchant-side decision cockpit
- [ ] No final-facing file claims marketplace, payment, POS, delivery, or consumer app as final MVP
- [ ] Local/noisy files are removed or ignored:
  - `.claude/`
  - `.env`
  - `.pytest_cache/`
  - `__pycache__/`
  - `__MACOSX/`
  - `workspaces/_template/`
  - `tests/sdk/`
  - `scripts/`
  - `deploy/`
  - `mcp-configs/`
  - `specs/`

## Grading Alignment

- [ ] Executive report reads as MBA-executive-level (not technical documentation)
- [ ] COC decision log shows human judgment, not blind AI delegation
- [ ] At least 5 COC defaults/AI suggestions explicitly rejected and documented
- [ ] Model validity honestly assessed (not overclaimed)
- [ ] Prototype-to-product maturity evolution documented
- [ ] Business case includes ROI logic and buyer-validation table
- [ ] Risk and governance section includes human-in-the-loop framing
- [ ] Safety gate clearly described as advisory (not SFA-validated)

## Demo Readiness

- [ ] DEMO_SCRIPT.md exists and is usable for 3–5 minute demo
- [ ] App clearly shows synthetic/demo data disclaimer
- [ ] App shows human-decision framing (merchant makes final call)

## Final Verification

- [x] `python -m pytest tests/unit/ -q` — **75 passed** (2026-05-17)
- [x] `python -m compileall app src tests` — **all Python files compile cleanly** (2026-05-17)
- [x] `python src/evaluate_model.py` — **completes successfully** (XGBoost MAE 0.6355, 2026-05-17)
- [x] README.md is accurate and consistent with deliverables
- [x] No broken file references in any document
