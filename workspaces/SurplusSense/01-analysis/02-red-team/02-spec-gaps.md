# Spec Gap Analysis: Red Team Findings

> **Phase 2 / Historical note:** This analysis was part of early marketplace exploration. The final submitted MVP is the merchant-side decision-support cockpit. This spec gap analysis is retained as process evidence.

## Executive Summary

The specification suite (13 files) provides solid coverage of the core marketplace, ML models, and user experiences. However, the audit found **44 gaps, inconsistencies, or missing details** across 7 severity categories. The most critical findings are: (1) missing database entities and tables for several documented features, (2) API contract inconsistencies between spec files, (3) notification data model entirely absent, (4) several brief objectives and research requirements unaccounted for in specs, and (5) critical edge cases in concurrent operations and food safety that lack implementation-level detail.

Complexity: **Moderate** -- the specs are well-structured and internally coherent at a high level, but the gaps below would cause implementation ambiguity or rework if not resolved before `/todos`.

---

## 1. Missing Data Model Entities (CRITICAL)

### GAP-01: No Notification table in data-model.md

The `notifications.md` spec describes a full notification system with storage, read/unread status, FCM tokens, preferences, and 30-day retention. The `data-model.md` has zero notification-related tables.

Missing tables needed:

- **Notification** -- id, user_id, type, title, body, data (JSONB), read_at, created_at, expires_at
- **NotificationPreference** -- per-user, per-category toggle, quiet_hours, max_daily
- **FCMToken** -- user_id, token, platform, device_id, registered_at

**Impact**: An implementer building notifications has no schema to work from. The data model spec is the authority for all table definitions.

### GAP-02: No SavedListing / Bookmark table

The `notifications.md` spec mentions "bookmarked/watched a listing" triggers price drop notifications. The `marketplace.md` consumer feed mentions bookmarking behavior. There is no SavedListing or Bookmark entity in `data-model.md`.

The existing `SavedMerchant` covers favoriting merchants, but there is no entity for favoriting/bookmarking individual listings.

### GAP-03: No MerchantPayout / TransactionLedger table

The `payments.md` spec describes weekly payouts, payout history, pending balances, and CSV export. The `data-model.md` has no payout tracking table.

Missing:

- **MerchantPayout** -- id, merchant_id, period_start, period_end, gross_amount, refund_deductions, net_amount, status (pending, processing, paid, failed), paid_at, stripe_payout_id
- **TransactionLedger** (or similar) -- to track per-order financial line items for audit and payout calculation

The Order table has `merchant_payout` and `platform_fee` fields, but there is no accumulated ledger or payout record entity.

### GAP-04: No Admin-specific tables

The brief specifies an **Admin** user role. The `authentication.md` spec defines admin endpoints and RBAC. The `data-model.md` has no admin-specific entities:

- Admin audit log
- Platform configuration / feature flags
- Merchant verification workflow state
- Reported content / complaints

The food-safety spec mentions "complaints" and "investigations" with resolution status, but there is no Complaint or Investigation table.

### GAP-05: No MLFeatureStore tables

The `03-ml-architecture.md` research file specifies feature store tables (`merchant_daily_features`, `user_interaction_features`, `item_features`, `contextual_features`). None of these appear in `data-model.md`. The ML specs reference features but do not define where computed features are persisted.

While this may be deferred to Phase 3, the data model should at minimum acknowledge these as planned entities or the ML specs should clarify they use views or ad-hoc computation.

### GAP-06: No Achievement / Badge definition tables

The `consumer-experience.md` spec defines 7 achievement badges (First Rescue, Regular Rescuer, Waste Warrior, etc.) with progress tracking. The `consumer-flows.md` describes a level/badge system. The `data-model.md` has no entity for badge definitions, user badge progress, or earned badges.

Missing:

- **Badge** -- id, name, description, icon_url, threshold_type, threshold_value
- **UserBadge** -- user_id, badge_id, earned_at, progress

The `ImpactRecord` table tracks per-order impact, but badge logic and aggregation have no home.

### GAP-07: No MerchantBankAccount entity

The `payments.md` spec says "merchant provides bank details during onboarding." The `merchant-experience.md` Settings page includes "Payment settings: Bank account for payouts." The `data-model.md` Merchant entity has no bank account fields.

