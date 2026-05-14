# Competitive Landscape Analysis

## Executive Summary

The food waste reduction app market is growing globally but remains fragmented in Southeast Asia. Singapore has one direct competitor (TreatSure) with limited market penetration. No existing platform combines marketplace functionality with ML-driven surplus prediction, dynamic pricing, and prescriptive waste analytics — creating a clear differentiation opportunity.

---

## 1. Direct Competitors

### Too Good To Go (Global Leader)

| Attribute              | Details                                       |
| ---------------------- | --------------------------------------------- |
| **Founded**            | 2016, Denmark                                 |
| **Markets**            | 17 countries (Europe, US)                     |
| **Users**              | 75M+ registered users                         |
| **Merchants**          | 130K+ partner stores                          |
| **Meals saved**        | 300M+ (cumulative)                            |
| **Business model**     | Commission per transaction (varies by market) |
| **Funding**            | €150M+ total funding                          |
| **Singapore presence** | Not yet launched (as of early 2025)           |

**Core features**:

- "Surprise Bag" model — consumers buy a mystery bag at ~1/3 of retail price
- Simple merchant interface — set daily quantity and price
- Gamified consumer experience (impact tracking, badges)
- Strong brand identity around food waste reduction

**Strengths**:

- Massive global scale and brand recognition
- Proven business model with high merchant retention
- Low-friction "surprise bag" format appeals to consumers
- Deep consumer engagement through gamification
- Strong sustainability narrative

**Weaknesses**:

- No ML/AI capabilities — merchants manually set quantities and pricing
- Surprise bag model creates consumer uncertainty (don't know exactly what they'll get)
- No personalized recommendations — flat listing feed
- Fixed pricing model — no dynamic adjustment based on demand
- No waste analytics for merchants — pure marketplace, no insights
- Western-centric design — may not suit Singapore's hawker culture
- No POS integration for automated surplus detection

**User pain points (from reviews)**:

- "You never know what you'll get — sometimes great, sometimes disappointing"
- "Limited availability in my area"
- "Merchants run out of bags quickly — need to check constantly"
- "No way to filter by dietary restrictions or preferences"
- "App doesn't learn what I like"

### OLIO (UK-based, Community-Driven)

| Attribute              | Details                                                    |
| ---------------------- | ---------------------------------------------------------- |
| **Founded**            | 2015, UK                                                   |
| **Markets**            | 100+ countries (community-driven)                          |
| **Users**              | 7M+ registered users                                       |
| **Business model**     | Freemium + "Food Waste Heroes" program + B2B               |
| **Funding**            | £50M+ total funding                                        |
| **Singapore presence** | Limited community activity, no structured merchant program |

**Core features**:

- Peer-to-peer food sharing (household to household)
- "Food Waste Heroes" — volunteers collect surplus from local businesses
- Listings for both food and non-food items
- Community-oriented design with local groups

**Strengths**:

- Strong community engagement model
- Peer-to-peer sharing extends beyond merchant surplus
- Free for basic use — low barrier to entry
- Active in 100+ countries through community volunteers

**Weaknesses**:

- Not merchant-focused — relies on volunteers to collect and redistribute
- Quality control challenges with peer-to-peer sharing
- No ML capabilities — purely community-driven
- No pricing optimization — items are given away free
- Scale limited by volunteer network density
- Not optimized for commercial F&B surplus

### TreatSure (Singapore-Based)

| Attribute          | Details                        |
| ------------------ | ------------------------------ |
| **Founded**        | 2017, Singapore                |
| **Markets**        | Singapore only                 |
| **Users**          | Estimated 50K-100K             |
| **Merchants**      | 100-200 partner establishments |
| **Business model** | Commission per transaction     |
| **Funding**        | Seed stage (undisclosed)       |

**Core features**:

- Buffet surplus and restaurant surplus deals
- Timed deals (end-of-meal-period discounts)
- Mobile-first consumer app
- Basic merchant dashboard

**Strengths**:

- Local Singapore market knowledge and merchant relationships
- First-mover advantage in Singapore
- Focus on buffet surplus (a uniquely Singapore opportunity — hotel buffets)
- Understanding of local F&B regulations

**Weaknesses**:

