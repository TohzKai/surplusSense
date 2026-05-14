# ML Recommendations Specification

> **Phase 2 — Not part of final submitted MVP.** Consumer-facing recommendation ranking is Phase 2. The submitted MVP uses a deterministic 10-tier discount recommendation engine documented in `src/recommendation_engine.py`.

## Overview

Hybrid recommendation engine that ranks available deals for each consumer based on preferences, behavior, context, and social signals. Designed to maximize conversion while maintaining discovery diversity.

## Recommendation Signals

### Explicit Signals (User-Provided)

- Preferred cuisines (from onboarding quiz and profile settings)
- Dietary restrictions (halal, vegetarian, etc.)
- Budget range (max preferred price)
- Saved/favorited merchants

### Implicit Signals (Behavior-Derived)

- Purchase history (cuisine, merchant, price range, time of day)
- Click/browsing history (categories viewed, dwell time)
- Rating patterns (cuisines rated highly vs. lowly)
- Pickup patterns (distance willing to travel, time of pickup)
- Skip patterns (categories scrolled past without clicking)

### Contextual Signals (Real-Time)

- Current time of day (lunch deals vs. dinner deals)
- Current day of week
- Current weather (rainy → comfort food, sunny → light meals)
- User's current location (latitude/longitude)
- Nearby events (increased demand areas)

### Listing Signals

- Time remaining on listing (urgency)
- Quantity remaining (scarcity)
- Current discount percentage (value)
- Merchant rating and review count (quality)
- Distance from user's location (convenience)

## Model Architecture

### Layer 1: Candidate Generation

- **Content-based**: Filter listings matching user's cuisine/dietary/budget preferences
- **Geographic**: Filter listings within user's preferred distance radius
- **Availability**: Only active listings with quantity > 0 and pickup window not expired
- Target: Generate 50-200 candidates from full listing pool

### Layer 2: Scoring and Ranking

**Content-Based Score (0-1)**

```python
score_content = weighted_sum([
    0.25 × cuisine_match(user.cuisines, listing.cuisine),
    0.20 × dietary_match(user.dietary, listing.tags),
    0.20 × price_match(user.budget, listing.current_price),
    0.15 × distance_score(user.location, listing.location),
    0.10 × quality_score(listing.merchant_rating),
    0.10 × recency_bonus(listing.created_at)
])
```

**Collaborative Score (0-1)**

- Matrix factorization (SVD) on user-item interaction matrix
- Interactions weighted: purchase=5, click=2, view=1, skip=-0.5
- Latent factors: 50 dimensions
- Requires minimum 10 user interactions before collaborative scoring activates

**Contextual Score (0-1)**

```python
score_context = weighted_sum([
    0.30 × time_relevance(hour, listing.pickup_window),
    0.25 × weather_relevance(weather, listing.category),
    0.25 × urgency_score(listing.time_remaining),
    0.20 × scarcity_score(listing.quantity_remaining, listing.quantity_total)
])
```

**Final Ranking Score**

```python
final_score = (
    0.35 × score_content +
    0.35 × score_collaborative +
    0.30 × score_context
)
```

### Layer 3: Re-Ranking and Diversity

- Ensure no more than 3 listings from same merchant in top 20
- Ensure at least 3 different cuisine types in top 10
- Boost listings from new merchants by 10% (exploration signal)
- Apply business rules: sold-out items removed, expired items removed

## Cold Start Handling

### New Consumer (0-5 interactions)

1. Use onboarding quiz preferences for content-based scoring
2. Collaborative score = 0 (weight redistributed to content and context)
3. Show popular deals filtered by stated preferences
4. Include 2-3 exploration items outside stated preferences

### New Merchant / New Listing (0 interactions)

1. Content-based matching only (cuisine, location, price)
2. Similar merchant proxy: find merchants with similar cuisine/price/location profile, borrow interaction patterns
3. Exploration boost: Show to 5-10% of likely-interested users for signal collection
4. After 10+ interactions: Full collaborative scoring activates

## Feed Sections

| Section       | Ranking Logic                            | Refresh Rate                              |
| ------------- | ---------------------------------------- | ----------------------------------------- |
| For You       | Full hybrid ranking                      | Every app open + every 5 min while active |
| Nearby        | Distance ascending, then by final_score  | Every location update                     |
| Expiring Soon | Time remaining ascending                 | Every minute                              |
| Best Value    | Discount % descending                    | Every 5 minutes                           |
| Surprise Bags | Surprise bag type, ranked by final_score | Every app open                            |

## Evaluation

### Offline Metrics (During Training)

| Metric      | Target | Measurement                                            |
| ----------- | ------ | ------------------------------------------------------ |
| Precision@5 | > 20%  | Fraction of top-5 recommendations that user purchased  |
| NDCG@10     | > 0.35 | Normalized discounted cumulative gain at position 10   |
| Coverage    | > 60%  | Fraction of active listings shown to at least one user |
| Diversity   | > 0.6  | Category entropy in recommendations                    |

### Online Metrics (In Production)

| Metric             | Target  | Measurement                                          |
| ------------------ | ------- | ---------------------------------------------------- |
| Click-through rate | > 15%   | Clicks / impressions                                 |
| Conversion rate    | > 30%   | Purchases / clicks                                   |
| Session duration   | > 2 min | Time spent browsing                                  |
| Feed freshness     | < 5 min | Time between listing creation and appearance in feed |

## API Endpoints

| Method | Path                                | Description                                  |
| ------ | ----------------------------------- | -------------------------------------------- |
| GET    | /api/v1/ml/recommendations          | Personalized feed for authenticated consumer |
| GET    | /api/v1/ml/recommendations/nearby   | Location-based recommendations               |
| POST   | /api/v1/ml/recommendations/feedback | Record interaction (view, click, skip)       |

## Feedback Loop

1. Every consumer interaction (view, click, purchase, skip, rate) logged to MLUserInteraction
2. Interaction context captured: time, weather, location, position in feed
3. Weekly retraining: Collaborative model retrained on accumulated interactions
4. Online updates: Content-based scores update immediately on preference changes
5. A/B testing: 10% of users receive baseline ranking (no ML) for comparison
