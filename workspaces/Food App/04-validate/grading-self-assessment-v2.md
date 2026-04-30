# Grading Self-Assessment — SurplusSense (MGMT 655)

**Date:** 2026-04-26
**Target Grade:** A+ (90+)
**Confidence:** Moderate — assessing without instructor rubric

---

## 1. Score Table

| Criterion                               | Max     | Current   | Evidence                                                                                                                                                                                                                                             |
| --------------------------------------- | ------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Project Report**                      | **60**  | **~47**   |                                                                                                                                                                                                                                                      |
| 1a. Executive Summary & Problem Framing | 10      | 5         | `docs/executive_report_notes.md` — clear structure but placeholder "[X] tonnes" for NEA data. No actual 4-page polished document exists.                                                                                                             |
| 1b. Data Understanding & Preparation    | 15      | 11        | 944 synthetic records, 8 merchants, 4 categories. Feature engineering: 48 features. Deductions: data_generator.py is 17 lines (minimal), no EDA visualizations in report.                                                                            |
| 1c. Model Development                   | 20      | 15.5      | XGBoost + RandomizedSearchCV + 5-seed holdout validation. Deductions: executive report has stale metrics (RF mentioned, MAE=0.35 instead of XGBoost MAE=0.15), CV-vs-holdout gap not explained in report, MAPE/SMAPE not shown in exec report table. |
| 1d. Analysis & Decision Support         | 10      | 7.5       | Recommendation engine (4 discount tiers), food safety (SAFE/CAUTION/BLOCK), revenue simulator. Deductions: executive report doesn't clearly show end-to-end merchant workflow output.                                                                |
| 1e. Presentation & Communication        | 5       | 3         | Dashboard live at :8502. Report is working notes, not polished. No actual 4-page executive summary document exists as a deliverable file.                                                                                                            |
| **Implementation & Code**               | **25**  | **~21.5** |                                                                                                                                                                                                                                                      |
| 2a. Code Functionality                  | 10      | 9         | All modules import and execute. Streamlit runs end-to-end. Deduction: data_generator.py is 17 lines — minimal stub.                                                                                                                                  |
| 2b. Code Organization & Best Practices  | 10      | 8.5       | Good separation (6 modules, 2,055 LOC total). Consistent patterns. Deduction: some quality inconsistency between modules (data_generator.py minimal vs train_model.py at 623 lines).                                                                 |
| 2c. Reproducibility                     | 5       | 4         | Random seed fixed (42). outputs/ contain evaluation artifacts. Deduction: no requirements.txt (pip install from pyproject.toml works but not documented).                                                                                            |
| **Bonus**                               | **15**  | **~7**    |                                                                                                                                                                                                                                                      |
| 3a. Innovation & Complexity             | 5       | 3         | 5-seed holdout validation methodology is above-and-beyond. Food-safety-as-feature is differentiated.                                                                                                                                                 |
| 3b. Real-world Application              | 5       | 3         | Singapore F&B context. Synthetic data honestly disclosed.                                                                                                                                                                                            |
| 3c. Video Demo                          | 5       | 1         | Not present in repo.                                                                                                                                                                                                                                 |
| **TOTAL**                               | **100** | **~75.5** |                                                                                                                                                                                                                                                      |

---

## 2. Two-Dimensional Analysis

### Dimension A — Decision-Making Mastery (evidence: COC decision log + journal/)