This could be added to the Merchant table (bank_account_encrypted, bank_name, bank_code) or as a separate entity. Either way, it is missing.

---

## 2. API Contract Inconsistencies (CRITICAL)

### GAP-08: Surplus Prediction API -- POST vs GET mismatch

The `ml-surplus-prediction.md` spec defines:

```
GET /api/v1/ml/surplus-prediction?merchant_id={id}&date={date}
```

The `03-ml-architecture.md` research file defines:

```
POST /api/v1/ml/predict-surplus
  merchant_id: str, date: date, categories: list[str]
```

Two different HTTP methods, two different URL paths, two different request shapes. The spec file is the authority, but the research document may have been the basis for earlier planning. This must be reconciled.

### GAP-09: Notification API -- missing from data-model and marketplace endpoint lists

The `notifications.md` spec defines 6 API endpoints under `/api/v1/notifications/`. These endpoints do not appear in any other spec's API table. The `authentication.md` RBAC table does not include `/notifications/*` routes.

### GAP-10: ML Analytics API -- merchant_id in path vs query

The `ml-analytics.md` spec puts merchant_id in the path: `/api/v1/ml/analytics/{merchant_id}/overview`. The `authentication.md` RBAC table shows `/ml/*` endpoints with merchant access as "Predictions, analytics." An implementer needs to know: can a merchant only access their own analytics? Can an admin access any merchant's? The auth spec does not address path-parameter-based authorization.

### GAP-11: Listing creation -- conflicting required fields

The `marketplace.md` spec says merchant "Sets quantity, price (within floor/ceiling bounds), pickup window" when creating a listing. The `data-model.md` Listing entity requires: `merchant_id, category_id, title, description, item_type, original_price, current_price, min_price, quantity_total, quantity_remaining, pickup_start, pickup_end, listing_type, status, dietary_tags, image_urls, expires_at`.

The `marketplace.md` listing creation flow does not mention: `title` (required), `expires_at` (required), how `current_price` is set initially (same as original? from pricing engine?), or how `dietary_tags` are populated (inherited from category?).

### GAP-12: Order status enum mismatch between marketplace.md and data-model.md

The `marketplace.md` Order Status Machine shows:

```
placed -> preparing -> ready -> collected -> completed
placed -> expired -> refunded
placed -> cancelled -> refunded
```

The `data-model.md` OrderStatus enum is:

```
placed, preparing, ready, collected, expired, cancelled, refunded
```

The marketplace spec has "completed" as a state after "collected". The data model has no "completed" state -- it goes directly to "collected". The payments spec says QR scan triggers "order status -> collected." Which is it: collected = terminal, or collected -> completed?

### GAP-13: Review API endpoints -- merchant ID endpoint not in marketplace table

The `marketplace.md` spec lists review endpoints including:

```
GET /api/v1/merchants/{id}/reviews
```

This is nested under the merchants path, not under `/reviews`. The `authentication.md` RBAC shows `/reviews/*` routes but does not show `/merchants/{id}/reviews` as a route pattern. The merchant routes show `Own merchant CRUD` for `/merchants/*` but reviews are public reads -- this should be explicitly covered.

### GAP-14: Pricing API -- not covered in authentication RBAC

The `pricing.md` spec defines 3 endpoints:

```
GET /api/v1/pricing/{listing_id}
GET /api/v1/pricing/{listing_id}/history
POST /api/v1/ml/pricing/optimize
```

The `authentication.md` RBAC table does not include `/pricing/*` routes. The `/ml/*` row covers "Predictions, analytics" -- is the optimize endpoint covered? The read endpoints are presumably public or consumer-accessible, but this is not stated.

---

## 3. Missing Specification Topics (MAJOR)

### GAP-15: No image/file storage spec

Multiple specs reference image uploads:

- `data-model.md`: `logo_url` on Merchant, `image_urls` on Listing
- `merchant-experience.md`: "Optional: description, photos"
- `consumer-experience.md`: "[Image]" on deal cards

No spec covers:

- Where images are stored (S3? Cloudinary? Local filesystem?)
- Accepted formats and size limits
- Upload endpoints and authentication
- Image processing (thumbnails, compression)
- Fallback/placeholder images

