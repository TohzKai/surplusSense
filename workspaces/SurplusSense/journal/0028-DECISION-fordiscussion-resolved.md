---
type: DECISION
date: 2026-04-26
created_at: 2026-04-26T00:00:00+08:00
author: human
session_id: grading-phase
project: Food App
topic: All 12 open For-Discussion questions resolved — scope, data, pricing, regulatory, ML depth
phase: analyze
tags:
  [
    scope,
    data-moat,
    synthetic-data,
    pricing,
    pdpa,
    insurance,
    ml-breadth,
    hawkers,
    resolution,
  ]
---

# For-Discussion Questions — Resolved Decisions

Resolves all 12 open "For Discussion" questions from journals 0001–0004. Each question is answered and the resolution is recorded here as the canonical decision.

---

## From 0001-DISCOVERY (Data Moat vs Incumbents)

**Q1: What if Grab/Deliveroo entered surplus food — how does the data moat hold?**

**Decision:** SurplusSense's defensibility is not "more data than incumbents." It is a focused structural position serving a use case Grab/Deliveroo are structurally uninterested in optimizing for. Their unit economics depend on full-price commissions and high GMV per order; surplus food sells at 50% discounts and lower margins, diluting their core metrics. Incumbents won't close this gap because the margin profile doesn't justify it for their existing business.

**Q2: Should MVP focus on merchant-side value before marketplace?**

**Decision:** Yes — the MVP focuses entirely on merchant-side value. Consumer listing is a preview, not a working marketplace. The chicken-and-egg problem is solved by delivering merchant value (predictions, recovery estimates, food safety) before depending on consumer demand. The merchant-first sequence also correctly sequences the data moat: merchants generate the transaction data that compounds it.

**Q3: Is the 10-week timeline realistic for 4 ML capabilities?**

**Decision:** No — original plan was over-scoped. Implementation cuts to two technique families: supervised (XGBoost surplus prediction) and unsupervised (k-means merchant clustering). Rule-based logic is used for recommendations and food safety since real merchant data for training doesn't yet exist. Depth on supervised side (5-seed validation, CV-vs-holdout analysis) demonstrates methodological rigor appropriate to the timeline.

---

## From 0002-GAP (Singapore Regulatory)

**Q4: Insurance requirement or self-certification for MVP?**

**Decision:** Merchant self-certification is sufficient for MVP. Real transactions aren't happening yet — synthetic data has zero liability exposure. Requiring insurance at this stage creates friction that blocks pilot validation. Insurance becomes table-stakes once real transactions begin. Transition documented in journal 0006. Dashboard food safety advisory disclaimer signals this boundary explicitly.

**Q5: PDPA at MVP or designed in from day one?**

**Decision:** Deferred to pilot phase. MVP uses synthetic data with zero PDPA exposure. Designing consent flows without knowing what data the platform actually collects risks getting it wrong twice. The pilot phase — when real data first enters — is when consent flows must be built. Documented in journal 0011.

**Q6: Hawker stalls in MVP or defer?**

**Decision:** Deferred to Phase 2. Hawker SFA licensing differs from restaurants/cafes; margins are thinner; a 50% discount that recovers SGD 19 for a bakery may be unviable for a hawker stall. Pilot should validate on a simpler, more uniform segment first (restaurants, cafes, bakeries). Single SFA pathway is easier to navigate at MVP than three. Deferral documented in journal 0002.

---

## From 0003-CONNECTION (ML Features → Retention)

**Q7: Free analytics tier with marketplace as paid tier?**

**Decision:** Yes. Free analytics tier solves the bootstrap cold-start problem; merchants get value before consumers exist. Transaction fees (15% of recovered revenue) monetize without taxing the analytics value. Platform incentive is aligned: more merchant recovery means more platform fee. This also sequences the data moat correctly — merchants generate data before consumers are needed.

**Q8: Does waste reduction at source conflict with marketplace revenue?**

