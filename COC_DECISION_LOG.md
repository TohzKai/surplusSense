# COC Decision Log: From 90-Minute Prototype to Market-Ready Product

**Project:** SurplusSense — AI Decision Intelligence for F&B Merchants
**Assignment:** SMU MBA Machine Learning Individual Project
**Date:** April 2026
**Framework:** Kailash COC (Cognitive Orchestration for Codegen) with human judgment

---

## 1. Starting Point: The 90-Minute Prototype

The weekly prototype had a clear ML pipeline but was not a product:

**What the prototype did:**

- Trained an XGBoost model on synthetic F&B surplus data
- Generated predictions and accuracy metrics
- Displayed results in a Streamlit dashboard

**What was missing or incomplete:**

- No clear problem statement or target customer definition
- Prediction was the output — there was no guidance on what to _do_ with the prediction
- No safety logic — any item could be recommended for listing regardless of food safety
- No business case — no discussion of who would pay, why, or how much
- Cold-start problem unaddressed — what happens for a new merchant with no history?
- Dashboard was a technical demo, not a decision-support interface

**Why it was not market-ready:**
A merchant looking at the prototype would see a prediction number with no recommended action, no safety guidance, and no recovery estimate. It answered "how much waste might occur" but not "what should I do about it."

---

## 2. Product Selected and Why

SurplusSense was selected as the strongest weekly product for two reasons:

**Commercial relevance:** Singapore's F&B waste problem is large (784,000 tonnes annually; NEA, 2024), well-documented, and has active government support. The problem is real, not hypothetical.

**AI decision opportunity:** The incumbent solutions (Treatsure, Yindii, Too Good To Go) are consumer-facing discovery apps. None address the merchant's core decision problem: _what to do with unsold inventory before it becomes waste_. This is a decision-support gap, not another discovery tool.

**Who the paying users are:** Bakeries, cafés, and small F&B operators with 5–50 daily surplus units. This segment has predictable surplus patterns, digital readiness, and genuine economic pain from food waste.

---

## 3. Key Product Decisions

| Decision Area            | Options Considered                                     | Final Choice                                   | Why This Improved the Product                                                                                                                                                                                 |
| ------------------------ | ------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Target user**          | Consumer marketplace vs merchant operations            | Merchant operations                            | Merchants have clearer pain, single-sided acquisition, defensible AI value                                                                                                                                    |
| **Problem scope**        | Full marketplace vs decision support only              | Decision support only                          | Faster to deploy, clearer value proposition, no chicken-and-egg                                                                                                                                               |
| **Model role**           | Central ML dashboard vs one layer of a decision system | One layer of a decision system                 | Prediction alone doesn't help a merchant act; downstream logic converts prediction to action                                                                                                                  |
| **Decision workflow**    | Show prediction score vs guide to action               | Guide to action (HOLD/DISCOUNT/DONATE/DISCARD) | Merchants need operational guidance, not another number                                                                                                                                                       |
| **Recommendation logic** | Learned discount policy vs rule-based tier engine      | Rule-based tier engine                         | Transparent, explainable, no feedback loop required, safety-appropriate                                                                                                                                       |
| **Food-safety logic**    | Disclaimer vs active gate                              | Active gate with BLOCK/CAUTION/SAFE            | Safety is non-negotiable; merchants need to trust the system before acting                                                                                                                                    |
| **Recovery-value logic** | None vs calculated estimate                            | Calculated estimate                            | Merchants care about revenue recovery, not just discount percentage                                                                                                                                           |
| **Cold-start approach**  | Generic average vs category benchmark                  | Category benchmark                             | New merchants get relevant estimates immediately; improves with their own data                                                                                                                                |
| **Business model**       | Transaction commission only vs SaaS + commission       | SaaS + 15% transaction fee                     | SaaS provides immediate revenue; commission aligns incentives once volume builds. Note: SaaS pricing figures are proposed hypotheses, not validated willingness-to-pay — merchant pilots required to confirm. |
| **Deployment model**     | Consumer app vs merchant dashboard                     | Merchant dashboard                             | Simpler acquisition, clearer value, faster pilot                                                                                                                                                              |

---

## 4. Rejected Options