### GAP-16: No search indexing or full-text search spec

The `marketplace.md` spec mentions "Full-text search on listing title, description, merchant name" and "Autocomplete suggestions from popular queries." PostgreSQL full-text search requires specific index types (GIN on tsvector), search configuration, and ranking functions. The `data-model.md` has no full-text search indexes defined.

The implementation needs:

- tsvector columns or functional indexes
- Search ranking function specification
- Autocomplete data source (materialized view? separate table?)
- Search analytics (popular queries, zero-result queries)

### GAP-17: No error response format specification

None of the spec files define a standard error response shape. When APIs return 4xx/5xx, what does the response body look like? An implementer needs:

```json
{
  "error": {
    "code": "LISTING_SOLD_OUT",
    "message": "This deal just sold out",
    "details": {...}
  }
}
```

Without a standard format, each endpoint will produce inconsistent error responses.

### GAP-18: No pagination specification

The `marketplace.md` spec defines listing and order endpoints that return collections:

```
GET /api/v1/listings
GET /api/v1/orders
GET /api/v1/reviews
```

No spec defines:

- Pagination method (offset/limit? cursor-based?)
- Default page size
- Maximum page size
- Response envelope format (total_count, has_next, items)
- Sort order when not specified

### GAP-19: No rate limiting specification (beyond auth)

The `authentication.md` spec defines rate limiting for login (10 per email per 15 minutes). No other endpoint has rate limiting defined. For a marketplace:

- Listing creation abuse (merchant spam)
- Purchase bot prevention
- Search/query rate limits
- ML prediction endpoint limits

### GAP-20: No webhook/specification for Stripe integration detail

The `payments.md` spec mentions Stripe webhooks but does not specify:

- Webhook signature verification method
- Idempotency key handling
- Webhook retry policy
- Which events are subscribed beyond the 4 listed
- How duplicate webhook deliveries are handled

### GAP-21: No geospatial query specification

Multiple specs reference distance-based features:

- Consumer feed: "Nearby" sorted by distance
- Search filters: distance (500m, 1km, 3km, etc.)
- ML recommendations: `distance_score(user.location, listing.location)`

The `data-model.md` defines a GiST index on Merchant lat/lon but does not specify:

- How distance is calculated (Haversine? PostGIS? ST_DWithin?)
- Whether PostGIS extension is required
- How consumer location is obtained and updated
- Accuracy expectations for distance calculation

### GAP-22: No scheduled job / background task specification

Multiple specs reference background processes:

- Surplus prediction: "Nightly batch job"
- Food safety: "Scheduled check every 30 minutes"
- Dynamic pricing: "Check every 5 minutes"
- Payouts: "Weekly payout every Monday"
- ML retraining: "Weekly," "daily," "monthly" schedules
- Notifications: "Background worker processes queue"

No spec defines the task scheduling infrastructure:

- What scheduler? (APScheduler is mentioned in research but not in specs)
- Task definition format
- Failure handling and retry
- Monitoring and alerting
- Concurrency limits

### GAP-23: No data seeding / synthetic data generation spec

The `01-implementation-plan.md` risk section identifies "Not enough real data for ML" as a risk and proposes "Generate realistic synthetic data." The implementation plan Phase 3 mentions demo preparation. No spec defines:

- Seed data schema
- Synthetic data generation rules
- Demo user accounts
- Data volume requirements for ML model training

---

## 4. Brief-to-Spec Coverage Gaps (MAJOR)

### GAP-24: "Explore commercial viability as a startup" -- no business metrics spec

Brief objective: "Explore commercial viability as a startup in Singapore's F&B market." The research files extensively analyze the business model (commission structure, unit economics, break-even analysis). No spec file defines:

- Platform-level business metrics (GMV, take rate, CAC, LTV)
- Merchant acquisition funnel tracking
- Consumer retention metrics
- Revenue dashboard for admin

### GAP-25: "Deliver a working prototype for SMU MBA ML project" -- no demo/test data spec

Brief objective: "Deliver a working prototype demonstrating ML capabilities." The implementation plan mentions demo preparation in Phase 3. No spec defines:

- Demo scenario (what the walkthrough looks like)
- Test accounts and seed data
- ML model performance benchmarks for presentation
- What "working" means in measurable terms