| Area                  | Score     | Justification                                                                                                                                                                                                     |
| --------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ML pipeline decisions | 8/10      | XGBoost selected over RF after 5-seed validation. Specific reasoning: RF won TimeSeriesSplit CV but lost random holdout (grading-relevant metric). Journal 0019 has full data table. Genuine choice, not default. |
| Scope decisions       | 7/10      | Clear MVP boundary (merchant cockpit vs marketplace). Trade-offs documented with alternatives rejected (RL removed, hawkers deferred). Some decisions lack alternatives-with-cause documentation.                 |
| Technical decisions   | 7/10      | Discount tier bug caught and fixed (journal 0018). Food safety rules structured. Synthetic data accepted with explicit limitations. Some documented decisions read like marketing copy.                           |
| Depth of engagement   | 6/10      | Journal 0004 asks 3 "For Discussion" questions — none resolved in later DECISION entries. COC decision log (docs/coc_decision_log.md, 331 lines) reads as polished document, not raw decision reasoning.          |
| COC journal coverage  | 8/10      | 19 substantive entries. All 8 types present (DISCOVERY×2, GAP×7, CONNECTION×1, TRADE-OFF×4, RISK×4, METRIC×1, ASSUMPTION×1, DECISION×3). Two are genuine DECISION entries (0017, 0019).                           |
| **Dimension A Total** | **36/50** |                                                                                                                                                                                                                   |

**What shows real critical engagement:**

- Journal 0019 (XGBoost selection): Full 5-seed data table, specific numbers, rationale for why random holdout > TimeSeriesSplit for grading
- Journal 0018 (discount tier bug): Specific root cause analysis with actual condition traces showing why the wrong tier matched
- Journal 0004 (TRADE-OFF): Three genuine For-Discussion questions about scope depth vs breadth, synthetic data honesty, real merchant recruitment

**What is weaker:**

- COC decision log reads like a product brief, not raw decision reasoning
- Some entries (0001, 0002) are thin — surface-level observations
- No entry resolves the 3 For-Discussion questions from 0004
- Risk entries (0006, 0008, 0015) document risks but rarely show mitigation actions

### Dimension B — Decision-Support Value (evidence: working product)

| Area                      | Score     | Justification                                                                                                                                                                         |
| ------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Product works             | 9/10      | Dashboard live at :8502. All modules functional. Predictions, recommendations, safety checks all execute end-to-end. Minor deduction: data_generator.py is a minimal stub (17 lines). |
| Problem framing for user  | 7/10      | Singapore F&B surplus is specific and credible. Café/bakery beachhead is defensible. Placeholder NEA data "[X] tonnes" undermines credibility for an instructor reviewing it.         |
| Actionable merchant value | 8/10      | Surplus prediction → discount recommendation → revenue recovery → food safety. Full workflow. Merchant can log in and get a decision, not just a number.                              |
| Explainability            | 8/10      | Feature importance shown. Baselines compared. Food safety checks explained. Rule-based discount logic is transparent.                                                                 |
| Presentation quality      | 6/10      | Dashboard is functional. Executive report is working notes with stale metrics. No polished 4-page executive summary exists.                                                           |
| **Dimension B Total**     | **38/50** |                                                                                                                                                                                       |

---

## 3. Hard-Rule Check

| Rule                                           | Status                 | Evidence                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Technique family differs from team project** | ⚠️ UNVERIFIED          | User says team project family is [USER WILL FILL IN]. The individual uses supervised learning (XGBoost regression). If team also used XGBoost or RF, this violates the rule. **Flag: CRITICAL if same family.**                                                                                                                   |
| **Critical engagement, not AI delegation**     | ✅ PASS (with caveats) | Journal 0018 (discount tier bug) and 0019 (XGBoost selection with data) show genuine reasoning. However, COC decision log in docs/ reads like a polished product document rather than raw decision traces. Some earlier journal entries are thin.                                                                                 |
| **Not COC defaults only**                      | ⚠️ PARTIAL             | 5-seed holdout validation methodology, food-safety-as-feature, and discount tier bug discovery are genuine custom work. However, the ML pipeline (XGBoost + feature engineering + RandomizedSearchCV) follows textbook patterns. The food safety rules use threshold constants that aren't validated against real SFA guidelines. |

**CRITICAL FLAG:**

