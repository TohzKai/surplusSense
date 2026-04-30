# ML Architecture Design

## Overview

The platform requires four ML capabilities, each addressing a distinct business problem. This document specifies the architecture for each, the overall pipeline, data requirements, and an implementation roadmap appropriate for an SMU MBA ML individual project with startup exploration intent.

---

## 1. Surplus Prediction

### Problem Statement

Predict how much surplus food a merchant will have on a given day, for each food category, so that listings can be auto-generated and merchants can adjust production.

### Approach

**Primary model**: Gradient Boosted Trees (XGBoost)

- Handles tabular features well
- Robust to missing data (common in early merchant data)
- Interpretable feature importance for merchant trust
- Fast training and inference

**Secondary model**: Prophet (Facebook) for time-series decomposition

- Captures weekly/seasonal patterns
- Provides uncertainty intervals (confidence bounds)
- Good baseline for merchants with limited data

**Ensemble**: Weighted average of XGBoost and Prophet predictions, with weights optimized per-merchant based on validation performance.

### Feature Engineering

| Feature Category      | Features                                                                                                  | Source              |
| --------------------- | --------------------------------------------------------------------------------------------------------- | ------------------- |
| **Temporal**          | Day of week, month, holiday flag, school holiday, payday proximity                                        | Calendar API        |
| **Weather**           | Temperature, rainfall, humidity, weather category                                                         | Weather API         |
| **Historical sales**  | Sales last 7 days (same item), sales same day last week, sales same day last month, 30-day moving average | POS / Platform data |
| **Merchant-specific** | Average surplus % by category, typical batch size, merchant operating hours                               | Platform data       |
| **Event-driven**      | Nearby events count, event attendance estimates, promotion flag                                           | Events API          |
| **Menu features**     | Item category (halal/vegetarian/etc.), price point, shelf life category                                   | Platform data       |
| **Lagged surplus**    | Surplus yesterday, surplus same day last week, 7-day surplus trend                                        | Platform data       |

### Data Requirements

- **Minimum for cold start**: 14 days of transaction data per merchant (rule-based predictions)
- **Good predictions**: 4-8 weeks of data (XGBoost begins outperforming rules)
- **Strong predictions**: 12+ weeks of data (ensemble model, per-merchant tuning)

### Target Variable

- `surplus_quantity` (units per food category per day)
- Alternative: `surplus_ratio` = surplus / prepared (percentage-based)

### Evaluation Metrics

| Metric                                | Purpose                                   | Target                 |
| ------------------------------------- | ----------------------------------------- | ---------------------- |
| MAE (Mean Absolute Error)             | Average prediction error                  | < 2 units per category |
| MAPE (Mean Absolute Percentage Error) | Relative accuracy                         | < 25%                  |
| RMSE                                  | Penalizes large errors                    | Minimize               |
| Directional accuracy                  | Correctly predicts surplus vs. no-surplus | > 85%                  |
| Coverage                              | % of days with predictions                | > 90%                  |

### Cold Start Strategy

1. **Week 1-2**: Use category-level averages across all merchants (e.g., "bakeries typically have 15% surplus on weekdays")
2. **Week 3-4**: Blend category averages with merchant's own short history
3. **Week 5+**: Full merchant-specific model with ensemble

### API Design

```
POST /api/v1/ml/predict-surplus
  merchant_id: str
  date: date (optional, defaults to tomorrow)
  categories: list[str] (optional, defaults to all)
→
  predictions: [
    { category: "pastries", predicted_surplus: 12, confidence: 0.82, suggested_price: 2.50 },
    { category: "sandwiches", predicted_surplus: 5, confidence: 0.71, suggested_price: 3.00 }
  ]
```

---

## 2. Personalized Recommendations

### Problem Statement

Rank available deals for each consumer based on their preferences, location, behavior, and context to maximize conversion and satisfaction.

### Approach

**Hybrid recommendation system** combining:

1. **Collaborative Filtering** (Matrix Factorization)
   - User-item interaction matrix (purchases, clicks, ratings)
   - SVD or ALS decomposition for latent factor discovery
   - Handles "users like you also liked" recommendations