### GAP-26: Admin persona -- under-specified across all specs

The brief defines three user personas. The Admin persona is mentioned in:

- `authentication.md`: Role definition, RBAC table, admin registration
- `data-model.md`: UserRole enum

The admin has no dedicated spec file and no detailed flows for:

- Merchant onboarding approval/rejection
- Platform health monitoring
- ML model performance oversight
- Dispute resolution
- Financial reporting
- Content moderation (review flagged content)

### GAP-27: "Singapore market focus -- local F&B regulations" -- partial coverage

The `food-safety.md` spec covers SFA regulations well. However, the research file `02-singapore-food-waste-context.md` identifies additional Singapore-specific requirements not in any spec:

- Multi-language support (English, Mandarin, Malay) -- mentioned in platform model analysis, absent from specs
- PayNow payment method -- listed as "Phase 2" in payments spec but no deferred spec
- Hawker stall category -- no special handling in merchant experience for digital adoption barriers
- NEA mandatory food waste reporting for large merchants -- not referenced in any spec

### GAP-28: "Budget-conscious -- leverage free tiers and open-source tools" -- no infrastructure/cost spec

The brief constraint about budget is not reflected in any spec's technology choices or infrastructure decisions. There is no spec that addresses:

- Deployment architecture
- Hosting cost estimates
- Free tier limits and upgrade triggers
- Database sizing and storage planning

---

## 5. Cross-Spec Inconsistencies (MAJOR)

### GAP-29: Payment methods inconsistency between payments spec and consumer flows

The `payments.md` spec defines supported methods as: Credit/Debit Card, Apple Pay, Google Pay. PayNow is "Phase 2."

The `02-consumer-flows.md` C3 purchase flow lists: "PayNow, credit/debit card, Apple Pay, Google Pay, GrabPay."

GrabPay appears in the user flow but not in the payments spec. PayNow is listed as available in the user flow but "Phase 2" in the payments spec. This inconsistency will confuse implementers.

### GAP-30: Consumer preference quiz -- 3 questions specified differently

The `authentication.md` spec says registration includes a "preference quiz (3 questions)" but does not specify the questions.

The `consumer-experience.md` spec describes 3 screens:

1. "What do you like to eat?" -- cuisine tiles
2. "What's your budget?" -- slider S$3-S$15
3. "Any dietary needs?" -- toggle chips

The `02-consumer-flows.md` C1 flow describes 3 questions:

1. Cuisine multi-select
2. "What's your typical lunch budget?" -- slider S$3-S$15
3. Dietary preferences multi-select

The `ml-recommendations.md` spec references "onboarding quiz preferences" as an explicit signal.

The wording difference ("What's your budget" vs "What's your typical lunch budget") and format difference (toggle chips vs multi-select) creates ambiguity.

### GAP-31: Listing type_enum -- "predicted" vs "manual" but no "flash_deal" or "pre-order"

The `data-model.md` defines `listing_type` as `ENUM(predicted, manual)`. The `04-platform-model-analysis.md` research document defines 4 transaction types:

1. Direct purchase
2. Surprise bag
3. Flash deal
4. Pre-order

The `item_type` enum covers `specific` and `surprise_bag`. But "flash deal" and "pre-order" are not represented in any listing field. Are these future phases? The `marketplace.md` spec does not mention them at all.

### GAP-32: Merchant onboarding steps -- conflicting descriptions

`authentication.md` merchant registration: email, password, full_name, business_name, address, sfa_license, cuisine_types, operating_hours (one form).

`merchant-experience.md` onboarding: 6-step wizard (welcome -> business details -> category setup -> pricing setup -> tutorial -> first prediction).

`01-merchant-flows.md` M1: Landing -> Sign up -> Business details -> SFA verification -> Profile setup -> Pricing preferences -> Tutorial.

These three documents describe different step counts and ordering for the same flow. The auth spec bundles everything into one form submission, while the UX specs break it into steps.

### GAP-33: CO2 calculation methodology not specified

Multiple specs reference CO2 prevention:

- `data-model.md`: ImpactRecord has `co2_prevented_kg`
- `ml-analytics.md`: Impact tab shows CO2 metrics
- `consumer-experience.md`: Impact dashboard shows CO2

