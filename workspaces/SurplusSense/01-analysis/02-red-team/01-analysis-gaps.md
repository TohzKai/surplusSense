# Analysis Gap Report: Food Waste Reduction Marketplace

> **Phase 2 / Historical note:** This analysis was part of early marketplace exploration. The final submitted MVP is the merchant-side decision-support cockpit. This gap analysis is retained as process evidence.

**Audit date**: 2026-04-17
**Scope**: All files in `01-analysis/01-research/` (5 documents)
**Severity scale**: CRITICAL / MAJOR / SIGNIFICANT / MINOR

---

## Executive Summary

The analysis is thorough in breadth and reads well as a business document, but it has three structural weaknesses that will bite during implementation. First, the ML architecture is over-specified for a course project: four ML systems in 10 weeks is ambitious even for a dedicated engineering team, and the document does not honestly reconcile the 20-week roadmap with the 10-week plan in `02-plans/`. Second, several competitive and market claims lack cited sources and may be outdated or inaccurate, which risks credibility during presentation. Third, the unit economics are optimistic by roughly 2-4x on key metrics (average deal value, transactions per merchant, break-even merchant count), which will produce a business case that collapses under mild scrutiny from MBA faculty or investors.

**Complexity verdict**: Moderate-to-Complex. The concept is sound but the analysis papers over real execution risk with optimistic assumptions.

---

## File-by-File Analysis

### 01-competitive-landscape.md

#### GAP-C01 (MAJOR): Too Good To Go Singapore status is unverified

The document states Too Good To Go "Not yet launched (as of early 2025)." This is a central competitive claim -- if TGTG has since entered Singapore, the entire market analysis shifts. No source is cited. A single web search would verify this. If TGTG has entered or announced entry, this is a CRITICAL gap because the competitive strategy assumes their absence.

**Action required**: Verify TGTG's current Singapore status. If they have entered, re-rate the competitive risk from "Moderate" to "High probability, Very High impact."

#### GAP-C02 (MAJOR): TreatSure user and merchant counts are unverified

TreatSure is described as "Estimated 50K-100K users" and "100-200 partner establishments." These are presented as estimates with no methodology or source. If the real numbers are 10K users and 30 merchants, the competitive landscape is much more open. If the real numbers are 200K users and 500 merchants, the first-mover advantage claim is wrong. The document should disclose that these are guesswork.

**Action required**: Attempt to verify via App Store reviews, LinkedIn employee count, or direct contact. Document methodology for the estimate.

#### GAP-C03 (SIGNIFICANT): Missing competitor -- GrabFood/foodpanda "green" features

The document lists Grab as a competitive risk but does not investigate whether GrabFood or foodpanda have piloted surplus food or sustainability features in Singapore. Grab in particular has experimented with "GrabFood for Business" and sustainability initiatives. If either platform has even a pilot program for surplus food, the competitive risk assessment needs updating.

**Action required**: Check Grab and foodpanda press releases and app updates for any surplus food / anti-waste features in the past 12 months.

#### GAP-C04 (SIGNIFICANT): Missing competitor -- Meituan/Keeta expansion potential

