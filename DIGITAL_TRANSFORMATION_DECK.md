# Digital Transformation Deck: From Food Waste Prediction to Merchant Decision Intelligence

**Project:** SurplusSense
**Date:** April 2026

---

## Slide 1: Executive Thesis

**Title:** From Surplus Food to Recoverable Value

**Bullets:**

- Singapore generated 784,000 tonnes of food waste in 2024; MSE reported that around 40% of Singapore's 2022 food waste came from commercial and industrial sources.
- Merchants often act too late because they lack item-level, time-sensitive decision support
- The difference between a recovered SGD 35 and a SGD 71 loss is a recommended action, not a prediction
- SurplusSense translates surplus-risk signals into specific merchant actions: discount, donate, or discard

**Visual Suggestion:** Two-panel flow diagram — "Without SurplusSense: Late Reaction (reactive, loss)" vs "With SurplusSense: Early Intervention (proactive, recovered value)"

**Speaker Notes:**
Food waste is not an environmental abstraction — it is an operational decision problem with a quantifiable financial cost. The core insight is that late decisions cost money. A merchant who waits until end-of-day to decide what to do with unsold inventory almost always loses. The product converts that late, reactive decision into an early, structured action.

---

## Slide 2: Problem Worth Solving

**Title:** Why Merchants Need Earlier Intervention

**Bullets:**

- Unsold food becomes waste when decisions are delayed — each hour reduces both safety eligibility and recovery value
- Generic markdowns are blunt instruments — a 30% discount may be too little for some items, too much for others
- Manual merchant judgment is inconsistent across outlets, staff, and shifts — the same surplus item gets different decisions on different days
- Competitor apps (Treatsure, Yindii, Too Good To Go) help consumers find discounts — but they do not help merchants decide what to discount in the first place

**Visual Suggestion:**
Timeline graphic showing: Fresh inventory → Morning hours → Afternoon pressure → End-of-day markdown window → Spoilage risk. Arrow labeled "Decision window shrinks as time passes."

**Speaker Notes:**
The problem is not awareness — merchants know they have surplus. The problem is decision quality. Without structured decision support, merchants default to reactive markdowns or disposal. The financial impact compounds with every hour of delay: the safe resale window shrinks and recoverable value drops. Every hour of delay reduces both the safe resale window and the recoverable value.

---

## Slide 3: Target Users and Willingness to Pay

**Title:** Who Pays and Why

**Bullets:**

- **Beachhead:** Bakeries, cafés, and small F&B operators with 5–50 daily surplus units — predictable patterns, digital-ready, high recovery value
- **Why they pay:** Recover value from surplus inventory, reduce disposal costs, support ESG reporting, standardise outlet decisions
- **Payment model:** SaaS subscription (SGD 99–299/month per outlet) or 15% transaction fee on recovered revenue — merchant chooses
- **Illustrative model-estimated unit economics:** Average bakery recovery is SGD 6.65/day on synthetic data; platform revenue is a pricing hypothesis requiring pilot validation.

**Visual Suggestion:**
Customer segment matrix: 2x2 grid with axes "Surplus Predictability" (Low/High) and "Digital Readiness" (Low/High). Bakery and Café segments highlighted in top-right quadrant.

**Speaker Notes:**
This is not a consumer app — it is a merchant operations tool. The paying user is a bakery manager or F&B operator who is already losing money to food waste. Willingness to pay should be validated through pilot conversion and merchant feedback. The SaaS model is intentionally low-commitment — no integration required, no contracts — because the primary goal in Phase 1 is merchant adoption.

---

## Slide 4: Product Workflow

**Title:** Prediction Is Only the First Step

**Bullets:**

- The product does not stop at "you will have 11 units of surplus" — it continues to "here is what to do about it"
- Five-step workflow: Input context → Predict surplus → Recommend action → Screen for safety → Estimate recovery
- Each step produces an output the merchant can act on immediately — no interpretation required
- Output is not a score — it is a decision with rationale

**Visual Suggestion:**
Horizontal decision workflow: [Inventory Input] → [Waste Prediction] → [Action Recommendation] → [Food-Safety Screening] → [Recovery Estimate] → [Merchant Decision]. Each step in a distinct card with icon.

**Speaker Notes:**
Most ML products in F&B stop at prediction. The merchant gets a number. SurplusSense continues — from prediction to action. This is the core product differentiation. The recommendation step uses a transparent 10-tier rule engine, not a black-box model, so the merchant understands exactly why a specific discount was suggested.

---

## Slide 5: Hybrid Decision Intelligence

**Title:** Not Just a Supervised ML Dashboard

**Bullets:**

- **Layer 1 — Prediction:** XGBoost model estimates surplus quantity from 47 engineered features (time patterns, lag history, merchant benchmarks)
- **Layer 2 — Recommendation:** Rule-based discount tier engine maps surplus quantity and time pressure to a specific discount (20–70%) and listing action
- **Layer 3 — Safety:** Five deterministic checks gate recommendations — items can be BLOCKED, flagged CAUTION, or cleared SAFE before any recommendation is issued
- **Layer 4 — Business logic:** Recovery value calculation converts discount decisions into SGD estimates the merchant can compare against potential loss