2. **Content-Based Filtering**
   - Item features: cuisine, price range, dietary tags, distance, freshness category
   - User profile: preferred cuisines, price sensitivity, dietary restrictions, location patterns
   - Cosine similarity between user profile and available items

3. **Contextual Bandit** (for real-time personalization)
   - Context: time of day, weather, user location, day of week
   - Actions: show deal A, B, C, etc.
   - Reward: click, purchase, rating
   - Balances exploitation (known preferences) and exploration (discovering new preferences)

### Feature Engineering

| Feature Category  | Features                                                                      | Type                |
| ----------------- | ----------------------------------------------------------------------------- | ------------------- |
| **User profile**  | Preferred cuisines, price range, dietary tags                                 | Explicit + Implicit |
| **Behavioral**    | Purchase history, click history, browse time per category, ratings            | Implicit            |
| **Contextual**    | Time of day, day of week, weather, user location (lat/lon)                    | Real-time           |
| **Item features** | Cuisine, merchant type, price, discount %, distance from user, expiry urgency | Item attributes     |
| **Social**        | Popularity (purchase count), friend purchases (if social graph exists)        | Aggregate           |
| **Temporal**      | User's typical browsing time, typical purchase day patterns                   | Behavioral          |

### Cold Start Solutions

**New user (no history)**:

1. Onboarding: Quick 3-question preference quiz (favorite cuisines, budget range, dietary restrictions)
2. Location-based defaults: Show popular deals near user's location
3. Popularity-based: Rank by overall purchase count and rating
4. Rapid learning: After 3-5 interactions, switch to personalized model

**New merchant/item (no interaction history)**:

1. Content-based: Match to users based on item features (cuisine, location, price)
2. Similar merchant proxy: Use data from merchants with similar profiles
3. Exploration: Show to small % of likely-interested users, collect signal

### Evaluation Metrics

| Metric                   | Purpose                                          | Target          |
| ------------------------ | ------------------------------------------------ | --------------- |
| Precision@5              | % of top-5 recommendations purchased             | > 20%           |
| NDCG@10                  | Ranking quality (discounted cumulative gain)     | > 0.35          |
| Click-through rate (CTR) | % of recommendations clicked                     | > 15%           |
| Conversion rate          | % of clicks leading to purchase                  | > 30%           |
| Diversity                | Coverage of different cuisine/merchant types     | > 0.6 (entropy) |
| Serendipity              | % of purchases from previously unseen categories | > 10%           |

### Minimum Viable Model (MVP)

Start with content-based filtering (cosine similarity on item features + user profile). No interaction data needed. Upgrade to hybrid after collecting 500+ user-item interactions.

---

## 3. Dynamic Pricing

### Problem Statement

Optimize the price of surplus food items in real-time to maximize sell-through rate while maintaining merchant revenue and consumer perceived value.

### Approach

**Phase 1 (MVP): Rule-based with ML-informed parameters**

- Time-decay pricing: Price decreases linearly/exponentially as pickup window closes
- Demand-responsive: If N+ users viewing but 0 purchases in last X minutes, trigger price drop
- Merchant sets base price and floor price; system optimizes within bounds

**Phase 2: Multi-Armed Bandit**

- Arms = different price points (discretized)
- Context = time remaining, current viewers, category, merchant, weather
- Reward = revenue × sell-through probability
- Thompson Sampling for efficient exploration
- Learns optimal pricing policy per category and context

**Phase 3 (Advanced): Reinforcement Learning**

- State: [time_remaining, current_price, views, purchases, competition_prices, weather, day_of_week]
- Action: price adjustment (±delta)
- Reward: revenue if sold, 0 if unsold
- DQN or PPO for continuous price optimization
- Requires significant transaction data (10K+ transactions)

### Pricing Factors

| Factor                      | Effect                                                     | Weight (Phase 1) |
| --------------------------- | ---------------------------------------------------------- | ---------------- |
| **Time remaining**          | Price decays as pickup deadline approaches                 | 40%              |
| **Current demand**          | More views without purchases → lower price needed          | 20%              |
| **Historical sell-through** | Items with high sell-through maintain price longer         | 15%              |
| **Category base price**     | Premium categories have higher starting discount           | 10%              |
| **Competition**             | Similar deals nearby affect price sensitivity              | 10%              |
| **Weather**                 | Rain increases delivery demand, reduces pickup willingness | 5%               |