| Rejected Option                            | Why It Was Rejected                                                                                                                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Two-sided consumer marketplace**         | Chicken-and-egg problem, trust-building required, resource-intensive MVP, direct competition with established players                                         |
| **Pure prediction-only dashboard**         | Answers the wrong question; merchants don't need to know predicted waste — they need to know what to do about it                                              |
| **Black-box learned discount policy**      | Requires consumer purchase feedback to improve; not learnable in MVP timeframe; merchants wouldn't trust opaque recommendations for safety-critical decisions |
| **Hawker stalls as initial segment**       | Lower transaction values, less predictable surplus patterns, collective decision-making, different regulatory considerations                                  |
| **Overly complex ML ensemble**             | Higher accuracy but opaque; explanation becomes impossible; marginal improvement doesn't justify complexity for merchant trust                                |
| **Real merchant data from day one**        | Unavailable without partnerships; using real data without consent creates legal risk                                                                          |
| **Transaction commission as only revenue** | Zero revenue until consumer volume builds; merchants won't wait                                                                                               |
| **Automated safety decisions**             | Food safety liability requires human judgment; system should advise, merchant decides                                                                         |
| **Video demo as primary evidence**         | Recording/editing takes 1–2 hours; writing a working demo takes 20 minutes and is more impressive                                                             |
| **Generative AI for recommendations**      | Non-deterministic, harder to explain, potential hallucinations in safety contexts; rule-based is safer and clearer                                            |

---

## 5. Rejected COC Defaults and AI Suggestions

The course rewards student judgment, not blind acceptance of AI defaults. The following decisions represent cases where I actively rejected a COC or AI suggestion in favour of a deliberate alternative:

**1. Rejected: building a generic food-waste awareness dashboard**
_COC/AI default:_ Many COC-generated product concepts default to dashboards showing analytics and trend lines — a passive view of the problem.
_Why I rejected it:_ A dashboard answers "what happened?" not "what should I do?" Merchants do not have time to interpret a dashboard at 4pm. The recommendation engine translates prediction into action — that is the product, not the number.

**2. Rejected: a pure consumer marketplace (C2C or B2C)**
_COC/AI default:_ Consumer-facing platforms are the most common F&B waste tech concept and tend to appear in generic AI product generation.
_Why I rejected it:_ Consumer marketplaces face a cold-start problem (no consumers without merchants, no merchants without consumers), require liquidity at scale, and compete directly with established players (Treatsure, Too Good To Go). A merchant-side decision tool has single-sided acquisition — the merchant is the only user needed to get value.

**3. Rejected: relying on LLM/generative AI for recommendation logic**
_COC/AI default:_ Generative AI is the default "smart" recommendation approach in modern COC toolchains.
_Why I rejected it:_ Food safety cannot be entrusted to a non-deterministic model. An LLM might hallucinate a safe holding time or recommend listing an item past its safety window. A rule-based system is deterministic, fully explainable, and auditable. Every recommendation can be traced to a specific rule. When a merchant makes a wrong decision, we can identify exactly which rule failed — not which prompt token hallucinated.

**4. Rejected: overstating model accuracy claims**
_COC/AI default:_ Models tend to be presented with best-case metrics, using CV results as the primary headline number.
_Why I rejected it:_ The dataset is synthetic. Presenting a 0.68 MAE as a headline "accuracy" without disclosing that the data is prototype-generated is misleading. I chose to use holdout MAE as the headline number, disclose the synthetic data limitation prominently, and reframe the results as "evidence of technical feasibility" rather than production accuracy.

**5. Rejected: making the product fully autonomous**
_COC/AI default:_ AI products often imply or aim for autonomous decision-making — the AI "does the job."
_Why I rejected it:_ A merchant who delegates a food safety decision to an autonomous system creates unresolvable liability. If an unsafe item causes harm, the merchant is accountable, not the model. The product must position itself as advisory — the merchant decides, the system recommends. This framing also makes merchant adoption more likely: no merchant will trust a black-box system that bypasses their judgment.

