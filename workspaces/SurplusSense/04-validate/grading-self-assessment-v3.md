> **Superseded by grading-self-assessment-v6-final.md. See that file for the current assessment.**

# Grading Self-Assessment — SurplusSense (MGMT 655) — v3

**Date:** 2026-04-26
**Target Grade:** A+ (90+)
**Confidence:** Moderate — assessing against proxy rubric without instructor guidance

---

## 1. Score Table

| Criterion                               | Max     | Current   | Evidence                                                                                                                                                                                                         | Delta from v2                                                   |
| --------------------------------------- | ------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Project Report**                      | **60**  | **~46.5** |                                                                                                                                                                                                                  | **-0.5**                                                        |
| 1a. Executive Summary & Problem Framing | 10      | 7         | `docs/EXECUTIVE_REPORT.md` (4-page polished doc); NEA data filled (755k/784k tonnes, SGD 342M); SGD 342M from Singapore Environment Council. Deduct 3: exec notes still has `[X] tonnes` placeholder at line 13. | +2 (polished doc now exists; NEA data filled)                   |
| 1b. Data Understanding & Preparation    | 15      | 11        | 4,027 synthetic records, 15 merchants, 13 categories, 47 features post-encoding. Deduct 4: data_generator.py is 17 lines (stub); no EDA visualizations in report.                                                | ±0                                                              |
| 1c. Model Development                   | 20      | 16.5      | XGBoost n_estimators=250, max_depth=13, lr=0.295 (model_metadata.json:4-13); holdout MAE=0.68; MAPE=12.6% now in table; CV-vs-holdout gap (0.68 vs 1.22) explained in exec report line 75.                       | +1 (stale metrics fixed; MAPE added; gap explained in report)   |
| 1d. Analysis & Decision Support         | 10      | 7.5       | Recommendation engine (10 discount tiers 20-70%), food safety (SAFE/CAUTION/BLOCK), revenue recovery calculation. Deduct 2.5: end-to-end merchant workflow output not shown in report.                           | ±0                                                              |
| 1e. Presentation & Communication        | 5       | 4         | `docs/EXECUTIVE_REPORT.md` is polished 4-page doc; Generation Notes section explains sourcing. Deduct 1: no demo video exists in repo.                                                                           | +1 (polished doc added)                                         |
| **Implementation & Code**               | **25**  | **~22**   |                                                                                                                                                                                                                  | **+0.5**                                                        |
| 2a. Code Functionality                  | 10      | 9         | All modules import and execute; Streamlit runs; 59/59 tests pass (pytest, 4.18s). Deduct 1: data_generator.py is 17-line stub.                                                                                   | ±0                                                              |
| 2b. Code Organization & Best Practices  | 10      | 8.5       | 6 modules, 2,156 LOC; consistent patterns; src/ separation clean. Deduct 1.5: quality inconsistency (data_generator.py 17 lines vs train_model.py 623 lines).                                                    | ±0                                                              |
| 2c. Reproducibility                     | 5       | 4.5       | Random seed fixed (42); outputs/ contain evaluation artifacts; requirements.txt now exists. Deduct 0.5: no run script documented for fresh environment.                                                          | +0.5 (requirements.txt now exists)                              |
| **Bonus**                               | **15**  | **~6**    |                                                                                                                                                                                                                  | **-1**                                                          |
| 3a. Innovation & Complexity             | 5       | 3         | 5-seed holdout validation above-and-beyond; food-safety-as-feature differentiated.                                                                                                                               | ±0                                                              |
| 3b. Real-world Application              | 5       | 3         | Singapore F&B context; synthetic data honestly disclosed; SFA limitation explicit in report.                                                                                                                     | ±0                                                              |
| 3c. Video Demo                          | 5       | 0         | **No video file exists in repo root.** `find . -name "*.mp4" -o -name "*.mov"` returns empty. Cannot award points for absent artifact.                                                                           | -1 (v2 gave 1/5 "Not present in repo"; skeptic correction: 0/5) |
| **TOTAL**                               | **100** | **~74.5** |                                                                                                                                                                                                                  | **-0.5**                                                        |

---

## 2. Two-Dimensional Analysis

### Dimension A — Decision-Making Mastery (evidence: journal/ + docs/coc_decision_log.md)