### Price Curve Model

```
price(t) = base_price × (floor_ratio + (1 - floor_ratio) × decay(t))

Where:
  base_price = merchant's listed original price
  floor_ratio = minimum price as fraction of base (e.g., 0.2 = 20% of base)
  decay(t) = e^(-λt) where t = time_elapsed / total_window
  λ = decay rate (adjusted per category based on sell-through data)
```

### Constraints

- **Price floor**: Merchant sets minimum acceptable price (never go below)
- **Price transparency**: Consumer sees original price, current price, and savings %
- **No price increases**: Price can only decrease over time, never increase
- **Round pricing**: Final price rounded to nearest S$0.50 for simplicity
- **Notification**: Consumer who bookmarked gets notified of price drops

### Evaluation Metrics

| Metric                    | Purpose                                      | Target                  |
| ------------------------- | -------------------------------------------- | ----------------------- |
| Sell-through rate         | % of listed items sold                       | > 80%                   |
| Revenue per item          | Average revenue (vs. fixed pricing baseline) | > baseline              |
| Time-to-sell              | Average time from listing to purchase        | Decreasing trend        |
| Merchant satisfaction     | Survey / retention rate                      | > 90% monthly retention |
| Consumer value perception | Average rating of "was this a good deal?"    | > 4.0/5.0               |

### Minimum Viable Model (MVP)

Rule-based time-decay with 3 price tiers (full discount at listing, mid-point at 50% time, floor at 80% time). Collect pricing data for 4-6 weeks before training ML models.

---

## 4. Waste Analytics

### Problem Statement

Detect patterns in merchant food waste data and provide prescriptive recommendations to reduce waste at source — going beyond descriptive dashboards to actionable insights.

### Approach

**1. Pattern Detection (Clustering)**

- K-Means or DBSCAN on daily waste patterns
- Identify "waste profiles" (e.g., "consistent over-producer", "weekend spike", "weather-sensitive")
- Merchants grouped for benchmarking against similar profiles

**2. Anomaly Detection**

- Isolation Forest or Z-score detection on waste quantities
- Flag unusual waste events (spike above normal variation)
- Root cause correlation: was anomaly correlated with weather, event, holiday, or operational change?

**3. Trend Analysis**

- Time-series decomposition (trend + seasonal + residual)
- Moving averages for waste trajectory
- Statistical significance testing for trend direction

**4. Prescriptive Recommendations**

- Rule engine + ML confidence scoring
- Example outputs:
  - "Reduce [category] batch size by X% on [day] — predicted to save S$Y/month"
  - "Your waste spikes on rainy weekdays — consider reducing prep by 15% when forecast shows >60% rain probability"
  - "Top 3 waste categories account for 70% of your waste — focus reduction efforts here"

### Analytics Outputs

| Insight Type           | Example                                                                   | Value to Merchant         |
| ---------------------- | ------------------------------------------------------------------------- | ------------------------- |
| **Waste breakdown**    | "Pastries: 42% of waste, Rice dishes: 28%, Beverages: 15%"                | Know where to focus       |
| **Temporal pattern**   | "Tuesday waste is 40% above weekly average"                               | Adjust Tuesday operations |
| **Prediction alert**   | "Expected 20% higher surplus tomorrow due to rain forecast"               | Proactive adjustment      |
| **Batch optimization** | "Optimal batch size for chicken rice: 45 portions (current: 55)"          | Reduce overproduction     |
| **Revenue recovery**   | "S$380 recovered through platform this month (vs. S$0 wasted last month)" | Quantify platform ROI     |
| **Benchmark**          | "Your waste rate: 12% (similar merchants: 15% average)"                   | Competitive positioning   |

### Data Requirements

- Minimum 30 days of transaction/surplus data for initial insights
- 90+ days for reliable pattern detection and trend analysis
- Category-level granularity required (not just total waste)

### Evaluation Metrics

| Metric                              | Purpose                             | Target          |
| ----------------------------------- | ----------------------------------- | --------------- |
| Recommendation adoption rate        | % of insights merchants act on      | > 30%           |
| Waste reduction after adoption      | Measurable decrease post-action     | > 10% reduction |
| Insight relevance (merchant survey) | Are recommendations useful?         | > 4.0/5.0       |
| Prediction accuracy                 | Do predicted patterns match actual? | > 75%           |

