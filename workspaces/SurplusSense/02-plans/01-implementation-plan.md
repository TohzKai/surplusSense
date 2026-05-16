# Implementation Plan

## Final Submitted MVP — Implementation Scope

The final submitted MVP is the **merchant decision-support cockpit**: a Streamlit dashboard that takes merchant context (merchant type, category, storage, preparation time) and item details (price, shelf life, holding time) and outputs a recommended action (HOLD / MONITOR / DISCOUNT / DEEP DISCOUNT / DONATE / DISCARD) with discount tier, food-safety status, and revenue recovery estimate.

**What the MVP includes:**

- XGBoost surplus prediction (31 raw features → 47 model input columns, temporal 80/20 holdout validation)
- 10-tier discount recommendation engine with cold-start category benchmarks
- 5-check food-safety gate (BLOCK / CAUTION / SAFE)
- Recovery-value estimation
- 75 passing unit tests
- Reproducible pipeline (`RANDOM_SEED=42`)

**What is NOT in the MVP (Phase 2):**

- Consumer marketplace, consumer app, payments, QR pickup
- POS / inventory system integration
- Multi-tenant infrastructure
- Real merchant data (synthetic data only)

> **Scope note:** Earlier phases of this plan explored a broader two-sided marketplace. The final individual assignment scope is the merchant decision-support cockpit (Phase 1 merchant layer only). Consumer marketplace, payments, delivery, and POS integration are Phase 2. See `workspaces/SurplusSense/01-analysis/04-final-positioning.md`.

---

## Final Submitted MVP Implementation Plan

The final submitted product is intentionally narrow and decision-focused.

## Implemented Core Components

| Component                  | Purpose                                                    | Evidence                                           |
| -------------------------- | ---------------------------------------------------------- | -------------------------------------------------- |
| Streamlit merchant cockpit | Gives the merchant an interactive decision interface       | `app/streamlit_app.py`                             |
| XGBoost surplus prediction | Predicts expected surplus units                            | `src/train_model.py`, `models/model_metadata.json` |
| Temporal validation        | Evaluates model using future-like holdout                  | `src/train_model.py`; `outputs/model_results.csv`  |
| Leakage-aware features     | Prevents future data from entering prediction              | `src/feature_engineering.py` with `shift(1)`       |
| Recommendation engine      | Converts prediction into merchant action                   | `src/recommendation_engine.py`                     |
| Food-safety gate           | Prevents unsafe commercial recommendations                 | `src/food_safety_rules.py`                         |
| Recovery-value estimate    | Links ML output to business value                          | `src/recommendation_engine.py`; executive report   |
| Explanation layer          | Makes recommendation understandable to non-technical users | `app/streamlit_app.py`                             |
| Pilot validation plan      | Defines how merchant value would be tested                 | `PILOT_VALIDATION_PLAN.md`                         |

## Scope-Control Decision

I deliberately did not implement consumer marketplace, payments, QR pickup, delivery logistics, POS integration, or a consumer mobile app in the final MVP. Those items increase product breadth but do not strengthen the core ML decision-support evidence required by MGMT655.

This scope-control decision demonstrates human judgment: I prioritised a complete, testable, explainable decision-support product over a broader but less mature marketplace prototype.

---

## Historical / Phase 2 Marketplace Exploration

The sections below document the earlier marketplace concept. They are retained as process evidence and are not part of the submitted MVP.

### Phase 1: Core Marketplace (Weeks 1-3)

### Objective

Build the two-sided marketplace — merchants can list surplus food, consumers can browse and purchase, with basic payment and pickup flow.

### Objective

Build the two-sided marketplace — merchants can list surplus food, consumers can browse and purchase, with basic payment and pickup flow.

### Shard 1: Backend API + Data Model (Week 1)

**Scope**: PostgreSQL database, FastAPI backend, authentication, core CRUD endpoints.

**Data model**:

- Users (merchants + consumers + admin)
- Merchants (business profile, location, categories, SFA license)
- Listings (surplus food items, quantities, prices, pickup windows)
- Orders (purchase records, status, payment)
- Reviews (consumer ratings and feedback)