**6. Rejected: Hawker centres and markets as the initial target segment**
_COC/AI default:_ Hawker centres are a visible, relatable Singapore food context and commonly appear in F&B tech concepts.
_Why I rejected it:_ Hawker stall operators face collective decision-making (family-run operations), lower per-unit transaction values, and less predictable surplus patterns. Bakeries and cafés have more structured operations, higher average ticket prices, and clearer surplus economics. The merchant persona that pays SGD 99–299/month needs to be an operator with P&L accountability, not a hawker who disposes of 3 items a day.

---

## 6. Model Validity and Leakage Control

This section documents the honest ML judgment applied to this project, including where the current implementation has known limitations that production would need to address.

### Current Model Is Prototype-Level Only

The model was trained and evaluated on synthetic F&B data generated by `data/generate_synthetic_data.py`. The data is designed to reflect realistic merchant patterns but has not been validated against real merchant operations. **All performance metrics (temporal holdout MAE 0.64, RMSE 0.81, R² 0.91) are evidence of feature-signal logic and directional feasibility, not proof of production accuracy.** Real merchant data is required before the model can be trusted for commercial deployment.

### Aggregate Feature Leakage — FIXED

The original feature engineering pipeline (`src/feature_engineering.py`) used full-dataset aggregates for merchant-level, category-level, and merchant-type-level features — a form of **aggregate target leakage**. The fix has been **implemented**, not just documented:

**Fix implemented:** All aggregate features now use **expanding-window logic** with `shift(1)`:

```python
# Pattern used in create_merchant_aggregates(), create_category_aggregates(),
# create_merchant_type_aggregates(), and create_demand_features():
grp = df.groupby("merchant_id")["surplus_quantity"]
df["merchant_avg_surplus"] = grp.cumsum().shift(1) / grp.cumcount().replace(0, float("nan"))
```

For each row at date D, `merchant_avg_surplus` uses only surplus values from dates **strictly before D** — no future data leaks in. The same pattern applies to `category_avg_surplus`, `type_avg_surplus`, `dow_avg_sold`, and `dow_avg_surplus`.

**`surplus_vs_merchant_avg` removed:** This interaction feature computed `surplus_quantity - merchant_avg_surplus` using the current row's own target, which is **current-row target leakage**. It has been removed from the feature set entirely. The model now uses **46 features** (down from 47).

### Lag and Rolling Features Are Clean

- Lag features (`prev_day_surplus`, `same_weekday_last_week_surplus`) use `.shift(1)` and `.shift(7)` — point-in-time, no lookahead.
- Rolling features (`surplus_7day_avg`, `surplus_7day_max`, `surplus_7day_std`) use `.shift(1)` before `.rolling()` — window looks backward only.

### Evaluation Uses Temporal Holdout, Not Random Split

The holdout evaluation uses an **80/20 temporal split** (last 20% of dates as holdout, sorted by date), not a random split. This gives a more realistic estimate of forward-looking performance. The temporal holdout MAE is the authoritative metric.

TimeSeriesSplit cross-validation (5-fold) provides additional validation, with higher variance across folds reflecting distributional shift in the synthetic data.

### Production Validation Requirements

Before commercial deployment, the following must be completed:

1. Retrain model on real merchant data
2. Continue using temporal train/test split
3. Aggregate features already use expanding-window logic — ensure this is preserved on retraining
4. Evaluate MAE/RMSE on the temporal holdout
5. Compare against the Previous Day baseline in production conditions
6. Measure recommendation acceptance rate and avoided waste
7. Calibrate safety rule thresholds against actual operating conditions

### Honest Framing of Results

The model results (XGBoost temporal holdout MAE 0.64 vs historical average MAE 1.49) demonstrate that the 46-feature signal captures merchant-level and temporal patterns meaningfully. The **57% improvement** over the historical average baseline (computed on the same temporal holdout) is substantial. However, these numbers come from a synthetic dataset where the data-generating process is known to the model through the feature engineering. Real merchant data will have noise, anomalies, and distributional shift that the synthetic data does not fully represent.

---

## 7. Prototype-to-Mature-Product Evolution