| Area                  | Score       | Justification                                                                                                                                                                                                                                      | Delta                      |
| --------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| ML pipeline decisions | 8/10        | XGBoost selected over RF after 5-seed validation (journal 0019, multi_seed_validation.csv). Holdout > CV reasoning documented.                                                                                                                     | ±0                         |
| Scope decisions       | 7/10        | Clear MVP boundary documented; trade-offs in journal 0010, 0012. 3 For-Discussion questions from journal 0004 remain unresolved (confirmed via grep: "For Discussion" still present at line 25 of 0004).                                           | ±0                         |
| Technical decisions   | 7/10        | Discount tier bug caught and fixed (journal 0018). Decimal rounding fix applied. Synthetic data accepted with explicit limitations.                                                                                                                | ±0                         |
| Depth of engagement   | 6/10        | Journal 0004 asks 3 "For Discussion" questions — none resolved in later entries. COC decision log (docs/coc_decision_log.md, 331 lines) reads as polished product document, not raw decision traces. Journal 0018 and 0019 show genuine reasoning. | ±0                         |
| COC journal coverage  | 8.5/10      | 21 substantive entries now (19 + 0025 + 0027). All 8 types present. Entries 0018 and 0019 are substantive. **Cannot audit personalization** — COC wrote these; I cannot verify how much the student edited or personalized them.                   | +0.5 (2 new entries added) |
| **Dimension A Total** | **36.5/50** |                                                                                                                                                                                                                                                    | **+0.5**                   |

**What I can verify as genuine custom work:**

- XGBoost vs RF 5-seed validation with specific numbers (journal 0019 + multi_seed_validation.csv)
- Discount tier bug root cause trace (journal 0018)
- 10-tier discount structure in recommendation_engine.py (lines 37-53)
- Food safety rules implementation (food_safety_rules.py lines 25-37)
- Feature count: 47 post-encoding (model_metadata.json:80)

**What I cannot verify (COC authorship):**

- All journal entries — I (the COC agent) wrote initial versions. Student may have edited or approved them, but I have no evidence of personalization.
- docs/coc_decision_log.md (331 lines) — I wrote this document. It reads as polished product marketing, not raw decision reasoning.
- EXECUTIVE_REPORT.md Generation Notes section — explicitly says "Numbers sourced from:" then lists files. This is an AI artifact citing file paths.

**What is still weak:**

- No journal entry resolves the 3 For-Discussion questions from 0004
- No journal entry documents what the student decided about: (1) scope breadth vs depth, (2) synthetic data sufficiency, (3) real merchant recruitment
- COC decision log reads like a product brief, not evidence of critical engagement

### Dimension B — Decision-Support Value (evidence: working product)

| Area                      | Score       | Justification                                                                                                                                                                             | Delta                            |
| ------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| Product works             | 9/10        | Dashboard functional; all modules execute; predictions, recommendations, safety checks all end-to-end. 59/59 tests pass. Minor: data_generator.py is a stub.                              | ±0                               |
| Problem framing for user  | 7.5/10      | Singapore F&B surplus specific and credible; NEA data now filled (755k/784k); beachhead segment defensible. SGD 342M from Singapore Environment Council (line 10 of EXECUTIVE_REPORT.md). | +0.5 (NEA data filled in report) |
| Actionable merchant value | 8/10        | Surplus prediction → discount recommendation → revenue recovery → food safety. Full workflow. Merchant gets a decision, not just a number.                                                | ±0                               |
| Explainability            | 8/10        | Feature importance shown; baselines compared; food safety explained; rule-based discount transparent.                                                                                     | ±0                               |
| Presentation quality      | 6/10        | Dashboard functional. EXECUTIVE_REPORT.md polished but generated by COC (Generation Notes admit sourcing from model files). exec notes still has `[X] tonnes` placeholder.                | ±0                               |
| **Dimension B Total**     | **38.5/50** |                                                                                                                                                                                           | **+0.5**                         |

---

## 3. Hard-Rule Check

| Rule                                           | Status        | Evidence                                                                                                                                                                                                                                                                                                                                      | Flag                                                                     |
| ---------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Technique family differs from team project** | ⚠️ UNVERIFIED | Student says team project family is [NOT PROVIDED]. Individual uses supervised regression (XGBoost). Cannot verify team project ML technique.                                                                                                                                                                                                 | **CRITICAL — student must confirm**                                      |
| **Critical engagement, not AI delegation**     | ⚠️ PARTIAL    | Journal 0018 (discount tier bug) and 0019 (XGBoost selection) show genuine reasoning with specific traces. However, docs/coc_decision_log.md (331 lines) reads as I wrote it — polished product document. EXECUTIVE_REPORT.md Generation Notes explicitly attribute numbers to files.                                                         | **MEDIUM — journal entries show engagement; decision log is COC output** |
| **Not COC defaults only**                      | ⚠️ PARTIAL    | 5-seed holdout validation methodology, food-safety-as-feature, and discount tier bug discovery are genuine custom work. However, XGBoost + RandomizedSearchCV + feature engineering pipeline follows textbook ML patterns. Food safety threshold constants (MAX_HOLDING_TIMES, MAX_PICKUP_WINDOWS) not validated against real SFA guidelines. | **LOW**                                                                  |
| **No stubs in production**                     | ⚠️ PARTIAL    | data_generator.py is 17 lines — minimal stub. `if __name__ == "__main__":` blocks with print statements exist in src/ modules (confirmed by journal 0027 note). Functional but not production-grade.                                                                                                                                          | **LOW**                                                                  |

---

## 4. Honest Grade Estimate

### Current Score: ~74.5 / 100

