# User Guide — SurplusSense

**SurplusSense** is an AI decision-support tool for F&B merchants. It predicts how much surplus you will have at end of day and recommends what to do with it — hold, monitor, discount, donate, or discard.

---

## Who the App Is For

SurplusSense is designed for:
- **Bakery and café operators** who have surplus inventory at end of day
- **F&B outlet managers** who need a structured recommendation for surplus items
- **Small F&B operators** with 5–50 daily surplus units

You do not need to understand machine learning. You need to know what you made today and what it costs.

---

## What You Need to Get Started

1. **A computer or tablet** with a web browser
2. **Streamlit installed** (see installation guide in DEVELOPER_HANDOVER.md)
3. **Your outlet's product data** — the app works with synthetic demo data by default; real merchant data integration is planned for Phase 2

---

## Demo Flow: How to Use the App

### Step 1 — Open the App

Run `streamlit run app/streamlit_app.py` and open `http://localhost:8501` in your browser.

You will see the **Decision Workflow** at the top — a 5-step guide showing how to use the app.

### Step 2 — Select Your Merchant Context

In the **sidebar**, select:
- **Merchant** — your outlet name
- **Category** — the product category (Bread, Pastries, Cakes, etc.)
- **Product** — the specific item
- **Date** — today's date
- **Time** — current time

If you are a **new merchant** with fewer than 30 days of history, check the "Simulate new merchant (no history)" box to use category-benchmark predictions.

### Step 3 — Review the Executive Decision Summary

After selecting your context, you will see a summary at the top showing:
- **Recommended action** (HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD)
- **Why** — the predicted surplus quantity and recommended discount tier
- **Safety status** — SAFE, CAUTION, or BLOCKED
- **Estimated recovery** — SGD amount you could recover

### Step 4 — Check the Surplus Prediction

Scroll to **Surplus Prediction** to see:
- **Predicted surplus units** — how many units the model expects to go unsold
- **Historical average** — your outlet's typical surplus for this category
- **Today's actual** — the recorded surplus for the selected date

The prediction is most accurate when you have 30+ days of history.

### Step 5 — Review the Discount Recommendation

Scroll to **Discount Recommendation** to see:
- **Recommended discount** — the specific discount tier (e.g., 40%)
- **Original vs. discounted price** — what the item would sell for at the recommended discount
- **Revenue recovery estimate** — SGD amount you would recover
- **Listing schedule** — when to list the item and the pickup window deadline
- **Safety status** — whether the item is safe to list

### Step 6 — Adjust the Discount (Optional)

Use the **Revenue Recovery Simulator** to explore "what-if" scenarios:
- Move the **Discount Level** slider to see how different discounts affect recovery
- Move the **Surplus Quantity** slider to model different surplus volumes
- Adjust the **Original Price** to match your product

### Step 7 — Download or Save the Recommendation

Use the **Export** section to:
- Download the recommendation as a CSV file
- Save it to the Sample Recommendations log

---

## What Each Input Means

| Input | What It Is | How to Set It |
|-------|------------|---------------|
| **Merchant** | Your outlet name and type | Select from the list |
| **Category** | Product category (e.g., Bread, Pastries) | Select from the list |
| **Product** | Specific item name | Select from the filtered list |
| **Date** | Operating day | Select today's date or a historical date |
| **Time** | Current time | Select current time |
| **Cold-start mode** | New merchant simulation | Check if you have fewer than 30 days of history |

---

## What Each Output Means

| Output | What It Tells You |
|--------|-------------------|
| **Predicted surplus** | Estimated units that will not sell through normal channels today |
| **Recommended action** | The best next step: HOLD, MONITOR, DISCOUNT, DEEP DISCOUNT, DONATE, or DISCARD |
| **Discount tier** | The specific discount percentage (20–70%) to apply |
| **Safety status** | Whether the item is SAFE to list, CAUTION (list with warnings), or BLOCKED (do not list) |
| **Revenue recovery** | SGD amount you are estimated to recover from the recommended action |
| **Listing schedule** | When to list the item and the latest pickup time |
| **Holding time remaining** | How many hours of shelf life are left |