---

## 5. Overall ML Pipeline Architecture

### Data Collection Layer

```
┌─────────────────────────────────────────────────┐
│                  Data Sources                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Platform │  │ External │  │ Merchant │      │
│  │  Events   │  │   APIs   │  │   POS    │      │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘      │
│        │              │              │           │
│        └──────────────┼──────────────┘           │
│                       ▼                          │
│              ┌──────────────┐                    │
│              │  Event Queue │                    │
│              │  (Redis)     │                    │
│              └──────┬───────┘                    │
│                     ▼                            │
│           ┌──────────────────┐                   │
│           │  Data Warehouse  │                   │
│           │  (PostgreSQL)    │                   │
│           └──────────────────┘                   │
└─────────────────────────────────────────────────┘
```

### Feature Store

| Store                  | Technology        | Purpose                            |
| ---------------------- | ----------------- | ---------------------------------- |
| **Feature tables**     | PostgreSQL tables | Pre-computed features for training |
| **Feature cache**      | Redis             | Real-time feature serving          |
| **Feature versioning** | Git-tracked SQL   | Reproducible feature computation   |

**Key feature tables**:

- `merchant_daily_features`: Aggregated per merchant per day
- `user_interaction_features`: User behavior aggregates
- `item_features`: Deal/item characteristics
- `contextual_features`: Weather, events, temporal data

### Model Training Pipeline

```
┌─────────────────────────────────────────────────┐
│              Training Pipeline                    │
│                                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │ Extract │ →  │ Train   │ →  │ Evaluate│     │
│  │Features │    │ Model   │    │ & Validate│    │
│  └─────────┘    └─────────┘    └────┬────┘     │
│                                      │          │
│                              ┌───────┴──────┐   │
│                              │ Deploy if    │   │
│                              │ metrics pass │   │
│                              └───────┬──────┘   │
│                                      ▼          │
│                              ┌──────────────┐   │
│                              │ Model Registry│   │
│                              │ (file-based) │   │
│                              └──────────────┘   │
└─────────────────────────────────────────────────┘
```

**Training schedule**:

- Surplus prediction: Daily retrain (batch, overnight)
- Recommendations: Weekly retrain + online updates for new interactions
- Dynamic pricing: Continuous learning (bandit updates after each transaction)
- Waste analytics: Monthly retrain with new pattern detection

### Model Serving Layer

```
┌─────────────────────────────────────────────────┐
│              Serving Architecture                 │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐             │
│  │ REST API     │  │ Batch Jobs   │             │
│  │ (FastAPI)    │  │ (APScheduler)│             │
│  │              │  │              │             │
│  │ • Predict    │  │ • Nightly    │             │
│  │   surplus    │  │   surplus    │             │
│  │ • Recommend  │  │   predictions│             │
│  │ • Price      │  │ • Weekly     │             │
│  │              │  │   analytics  │             │
│  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                     │
│         ▼                  ▼                     │
│  ┌──────────────────────────────┐               │
│  │     Model Serving Layer      │               │
│  │  (joblib/pickle serialized)  │               │
│  └──────────────────────────────┘               │
└─────────────────────────────────────────────────┘
```

**Serving strategy**:

- **Real-time**: Predictions API, recommendations API, pricing API (< 100ms response)
- **Batch**: Nightly surplus predictions, weekly analytics reports, daily feature computation
- **Near-real-time**: Bandit updates for pricing (after each transaction event)

### Monitoring and Retraining

| Monitor                 | Metric                                             | Alert Threshold    |
| ----------------------- | -------------------------------------------------- | ------------------ |
| **Data drift**          | Feature distribution shift (KS test)               | p < 0.05           |
| **Prediction accuracy** | MAPE on recent predictions                         | > 30%              |
| **Model performance**   | Sell-through rate (pricing), CTR (recommendations) | 20% below baseline |
| **Retraining trigger**  | Accuracy degradation + data drift                  | Combined condition |

---

## 6. Implementation Roadmap

### Phase 1: MVP (4-6 weeks)

**Goal**: Working marketplace with basic ML features