| Area                        | 90-Minute Prototype                     | Mature Product                                                                   |
| --------------------------- | --------------------------------------- | -------------------------------------------------------------------------------- |
| **User**                    | Technical evaluator                     | F&B merchant operations manager                                                  |
| **Problem definition**      | "Predict food waste with ML"            | "Help merchants decide what to discount, donate, or discard before waste occurs" |
| **Model role**              | Central — the product is the prediction | Supporting — one layer of a decision workflow                                    |
| **Decision output**         | Prediction score (MAE, RMSE)            | Recommended action + discount tier + safety status + recovery estimate           |
| **Safety logic**            | None (implicit disclaimer)              | Five active checks with BLOCK/CAUTION/SAFE gating                                |
| **Recovery-value logic**    | None                                    | Calculated: original value, discount amount, estimated recovery, recovery rate   |
| **UI**                      | ML metrics dashboard                    | Step-by-step decision workflow with action recommendations                       |
| **Business case**           | None                                    | SaaS + 15% commission, TAM/SAM/SOM analysis, unit economics                      |
| **Cold-start**              | Not addressed                           | Category benchmark fallback for new merchants                                    |
| **Deployment readiness**    | Jupyter notebook                        | Interactive Streamlit dashboard, documented pipeline, 63 passing tests           |
| **Limitations**             | Not discussed                           | Explicitly documented: synthetic data, advisory safety rules, MVP scope          |
| **ML validity**             | Unquestioned                            | Aggregate leakage documented; expanding-window fix identified                    |
| **AI suggestion rejection** | Not applicable                          | Five explicit rejections of COC/AI defaults documented                           |

---

## 8. Evidence of Judgment

Every significant claim is tied to actual project outputs:

| Claim                               | Evidence                                                       |
| ----------------------------------- | -------------------------------------------------------------- |
| XGBoost MAE 0.64 (temporal holdout) | `outputs/model_results.csv`, `models/model_metadata.json`      |
| 57% improvement over baseline       | Computed: (1.49 − 0.64) / 1.49 on temporal holdout             |
| 10-tier discount engine             | `src/recommendation_engine.py` lines 37–53                     |
| 5 food safety checks                | `src/food_safety_rules.py` — 5 `check_*` functions             |
| 63 passing unit tests               | `pytest tests/unit/ -v` output                                 |
| RANDOM_SEED=42                      | `src/train_model.py`, `data/generate_synthetic_data.py`        |
| 46 engineered features              | `src/feature_engineering.py` `get_feature_columns()` (was 47)  |
| Expanding-window aggregates fixed   | `tests/unit/test_leakage_awareness.py` — confirms 5.0 not 10.0 |
| Temporal 80/20 holdout              | `src/train_model.py` lines 524–537                             |

**What I did NOT claim:**

- Real merchant adoption or pilot results
- Production deployment
- SFA regulatory approval for safety rules
- POS integration (not built)
- Actual revenue figures (used model-based estimates only)
- Model accuracy on real data (synthetic data only)
- That the current model is production-ready (clearly stated as prototype-level)

---

## 9. Remaining Limitations

These are honestly stated, not minimized:

| Limitation                            | Impact                                                                         | Mitigation                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Synthetic data only**               | Model accuracy on real merchant data unknown                                   | Pilot with 3–5 volunteer merchants before scaled deployment                   |
| **Aggregate feature leakage**         | Was a risk; FIXED: all aggregates now use expanding-window logic with shift(1) | No action needed — fix is implemented                                         |
| **Random train/test split**           | Was a risk; FIXED: temporal 80/20 holdout is now the primary evaluation metric | No action needed — fix is implemented                                         |
| **Food safety rules are advisory**    | Not SFA-validated; merchant assumes responsibility                             | Clear disclaimer in UI; BLOCK/CAUTION/SAFE is guidance, not authority         |
| **Single-tenant MVP**                 | No multi-merchant support, no auth                                             | Phase 2 requires multi-tenant infrastructure                                  |
| **Cold-start uses category averages** | Less accurate for unusual merchants                                            | Improves as merchant-specific data accumulates                                |
| **No POS/inventory integration**      | Manual data entry required                                                     | Phase 2 integrates with POS/inventory systems                                 |
| **No model drift monitoring**         | Model accuracy may degrade over time                                           | Phase 2 requires drift detection and retraining pipeline                      |
| **Transaction fee not yet charged**   | No real revenue validation                                                     | Pilot phase will validate willingness-to-pay                                  |
| **Validation evidence gap**           | No live merchant pilot conducted                                               | PILOT_VALIDATION_PLAN.md defines 4-week structured evidence-collection design |

