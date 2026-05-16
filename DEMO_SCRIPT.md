# SurplusSense Demo Script

**Duration:** 3–5 minutes
**Audience:** Professor, evaluator, or potential business sponsor
**Goal:** Demonstrate that SurplusSense is a working decision-support product — not a notebook or slide deck

---

## Opening (30 seconds)

> "SurplusSense helps food merchants decide what to do with predicted surplus before it becomes waste. It's a decision-support product for bakeries, cafés, and F&B operators — not a dashboard or an analytics view."

**Key point to emphasise:** The product answers "what should I do?" not "what happened?"

---

## The Problem (30 seconds)

> "Every day, food merchants face the same dilemma at 4pm: I have unsold inventory, what do I do with it?
>
> A deeper discount recovers more revenue but erodes margin on items that would have sold at full price. A shallow discount doesn't move enough units. Donation requires logistics. Disposal is pure loss.
>
> The decision is time-sensitive, involves margin, safety, and labour trade-offs — and most merchants make it from gut feel."

**Key point to emphasise:** This is a decision problem, not just a sustainability problem. The merchant needs to act, not just observe.

---

## Product Walkthrough (2–3 minutes)

**Step 1 — Open the app**

```
streamlit run app/streamlit_app.py
```

Dashboard opens at localhost:8501.

**Step 2 — Select merchant context**

Choose a merchant — for example, Bakery 001, Ciabatta bread.

The sidebar shows: merchant type, product category, storage type, holding time, shelf life.

**Step 3 — Run the prediction**

Click into the Surplus Prediction card. The model predicts — for example — **11 units** of predicted surplus for today.

Show the historical average next to it for comparison. The prediction is better than guessing from average.

**Step 4 — Show the recommendation**

Scroll to the Discount Recommendation hero card.

The app shows:

- **Recommended discount: 50%** (clearly displayed in large text)
- **Original price: SGD 6.47 → Discounted price: SGD 3.24**
- **Estimated recovery: SGD 35.64** against a potential loss of SGD 71.17
- **Recovery rate: 50%**

**Step 5 — Show the safety gate**

Below the recommendation: the Food Safety status shows **SAFE** — item passed all 5 safety checks.

Expand "View Safety Checks" to show:

- Shelf life check ✓
- Holding time check ✓
- Storage type check ✓
- Time-to-pickup window ✓
- Category-specific check ✓

> "If any safety check fails, the item is BLOCKED. It cannot receive a listing recommendation."

**Step 6 — Show the explanation**

The "Why this recommendation?" box explains in plain language:

> "11 units predicted surplus for Bread at Bakery 001 · 42h remaining shelf life · 50% discount recommended · Estimated recovery SGD 35.64 vs potential loss SGD 71.17"

**Step 7 — Show the consumer preview**

The "Phase 2 Listing Preview" card shows a preview of how the listing would appear to consumers — discount badge, pickup window, storage type, freshness. This is a Phase 2 extension preview; the submitted MVP is the merchant decision cockpit only.

**Step 8 — Adjust the inputs**

Use the sidebar to change to a different product — for example, Cakes from a Café — and show how the recommendation changes.

Use the Revenue Recovery Simulator to adjust discount level and surplus quantity and show how recovery value changes.

---

## How the ML Works (30 seconds)

> "The prediction model is XGBoost — 31 raw features (expanded to 47 model input columns after one-hot encoding), including:
>
> - Temporal patterns (day of week, weekend, month)
> - Lag features (previous day surplus, same weekday last week)
> - Rolling 7-day statistics
> - Merchant and category historical patterns (using expanding-window logic — no target lookahead)

> The model achieves MAE 0.64 units on a forward-looking temporal holdout — 57% better than the historical average baseline.

> The recommendation layer is rule-based, not learned. That is a deliberate choice: food safety decisions must be deterministic and explainable. We can trace every recommendation to a specific rule.

> The safety layer is a separate gate — it screens every recommendation before it reaches the merchant."

**Important caveat to state:**

> "These results are based on synthetic data — a prototype. Real merchant pilot validation is required before commercial deployment."

---

## Business Case (30 seconds)

> "Merchants pay because recovered value from surplus plus avoided disposal costs can exceed SGD 99–299 per month per outlet.
>
> Proposed pricing: SaaS subscription SGD 99–299/month per outlet, plus 15% transaction fee on recovered revenue.
>
> The market is Singapore's F&B operators — bakeries, cafés, small food operators with 5–50 daily surplus units. NEA data shows 784,000 tonnes of food waste annually, with commercial F&B a major contributor."

---

## Limitations (15 seconds)

> "Two important honest limitations:
>
> First — the dataset is synthetic. Model accuracy on real merchant data is unknown. The numbers demonstrate feature-signal logic, not production proof.
>
> Second — this is advisory only. Safety rules are based on general food safety principles, not SFA validation. The merchant remains the final decision-maker."

---

## Closing (15 seconds)

> "SurplusSense is not predicting surplus — it is supporting safer, faster, and more commercially disciplined end-of-day decisions.
>
> The product is working. The next step is a 4-week pilot with 3–5 real merchants to validate recovery value, staff adoption, and willingness to pay.
>
> Thank you."

---

## Demo Flow Summary (quick reference)

```
[Open app] → [Select merchant + product] → [Show prediction]
→ [Show recommendation card] → [Show safety gate]
→ [Show explanation] → [Show consumer preview]
→ [Run simulator] → [Business case] → [Limitations] → [Close]
```

## Key UI Elements to Highlight During Demo

During the live demo, call attention to these specific UI elements:

1. **Recommendation hero card** — large discount %, recovery value, action label (HOLD/DISCOUNT/DONATE/DISCARD)
2. **Food safety panel** — SAFE/CAUTION/BLOCKED status with the 5 checks listed
3. **Why this recommendation?** box — plain-language explanation of the recommendation logic
4. **Consumer listing preview** — how the item would appear to consumers on the listing platform
5. **Revenue Recovery Simulator** — interactive slider to explore discount/recovery trade-offs
6. **Model performance section** — MAE comparison chart vs baselines (shown in sidebar)

## Demo Tips

- Start with Bakery 001 + Ciabatta — the worked example in the executive report
- Show the cold-start mode (checkbox in sidebar) to demonstrate new merchant fallback
- If asked about model accuracy: repeat the synthetic data caveat clearly
- If asked about pricing: say "proposed hypothesis, not validated — needs pilot"
- If asked about competitors: "Treatsure/Yindii help consumers find discounts; we help merchants decide what to list"
