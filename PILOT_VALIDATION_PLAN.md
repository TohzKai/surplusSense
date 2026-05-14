# Pilot Validation Plan: SurplusSense

## 1. Validation Objective

The next step is to test whether the decision-support workflow actually improves merchant decisions in a real operating environment. This is not a deployment milestone — it is an evidence-gathering exercise designed to answer five questions:

- Does the recommendation adapt usefully to real operational context?
- Do merchants and staff accept and act on recommendations?
- Do safety-gate exceptions surface genuine risk cases?
- Is recovered value sufficient to justify a per-outlet subscription?
- What rule adjustments does real data demand?

---

## 2. Pilot Design

**Proposed setup:** 4-week engagement with 3–5 volunteer bakeries or cafés in Singapore.

**Scope per outlet:**

- 1–2 daily surplus decision cycles (morning and afternoon)
- Staff enter item context manually via the dashboard
- Recommendations issued; staff record accept / override / ignore with a brief reason

**Comparison baseline:** Each outlet's own pre-pilot surplus decisions (documented via a two-week observation period before the pilot starts).

**What this is not:** A live deployment, a commercial pilot, or a willingness-to-pay transaction. No actual pricing is charged during the trial.

---

## 3. Success Metrics

| Metric                         | What It Measures                                         | Why It Matters                                          |
| ------------------------------ | -------------------------------------------------------- | ------------------------------------------------------- |
| Recovery value per day         | Model-estimated or actual revenue recovered from surplus | Tests commercial usefulness directly                    |
| Waste avoided (units)          | Items diverted before disposal                           | Tests operational impact                                |
| Recommendation acceptance rate | % of recommendations accepted by staff                   | Tests workflow usability and trust                      |
| Override reason                | Why staff rejected recommendations                       | Identifies rule gaps and UX friction                    |
| Safety exception rate          | % of items flagged CAUTION or BLOCKED                    | Tests whether safety gates fire at meaningful frequency |
| Willingness-to-pay signal      | Staff / manager response to "would you pay for this?"    | Early indicator of commercial viability                 |

---

## 4. Decision Thresholds for Go / No-Go

| Pilot Result                               | Interpretation                          | Product Decision                                         |
| ------------------------------------------ | --------------------------------------- | -------------------------------------------------------- |
| High acceptance + positive recovery signal | Strong product-market fit               | Advance to paid pilot with 2–3 outlets                   |
| Low acceptance + positive recovery         | UX or onboarding friction               | Redesign workflow; clarify recommendation rationale      |
| High overrides due to safety concerns      | Safety rules mis-calibrated             | Revise rules against actual operating procedures         |
| Low recovery and low acceptance            | Weak value proposition for this segment | Reassess target segment or discount recommendation logic |

Thresholds are indicative; the pilot is diagnostic, not a pass/fail gate.

---

## 5. Data Needed Before Production

The pilot produces or refines the following real-data inputs required before full deployment:

- **POS sales history** — for retraining the surplus prediction model on actual merchant patterns
- **Inventory snapshots** — to calibrate category-specific surplus ratios and shelf-life assumptions
- **Actual disposal records** — to compare against model-predicted surplus
- **Markdown history** — to understand existing discount practices and set baseline recovery rates
- **Product shelf-life policies** — to validate or correct the safety rule parameters
- **Staff override reasons** — to improve rule thresholds and recommendation explanations
- **Outlet operating hours** — to calibrate listing time recommendations
- **Food-safety compliance review** — before safety gates are relied upon for actual listing decisions

---

## 6. Risks and Mitigations

| Risk                                                         | Mitigation                                                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Synthetic training data may not generalise to real merchants | Retrain XGBoost model on pilot merchant data; compare holdout performance before and after |
| Staff may ignore or override all recommendations             | Capture every override with reason; use findings to improve recommendation clarity         |
| Safety rules may be incomplete or mis-calibrated             | Run rules against actual operating conditions; calibrate against food-safety guidance      |
| Pricing may not match willingness to pay                     | Include explicit "would you pay" signal in end-of-pilot survey                             |
| POS integration may be harder than manual entry              | Start with manual CSV upload; do not scope POS integration to Phase 1 pilot                |

---

## 7. Why This Strengthens Market Readiness

The current product is **pilot-ready**: the dashboard works, the recommendation logic is documented, the safety rules are defined, and the model is reproducible. What the product does not yet have is evidence that it works in a real operating environment.

The pilot validation plan demonstrates that this evidence gap is understood, that the next step is concrete, and that the path from "working prototype" to "commercial product" is defined — not as an aspiration, but as a structured four-week data-collection exercise with defined success metrics.

This separates the product from a pure ML exercise: it shows the decision-support logic, the safety gating, and the business model are not academic abstractions — they are designed to be validated against actual merchant behaviour.

---

## 8. Merchant Interview Questions

The following five questions are proposed for qualitative interviews with outlet managers or staff, to be conducted before or during the pilot:

1. **Which surplus decisions are hardest to make in your current workflow?**
   _(Identifies decision pain points the dashboard should target)_

2. **When do staff typically decide to discount, donate, or discard items?**
   _(Reveals whether timing and process match the dashboard's workflow)_

3. **Would a recommendation dashboard fit into your daily outlet operations?**
   _(Tests workflow integration — manual entry friction is the key barrier)_

4. **What evidence would make you trust or override a recommendation?**
   _(Informs what the explanation layer needs to show — price, shelf life, safety, or history)_

5. **At what monthly price would this tool need to recover in value to be worth paying for?**
   _(Gives a direct willingness-to-pay anchor without a commitment)_