No spec defines:

- How CO2 prevented is calculated from a food order
- What conversion factors are used (kg CO2 per kg food?)
- Whether these factors differ by food category
- Source of the conversion factors

### GAP-34: Commission rate and minimum -- single mention, no detail

The `marketplace.md` spec states "Platform commission: 15% of sale price, Minimum commission: S$0.30 per transaction." The `payments.md` spec shows a breakdown example with 15% but does not mention the S$0.30 minimum.

Edge case not addressed: If a consumer buys 1 item at S$1.00, commission at 15% = S$0.15, which is below the S$0.30 minimum. Does the platform charge S$0.30 (merchant gets S$0.70) or is there a minimum listing price that prevents this?

### GAP-35: Price history "reason" enum -- incomplete

The `data-model.md` PriceHistory table has `reason VARCHAR(50) NOT NULL` with comment "time_decay, demand_drop, manual." The `pricing.md` spec describes demand modifiers (4 types) but the reason enum only covers 3 values. The pricing spec also mentions merchant manual price adjustments, which maps to "manual," but demand modifier types (high views zero purchase, rapid sell-through, etc.) are not distinguishable from the generic "demand_drop."

### GAP-36: Location -- multiple location fields with no coordination

The `data-model.md` has location data in:

- Merchant: lat/lon (business address)
- ConsumerPreference: home_lat/home_lon, work_lat/work_lon
- MLUserInteraction.context: "location context" in JSONB

The `consumer-experience.md` spec mentions "Location indicator: Near [neighborhood]" and map views.

No spec defines:

- How consumer real-time location is obtained (GPS? IP? User-set?)
- How often location is updated
- Privacy policy for location tracking
- Whether location history is stored
- What happens if location permission is denied (mentioned in consumer-experience error states but not in data model or auth specs)

---

## 6. Missing Edge Cases and Error States (SIGNIFICANT)

### GAP-37: Concurrent purchase race condition -- incomplete resolution

The `marketplace.md` spec mentions "Use database row lock on listing during quantity decrement" and "If quantity reaches 0 mid-purchase: refund and notify consumer." This is good but incomplete:

- What happens if 10 consumers purchase the last 5 items simultaneously? How many get refunds?
- What is the lock scope? Row-level SELECT FOR UPDATE on the listing?
- What happens to the Stripe PaymentIntent if the order is rejected after payment succeeds? Does the refund happen before the consumer sees confirmation?
- Timeout behavior: how long does the lock wait before failing?

### GAP-38: Listing expiry during active purchase

The `marketplace.md` spec says pickup window passing expires the listing. What if:

- A consumer is on the payment screen when the listing expires?
- The Stripe payment succeeds but by the time the callback arrives, the listing has expired?
- The listing is in "sold_out" state -- does it still expire at pickup_end?

### GAP-39: Merchant account suspension mid-transaction

The `food-safety.md` spec mentions merchant suspension for license lapse or safety violations. No spec addresses what happens to:

- Active listings when a merchant is suspended
- Pending orders for a suspended merchant
- In-progress payouts
- Whether consumers are notified

### GAP-40: Surprise bag allergen disclosure -- enforcement mechanism missing

The `food-safety.md` spec has an edge case table entry: "Surprise bag contains allergens not disclosed -> Merchant violation -> warning -> suspension on repeat." The `marketplace.md` spec says surprise bags have "category hints" but no specific item listing.

How does the system enforce allergen disclosure for surprise bags when the merchant does not know exact contents until pickup time? The spec says merchants must "declare common allergens for each category" -- but surprise bags span categories. There is no mechanism for the merchant to tag a surprise bag with allergens at listing creation time.

### GAP-41: Dynamic pricing with zero views

The `pricing.md` spec has a demand modifier: "Very low views (<5 in first hour) -> Visibility issue, don't change price." But:

- What triggers the "very low views" check? Is there a scheduled job?
- If a listing has zero views after 2 hours, does the price stay at initial level?
- How does view_count increment? Is every API GET on a listing a "view"? Is there deduplication per consumer?

The `data-model.md` Listing has a `view_count` field but no spec defines how it is incremented or deduplicated.

### GAP-42: Order cancellation window not defined