---

## How to Interpret Recommendations

### HOLD
**What it means:** No action needed yet.
**What to do:** Check back at 5pm or when the evening rush ends. If surplus builds, the recommendation will update.

### MONITOR
**What it means:** Watch the item for 1–2 hours before deciding.
**What to do:** Check the surplus again before committing to a discount. If surplus increases, apply a DISCOUNT.

### DISCOUNT
**What it means:** Apply a 20–40% discount and list now.
**What to do:** List the item at the recommended discount. Monitor acceptance. If not sold in 1 hour, increase to DEEP DISCOUNT.

### DEEP DISCOUNT
**What it means:** Apply a 50–70% discount immediately.
**What to do:** Urgent action needed — surplus is high or shelf life is short. List immediately.

### DONATE
**What it means:** The item is safe but there is no consumer demand. Redirect to a charity partner.
**What to do:** Contact your donation partner. The item is safe for consumption but has not sold through.

### DISCARD
**What it means:** The item has failed a safety check and cannot be listed.
**What to do:** Do not list this item. Dispose of it safely according to food waste procedures.

---

## Safety Status: What the Flags Mean

| Status | Meaning | What to Do |
|--------|---------|------------|
| **SAFE** | The item passed all 5 safety checks | Safe to list at the recommended discount |
| **CAUTION** | One or more safety checks raised a warning | Review the specific warnings. You may still list the item but should take precautions. |
| **BLOCKED** | One or more safety checks failed | Do not list this item. It has failed food safety requirements. |

### The 5 Safety Checks

1. **Shelf life remaining** — Is there enough time before the item spoils?
2. **Storage compatibility** — Is the storage type appropriate for this item?
3. **Preparation time** — Has the item been prepared correctly?
4. **Pickup window** — Is there enough time for a consumer to pick up before it spoils?
5. **Temperature hazard** — Are there any temperature-specific risks for this category?

**Important:** Safety checks are advisory. You are responsible for food safety compliance and handling decisions.

---

## What SurplusSense Cannot Do

- **Guarantee accuracy** — The prediction is an estimate based on historical patterns. Actual surplus will vary.
- **Replace your judgment** — You are always the decision-maker. The app recommends; you decide.
- **Override food safety** — If the safety check returns BLOCK, do not list the item regardless of commercial upside.
- **Predict consumer demand** — The model predicts your surplus, not consumer willingness to buy at a given price.
- **Integrate with your POS** — In Phase 1, data is entered manually. POS integration is planned for Phase 2.

---

## Cautions and Limitations

1. **The app uses demo/synthetic data** by default. Real merchant data pilot is required before commercial use.
2. **Predictions are estimates.** Do not make critical business decisions based solely on app output.
3. **Safety rules are advisory only.** They are based on general food safety principles and have not been validated by SFA or food safety experts.
4. **Cold-start predictions** (for new merchants) use category averages and are less accurate than merchant-specific predictions.
5. **Revenue recovery estimates** are model outputs applied to synthetic data. Actual recovery will vary.

---

## Where to Get Help

- **Repository:** https://github.com/TohzKai/surplusSense (private; Prof. Jack Hong invited for grading)
- **Individual Report:** `docs/INDIVIDUAL_REPORT.md` — full product and ML explanation
- **Developer Handover:** `docs/DEVELOPER_HANDOVER.md` — technical documentation
- **COC Decision Log:** `COC_DECISION_LOG.md` — prototype-to-product decision journey
- **Pilot Validation Plan:** `PILOT_VALIDATION_PLAN.md` — proposed 4-week merchant pilot design

---

*SurplusSense is a decision-support tool, not a substitute for merchant judgment or professional food safety advice. Always apply your own knowledge and judgment when making surplus decisions.*