- Small merchant base — limited deal variety
- No ML capabilities — manual listing and pricing
- Limited consumer engagement features
- Basic app functionality — no personalization
- Small team — slow feature development
- No waste analytics for merchants
- Primarily buffet-focused — limited to a subset of F&B

**User pain points**:

- "Not enough deals available near me"
- "Same restaurants all the time"
- "App feels basic compared to GrabFood/foodpanda"
- "No way to set preferences or get recommendations"

### Karma (Sweden)

| Attribute          | Details                    |
| ------------------ | -------------------------- |
| **Founded**        | 2016, Sweden               |
| **Markets**        | Sweden, UK, France         |
| **Users**          | 2M+                        |
| **Merchants**      | 15K+                       |
| **Business model** | Commission per transaction |
| **Funding**        | €35M+                      |

**Core features**:

- Real-time surplus listings from restaurants, cafes, grocery stores
- Map-based deal discovery
- Direct purchase and pickup
- Merchant dashboard with basic analytics

**Strengths**:

- Clean, intuitive UI
- Broad merchant categories (not just restaurants)
- Real-time availability updates
- Good merchant onboarding process

**Weaknesses**:

- No ML capabilities
- Limited geographic presence
- No dynamic pricing
- Basic analytics for merchants
- Not in Asian markets

### Phenix (France)

| Attribute          | Details                         |
| ------------------ | ------------------------------- |
| **Founded**        | 2014, France                    |
| **Markets**        | France, Belgium, Spain          |
| **Users**          | 5M+                             |
| **Business model** | B2B SaaS + consumer marketplace |
| **Funding**        | €85M+                           |

**Core features**:

- Consumer marketplace for discounted surplus food
- B2B platform for grocery anti-waste management
- Corporate catering surplus redistribution
- Strong analytics for enterprise clients

**Strengths**:

- B2B SaaS model provides stable revenue
- Strong grocery/supermarket partnerships
- Advanced analytics for enterprise clients
- Multi-channel approach (B2C + B2B)

**Weaknesses**:

- Enterprise focus may not suit small F&B merchants
- No consumer-facing ML features
- Limited international expansion
- Not in Asian markets

### Other Regional Players

| Platform         | Market    | Notes                                                                            |
| ---------------- | --------- | -------------------------------------------------------------------------------- |
| **Makan Rescue** | Singapore | Small-scale, volunteer-driven surplus redistribution. Not a commercial platform. |
| **Yindii**       | Thailand  | Surplus food marketplace in Bangkok. Similar concept, no ML.                     |
| **Ukara**        | Indonesia | Emerging food surplus platform. Early stage.                                     |
| **Fooco**        | Malaysia  | Food waste reduction concept. Pre-launch.                                        |

---

## 2. Comparative Matrix

| Feature                      | Too Good To Go | OLIO    | TreatSure | Karma | Phenix    | **Our Platform**       |
| ---------------------------- | -------------- | ------- | --------- | ----- | --------- | ---------------------- |
| Surplus marketplace          | Yes            | Partial | Yes       | Yes   | Yes       | **Yes**                |
| Surprise bag model           | Yes            | No      | No        | No    | Partial   | **Yes (optional)**     |
| ML surplus prediction        | No             | No      | No        | No    | No        | **Yes**                |
| Dynamic pricing              | No             | No      | No        | No    | No        | **Yes**                |
| Personalized recommendations | No             | No      | No        | No    | No        | **Yes**                |
| Waste analytics (merchant)   | Basic          | No      | No        | Basic | Yes (B2B) | **Yes (prescriptive)** |
| POS integration              | No             | No      | No        | No    | Partial   | **Planned**            |
| Pre-order/prediction         | No             | No      | No        | No    | No        | **Yes**                |
| Singapore market             | Not yet        | Limited | Yes       | No    | No        | **Yes**                |
| Mobile app                   | Yes            | Yes     | Yes       | Yes   | Yes       | **Yes**                |
| Impact tracking              | Yes            | Yes     | No        | No    | No        | **Yes**                |
| Social/community features    | Basic          | Strong  | No        | No    | No        | **Planned**            |

---

## 3. Singapore Market Analysis