**Decision:** Yes, in the long run — and that is the right tension. The product's mission is reducing food waste; declining marketplace volume as waste falls is a success metric, not a failure. In the medium term the conflict is muted because merchant acquisition dominates growth; waste reduction takes years to materially affect volume. By the time it does, the analytics tier should be a standalone revenue stream.

**Q9: Analytics-only as a standalone SMU project?**

**Decision:** Yes — analytics-only would be a defensible standalone scope. It would lose the network effect (no transaction flywheel), so the data moat compounds more slowly. For the SMU project specifically, the full marketplace adds a consumer-facing component that's mostly preview rather than functional; the merchant cockpit alone is the strongest product.

---

## From 0004-TRADE-OFF (Course Project vs Startup Scope)

**Q10: Deep on one ML system or breadth across four?**

**Decision:** Breadth-then-depth, constrained by the course rubric requirement that the team project use a different ML technique family. Two technique families with depth on the supervised side (XGBoost hyperparameter tuning, RandomizedSearchCV, 5-seed validation, CV-vs-holdout reasoning) demonstrates methodological rigor. Clustering for cold-start brings unsupervised in. Rule-based recommendations and food safety are appropriate given no real merchant training data.

**Q11: How to present synthetic data results honestly?**

**Decision:** Language distinguishes pipeline performance from real-world validation. Framing used throughout: "the model achieves 0.68 MAE on synthetic data" and "pipeline demonstrates 51% improvement over baseline." Avoids phrasing that implies direct transfer to real merchants. Synthetic caveat is in executive report, dashboard footer, and journal 0005. Dashboard shows "MVP Prototype" pill throughout.

**Q12: Would a real merchant recruited for the demo change priorities?**

**Decision:** Yes. With a real merchant, prediction matters less (they already know their patterns); recommendation engine sophistication matters more (when to list, what discount, how to balance recovery against waste reduction). Real-world validation would also surface food safety edge cases synthetic data doesn't capture. A real merchant demo would shift the story from abstract numbers to "bakery saved SGD X, reduced waste by Y%" — more concrete and more persuasive.

---

## Summary of Resolved Positions

| Question                       | Resolution                                                                  |
| ------------------------------ | --------------------------------------------------------------------------- |
| Data moat defensibility        | Structural position, not data volume; incumbents structurally disinterested |
| Merchant-side first            | Yes — chicken-and-egg solved; moat sequenced correctly                      |
| 10-week ML scope               | Two technique families; rule-based for cold-start features                  |
| Insurance at MVP               | Self-certification; insurance at pilot phase                                |
| PDPA timing                    | Deferred to pilot; consent flows depend on actual data collected            |
| Hawker stalls                  | Defer to Phase 2; simpler segment first                                     |
| Free analytics tier            | Yes — free tier + 15% transaction fee                                       |
| Waste reduction vs marketplace | Long-run tension; right tension; analytics tier as hedge                    |
| Analytics-only standalone      | Viable; loses network effect; merchant cockpit is strongest part            |
| ML depth vs breadth            | Breadth-then-depth; supervised with rigor; rubric-constrained               |
| Synthetic data framing         | Pipeline validation, not real-world claim; caveat throughout                |
| Real merchant for demo         | Would shift priority to recommendation engine; more persuasive              |

---

## Post-resolution Assessment

After closing all 12 questions, the project scope is now fully defined and internally consistent:

- **What the product is:** Merchant-facing AI decision cockpit (not a marketplace)
- **What it does:** Surplus prediction (XGBoost), discount recommendations (rule-based), food safety screening (rule-based), revenue recovery calculation
- **What it doesn't do:** Real transactions, consumer marketplace, PDPA-compliant data handling, hawker onboarding, insurance verification
- **What it honestly claims:** Pipeline performance on synthetic data; real-world accuracy unknown pending pilot
- **What Phase 2 must add:** Real merchant pilot, PDPA consent flows, insurance verification, hawker expansion, transaction infrastructure