---

## 10. Final Reflection

**What I learned about moving from prototype to product:**

A prototype demonstrates that a technology works. A product solves a problem someone will pay for. The gap between them is not technical — it is judgmental. The prototype's ML pipeline was sound. What made SurplusSense a product was asking: _what decision does this output enable, and does the merchant have everything they need to make it?_

The answer required more than better predictions. It required translating the prediction into an action, adding safety guardrails, calculating financial outcomes, and presenting it in a way that a busy merchant could use in 30 seconds.

**Why product judgment matters more than generating code:**

Code can be generated. Product sense cannot. The decision to use rule-based recommendation over learned policy was not a technical choice — it was a judgment about trust, explainability, and operational safety. No ML benchmark would have made that choice correctly.

**On separating model estimates from commercial validation:**

I deliberately separated model-estimated recovery value from validated willingness-to-pay. The SGD 6.65 daily recovery figure is a model output applied to synthetic data — useful for establishing a product hypothesis, but not proof of merchant demand. SaaS pricing (SGD 99–299/month per outlet) is a proposed range requiring pilot validation. This distinction keeps the business case honest: the product is pilot-ready; commercial assumptions require merchant feedback to confirm.

**On ML honesty and leakage:**

During the upgrade work, I identified that aggregate features (merchant_avg_surplus, category_avg_surplus, dow_avg_surplus) were computed over the full dataset before the train/test split — a form of aggregate target leakage. This was **fixed**: all aggregate features now use expanding-window logic with `shift(1)`, ensuring each row's aggregates use only data from prior dates. The lag features and rolling features were already clean.

**Final validation judgment:** Instead of overstating market readiness, I added a pilot validation plan to separate what the current product demonstrates (working decision-support logic, reproducible pipeline, transparent rules, documented leakage limitations) from what must still be proven in live merchant use (actual recovery value, staff adoption, willingness to pay). This is deliberate restraint — appropriate for an individual project, not a proof of commercial viability.

---

## 11. Final Decision Audit: Where Human Judgment Overrode Default AI Output

This section makes explicit where AI/COC environment generated options but human judgment shaped the final product.

| COC / AI tendency                                  | Human intervention                            | Final product decision                                  | Why this improved the product                                                 |
| -------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Treat the product as an ML dashboard               | Reframed it as a decision-support workflow    | Prediction became only one layer of the product         | Better aligned with merchant operational decisions                            |
| Optimise for model accuracy                        | Added safety and recovery-value layers        | Output became action + safety + commercial impact       | More useful to non-technical users                                            |
| Use generic random train/test split                | Required temporal holdout and TimeSeriesSplit | Evaluation better reflects real deployment conditions   | Reduced risk of overstated model performance                                  |
| Use aggregate features without checking leakage    | Identified and fixed target leakage           | Used expanding-window aggregates with shift(1)          | Improved methodological credibility                                           |
| Let ML recommend the final action                  | Rejected black-box learned policy             | Used deterministic recommendation and safety rules      | Safer and more explainable for food handling                                  |
| Assume commercial viability from prototype metrics | Added pilot validation plan                   | Separated technical feasibility from market validation  | Avoided overclaiming and showed business discipline                           |
| Target hawker stalls as initial segment            | Chose bakeries and cafés instead              | Bakery/cafe segment with clearer surplus economics      | Higher recovery value, more structured operations, clearer P&L accountability |
| Default to consumer marketplace                    | Chose merchant-side tool                      | Single-sided acquisition, no cold-start chicken-and-egg | Faster time-to-value, no competition with established consumer platforms      |

This decision audit is included to make my original contribution explicit. The AI/COC environment helped generate implementation options, but the final product direction was shaped by human judgment around merchant usability, safety risk, validation discipline, and commercial feasibility.

**Human judgment summary:** Every significant product decision — from rejecting the consumer marketplace to using rule-based recommendations to fixing aggregate leakage — was made by deliberate human evaluation of trade-offs, not by AI default. The 8-row audit table above documents where the AI/COC environment suggested one direction and human judgment chose another. This reflects the COC principle that AI agents generate options; humans evaluate and decide.