The `marketplace.md` spec says consumers can cancel "before pickup window." The `authentication.md` RBAC confirms "Consumer (before pickup)." But:

- Can a consumer cancel after the merchant has marked the order as "preparing" or "ready"?
- Is there a cutoff time (e.g., must cancel at least 1 hour before pickup starts)?
- What happens if the consumer cancels after the merchant has already prepared the food?
- Is there a cancellation fee or limit on cancellations?

### GAP-43: Refund timing and partial refund scenarios

The `payments.md` spec says "Full refund" for consumer cancellation or expired pickup. It says "Partial refund: Not supported in MVP." But:

- What if only some items in an order are unavailable? (The order is for quantity > 1 of the same item.)
- What if the merchant gives the wrong items?
- What if the consumer collects but the food quality is poor -- is that a refund or a food safety complaint?

### GAP-44: ML model cold start with zero merchants

The `ml-surplus-prediction.md` spec handles new-merchant cold start well. But:

- What happens on day 1 of the platform when there are zero merchants, zero transactions, and zero historical data?
- The "category-level averages" require at least some platform data. Where do initial category averages come from?
- Is there a bootstrap data import from the Singapore research benchmarks?

---

## 7. Internal Consistency Issues (SIGNIFICANT)

### GAP-45: Merchant rating update trigger not specified

The `data-model.md` Merchant entity has `avg_rating DECIMAL(3,2)` and `review_count INTEGER` as cached fields. The `marketplace.md` spec has review endpoints. No spec defines:

- When these cached fields are updated (trigger? application-level on review create?)
- Whether they update on review edit
- What happens to avg_rating if a review is deleted (not mentioned as a feature but implied by PATCH endpoint)

### GAP-46: "For You" feed -- consumer-experience vs ml-recommendations naming

The `consumer-experience.md` spec describes feed sections as: For You, Nearby, Expiring Soon, Best Value, Surprise Bags, and "Popular This Week."

The `marketplace.md` spec describes feed sections as: For You, Nearby, Expiring Soon, Best Value, Surprise Bags.

The `ml-recommendations.md` spec describes feed sections as: For You, Nearby, Expiring Soon, Best Value, Surprise Bags.

"Popular This Week" appears only in the consumer-experience spec. Is this a sixth section or a replacement for one of the others?

### GAP-47: Merchant total_meals_rescued and total_revenue_recovered -- update triggers

The Merchant entity has `total_meals_rescued INTEGER` and `total_revenue_recovered DECIMAL(10,2)`. No spec defines when and how these are updated:

- On order collection? On order placement?
- Batch update? Real-time?
- What happens on refund -- are these decremented?

### GAP-48: "first-purchase incentive" in user flow -- not in any spec

The `02-consumer-flows.md` C1 mentions: "First-purchase incentive: 'Get S$3 off your first order!'" This promotional feature appears in no spec file. It implies:

- A coupon/promotion system
- Balance tracking for the incentive
- Conditions and expiration

---

## 8. Completeness Assessment: Brief Objectives to Specs

| Brief Objective                                              | Covered by Spec                                                | Coverage    |
| ------------------------------------------------------------ | -------------------------------------------------------------- | ----------- |
| Reduce food waste by enabling merchants to sell surplus food | marketplace.md, merchant-experience.md, consumer-experience.md | Full        |
| Provide consumers access to quality food at reduced prices   | marketplace.md, consumer-experience.md, pricing.md             | Full        |
| ML to predict surplus                                        | ml-surplus-prediction.md                                       | Full        |
| ML to personalize recommendations                            | ml-recommendations.md                                          | Full        |
| ML to optimize dynamic pricing                               | pricing.md                                                     | Full        |
| ML to provide waste analytics                                | ml-analytics.md                                                | Full        |
| Explore commercial viability                                 | No dedicated spec                                              | **Missing** |
| Deliver working prototype for SMU MBA ML project             | No demo/test spec                                              | **Partial** |
| Singapore market focus                                       | food-safety.md, partial in others                              | **Partial** |
| Two-sided marketplace flows                                  | marketplace.md, both experience specs                          | Full        |
| Budget-conscious tech choices                                | No infrastructure spec                                         | **Missing** |

---

## 9. Completeness Assessment: User Flows to Specs