| Component             | Max     | Est.      | Delta from v2 |
| --------------------- | ------- | --------- | ------------- |
| Project Report        | 60      | ~46.5     | -0.5          |
| Implementation & Code | 25      | ~22       | +0.5          |
| Bonus                 | 15      | ~6        | -1            |
| **Total**             | **100** | **~74.5** | **-0.5**      |

**v2 reported ~75.5. Score decreased because:**

1. Video demo correctly scored 0/5 (v2 gave 1/5 for "not present in repo" — skeptic correction)
2. No other category improved enough to offset

**Confidence: ±5 pts. Range: 70–80 based on how strictly bonuses are applied and whether Dimension A journal entries are accepted as evidence of student engagement.**

**A+ (90+) requires:** ~90/100
**Gap to A+:** ~15.5 pts

---

## 5. Top 3 Things That Could STILL Hurt at Grading Time

### Risk 1: COC artifacts undermine Dimension A claims (SEVERITY: HIGH)

The docs/coc_decision_log.md (331 lines) and EXECUTIVE_REPORT.md Generation Notes section were written by me (the COC agent). The Generation Notes explicitly say "Numbers sourced from: models/model_metadata.json, outputs/multi_seed_validation.csv..." — this is AI attribution, not student reasoning. A professor who reads these documents closely will see AI-generated content attributed to the student.

**Mitigation:** Student should either (a) rewrite coc_decision_log.md in their own voice showing the actual decision process, or (b) delete it and rely only on journal entries which show more authentic reasoning traces.

### Risk 2: data_generator.py is a 17-line stub (SEVERITY: HIGH for 1b score)

`src/data_generator.py` is 17 lines. The v2 rubric flagged this. It has not changed. If a professor looks at the data pipeline, they'll see a trivial stub generating what appears to be random-looking data with a simple formula. The sophistication of the ML pipeline is undercut by the trivial data generator.

**Mitigation:** Expand data_generator.py to at least 100+ lines with realistic distributions, outlier generation, and day-of-week effects. Even if the synthetic nature is disclosed, the generator itself should demonstrate domain knowledge.

### Risk 3: 3 For-Discussion questions from journal 0004 remain unresolved (SEVERITY: MEDIUM)

Journal 0004 line 25 has "For Discussion" questions about: (1) scope breadth vs depth, (2) synthetic data sufficiency, (3) real merchant recruitment. No journal entry resolves any of these. A professor reading the journal trail sees open questions that were never closed.

**Mitigation:** Add journal entries resolving each question — even "decided to defer (1) to Phase 2" is a resolution.

---

## 6. Recommended Pre-Submission Actions (prioritized)

| #     | Action                                                                                                                             | Pts gained (est.) | Evidence                                                           |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------ |
| **1** | Expand data_generator.py to 100+ lines with realistic Singapore F&B distributions, outlier handling, day-of-week patterns          | +2–3 (1b)         | Currently 17 lines; stub visible to any code reviewer              |
| **2** | Rewrite coc_decision_log.md in student's own voice — 3-5 key decisions with why/why-not reasoning (not product marketing)          | +2–3 (Dim A)      | Currently 331 lines of COC-written polished prose                  |
| **3** | Add 2–3 journal entries closing the 3 unresolved "For Discussion" questions from journal 0004                                      | +1–2 (Dim A)      | grep confirms "For Discussion" unresolved at 0004:25               |
| **4** | Add EDA visualizations to docs/ (surplus distribution by category, day-of-week heatmap, model residual analysis)                   | +1–2 (1b, 1e)     | No visualizations exist in docs/                                   |
| **5** | Record 3-minute screen-capped demo of dashboard — even a quick walkthrough showing prediction → recommendation → safety check flow | +1–2 (3c)         | No video exists; without it, bonus criterion 3c is permanently 0/5 |

**Realistic ceiling if all 5 done: 80–84**

---

## 7. Delta from v2 — What Actually Changed

| What changed         | v2 score  | v3 score  | Reason                                                                                     |
| -------------------- | --------- | --------- | ------------------------------------------------------------------------------------------ |
| Executive Summary    | 5         | 7         | EXECUTIVE_REPORT.md exists now; NEA data filled                                            |
| Model Development    | 15.5      | 16.5      | Stale metrics fixed (XGBoost throughout, MAE=0.68); MAPE in table; gap explained in report |
| Presentation         | 3         | 4         | Polished 4-page doc exists; no video → correct to 0/5                                      |
| Reproducibility      | 4         | 4.5       | requirements.txt added                                                                     |
| Journal COC coverage | 8         | 8.5       | 21 entries (was 19)                                                                        |
| Video Demo           | 1         | 0         | v2 incorrectly gave 1/5 for "not present in repo" — skeptic correction                     |
| **TOTAL**            | **~75.5** | **~74.5** | Video demo skeptic correction (-1) outweighs modest improvements (+0)                      |

---

_Generated 2026-04-26 — Self-assessment v3 against MGMT 655 proxy rubric. Conservative/skeptical scoring applied._