### Current State of Food Waste Apps in Singapore

Singapore's food waste app market is **nascent**:

- **TreatSure** is the only dedicated commercial platform — estimated 100-200 merchants, 50K-100K users
- **OLIO** has community presence but no structured merchant program
- **Too Good To Go** has not entered Singapore (focused on Western markets)
- **GrabFood/foodpanda** dominate food delivery but have no surplus/waste features
- **No platform offers ML-driven features** in Singapore or globally

### Market Gaps in Singapore

1. **No ML-powered surplus platform exists** — global gap, not just Singapore
2. **Hawker center surplus is untapped** — no platform addresses this uniquely Singapore segment
3. **Grocery/supermarket near-expiry** is largely offline — "markdown corners" exist in-store but not on apps
4. **No prescriptive analytics** for small F&B merchants — only large chains have waste data insights
5. **Consumer awareness of surplus food apps is low** — TreatSure has not achieved mainstream awareness

### Consumer Behavior Specifics

- Singapore consumers are **value-conscious** (especially post-COVID cost-of-living pressures)
- High density means short distances between merchants and consumers — ideal for pickup model
- Strong food culture means consumers care about food quality — trust signals are critical
- Multi-ethnic cuisine diversity creates opportunity for personalized recommendations
- Hawker culture provides baseline price expectation (~S$3-6 per meal) — surplus deals must compete

---

## 4. Differentiation Opportunities

### Where ML Creates Competitive Advantage

| ML Capability                | Competitor Gap                         | Our Advantage                                   | Impact                                 |
| ---------------------------- | -------------------------------------- | ----------------------------------------------- | -------------------------------------- |
| Surplus prediction           | All competitors require manual listing | Auto-predicted listings, one-tap approval       | Reduces merchant friction to near-zero |
| Dynamic pricing              | All use fixed pricing                  | Time/demand-based pricing optimization          | Increases sell-through by 15-25%       |
| Personalized recommendations | All show flat listing feeds            | ML-ranked, context-aware deal feed              | Increases conversion and engagement    |
| Prescriptive analytics       | None offer actionable recommendations  | "Reduce batch size by X%" not "You wasted Y kg" | Reduces waste at source (higher value) |

### What Cannot Be Replicated Quickly

1. **Data moat**: Transaction + surplus prediction data compounds over time. Each prediction improves the model. New entrants start from zero.
2. **Prediction accuracy**: Surplus prediction accuracy improves with merchant-specific data. Switching cost for merchants = losing prediction history.
3. **Recommendation depth**: Consumer behavior data builds richer profiles over time. Personalization improves with every interaction.

### What Can Be Replicated (Table Stakes)

1. Basic deal listing and purchase flow
2. Payment processing
3. Push notifications
4. Basic merchant dashboard
5. Ratings and reviews

### Recommended Differentiation Strategy

**Lead with ML, not marketplace**: The marketplace is table-stakes. The ML capabilities are the moat. Positioning should emphasize:

- "The first food waste platform that predicts surplus before it happens"
- "AI-powered pricing that ensures every item sells"
- "Personalized deals that find you, not the other way around"

---

## 5. Competitive Risks

### Risk: Too Good To Go enters Singapore

- **Probability**: Moderate (they've expanded to US, Singapore is a logical next step)
- **Impact**: High (brand recognition, funding, proven model)
- **Mitigation**: First-mover advantage with ML features; local partnerships; hawker-specific features they won't build

### Risk: Grab adds surplus food feature

- **Probability**: Low-Moderate (they have the merchant network)
- **Impact**: Very High (installed user base, merchant relationships, delivery infrastructure)
- **Mitigation**: Focus on ML differentiation; Grab's core business is delivery, not waste reduction — different incentive structure

### Risk: TreatSure pivots to ML

- **Probability**: Low (resource-constrained, no ML expertise evident)
- **Impact**: Moderate (they have local merchant relationships)
- **Mitigation**: Speed to market; superior ML capabilities; broader merchant base

### Risk: New entrant with ML focus

- **Probability**: Low (requires ML expertise + marketplace operations)
- **Impact**: High (direct competitor with same differentiation)
- **Mitigation**: Data moat; first-mover advantage; continuous ML improvement