| User Flow                     | Spec Coverage                                                    | Gaps                                        |
| ----------------------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| M1: Merchant Onboarding       | authentication.md, merchant-experience.md                        | Step count conflict (GAP-32)                |
| M2: Daily Surplus Listing     | ml-surplus-prediction.md, merchant-experience.md, marketplace.md | Full                                        |
| M3: Manual Listing            | marketplace.md, merchant-experience.md                           | Full                                        |
| M4: Waste Analytics Dashboard | ml-analytics.md, merchant-experience.md                          | Full                                        |
| M5: Pricing Management        | pricing.md, merchant-experience.md                               | Full                                        |
| M6: Order Management          | marketplace.md, merchant-experience.md, payments.md              | Full                                        |
| M7: Settings and Profile      | merchant-experience.md                                           | No API spec for merchant settings endpoints |
| C1: Consumer Onboarding       | authentication.md, consumer-experience.md                        | Quiz detail conflict (GAP-30)               |
| C2: Deal Discovery            | marketplace.md, consumer-experience.md, ml-recommendations.md    | Full                                        |
| C3: Purchase Flow             | marketplace.md, payments.md, consumer-experience.md              | Payment method conflict (GAP-29)            |
| C4: Search and Discovery      | marketplace.md                                                   | Full-text search unspecified (GAP-16)       |
| C5: Notifications             | notifications.md                                                 | Missing data model (GAP-01)                 |
| C6: Profile and Impact        | consumer-experience.md                                           | Badge data model missing (GAP-06)           |
| C7: Surprise Bag Flow         | marketplace.md (item_type)                                       | Allergen enforcement gap (GAP-40)           |
| C8: Social Features           | Not spec'd (marked Phase 2)                                      | Acceptable deferral                         |

---

## 10. Recommendations

### Must Fix Before `/todos`

1. **Resolve GAP-01 through GAP-07**: Add missing tables to `data-model.md` or create a `data-model-extended.md` for Phase 2 entities.
2. **Resolve GAP-08, GAP-12**: Reconcile API path/method conflicts between specs and research documents.
3. **Resolve GAP-17, GAP-18**: Define standard error response format and pagination contract -- these are cross-cutting concerns that affect every endpoint.
4. **Resolve GAP-29**: Pick one source of truth for payment methods and update all other documents.

### Should Fix Before `/implement`

5. **Resolve GAP-22**: Specify the background task framework (even if just "APScheduler with PostgreSQL job store").
6. **Resolve GAP-37, GAP-38**: Add concrete concurrent operation handling -- row-level locking strategy, timeout values, and the exact sequence of payment-then-quantity-check vs. quantity-check-then-payment.
7. **Resolve GAP-26**: Add at minimum a stub `admin-experience.md` with the admin's key workflows.
8. **Resolve GAP-15**: Add image storage decisions (even if "local filesystem for MVP, S3 later").

### Can Defer to Implementation

9. GAP-21 (PostGIS decision), GAP-23 (seed data), GAP-24 (business metrics dashboard), GAP-28 (cost planning).
10. GAP-44 (day-1 cold start) -- resolve during demo preparation.

---

## Risk Register

| ID     | Gap                         | Likelihood of Bug | Impact If Unresolved                 | Severity    |
| ------ | --------------------------- | ----------------- | ------------------------------------ | ----------- |
| GAP-01 | Notification tables missing | High              | Implementer builds wrong schema      | Critical    |
| GAP-08 | API method/path conflict    | High              | Two implementations built            | Critical    |
| GAP-12 | Order status enum mismatch  | High              | State machine broken                 | Critical    |
| GAP-17 | No error response format    | High              | Inconsistent API, frontend breaks    | Major       |
| GAP-18 | No pagination spec          | High              | Performance issues, frontend breaks  | Major       |
| GAP-29 | Payment methods conflict    | Medium            | Wrong payment UI built               | Major       |
| GAP-37 | Concurrent purchase race    | Medium            | Lost sales, double charges           | Major       |
| GAP-02 | No bookmark/listing save    | Low               | Price drop notifications impossible  | Significant |
| GAP-06 | No badge tables             | Low               | Gamification feature cannot be built | Significant |
| GAP-32 | Onboarding step conflict    | Low               | Confusing implementation             | Significant |