> The technique family rule cannot be verified. User must confirm the team project uses a different ML technique family (e.g., if the team used Random Forest, XGBoost is the same supervised learning family and this would be a violation). The individual project uses **supervised regression with XGBoost** — if the team also used supervised learning (even with a different algorithm), explicit justification is needed.

---

## 4. Top 5 Highest-Leverage Improvements (by pts/hour)

| #     | Action                                                                                                             | Pts gained (est.) | Hours (est.) |
| ----- | ------------------------------------------------------------------------------------------------------------------ | ----------------- | ------------ |
| **1** | Write a polished 4-page executive summary                                                                          | +4–6 (1a, 1e, 1d) | 3–4          |
| **2** | Fix stale metrics in executive report notes (RF→XGBoost, MAE=0.35→0.15, update MAPE/SMAPE)                         | +2–3 (1c)         | 0.5          |
| **3** | Fill in placeholder NEA data — search for real Singapore food waste stats                                          | +1–2 (1a)         | 0.5          |
| **4** | Add 2–3 EDA visualizations to the report (surplus distribution by category, day-of-week patterns, model residuals) | +1–2 (1b)         | 2–3          |
| **5** | Record a 3-minute screen-cap walkthrough of the dashboard                                                          | +1–2 (3c)         | 1            |

**Notes:**

- Items 2 and 3 are quick fixes with high credibility impact
- Item 1 is the biggest point gainer but also highest effort
- The stale metrics are a genuine risk — if a professor sees RF mentioned in the report after XGBoost deployment, it raises questions about rigor

---

## 5. Top 3 Risks That Could Cap Grade Below A+

| Risk                                   | Severity | Why it caps the grade                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stale executive report metrics**     | HIGH     | The exec report notes still say "Random Forest" and "MAE=0.35". The XGBoost redeployment happened AFTER the exec report was written. If this is the submitted document, it looks like the student forgot to update the report after Phase 5. This undermines the rigor narrative.                                                               |
| **CV-vs-holdout gap unexplained**      | HIGH     | XGBoost holdout MAE = 0.15 but TimeSeriesSplit CV = 1.22. That's an 8× difference. The decision log explains this (RF's regularization tolerates temporal shift) but the executive report doesn't. If a professor asks "why does your model perform 8× better on random holdout than temporal CV?", there's no documented answer in the report. |
| **No actual 4-page executive summary** | MEDIUM   | The repo has "executive_report_notes.md" (306 lines of working notes). The team project instructions say "executive summary not exceeding 4 pages" — if the individual submission also requires this format and only notes are provided, presentation score is capped at ~3/5 instead of 4–5/5.                                                 |

---

## 6. Honest Grade Estimate

### Current Score: ~75.5 / 100

| Component             | Max     | Est.      |
| --------------------- | ------- | --------- |
| Project Report        | 60      | ~42       |
| Implementation & Code | 25      | ~21.5     |
| Bonus                 | 15      | ~7        |
| **Total**             | **100** | **~70.5** |

**Confidence:** ±5 pts. The range is **66–76** based on how strictly bonuses are applied.

**A+ (90+) requires:** ~90/100
**Gap to A+:** ~14–20 pts

### What's needed to reach 90:

The most realistic path to 90+:

1. **+6 pts**: Write the polished 4-page executive summary (addresses 1a fully + partial 1e, 1d)
2. **+3 pts**: Fix stale metrics (XGBoost throughout, correct MAE=0.15, add MAPE/SMAPE to table)
3. **+3 pts**: Add EDA visualizations + fill NEA placeholder
4. **+2 pts**: Explain CV-vs-holdout gap in the report (1 sentence is enough)
5. **+2 pts**: Video demo
6. **+1 pt**: Fill in TRADE-OFF For-Discussion resolutions in journal

**Realistic ceiling if all improvements done: 87–91**

### Weakest dimension

**Dimension A (Decision-Making): 36/50**

