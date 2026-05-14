# Value Propositions and Unique Selling Points

> **Phase 2 / Historical note:** This document was part of early marketplace exploration. The final submitted MVP value proposition is merchant-side decision support as documented in `docs/EXECUTIVE_REPORT.md`. This file is retained as process evidence.

## Core Value Propositions

### For Merchants (Food Businesses)

**VP1: Turn waste into revenue**
"Every day, you throw away food that cost money to produce. We predict your surplus before it happens and connect you with customers who want to buy it — turning your waste line into a revenue line."

- Quantifiable: Average merchant recovers S$200-500/month in otherwise wasted inventory
- Measurable: Dashboard shows exact revenue recovery, waste reduction percentage, and trend

**VP2: Zero-effort surplus management**
"You don't need to manually create listings or figure out pricing. Our AI predicts what you'll have left over, suggests the right price, and handles the rest. One tap to approve."

- Quantifiable: < 5 minutes/day vs. 30+ minutes on manual platforms
- Differentiator: No competitor offers ML-predicted listing automation

**VP3: Actionable waste insights**
"We show you exactly where your waste comes from and what to do about it — not just 'you wasted X kg' but 'reduce your Tuesday pastry batch by 20% to save S$150/month.'"

- Quantifiable: Data-driven recommendations that reduce waste at source
- Differentiator: Prescriptive analytics, not descriptive dashboards

### For Consumers

**VP4: Premium food at fraction of the price**
"Get quality meals from restaurants, bakeries, and cafes you already love — at 50-70% off. Same food, same quality, just surplus timing."

- Quantifiable: Average savings of S$3-7 per meal
- Emotional: "Smart spending" not "cheap eating"

**VP5: Deals that find you**
"Stop scrolling through endless listings. We learn what you like, when you eat, and where you are — and surface the perfect deal at the right moment."

- Differentiator: ML-powered personalization vs. static listing feeds
- Experience: Feels like the app "knows" you

**VP6: Make a tangible impact**
"Every meal you rescue prevents X kg of CO2 emissions and saves perfectly good food from the incinerator. Track your personal impact over time."

- Emotional: Purpose-driven consumption
- Quantifiable: Personal sustainability dashboard (meals rescued, CO2 saved, money saved)

### For the Platform (Societal)

**VP7: Singapore's food waste intelligence layer**
"We don't just move surplus food — we build the data infrastructure that helps Singapore understand, predict, and ultimately prevent food waste at scale."

- Strategic: Platform data becomes valuable for policy, research, and industry
- Long-term: Data moat creates compounding value

---

## Unique Selling Points (USPs)

### USP 1: ML-Predicted Surplus Listing (Strongest)

**What**: AI predicts merchant surplus before it happens and auto-generates listings for one-tap approval.

**Why it's unique**: No competitor does predictive surplus listing. Existing platforms require merchants to manually identify and list surplus items — a process that takes time and relies on human judgment. Our model learns patterns from historical sales, weather, events, and day-of-week to predict surplus quantities with accuracy.

**Critical evaluation**:

- Strength: Genuine innovation — no direct competitor offers this
- Risk: Prediction accuracy must be high (>80%) or merchants lose trust
- Dependency: Requires sufficient historical data per merchant (cold start challenge)
- Mitigation: Start with rule-based suggestions, graduate to ML predictions as data accumulates

**Verdict**: Defensible USP if accuracy targets are met. Creates a data moat.

### USP 2: Dynamic Pricing Engine (Strong)

**What**: ML-driven pricing that adjusts in real-time based on demand signals, time remaining, inventory levels, and competitive positioning.

**Why it's unique**: Most competitors use fixed discount percentages (e.g., "70% off"). Dynamic pricing maximizes both sell-through rate (for merchants) and value perception (for consumers) by finding the optimal price point.

**Critical evaluation**:

- Strength: Increases sell-through rates significantly (estimated 15-25% improvement over fixed pricing)
- Risk: Consumers may feel "gamed" if prices fluctuate unpredictably
- Dependency: Requires demand data and real-time serving infrastructure
- Mitigation: Price floors set by merchants; transparent "price drops over time" model

**Verdict**: Strong USP but needs careful UX design to avoid consumer alienation. Transparency is key.

### USP 3: Prescriptive Waste Analytics (Moderate-Strong)

**What**: Analytics that don't just describe what happened but prescribe specific actions to reduce waste at source.

**Why it's unique**: Competitor dashboards show "you wasted X kg this month." Our analytics show "reduce your Wednesday chicken rice batch by 3 portions to save S$180/month while maintaining 98% order fulfillment."

**Critical evaluation**:

- Strength: High value for merchants — directly impacts their bottom line
- Risk: Recommendations must be actionable and accurate — vague advice erodes trust
- Dependency: Requires 4-8 weeks of transaction data per merchant to generate reliable patterns
- Mitigation: Start with category-level benchmarks, refine to merchant-specific recommendations

