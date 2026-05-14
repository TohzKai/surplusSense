# CONNECTION: Stale model metrics synced to XGBoost deployed state

> **Supersession note:** This journal entry was written when the project used the working title "Food App" and references `workspaces/Food App/` paths. That workspace was renamed to `workspaces/SurplusSense/`. References to `workspaces/Food App/` in this entry are historical workspace paths. The content is retained as process evidence.

**Date**: 2026-04-26
**Type**: CONNECTION
**Scope**: Documentation audit and correction

---

## Problem

The production model was switched from Random Forest to XGBoost (5-seed holdout validation, 2026-04-26), but several documentation files still referenced the old RF metrics. This is a credibility issue before submission.

---

## Canonical XGBoost Numbers (from `models/model_metadata.json` + `outputs/multi_seed_validation.csv`)

| Metric                               | Value                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------ |
| Model                                | XGBoost                                                                              |
| n_estimators                         | 250                                                                                  |
| max_depth                            | 13                                                                                   |
| learning_rate                        | 0.295                                                                                |
| gamma                                | 2.35                                                                                 |
| subsample                            | 0.616                                                                                |
| colsample_bytree                     | 0.921                                                                                |
| reg_alpha                            | 0.64                                                                                 |
| reg_lambda                           | 0.93                                                                                 |
| n_features                           | 47                                                                                   |
| Holdout MAE (XGBoost, mean 5 seeds)  | 0.6824                                                                               |
| Holdout MAE (RF Tuned, mean 5 seeds) | 0.8675                                                                               |
| Holdout advantage                    | XGBoost wins 5/5 seeds, mean 0.1851 better                                           |
| TimeSeriesSplit CV MAE (XGBoost)     | 1.2235                                                                               |
| TimeSeriesSplit CV MAE (RF)          | 1.0745                                                                               |
| Historical Average baseline MAE      | 1.39                                                                                 |
| Holdout improvement vs Hist Avg      | ~51%                                                                                 |
| CV-vs-holdout gap                    | XGBoost: 0.54 MAE gap (CV is worse); RF regularization handles temporal shift better |

---

## Files Updated

### 1. `README.md`

- Line 29: `Random Forest model (n_estimators=100, max_depth=15), 45 engineered features` → `XGBoost model (n_estimators=250, max_depth=13), 47 engineered features`
- Line 39: `Random Forest model design` → `XGBoost model design`
- Line 52: `Random Forest training` → `XGBoost training`

### 2. `docs/executive_report_notes.md`

- Line 63: "Random Forest for surplus prediction" → "XGBoost for surplus prediction"
- Performance table: Removed old MAE=0.35/RMSE=0.50 row; replaced with holdout MAE=0.68, noting XGBoost wins 5/5 holdout seeds
- Key findings: Removed "75% improvement" (old RF number); replaced with accurate ~51% holdout improvement vs Historical Average baseline; noted CV-vs-holdout gap
- Line 94: Updated to reflect XGBoost selection over RF

### 3. `docs/product_hardening_plan.md`

- Line 25: "3 baselines + Random Forest" → "3 baselines + XGBoost"

### 4. `workspaces/Food App/04-validate/red-team-validation-report.md`

- ML predictions row: "Random Forest model" → "XGBoost model"
- Model training results: Updated from RF (100 trees, max_depth=15) to XGBoost (n_estimators=250, max_depth=13)
- Baseline comparison table: Removed stale MAE=0.35 row; replaced with holdout-based XGBoost MAE=0.68, ~51% improvement
- Finding text updated accordingly

---

## NOT Modified (Historical Records)

The following are preserved as-is as historical session records:

- `workspaces/Food App/04-validate/grading-self-assessment-v2.md` — grading record
- `workspaces/Food App/04-validate/red-team-validation-report-v2.md` — historical validation
- `workspaces/Food App/04-validate/red-team-validation-report-v3.md` — historical validation
- `workspaces/Food App/journal/0007-GAP-cold-start-new-merchants.md` — references RF but is a historical discovery record
- `workspaces/Food App/journal/0008-RISK-model-drift-without-monitoring.md` — historical risk record
- `workspaces/Food App/journal/0019-DECISION-xgboost-selected-over-rf.md` — historical decision record (already correctly notes XGBoost selection)
- `src/train_model.py`, `src/evaluate_model.py` — source code (trained both models; XGBoost selected as deployed)
- `app/streamlit_app.py` — already uses dynamic `model_type` from pickle metadata

---

## Notes

- The XGBoost holdout MAE (0.68) is substantially worse than the old RF number (0.35) that appeared in the executive report — that 0.35 figure appears to have been from a different (likely CV) evaluation of RF, not a holdout number
- The CV-vs-holdout gap for XGBoost (1.22 CV vs 0.68 holdout) is large — XGBoost performs better on random holdout splits but worse under TimeSeriesSplit, meaning RF's stronger regularization is better at handling temporal distribution shift
- The ~51% holdout improvement vs Historical Average baseline (1.39 → 0.68) is the correct metric to quote for the demo; avoid citing the old 75% figure which was from a different evaluation setup