The COC decision log in `docs/coc_decision_log.md` is the weakest point. It reads like a product marketing document (331 lines of "here's what we built and why it's great") rather than evidence of genuine critical engagement with alternatives. The rubric says: _"Submitting work where all decisions were delegated to AI without evidence of critical engagement (as shown in the COC decision log) will be treated as insufficient original contribution."_

The actual journal entries (journal/ folder) show more genuine reasoning than the decision log, but the decision log is what a professor would read to verify this criterion.

---

## 7. What Stands Out Positively

1. **5-seed holdout validation**: This is genuinely above-and-beyond. The explicit reasoning for why random holdout > TimeSeriesSplit for grading is exactly what the rubric wants to see.
2. **Discount tier bug caught**: Journal 0018 shows real debugging — specific condition traces, root cause identified, fix applied. This is evidence of critical engagement, not AI delegation.
3. **Food safety disclaimer + synthetic data disclosure**: These two grading-relevant todos show the student thought about what the professor would care about.
4. **Working end-to-end pipeline**: From data generation through XGBoost training, evaluation, and Streamlit dashboard — everything executes. This is not a demo, it's a product.

---

## 8. Journal Quality Audit

| Entry                              | Type       | Substantive? | Shows Reasoning?                                | Resolves Earlier Questions? |
| ---------------------------------- | ---------- | ------------ | ----------------------------------------------- | --------------------------- |
| 0001 DISCOVERY marketplace moat    | DISCOVERY  | Thin         | No — brief observation                          | N/A                         |
| 0002 GAP regulatory                | GAP        | Yes          | Surface-level (notes issue)                     | N/A                         |
| 0003 CONNECTION ML-retention       | CONNECTION | Yes          | Brief                                           | N/A                         |
| 0004 TRADE-OFF scope               | TRADE-OFF  | Yes          | Yes — 3 alternatives + questions                | Questions remain open       |
| 0005 GAP synthetic data            | GAP        | Yes          | Yes — clear limitation                          | N/A                         |
| 0006 RISK safety unvalidated       | RISK       | Yes          | Yes — describes unvalidated nature              | N/A                         |
| 0007 GAP cold start                | GAP        | Yes          | Surface-level                                   | N/A                         |
| 0008 RISK model drift              | RISK       | Yes          | Yes — describes monitoring gap                  | N/A                         |
| 0009 GAP feedback loop             | GAP        | Yes          | Yes                                             | N/A                         |
| 0010 TRADE-OFF MVP vs prod         | TRADE-OFF  | Yes          | Yes — table of what's deferred                  | N/A                         |
| 0011 GAP PDPA                      | GAP        | Yes          | Brief                                           | N/A                         |
| 0012 TRADE-OFF Streamlit vs prod   | TRADE-OFF  | Yes          | Brief                                           | N/A                         |
| 0013 METRIC success criteria       | METRIC     | Yes          | Yes                                             | N/A                         |
| 0014 ASSUMPTION biz assumptions    | ASSUMPTION | Yes          | Brief                                           | N/A                         |
| 0015 RISK incumbent response       | RISK       | Yes          | Brief                                           | N/A                         |
| 0016 GAP unit tests                | GAP        | Yes          | Brief                                           | N/A                         |
| 0017 DECISION codified ML patterns | DECISION   | Yes          | Thin — states what was codified                 | N/A                         |
| 0018 DISCOVERY discount tier bug   | DISCOVERY  | Yes          | **Yes — specific condition traces, root cause** | N/A                         |
| 0019 DECISION XGBoost over RF      | DECISION   | Yes          | **Yes — full 5-seed table, specific numbers**   | N/A                         |

**Assessment:** 19 substantive entries. 4 show genuine reasoning depth (0004, 0018, 0019). 3 "For Discussion" questions in 0004 remain unresolved. DECISION entries (0017) are thin — states outcomes but not the reasoning process.

---

_Generated 2026-04-26 — Self-assessment against MGMT 655 proxy rubric_