Keeta (Meituan's international food delivery brand) entered Hong Kong in 2023 and is expanding in the region. While not yet in Singapore, a regional food delivery giant with ML expertise and a sustainability mandate entering the surplus food space is a more credible competitive threat than "new entrant with ML focus" (rated Low probability). The competitive risk section underweights the probability of well-funded regional players entering this niche.

#### GAP-C05 (MINOR): Comparative matrix is self-serving

Every cell in the "Our Platform" column is "Yes" or "Yes (planned)" while competitors have gaps. This is a marketing slide, not an honest comparison. The platform has not launched -- none of these features exist yet. A more honest matrix would distinguish "currently operational" from "designed" from "aspirational."

#### GAP-C06 (SIGNIFICANT): No competitive analysis of user acquisition costs

The document discusses competitive features but never addresses how competitors acquire users or what customer acquisition cost (CAC) looks like in Singapore's food app market. GrabFood reportedly spends S$8-15 per user acquired. If this platform needs to acquire both merchants and consumers with no brand recognition, the CAC will be substantial and is not modeled anywhere in the analysis.

---

### 02-singapore-food-waste-context.md

#### GAP-S01 (MAJOR): Food waste statistics lack primary source citation

The document states "755,000 tonnes (2023)" and provides a 5-year trend table, but never cites the NEA report or URL where these numbers come from. For an MBA project that will be graded on rigor, every statistic needs a traceable source. An MBA faculty member or investor will ask "where did you get these numbers?" and "NEA data" is not a sufficient answer.

**Action required**: Add specific citations to every statistic. Format: "Source: NEA Waste Statistics and Recycling Rates 2023, https://www.nea.gov.sg/..."

#### GAP-S02 (MAJOR): Breakdown by source is unreferenced

The breakdown table (Households 40%, F&B 17%, Retail 13%, Manufacturing 15%, Others 15%) is presented as fact with no source. NEA's published waste statistics typically do not break down food waste by source at this granularity. This may be from a specific NEA study or academic paper, but the reader cannot verify.

**Action required**: Cite the specific study or report. If this is estimated from multiple sources, say so and show the methodology.

#### GAP-S03 (SIGNIFICANT): "65% of Singapore consumers willing to purchase near-expiry food" claim is unsourced

This is a critical consumer adoption claim. The document attributes it to "NEA survey" but does not specify which survey, what year, or what the sample size was. If this statistic is inaccurate or from a small-sample survey, the entire consumer demand thesis is weakened.

**Action required**: Cite the specific NEA survey name, year, sample size, and methodology.

#### GAP-S04 (SIGNIFICANT): "F&B inflation running 5-7% annually (2023-2024)" may be inaccurate

Singapore's CPI for food excluding food services was around 3-4% in 2023-2024, not 5-7%. Restaurant food inflation may have been higher, but the claim needs a specific source. Inflating the inflation figure makes the value proposition look stronger than it may be.

**Action required**: Verify against SingStat CPI data and cite the specific index and time period.

#### GAP-S05 (SIGNIFICANT): Regulatory claims about "Mandatory Food Waste Reporting" need verification

The document states this became effective in 2021 and applies to "hotels with >200 rooms, malls with >10,000 sqm." The Resource Sustainability Act 2019 does mandate food waste reporting, but the effective dates and thresholds should be verified against the actual legislation, not stated from memory. Getting the regulatory details wrong in a Singapore-focused MBA project would be embarrassing.

**Action required**: Cite the specific sections of the Resource Sustainability Act and the NEA implementation timeline.

#### GAP-S06 (MAJOR): Use-by vs. best-before legal analysis is incomplete

The document correctly identifies this distinction but fails to mention a critical practical issue: many F&B merchants sell freshly prepared food that has NEITHER a use-by nor a best-before date. Prepared food (hawker dishes, restaurant meals, bakery items) falls under different SFA regulations regarding time-temperature control and shelf life. The legal analysis as written implies the use-by/best-before framework covers all food on the platform, which is false.

**Action required**: Research and document SFA regulations specifically for prepared/hot food sales, including requirements for time since preparation, temperature control, and labeling of freshly made items.

#### GAP-S07 (SIGNIFICANT): Hawker stall inclusion is under-analyzed

The document identifies hawker stalls as a unique opportunity (6,000 stalls) but glosses over the significant barriers: (1) most hawker stalls are one-person operations with no digital infrastructure, (2) many older hawkers are not comfortable with apps, (3) hawker food margins are already razor-thin so the surplus discount cannibalizes already-low prices, (4) hawker food is already cheap (S$3-6) so a 50% discount brings it to S$1.50-3, which may not justify the platform commission. The analysis says "challenge: digital adoption barriers" in one sentence and never revisits it.

**Action required**: Either commit to a realistic hawker onboarding strategy (with associated costs and timeline), or explicitly exclude hawkers from the MVP and treat them as a Phase 3+ expansion target. The current position of "we'll serve hawkers but acknowledge it's hard" is not actionable.

#### GAP-S08 (MINOR): "96% smartphone penetration" needs a year and source

This is a commonly cited Singapore statistic but it varies by source and year. Cite the specific IMDA or Statista report.

---

### 03-ml-architecture.md

#### GAP-M01 (CRITICAL): Timeline contradiction with implementation plan

The ML architecture document proposes a Phase 1 (4-6 weeks), Phase 2 (4-6 weeks), and Phase 3 (6-8 weeks) roadmap totaling 14-20 weeks. The implementation plan (`02-plans/01-implementation-plan.md`) allocates Weeks 4-7 (4 weeks) for ALL ML features. These two documents directly contradict each other. For a 10-week course project, the ML architecture as specified is not achievable.

**Action required**: Reconcile the timelines. Either (a) cut the ML scope to fit 4 weeks (rule-based pricing, content-based recommendations only, no ensemble), or (b) extend the project timeline. Option (a) is strongly recommended for an MBA course project.

#### GAP-M02 (CRITICAL): No synthetic data strategy despite being a course project

The ML architecture specifies data requirements of "14 days minimum," "4-8 weeks for good predictions," and "12+ weeks for strong predictions." A platform that has not launched has ZERO days of data. The implementation plan mentions "Generate realistic synthetic data based on research benchmarks" as a risk mitigation, but the ML architecture document never addresses how models will be trained and evaluated without real data.

For an MBA ML project, the data problem IS the project. How synthetic data will be generated, what distributions it will follow, how it will be validated against known Singapore F&B patterns -- all of this is missing.

**Action required**: Add a dedicated section on synthetic data generation: what distributions, what assumptions, how much data, how to validate that synthetic patterns are realistic. This is not a footnote; for a course project with no real users, it is the single most important design decision.

#### GAP-M03 (MAJOR): Surplus prediction model is specified in detail that exceeds available data

The surplus prediction section specifies XGBoost + Prophet ensemble with 6 feature categories and 20+ individual features. This model requires per-merchant, per-category, per-day historical data. With zero merchants at launch and synthetic data of unknown quality, this specification is academic -- it cannot be validated against real patterns. The cold start strategy (2 weeks of data for rules, 4-8 weeks for XGBoost) implies merchants have been onboarded and generating data for months before the model becomes useful.

**Action required**: Design the ML for what is actually achievable in the project timeline. For the course project, demonstrate the surplus prediction pipeline on synthetic data with a clear explanation of assumptions. Do not present the model as if it will achieve <25% MAPE on day one.

#### GAP-M04 (MAJOR): Dynamic pricing with reinforcement learning is not achievable

The document proposes a 3-phase pricing evolution: rule-based, multi-armed bandit, then reinforcement learning (DQN/PPO). Phase 3 requires "10K+ transactions" and continuous real-time serving. The platform will have zero real transactions for the course project. Proposing RL for pricing in a system with no real users is academic theater that will not survive faculty review.

**Action required**: Keep dynamic pricing at the rule-based phase for the course project. The rule-based time-decay model with merchant-configurable parameters is already a solid contribution. Show how the rules would be parameterized by ML if data were available, but do not claim RL will be implemented.

#### GAP-M05 (SIGNIFICANT): Recommendation system assumes interaction data that will not exist

The hybrid recommendation system (collaborative filtering + content-based + contextual bandit) requires user-item interaction data. The cold start section acknowledges this but proposes solutions (onboarding quiz, popularity-based defaults) that require real users. For a course demo, the recommender will be running on synthetic users with synthetic interactions.

**Action required**: Explicitly scope what the recommendation demo will show. Content-based filtering on synthetic item data is achievable. Collaborative filtering on synthetic interactions is achievable but needs the synthetic data strategy (see GAP-M02). Contextual bandits are not achievable without real-time user feedback.

#### GAP-M06 (SIGNIFICANT): Technology stack includes infrastructure not needed for a course project

The architecture specifies Redis (event queue, feature cache, session management), PostgreSQL (data warehouse, feature store), APScheduler (batch jobs), Docker deployment, and a model registry. This is production infrastructure for a system that will be demoed to faculty. The engineering overhead of setting up and maintaining this infrastructure is substantial and adds nothing to the ML demonstration.

**Action required**: For the course project, use a simpler stack: SQLite or PostgreSQL for persistence, in-memory caching, file-based model storage, and a single FastAPI server. The infrastructure complexity can be described as "production architecture" in documentation without actually building it.

#### GAP-M07 (MINOR): Evaluation metric targets are aspirational, not calibrated

"< 2 units per category" MAE, "> 85% directional accuracy", "> 20% Precision@5" -- these targets are stated without any baseline comparison. What does a naive baseline (e.g., "predict yesterday's surplus") achieve? Without baseline comparisons, the targets are meaningless. An MBA faculty member will ask "compared to what?"

**Action required**: Establish naive baselines (e.g., predict mean, predict yesterday, predict last-week-same-day) and compare model performance against them. The value is in the improvement over naive, not in absolute numbers.

#### GAP-M08 (SIGNIFICANT): Monitoring and retraining pipeline is over-engineered

The document specifies data drift monitoring (KS test), prediction accuracy monitoring, model performance monitoring, and automated retraining triggers. This is MLOps infrastructure for a production system. For a course project with synthetic data that does not drift, this is pure overhead.

**Action required**: Remove or clearly mark as "future work." The course project needs model training scripts, evaluation notebooks, and a serving API. It does not need drift monitoring.

---

### 04-platform-model-analysis.md

#### GAP-P01 (MAJOR): Unit economics are optimistic by 2-4x

The unit economics table claims:

- Average deal value: S$5-8
- Transactions per merchant/week: 10-30
- Active merchants needed for break-even: 200-500
- Consumer acquisition cost: S$3-5

Let's stress-test these:

**Average deal value S$5-8**: This implies the original price is S$10-16 and the discount is 50%. But the competitive landscape document says hawker meals cost S$3-6. A bakery surprise bag at S$5 is reasonable, but many deals will be smaller (S$2-4 for individual items). A weighted average across item types is more likely S$3-5.

**10-30 transactions per merchant/week**: TreatSure, the only comparable Singapore platform with 100-200 merchants, has likely not achieved this per-merchant frequency. New merchants on a new platform with a small consumer base will see far fewer transactions -- 2-5 per week in the early months is more realistic.

**200-500 merchants for break-even**: At a more realistic S$3 deal value and 5 transactions/week/merchant, the revenue per merchant per week is S$3 x 0.15 commission x 5 = S$2.25. For 200 merchants, that is S$450/week or about S$1,950/month. This does not cover even basic operating costs (servers, payment processing, customer support, marketing).

**Consumer acquisition cost S$3-5**: For a food app in Singapore competing with GrabFood and foodpanda for attention, S$3-5 is extremely optimistic. Expect S$8-15 based on food delivery app benchmarks.

**Action required**: Provide a pessimistic scenario alongside the optimistic one. Show break-even under both sets of assumptions. An MBA project that only shows optimistic numbers will not be credible.

#### GAP-P02 (SIGNIFICANT): "Data moat" is claimed but not defended

The document states "the more transactions flow through the platform, the better predictions become, creating a compounding advantage." This is a standard platform economy claim, but it assumes: (1) enough data volume to improve models, (2) model improvement is actually noticeable to users, (3) competitors cannot achieve similar accuracy with less data. None of these assumptions are examined.

In reality, a Singapore food surplus platform with 50-200 merchants will have sparse data. Surplus prediction for a bakery with 15 daily items is not a big data problem -- it is a small data problem where domain heuristics may outperform ML for months.

**Action required**: Either drop the "data moat" language or provide a realistic assessment of how many transactions per merchant per week are needed before ML demonstrably outperforms simple rules.

#### GAP-P03 (SIGNIFICANT): Transaction types include "pre-order" without addressing feasibility

The platform model lists "Pre-order: Consumer commits to buying predicted surplus before it occurs." This is a compelling concept but has a fundamental chicken-and-egg problem: the surplus prediction must be accurate enough that the merchant actually has the item, AND the consumer must trust they will get what they ordered. If the prediction is wrong and the merchant does not have the item, the consumer is frustrated. If the prediction is wrong and the merchant has too much, the surplus is not reduced. Pre-order requires the prediction model to already be working well, which requires data, which requires the platform to be running.

**Action required**: Either remove pre-order from the MVP or clearly mark it as a Phase 3+ feature that depends on prediction accuracy reaching a defined threshold.

#### GAP-P04 (MINOR): Platform model describes features that are not in the ML architecture

The AAA framework describes "Fraud detection," "Quality scoring," "Market gap detection," "Group buying," and "Community requests." None of these appear in the ML architecture document. If these are planned features, they need ML specifications. If they are aspirational, they should be marked as future work.

---

### 05-value-propositions-and-usps.md

#### GAP-V01 (MAJOR): "No competitor offers ML-predicted listing automation" is unverified and potentially misleading

The document states this as a fact multiple times. While no direct competitor may advertise ML surplus prediction, Phenix (France) has B2B analytics with "advanced analytics for enterprise clients." It is plausible that Phenix or other enterprise-focused platforms have internal ML tools for surplus prediction that are not consumer-facing. Claiming uniqueness without verifying what enterprise competitors offer internally is risky.

More importantly, for an MBA project, claiming "no competitor does this" without rigorous verification will invite skeptical questioning from faculty.

**Action required**: Refine the claim to "No consumer-facing food surplus marketplace publicly offers ML-predicted surplus listings." The qualifier matters.

#### GAP-V02 (SIGNIFICANT): USP strength ratings lack criteria

USPs are rated "Strongest," "Strong," "Moderate-Strong," and "Moderate" without defining what these ratings mean. Is "Strongest" about defensibility, market impact, or implementation feasibility? The rating system is subjective and therefore unpersuasive.

**Action required**: Define rating criteria (e.g., defensibility, implementation feasibility, user-perceived value, market timing) and rate each USP on each dimension. A 2x2 matrix (defensibility vs. feasibility) would be more useful than ordinal labels.

#### GAP-V03 (SIGNIFICANT): "S$200-500/month revenue recovery" claim is unsubstantiated

VP1 states "Average merchant recovers S$200-500/month in otherwise wasted inventory." No source, no methodology, no calculation. If the average deal value is S$5 and a merchant does 10-30 transactions/week, monthly revenue is S$200-600, of which the merchant keeps 85% = S$170-510. But these transaction numbers are the optimistic scenario (see GAP-P01). Under pessimistic assumptions (S$3 deal, 5 transactions/week), recovery is S$3 x 5 x 4 x 0.85 = S$51/month. The S$200-500 claim is a best case, not an average.

**Action required**: Show the calculation. Provide a range (pessimistic, moderate, optimistic) rather than a single aspirational number.

#### GAP-V04 (SIGNIFICANT): "S$3-7 savings per meal" claim is inconsistent with hawker pricing

VP4 states consumers save "S$3-7 per meal." If the discounted price is S$2.50-5 (implied by 50-70% off original S$5-8), the savings is S$2.50-5.67, which is approximately S$3-6. But if the original meal is hawker food at S$4-6, a 50% discount means the consumer pays S$2-3, saving S$2-3. The S$3-7 range is achievable only for restaurant/cafe meals, not hawker food, but the competitive analysis says hawker centers are a key market segment.

**Action required**: Segment savings by establishment type. Do not present a single range that blurs hawker and restaurant economics.

#### GAP-V05 (MINOR): The "Honest Assessment" section is not fully honest

The "Aspirational" list includes "POS integration," "Dynamic pricing with real-time serving," "Corporate meal program partnerships," and "Government/regulatory data partnerships." But the ML architecture document (03) already specifies real-time dynamic pricing as Phase 2 and POS integration as a core feature. Either these are aspirational (not designed) or they are designed (not aspirational). The contradiction between the USP document calling them aspirational and the architecture document specifying them needs resolution.

---

## Cross-File Contradictions

#### GAP-X01 (CRITICAL): ML timeline mismatch (files 03 vs. 02-plans)

Already detailed in GAP-M01. The ML architecture proposes 14-20 weeks of ML work. The implementation plan allocates 4 weeks. This is the most consequential contradiction in the analysis.

#### GAP-X02 (SIGNIFICANT): Hawker positioning is inconsistent across files

- File 01 (competitive): "Hawker center surplus is untapped" -- suggests hawkers are a priority
- File 02 (context): Identifies hawker barriers in one sentence, never resolves
- File 03 (ML): Surplus prediction features include "halal/vegetarian" tags but not hawker-specific patterns
- File 04 (platform): Lists hawker stalls as producers with "5-10% surplus" and "S$200-500 disposal cost" -- but most hawkers do not pay separate disposal fees
- File 05 (USPs): USP 5 claims "Singapore-First Design" includes hawker centers

The platform is simultaneously claiming hawkers as a key differentiator AND acknowledging they are hard to serve AND never producing a concrete plan for hawkers.

**Action required**: Make an explicit decision: hawkers in MVP, or hawkers in Phase 3? If in MVP, produce a realistic onboarding plan. If in Phase 3, remove hawker claims from USPs and competitive positioning.

#### GAP-X03 (SIGNIFICANT): Payment method differs between files

- File 02 (context): Lists PayNow (72%), credit cards (65%), GrabPay (45%), Apple/Google Pay (30%)
- File 04 (platform): Lists "Payment gateway" and "QR code scan" but does not specify which payment methods
- Implementation plan: Specifies Stripe

Stripe in Singapore supports cards and Apple/Google Pay but does NOT natively support PayNow. PayNow is used by 72% of Singapore consumers. This is a significant gap -- a food app in Singapore that does not support PayNow will lose a large portion of potential consumers.

**Action required**: Research Stripe's PayNow integration capability (it may be available via Stripe Singapore) or identify an alternative payment gateway that supports PayNow, GrabPay, and credit cards. Document the decision.

#### GAP-X04 (MINOR): Consumer willingness to buy near-expiry food percentages differ between contexts

File 02 states "65% of Singapore consumers willing to purchase near-expiry food at 30-50% discount." This is used to justify demand. But the value proposition (File 05) positions the platform as offering "premium food at fraction of the price" and "smart spending not cheap eating." These are different value propositions aimed at different consumer segments. The 65% figure is about near-expiry food acceptance, not about "premium food at a discount." The analysis conflates price-sensitive consumers who will buy near-expiry food with brand-conscious consumers who want premium food cheaply.

---

## Structural Gaps Across All Files

#### GAP-G01 (CRITICAL): No honest acknowledgment of the cold start problem's severity

All five files acknowledge cold start challenges in passing, but none confront the reality: a two-sided marketplace with ML features requires BOTH sides to be active before EITHER side gets value. This is the classic marketplace chicken-and-egg problem, compounded by the fact that ML features (prediction, recommendations, dynamic pricing) need data from both sides.

The analysis should model the cold start phase explicitly:

- Month 1-2: How many merchants and consumers are needed for the ML models to begin producing useful output?
- Month 3-6: What does the user experience look like when recommendations are poor because data is sparse?
- What is the plan for the gap between "marketplace works" and "ML adds value"?

#### GAP-G02 (MAJOR): No analysis of the cost to acquire and onboard merchants

The analysis discusses merchant value propositions extensively but never addresses how merchants will be acquired, how long onboarding takes, what it costs, and what the churn rate is likely to be. Singapore F&B merchants are notoriously difficult to onboard onto new platforms -- many are already overwhelmed by GrabFood, foodpanda, Burpple, Chope, and other platforms demanding their attention.

For the course project, merchant onboarding is the difference between a demo with synthetic data and a demo with real merchants. The analysis should address whether the plan is to recruit real merchants or simulate the entire experience.

**Action required**: Add a section on merchant acquisition strategy: target merchant segments, outreach channels, onboarding process, expected conversion rate, and whether real merchants are part of the course project scope.

#### GAP-G03 (MAJOR): No failure mode analysis

No document addresses what happens when things go wrong:

- What if a consumer gets food poisoning from surplus food purchased on the platform? Who is liable?
- What if a merchant consistently over-predicts surplus and the platform shows deals that do not exist?
- What if a merchant lists food that is past its use-by date (not just best-before)?
- What if a consumer claims the food quality was poor and demands a refund?
- What if the dynamic pricing algorithm prices food too low and merchants lose money?

These are not hypothetical -- they are the operational reality of a food marketplace. The legal analysis (File 02) addresses regulatory compliance but not liability allocation.

**Action required**: Add a risk/failure mode analysis with liability allocation, dispute resolution process, and insurance considerations. Even for a course project, this shows MBA-level business thinking.

#### GAP-G04 (SIGNIFICANT): No analysis of food safety operational requirements

The platform involves perishable food. The analysis never addresses:

- How food quality will be verified at listing time
- Who is responsible if food is improperly stored between listing and pickup
- What happens if a consumer cannot pick up within the pickup window and the food spoils
- Whether the platform needs food handling certifications or insurance
- Temperature control requirements for different food categories

These operational requirements affect both the legal liability and the user experience design.

#### GAP-G05 (SIGNIFICANT): No assessment of alternative approaches for the MBA project

The analysis jumps straight to a full two-sided marketplace with four ML systems. For an MBA ML individual project, alternative approaches should be evaluated:

- **Option A**: Full marketplace with ML (current proposal) -- highest effort, highest risk
- **Option B**: ML-focused prototype demonstrating prediction/recommendation on synthetic data, with marketplace UX mocked -- lower risk, still demonstrates ML
- **Option C**: Partner with one real merchant to build a single-merchant case study -- demonstrates real data but limits scope
- **Option D**: Focus on one ML system (e.g., surplus prediction only) with a simple marketplace wrapper -- deepest ML demonstration, narrowest scope

The analysis should explicitly choose one approach and justify why it is optimal for the dual objectives (MBA ML course + startup exploration).

#### GAP-G06 (MINOR): No competitor app review methodology

The competitive analysis reviews features from publicly available information and reviews but does not describe a systematic methodology. Did the analyst download and use each competitor's app? For how long? In which market? First-hand experience with Too Good To Go, TreatSure, and OLIO would significantly strengthen the competitive analysis.

---

## Summary of Findings

| ID      | Severity    | File(s)       | Issue                                                       |
| ------- | ----------- | ------------- | ----------------------------------------------------------- |
| GAP-M01 | CRITICAL    | 03, 02-plans  | ML timeline contradicts implementation plan (20 weeks vs 4) |
| GAP-M02 | CRITICAL    | 03            | No synthetic data strategy for a platform with zero users   |
| GAP-G01 | CRITICAL    | All           | Cold start severity not honestly confronted                 |
| GAP-C01 | MAJOR       | 01            | TGTG Singapore status unverified                            |
| GAP-C02 | MAJOR       | 01            | TreatSure estimates unverified                              |
| GAP-M03 | MAJOR       | 03            | Surplus prediction spec exceeds achievable data             |
| GAP-M04 | MAJOR       | 03            | RL pricing not achievable in course project                 |
| GAP-P01 | MAJOR       | 04            | Unit economics optimistic by 2-4x                           |
| GAP-V01 | MAJOR       | 05            | "No competitor" claim unverified                            |
| GAP-G02 | MAJOR       | All           | Merchant acquisition strategy missing                       |
| GAP-G03 | MAJOR       | All           | No failure mode / liability analysis                        |
| GAP-S01 | MAJOR       | 02            | Food waste statistics lack primary source citations         |
| GAP-S02 | MAJOR       | 02            | Breakdown by source unreferenced                            |
| GAP-S06 | MAJOR       | 02            | Use-by/best-before analysis incomplete for prepared food    |
| GAP-X02 | SIGNIFICANT | 01-05         | Hawker positioning inconsistent                             |
| GAP-X03 | SIGNIFICANT | 02, 04, plans | PayNow not addressed despite 72% consumer usage             |
| GAP-C03 | SIGNIFICANT | 01            | Grab/foodpanda sustainability features not investigated     |
| GAP-C04 | SIGNIFICANT | 01            | Keeta/Meituan regional expansion risk undervalued           |
| GAP-C06 | SIGNIFICANT | 01            | No competitive CAC analysis                                 |
| GAP-S03 | SIGNIFICANT | 02            | "65% willing to buy near-expiry" claim unsourced            |
| GAP-S04 | SIGNIFICANT | 02            | F&B inflation rate may be overstated                        |
| GAP-S05 | SIGNIFICANT | 02            | Regulatory effective dates need primary source              |
| GAP-S07 | SIGNIFICANT | 02            | Hawker inclusion under-analyzed                             |
| GAP-M05 | SIGNIFICANT | 03            | Recommendation system needs data that will not exist        |
| GAP-M06 | SIGNIFICANT | 03            | Infrastructure over-specified for course project            |
| GAP-M08 | SIGNIFICANT | 03            | Monitoring/retraining pipeline over-engineered              |
| GAP-P02 | SIGNIFICANT | 04            | Data moat claimed but not defended                          |
| GAP-P03 | SIGNIFICANT | 04            | Pre-order feature has chicken-and-egg dependency            |
| GAP-P04 | MINOR       | 04            | Platform model describes features not in ML architecture    |
| GAP-V02 | SIGNIFICANT | 05            | USP strength ratings lack defined criteria                  |
| GAP-V03 | SIGNIFICANT | 05            | Revenue recovery claim unsubstantiated                      |
| GAP-V04 | SIGNIFICANT | 05            | Savings claim inconsistent with hawker pricing              |
| GAP-V05 | MINOR       | 03, 05        | Features called "aspirational" in USPs but "designed" in ML |
| GAP-X04 | MINOR       | 02, 05        | Consumer segment conflation                                 |
| GAP-G04 | SIGNIFICANT | All           | Food safety operational requirements not addressed          |
| GAP-G05 | SIGNIFICANT | All           | No evaluation of alternative project approaches             |
| GAP-M07 | MINOR       | 03            | Evaluation targets lack naive baselines                     |
| GAP-S08 | MINOR       | 02            | Smartphone penetration stat needs source                    |
| GAP-C05 | MINOR       | 01            | Comparative matrix is self-serving                          |
| GAP-G06 | MINOR       | 01            | No competitor app review methodology                        |

**Total findings**: 39

- CRITICAL: 3
- MAJOR: 10
- SIGNIFICANT: 18
- MINOR: 8

---

## Recommended Priority Actions (in order)

1. **Resolve the timeline contradiction** (GAP-M01). Decide whether this is a 10-week course project with limited ML, or a 20-week startup prototype. The rest of the analysis depends on this decision.

2. **Write the synthetic data strategy** (GAP-M02). For a course project with no real users, this is the most important design document. It determines whether the ML demo is credible.

3. **Verify all factual claims with sources** (GAP-C01, GAP-C02, GAP-S01 through GAP-S08). An MBA project without citations is an opinion piece, not an analysis.

4. **Re-run unit economics with pessimistic assumptions** (GAP-P01). Show the break-even under best case, moderate, and pessimistic scenarios.

5. **Make the hawker decision** (GAP-X02). Include or exclude hawkers from the MVP. The current ambiguity weakens every document.

6. **Add failure mode and liability analysis** (GAP-G03). This demonstrates MBA-level business thinking and fills a genuine gap.

7. **Right-size the ML architecture for the actual timeline** (GAP-M03 through GAP-M08). Cut RL, cut monitoring, cut infrastructure complexity. Focus on one or two ML systems done well.