**Verdict**: Strong USP for merchant retention. The "reduce waste at source" angle is more valuable than "sell surplus."

### USP 4: Behavioral Personalization (Moderate)

**What**: Recommendation engine that learns consumer preferences implicitly from behavior, not explicit preference settings.

**Why it's unique**: Most food apps show all deals in a flat list sorted by distance or time. Our engine considers cuisine preference, price sensitivity, dietary restrictions, time-of-day patterns, and location context.

**Critical evaluation**:

- Strength: Standard ML capability applied to a new domain — well-understood, achievable
- Risk: Not truly unique — any competitor with ML expertise can replicate
- Dependency: Needs user interaction data (browsing, purchases, ratings)
- Mitigation: Focus on contextual signals (time, weather, events) that competitors don't use

**Verdict**: Table-stakes feature, not a moat. Must execute well but don't rely on it for differentiation.

### USP 5: Singapore-First Design (Moderate)

**What**: Built specifically for Singapore's unique F&B ecosystem — hawker centers, food courts, kopitiams, and the full spectrum of F&B establishments.

**Why it's unique**: Global competitors (Too Good To Go) designed for Western restaurant models. Singapore's hawker culture, high density, multi-ethnic cuisine, and unique dining patterns require local adaptation.

**Critical evaluation**:

- Strength: Local knowledge advantage over global competitors entering Singapore
- Risk: Local competitors (TreatSure) already have this advantage
- Dependency: Requires local market understanding and connections
- Mitigation: Leverage SMU network for F&B industry access and user testing

**Verdict**: Necessary but not sufficient. Must be combined with ML USPs for full differentiation.

---

## Value Proposition Canvas

### Merchant Pain Points → Solutions

| Pain Point                                   | Solution                                    | ML Component                    |
| -------------------------------------------- | ------------------------------------------- | ------------------------------- |
| Don't know how much surplus until end of day | Predict surplus in advance                  | Surplus prediction model        |
| Manual listing takes too much time           | Auto-generated listings from predictions    | Prediction + listing automation |
| Don't know what price to set                 | Dynamic pricing suggestion                  | Pricing optimization model      |
| Waste reports are generic                    | Specific, actionable recommendations        | Prescriptive analytics          |
| New customers from discounts don't return    | Conversion analytics and retention features | Recommendation engine           |
| Disposal costs S$200-500/month               | Revenue recovery from surplus sales         | Platform marketplace            |

### Consumer Pain Points → Solutions

| Pain Point                               | Solution                               | ML Component                   |
| ---------------------------------------- | -------------------------------------- | ------------------------------ |
| Good food is expensive in Singapore      | Premium food at 50-70% off             | Dynamic pricing                |
| Too many food apps, overwhelming choices | Curated, personalized deal feed        | Recommendation engine          |
| Don't know if surplus food is safe       | Quality verification and ratings       | Trust scoring model            |
| Deals sell out before I see them         | Predictive notifications at right time | Personalization + timing model |
| Want to be sustainable but inconvenient  | Frictionless rescue experience         | UX + location-based features   |
| Don't know what's available near me      | Location-aware deal discovery          | Geospatial recommendations     |

---

## Competitive Positioning Statement

**For** budget-conscious Singapore diners **who** want quality food at affordable prices, **our platform** is a food waste marketplace **that** uses AI to predict surplus, personalize recommendations, and optimize pricing — **unlike** Too Good To Go (no ML), TreatSure (limited merchant base), or OLIO (community-driven, not merchant-focused) — **because** our ML-powered approach delivers higher sell-through rates for merchants and better-matched deals for consumers, creating a self-improving marketplace that gets smarter with every transaction.

---

## Honest Assessment of Differentiation

### What genuinely differentiates (hard to replicate):

1. **ML-predicted surplus listings** — requires merchant data + ML expertise + prediction accuracy
2. **Prescriptive waste analytics** — requires domain knowledge + data + analytical depth
3. **Data moat from transactions** — compounding advantage that grows over time

### What's table-stakes (must have but easily copied):

1. Mobile app with deal listings
2. Payment processing
3. Basic ratings and reviews
4. Push notifications

### What's aspirational (valuable but hard to achieve initially):

1. POS integration for real-time inventory sync
2. Dynamic pricing with real-time serving
3. Corporate meal program partnerships
4. Government/regulatory data partnerships

### Recommended MVP Focus

For the SMU MBA ML project + startup exploration:

1. **Lead with**: Surplus prediction + dynamic pricing (demonstrates ML depth)
2. **Support with**: Personalized recommendations (shows ML breadth)
3. **Differentiate with**: Prescriptive analytics dashboard (merchant value)
4. **Defer**: POS integration, corporate programs, government partnerships