**API endpoints**:

- Auth: register, login, refresh token
- Merchants: CRUD profile, manage categories, set pricing
- Listings: create, read, update, delete, search/filter
- Orders: create, read, update status, cancel
- Reviews: create, read by merchant/listing

**Files to create**:

```
src/
  app/
    main.py              # FastAPI app entry point
    config.py            # Settings from .env
    database.py          # PostgreSQL connection
    models/
      user.py
      merchant.py
      listing.py
      order.py
      review.py
    routers/
      auth.py
      merchants.py
      listings.py
      orders.py
      reviews.py
    schemas/
      user.py
      merchant.py
      listing.py
      order.py
      review.py
    services/
      auth_service.py
      merchant_service.py
      listing_service.py
      order_service.py
  alembic/               # Database migrations
  tests/
    test_auth.py
    test_listings.py
    test_orders.py
```

### Shard 2: Merchant Dashboard (Week 2)

**Scope**: Merchant-facing web interface for managing listings, viewing orders, and basic analytics.

**Key pages**:

- Login / Registration
- Dashboard (today's overview: predicted surplus, active listings, orders)
- Create/Edit listing
- Order management (incoming orders, QR scan)
- Basic analytics (sales this week, top categories)

**Tech**: React or Flutter Web (depending on frontend choice)

### Shard 3: Consumer Mobile App (Week 2-3)

**Scope**: Consumer-facing mobile app for browsing, purchasing, and pickup.

**Key screens**:

- Onboarding (sign up + preference quiz)
- Home feed (nearby deals, personalized)
- Deal detail + purchase
- Order tracking (QR code, pickup status)
- Profile + impact dashboard
- Search + filters

**Tech**: Flutter (cross-platform mobile)

### Shard 4: Payment + QR Pickup (Week 3)

**Scope**: Payment integration and QR-based pickup flow.

**Components**:

- Stripe payment processing (supports cards, Apple Pay, Google Pay)
- QR code generation (order confirmation)
- QR code scanning (merchant side)
- Order status state machine (placed → preparing → ready → collected)
- Payment settlement and merchant payout tracking

---

## Phase 2: ML Features (Weeks 4-7)

### Shard 5: Surplus Prediction Model (Week 4-5)

**Scope**: Build and deploy the surplus prediction model.

**Steps**:

1. Feature engineering pipeline (extract features from transaction data)
2. Baseline: Rule-based predictions using category averages
3. XGBoost model training on historical data
4. Prophet model for time-series decomposition
5. Ensemble combining XGBoost + Prophet
6. REST API endpoint for predictions
7. Integration with merchant dashboard (morning prediction card)

**Files**:

```
src/ml/
  surplus_prediction/
    features.py          # Feature engineering
    model.py             # XGBoost + Prophet ensemble
    train.py             # Training pipeline
    predict.py           # Prediction serving
    evaluate.py          # Model evaluation
  tests/
    test_surplus_prediction.py
```

### Shard 6: Recommendation Engine (Week 5-6)

**Scope**: Build and integrate the recommendation engine.

**Steps**:

1. Content-based filtering (user profile → item similarity)
2. Collaborative filtering (user-item interaction matrix)
3. Hybrid scoring and ranking
4. Cold start handling (new users, new items)
5. API endpoint for personalized feed
6. Integration with consumer home feed

**Files**:

```
src/ml/
  recommendations/
    content_based.py     # Content filtering
    collaborative.py     # Matrix factorization
    hybrid.py            # Ensemble scoring
    cold_start.py        # New user/item handling
    features.py          # Feature extraction
  tests/
    test_recommendations.py
```

### Shard 7: Dynamic Pricing Engine (Week 6-7)

**Scope**: Build and deploy dynamic pricing.

**Steps**:

1. Price curve model (time-decay with configurable parameters)
2. Demand signal tracking (views, purchases over time)
3. Rule-based pricing adjustments (3-tier: initial → mid → floor)
4. Price update API (real-time price queries)
5. Integration with listing display (live price updates)
6. Data collection for ML-based pricing (Phase 3)

**Files**:

```
src/ml/
  pricing/
    price_curve.py       # Time-decay model
    demand_tracker.py    # Demand signal processing
    engine.py            # Pricing orchestration
    rules.py             # Rule-based pricing logic
  tests/
    test_pricing.py
```

### Shard 8: Waste Analytics (Week 7)

**Scope**: Build merchant waste analytics with prescriptive recommendations.

**Steps**:

1. Data aggregation pipeline (daily/weekly waste metrics)
2. Pattern detection (clustering merchants by waste profile)
3. Anomaly detection (flag unusual waste events)
4. Recommendation engine (actionable insights with confidence scores)
5. Analytics API endpoints
6. Merchant dashboard analytics views

**Files**:

```
src/ml/
  analytics/
    aggregation.py       # Data aggregation
    patterns.py          # Clustering + pattern detection
    anomalies.py         # Anomaly detection
    recommendations.py   # Prescriptive insights
    reports.py           # Report generation
  tests/
    test_analytics.py
```

---

## Phase 3: Polish and Demo (Weeks 8-10)

### Shard 9: ML Pipeline Infrastructure (Week 8)

**Scope**: Automated training, evaluation, and serving infrastructure.

**Steps**:

1. Feature store tables in PostgreSQL
2. Scheduled training jobs (APScheduler)
3. Model versioning and registry (file-based)
4. Model performance monitoring
5. Automated retraining triggers

### Shard 10: End-to-End Polish (Week 9)

**Scope**: Refine UX, fix bugs, improve ML model performance.

**Focus areas**:

- Consumer app UX polish (animations, loading states, error handling)
- Merchant dashboard refinement (prediction UX, analytics visualization)
- ML model tuning (hyperparameter optimization, feature selection)
- Performance optimization (caching, query optimization)
- Error handling and edge cases

### Shard 11: Demo Preparation (Week 10)

**Scope**: Prepare for SMU MBA ML project presentation.

**Deliverables**:

1. Working end-to-end demo (merchant lists → consumer purchases → pickup)
2. ML feature demonstrations (surplus prediction accuracy, recommendation quality, dynamic pricing in action, waste analytics insights)
3. Technical documentation (model architectures, training results, evaluation metrics)
4. Business case presentation (market analysis, competitive positioning, financial projections)
5. Video walkthrough of the application

---

## Technology Decisions

| Decision | Choice                         | Rationale                                             |
| -------- | ------------------------------ | ----------------------------------------------------- |
| Backend  | Python + FastAPI               | Async, typed, auto-docs, ML ecosystem alignment       |
| Frontend | Flutter                        | Cross-platform mobile + web, single codebase          |
| Database | PostgreSQL                     | Relational data, JSON support, free, reliable         |
| ML       | scikit-learn, XGBoost, Prophet | Proven, interpretable, good for tabular data          |
| Payments | Stripe                         | Fast setup, supports Singapore, multi-payment methods |
| Hosting  | Railway or Render              | Simple deployment, free tier available                |
| Maps     | Google Maps API                | Location features, distance calculation               |

---

## Testing Strategy

| Tier              | Scope                                  | Tools                      |
| ----------------- | -------------------------------------- | -------------------------- |
| Unit tests        | Individual functions, model components | pytest                     |
| Integration tests | API endpoints with test database       | pytest + test client       |
| ML tests          | Model accuracy, feature pipelines      | pytest + custom evaluators |
| E2E tests         | Full user flows (optional)             | Flutter integration tests  |

---

## Risk Mitigation

| Risk                           | Mitigation                                                     |
| ------------------------------ | -------------------------------------------------------------- |
| Not enough real data for ML    | Generate realistic synthetic data based on research benchmarks |
| Payment integration complexity | Start with Stripe test mode; simulate payments in demo         |
| Flutter learning curve         | Keep UI simple; use Material Design components                 |
| Scope creep                    | Strict phase boundaries; each phase delivers working product   |
| Time pressure                  | Phase 1 is the MVP; Phases 2-3 are enhancements                |