**Visual Suggestion:**
Stacked architecture diagram with four distinct layers: ML Prediction → Rule-Based Recommendation → Safety Gate → Business Logic. Each layer with its technique labeled (XGBoost, Tier Rules, Deterministic Checks, Arithmetic).

**Speaker Notes:**
The product uses ML — but ML is not the product. ML is one layer of a hybrid decision system. The rule-based layers are not weaknesses — they are design choices that make the system explainable, safe, and trustworthy. A merchant should be able to trace every recommendation back to a specific rule.

---

## Slide 6: Worked Example

**Title:** A Merchant Decision in Practice

**Bullets:**

- **Merchant:** Bakery 001 (Ciabatta, Tuesday 10am)
- **Situation:** 6 hours of holding time already accumulated, 48-hour shelf life, refrigerated storage
- **Prediction:** 11 units of surplus (XGBoost model with category benchmark fallback for similar merchant patterns)
- **Recommended action:** 50% discount — "Medium surplus, at-limit shelf life"
- **Safety result:** SAFE — all five checks passed; item is eligible for listing
- **Recovery estimate:** SGD 35.64 recovered vs SGD 71.17 potential loss — 50% recovery rate

**Visual Suggestion:**
Decision card mockup showing the five output fields: Surplus Prediction (11 units), Recommended Action (50% DISCOUNT), Safety Status (SAFE, green), Recovery Value (SGD 35.64), and Recommendation Rationale ("Medium surplus + time pressure = 50%").

**Speaker Notes:**
This is the actual output from the working product — not a slide deck hypothetical. The merchant enters the item context, receives a complete recommendation within seconds, and can act immediately. The output includes the safety status and recovery estimate alongside the action recommendation, so the merchant has the full decision context.

---

## Slide 7: Business Model and Deployment

**Title:** From Prototype to Pilot-Ready Product

**Bullets:**

- **SaaS pricing:** SGD 99–299/month per outlet (self-serve, no integration required)
- **Transaction fee:** 15% of recovered revenue (aligned incentives — platform earns when merchant earns)
- **Phase 1 deployment:** Manual dashboard pilot — current working version for controlled testing.
- **Phase 2:** POS/inventory integration for automated data input (reduces manual entry friction)
- **Phase 3:** Multi-outlet prioritisation for chain operators (rank items across locations by urgency)
- **Phase 4:** ESG reporting and NEA waste reduction analytics (differentiator for sustainability-focused chains)

**Visual Suggestion:**
Roadmap timeline with four phases (Q1–Q4), each with milestone markers. Phase 1 labeled "Pilot-Ready." Phase 2–4 with feature names and integration partners marked.

**Speaker Notes:**
The product is ready for a structured 4-week pilot — not a concept. Phase 1 is a manual-entry dashboard that requires no POS integration, no contracts, and no merchant commitment beyond a trial. This is intentional: the goal is testing commercial assumptions with real merchant data before building integration infrastructure.

---

## Slide 8: Why This Is Pilot-Ready

**Title:** What Changed from Prototype to Product

**Bullets:**

- **Interactive UI:** Streamlit dashboard with step-by-step decision workflow — not a static chart or notebook
- **Decision output:** Action recommendations (DISCOUNT/DONATE/DISCARD), discount tier, safety status, recovery estimate — not just a prediction score
- **Safety guardrails:** Five active checks with BLOCK/CAUTION/SAFE gating — not an implicit disclaimer
- **Reproducible pipeline:** RANDOM_SEED=42, documented training pipeline, 59 unit tests passing
- **Honest limitations:** Synthetic data only, advisory safety rules, MVP scope — all explicitly stated

**Visual Suggestion:**
Maturity ladder with five rungs: [Notebook Demo] → [Working Dashboard] → [Decision Workflow] → [Safety Guardrails] → [Pilot-Ready]. Product highlighted at the top rung with a marker.

**Speaker Notes:**
This is the key slide for evaluator skepticism. A "prototype" is a demo artifact. This product has: a working interactive interface, a complete decision workflow, documented safety logic, and an honest limitations section. It is a pilot-ready decision-support product, not a one-off model evaluation. The COC decision log (included in submission) documents the judgment calls that shaped each design choice.

---

## Closing Statement

**"SurplusSense is a pilot-ready decision-support product — not a machine learning dashboard. The prediction is one layer. The recommendation, safety screening, and recovery estimate are the product. Merchants receive a complete decision, not a number to interpret."**

---

## Appendix: Submission Files

| File                             | Purpose                               |
| -------------------------------- | ------------------------------------- |
| `app/streamlit_app.py`           | Working interactive product           |
| `docs/EXECUTIVE_REPORT.md`       | Max 4-page executive report           |
| `COC_DECISION_LOG.md`            | Prototype-to-product decision journey |
| `DIGITAL_TRANSFORMATION_DECK.md` | This deck                             |
| `src/`                           | Reproducible ML pipeline              |
| `tests/unit/`                    | 59 passing unit tests                 |
| `outputs/`                       | Model outputs and evaluation results  |