---

## 12. ML Technique Family Declaration

SurplusSense foregrounds **supervised machine learning** through XGBoost surplus prediction, combined with deterministic recommendation and food-safety rules. This differs from the team project, WanderLess, which foregrounds recommender systems and optimization through hybrid tourist-guide matching, TruncatedSVD collaborative filtering, content-based compatibility scoring, and itinerary optimization.

The supervised regression approach (XGBoost predicting surplus units) was chosen for temporal holdout performance and explainability, not as the only viable ML technique for the problem space.

---

## Final Decision Completeness Check

| Decision area       | Final decision                             | Rejected alternative                      | Why the final decision is stronger                                                   |
| ------------------- | ------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------------------------------ |
| Product scope       | Merchant-side decision cockpit             | Full consumer marketplace                 | Better aligned to MGMT655 decision-support requirement and achievable as working MVP |
| User                | F&B outlet manager / staff                 | General consumers                         | Merchant owns the surplus action decision                                            |
| ML technique        | Supervised regression with XGBoost         | Generic AI dashboard or pure rules        | Predicts surplus quantitatively while retaining explainable decision rules           |
| Validation          | Temporal holdout and TimeSeriesSplit       | Random split as primary claim             | Better reflects future deployment and reduces inflated accuracy risk                 |
| Feature engineering | Shifted lag / rolling / expanding features | Full-dataset aggregates                   | Reduces target leakage                                                               |
| Recommendation      | Deterministic action rules                 | Black-box learned policy                  | Safer and easier for merchants to trust                                              |
| Safety              | Safety gate overrides commercial action    | Optimise purely for recovery value        | Avoids unsafe food recommendations                                                   |
| Business case       | SaaS + recovered-value logic               | Generic ESG benefit claim                 | Links product value to merchant economics                                            |
| Market expansion    | Marketplace as Phase 2                     | Marketplace as final MVP                  | Avoids overbuilding and preserves ML decision depth                                  |
| Validation claim    | Pilot-ready, not production-validated      | Claiming market proof from synthetic data | More honest and academically defensible                                              |

The final decision trail is complete because it shows problem framing, scope narrowing, user selection, ML technique selection, validation design, leakage control, recommendation design, safety governance, business-case logic, and pilot limitation. These decisions demonstrate human judgment over COC-generated alternatives.

---

## Appendix: Decision Summary Table

| Decision                                   | Status   | Key Reason                                                     |
| ------------------------------------------ | -------- | -------------------------------------------------------------- |
| Merchant vs consumer focus                 | ACCEPTED | Clearer pain, single-sided acquisition                         |
| Decision support vs prediction dashboard   | ACCEPTED | Answers what merchants actually need                           |
| XGBoost as predictive layer                | ACCEPTED | Best temporal holdout performance, 57% improvement             |
| Rule-based recommendation engine           | ACCEPTED | Transparent, explainable, no feedback loop needed              |
| Food safety as active gate                 | ACCEPTED | Merchant trust, liability protection                           |
| Recovery value calculation                 | ACCEPTED | Merchants care about revenue, not just discount %              |
| Category benchmark for cold-start          | ACCEPTED | Immediate value for new merchants                              |
| SaaS + transaction fee model               | ACCEPTED | Revenue from day one, incentives align                         |
| Synthetic data                             | ACCEPTED | No real data available; limitations documented                 |
| Aggregate leakage fixed (expanding-window) | ACCEPTED | Expanding-window aggregates implemented in feature engineering |
| Hawker segment deferred                    | ACCEPTED | Lower recovery, higher complexity                              |
| Reinforcement learning deferred            | ACCEPTED | Requires feedback loop not available in MVP                    |
| Consumer recommender deferred              | ACCEPTED | No interaction data; wrong MVP focus                           |
| Reject LLM recommendation logic            | ACCEPTED | Non-deterministic; unsafe for food safety                      |
| Reject autonomous decisions                | ACCEPTED | Merchant accountability and food safety                        |

---

_Document maintained as part of SMU MBA ML course submission. Each decision reflects deliberate product thinking, validated against actual model outputs and business analysis._