| Week | Deliverable                                                                  |
| ---- | ---------------------------------------------------------------------------- |
| 1-2  | Core platform: User auth, merchant listing, consumer browsing, purchase flow |
| 3-4  | Surplus prediction: Rule-based + simple XGBoost model                        |
| 4-5  | Recommendations: Content-based filtering with cosine similarity              |
| 5-6  | Basic analytics: Descriptive waste dashboard for merchants                   |

**Tech stack**:

- Backend: Python + FastAPI
- Database: PostgreSQL
- ML: scikit-learn, XGBoost
- Serving: joblib model serialization, FastAPI endpoints

### Phase 2: Enhanced ML (4-6 weeks)

**Goal**: ML-driven features that create competitive advantage

| Week  | Deliverable                                                |
| ----- | ---------------------------------------------------------- |
| 7-8   | Dynamic pricing: Time-decay rule engine + data collection  |
| 9-10  | Recommendations: Hybrid (collaborative + content-based)    |
| 11-12 | Waste analytics: Pattern detection + prescriptive insights |
| 12    | Surplus prediction: Ensemble (XGBoost + Prophet)           |

**Additional tech**:

- Prophet for time-series
- Surprise library for collaborative filtering
- Isolation Forest for anomaly detection

### Phase 3: Advanced (6-8 weeks)

**Goal**: Production-grade ML with real-time serving

| Week  | Deliverable                                                    |
| ----- | -------------------------------------------------------------- |
| 13-16 | Dynamic pricing: Multi-armed bandit                            |
| 16-18 | Deep learning recommendations (neural collaborative filtering) |
| 18-20 | Feature store and pipeline automation                          |

**Additional tech**:

- TensorFlow/PyTorch for neural models
- Redis for feature caching
- APScheduler for batch jobs

---

## 7. Risk Analysis

### Technical Risks

| Risk                                 | Probability        | Impact | Mitigation                                                     |
| ------------------------------------ | ------------------ | ------ | -------------------------------------------------------------- |
| Insufficient data for ML training    | High (early stage) | High   | Rule-based fallbacks; category-level models                    |
| Surplus prediction inaccuracy        | Medium             | High   | Conservative predictions; merchant override; confidence scores |
| Recommendation cold start            | High               | Medium | Content-based baseline; onboarding quiz; popularity defaults   |
| Pricing model errors (under-pricing) | Medium             | High   | Price floors; merchant approval for aggressive discounts       |
| Real-time serving latency            | Low                | Medium | Pre-compute predictions; cache results; batch where possible   |

### Business Risks

| Risk                                 | Probability | Impact | Mitigation                                                   |
| ------------------------------------ | ----------- | ------ | ------------------------------------------------------------ |
| Merchants don't trust ML predictions | Medium      | High   | Transparent confidence scores; easy override; A/B test proof |
| Consumers don't trust surplus food   | Medium      | High   | Quality verification; ratings; food safety education         |
| Data privacy concerns                | Low         | Medium | PDPA compliance; anonymized analytics; clear consent         |

---

## 8. Technology Stack Summary

| Component                | Technology            | Justification                              |
| ------------------------ | --------------------- | ------------------------------------------ |
| **Language**             | Python 3.11+          | ML ecosystem, FastAPI, course alignment    |
| **Web framework**        | FastAPI               | Async, typed, auto-docs, Python-native     |
| **Database**             | PostgreSQL            | Relational data, JSON support, free        |
| **ML — Classical**       | scikit-learn, XGBoost | Proven, interpretable, fast training       |
| **ML — Time-series**     | Prophet               | Seasonality handling, uncertainty bounds   |
| **ML — Deep Learning**   | PyTorch               | Flexibility, research-friendly (Phase 3)   |
| **ML — Recommendations** | Surprise, implicit    | Specialized recommendation libraries       |
| **Data processing**      | pandas, numpy         | Standard Python data stack                 |
| **Visualization**        | Plotly, matplotlib    | Interactive charts for analytics dashboard |
| **Model serving**        | joblib + FastAPI      | Simple, effective for MVP                  |
| **Task scheduling**      | APScheduler           | Python-native, lightweight                 |
| **Caching**              | Redis                 | Feature serving, session management        |
| **Deployment**           | Docker + cloud (TBD)  | Containerized, portable                    |
