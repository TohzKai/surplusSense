# User Flows: Merchant Journey

## Merchant User Flow — Final Submitted MVP

The final submitted MVP covers one user flow:

**Merchant enters item details → sees a recommended action → acts on it.**

1. Merchant opens SurplusSense dashboard
2. Enters merchant context: type, category, storage, preparation time
3. Enters item details: original price, shelf life, current holding time
4. System outputs: predicted surplus units, recommended action, discount tier, food-safety status, recovery estimate
5. Merchant reviews and acts on the recommendation

**All other flows (M1 through M7 below) are Phase 2 — not part of the submitted MVP. They document earlier marketplace exploration and are retained as process evidence.**

---

## Final Merchant Decision Flow

## Primary User

Outlet manager or staff member at a bakery, café, or prepared-food outlet.

## Decision Moment

Late-day surplus decision, before products lose value or become unsafe.

## Flow

1. Merchant enters outlet and item context.
2. Merchant enters quantity, price, time of day, shelf-life, and relevant operating conditions.
3. SurplusSense predicts expected surplus units.
4. System applies food-safety gate.
5. System recommends one action:
   - hold
   - monitor
   - discount
   - deep discount
   - donate
   - discard
6. System estimates recovery value.
7. System explains recommendation in business language.
8. Merchant accepts or overrides recommendation.
9. Override reason is captured for pilot learning.

## Why This Is Decision Support

The merchant does not receive only a forecast. The merchant receives an action recommendation constrained by safety and linked to recovery value. This makes the product a decision-support cockpit rather than a generic ML dashboard.

---

## Phase 2 Merchant Marketplace Flow — Not Part of Final Submitted MVP

## M1: Merchant Onboarding

```
Landing page → Sign up (email/password or Google) → Business details form
→ SFA license verification → Set merchant profile (name, location, cuisine, hours)
→ Set default categories (what surplus they typically have)
→ Set pricing preferences (floor prices, discount range)
→ Dashboard tutorial (3-step walkthrough) → Active
```

**Details**:

- Sign up: Email + password, or Google OAuth
- Business details: Business name, address (Google Maps integration), cuisine type, operating hours, SFA license number
- SFA verification: Auto-check against SFA database (or manual verification within 24h)
- Profile setup: Logo upload, description, typical surplus categories, dietary tags (halal, vegetarian, etc.)
- Pricing preferences: Set minimum price per category, default discount percentage, maximum daily listing count
- Onboarding time target: < 15 minutes

**ML integration**: During onboarding, merchant selects from predefined categories. System immediately applies category-level surplus benchmarks as initial predictions.

---

## M2: Daily Surplus Listing (Phase 2 — Marketplace Flow)

```
Morning notification → "Predicted surplus for today" → Review prediction
→ Accept / Adjust quantities / Reject → Listing goes live
→ Monitor throughout day → Dynamic pricing adjusts → End-of-day summary
```

### Step-by-step:

**2a. Morning prediction notification** (8-10am, based on merchant operating hours)

- Push notification: "Good morning! Based on today's patterns, we predict you'll have ~12 portions of chicken rice and ~8 portions of nasi lemak unsold today."
- In-app: Prediction card showing each category with predicted quantity and suggested price

**2b. Merchant reviews prediction**

- Each category shows: Predicted surplus (units), Confidence level (high/medium/low), Suggested discount price, Original price for comparison
- Merchant actions per category:
  - **Accept** (one tap) — listing created with suggested parameters
  - **Adjust** — modify quantity or price, then accept
  - **Reject** — don't list this category today
  - **Snooze** — remind me later

**2c. Listing goes live**

- Items appear in consumer feed with countdown timer
- Dynamic pricing begins: price may decrease over time based on demand
- Merchant sees real-time: views, purchases, remaining quantity

**2d. Ongoing monitoring (optional)**

- Real-time dashboard: items sold, items remaining, current price, revenue earned
- Alert if demand is lower than expected: "Only 2 of 12 items sold with 2 hours remaining — consider accepting a price reduction?"

**2e. End-of-day summary**

- Push notification: "Today's results: 10/12 items sold, S$XX recovered, X% sell-through rate"
- In-app: Comparison of predicted vs. actual surplus, revenue earned, items that didn't sell

---

## M3: Manual Listing (Override Flow)

```
Dashboard → "Create Listing" → Select category → Set quantity and price
→ Set pickup window → Add photos (optional) → Publish
```

**Use cases**: Unexpected surplus (catering cancellation, unexpected slow day), items not in prediction, testing new categories.

---

## M4: Waste Analytics Dashboard

```
Dashboard → Analytics tab → Select time period
→ View waste breakdown → View trends → View recommendations
→ Act on recommendation (adjust production) → Track improvement
```

### Dashboard sections:

**4a. Overview**

- Total waste this period (kg), Revenue recovered through platform (S$), Waste reduction trend (% change)
- Comparison: "This month vs. last month", "You vs. similar merchants"

**4b. Waste breakdown by category**

- Bar chart: Each food category with waste quantity and percentage
- "Top 3 waste categories account for X% of your total waste"
- Drill-down: Click category to see daily breakdown

**4c. Temporal patterns**

- Heatmap: Waste by day of week and category
- "Your highest waste day is [day] — primarily [category]"
- Calendar view: Color-coded daily waste intensity

**4d. ML recommendations** (prescriptive)

- Cards with actionable recommendations:
  - "Reduce Tuesday pastry production by 20% — save ~S$180/month"
  - "Rainy days increase your surplus by 35% — consider smaller batches when rain is forecast"
  - "Your chicken rice sell-through rate is 92% — safe to maintain current batch size"
- Each recommendation shows: Confidence level, Estimated savings, Action required

**4e. Impact tracking**

- CO2 emissions prevented, Meals rescued, Cumulative revenue recovered
- Shareable impact card for social media / CSR reports
- Monthly sustainability report (downloadable PDF)

---

## M5: Pricing Management (Phase 2)

> **Not in submitted MVP.** Pricing management is Phase 2.

```
Dashboard → Pricing settings → Set defaults per category
→ Set floor prices → Enable/disable dynamic pricing
→ View pricing history → Adjust strategy
```

**Controls**:

- Category-level default discount (e.g., "Pastries: 50-70% off")
- Price floor per category (minimum acceptable price)
- Dynamic pricing toggle (on/off per category)
- Aggressive vs. conservative pricing mode
- Pricing history: Chart showing price curves and sell-through correlation

---

## M6: Order Management (Phase 2)

> **Not in submitted MVP.** Order management is Phase 2 — no consumer marketplace, payments, or QR pickup in the MVP.

```
Notification: "New order!" → View order details → Prepare order
→ Consumer arrives → Scan QR code → Order confirmed → Payment settled
```

**Order states**:

1. **Placed** → Consumer has paid, pickup window active
2. **Preparing** → Merchant acknowledges, preparing the order
3. **Ready** → Order is ready for pickup, consumer notified
4. **Collected** → Consumer scanned QR, order complete
5. **Expired** → Pickup window passed without collection (refund initiated)

---

## M7: Merchant Settings and Profile (Phase 2)

> **Not in submitted MVP.** Settings and profile management is Phase 2.

```
Dashboard → Settings → Edit business hours / location / categories
→ Manage notifications → View transaction history → Export reports
```

**Settings include**:

- Business hours (affects prediction timing and listing windows)
- Location and pickup instructions
- Category management (add/remove food categories)
- Notification preferences (prediction alerts, order alerts, daily summary)
- Transaction history and financial reports
- Account settings (password, email, etc.)
