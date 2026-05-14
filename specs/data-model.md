# Data Model Specification

> **Phase 2 — Not part of final submitted MVP.** The data model covers a full marketplace (consumer, merchant, order, payment entities). The submitted MVP uses a simplified in-memory data model documented in `src/` modules.

## Entity Relationship Overview

```
User ─┬─> Merchant ─┬─> MerchantCategory
      │             ├─> Listing ─┬─> Order ──> Review
      │             │             ├─> PriceHistory
      │             │             └─> SavedListing
      │             ├─> MerchantPayout
      │             ├─> MerchantBankAccount
      │             └─> MLSurplusPrediction
      │
      └─> Consumer ──> ConsumerPreference
                   ├─> SavedMerchant
                   ├─> SavedListing
                   ├─> ImpactRecord
                   ├─> UserBadge ──> Badge
                   └─> MLUserInteraction

User ──> Notification
User ──> NotificationPreference
User ──> FCMToken
```

## Entities

### User

Base identity for all platform users.

| Field          | Type                            | Constraints                | Description                             |
| -------------- | ------------------------------- | -------------------------- | --------------------------------------- |
| id             | UUID                            | PK                         | Unique user identifier                  |
| email          | VARCHAR(255)                    | UNIQUE, NOT NULL           | Login email                             |
| password_hash  | VARCHAR(255)                    | NOT NULL                   | bcrypt hashed password                  |
| full_name      | VARCHAR(100)                    | NOT NULL                   | Display name                            |
| phone          | VARCHAR(20)                     | NULLABLE                   | Optional phone for pickup notifications |
| role           | ENUM(merchant, consumer, admin) | NOT NULL, DEFAULT consumer | User role                               |
| oauth_provider | VARCHAR(50)                     | NULLABLE                   | Google, Apple, or NULL                  |
| oauth_id       | VARCHAR(255)                    | NULLABLE                   | Provider-specific ID                    |
| created_at     | TIMESTAMP                       | NOT NULL, DEFAULT NOW()    | Registration timestamp                  |
| updated_at     | TIMESTAMP                       | NOT NULL                   | Last profile update                     |
| is_active      | BOOLEAN                         | NOT NULL, DEFAULT TRUE     | Account status                          |
| last_login     | TIMESTAMP                       | NULLABLE                   | Last login time                         |

**Indexes**: `idx_user_email` (unique), `idx_user_role`

### Merchant

Business profile for food establishments.

| Field                   | Type          | Constraints             | Description                                                      |
| ----------------------- | ------------- | ----------------------- | ---------------------------------------------------------------- |
| id                      | UUID          | PK                      | Unique merchant identifier                                       |
| user_id                 | UUID          | FK → User.id, UNIQUE    | Link to user account                                             |
| business_name           | VARCHAR(200)  | NOT NULL                | Business display name                                            |
| description             | TEXT          | NULLABLE                | Business description                                             |
| address                 | VARCHAR(500)  | NOT NULL                | Physical address                                                 |
| latitude                | DECIMAL(9,6)  | NOT NULL                | GPS latitude                                                     |
| longitude               | DECIMAL(9,6)  | NOT NULL                | GPS longitude                                                    |
| cuisine_types           | VARCHAR[]     | NOT NULL                | Array of cuisine tags                                            |
| operating_hours         | JSONB         | NOT NULL                | Daily hours: `{"mon": {"open": "08:00", "close": "22:00"}, ...}` |
| sfa_license             | VARCHAR(100)  | NOT NULL                | SFA food establishment license number                            |
| sfa_verified            | BOOLEAN       | NOT NULL, DEFAULT FALSE | License verification status                                      |
| logo_url                | VARCHAR(500)  | NULLABLE                | Business logo image URL                                          |
| dietary_tags            | VARCHAR[]     | DEFAULT '{}'            | Halal, vegetarian, vegan, etc.                                   |
| avg_rating              | DECIMAL(3,2)  | DEFAULT 0.00            | Cached average rating                                            |
| review_count            | INTEGER       | DEFAULT 0               | Cached review count                                              |
| total_meals_rescued     | INTEGER       | DEFAULT 0               | Cumulative meals sold                                            |
| total_revenue_recovered | DECIMAL(10,2) | DEFAULT 0.00            | Cumulative revenue from platform                                 |
| is_active               | BOOLEAN       | NOT NULL, DEFAULT TRUE  | Merchant can be deactivated                                      |
| created_at              | TIMESTAMP     | NOT NULL, DEFAULT NOW() | Registration timestamp                                           |
| updated_at              | TIMESTAMP     | NOT NULL                | Last profile update                                              |

**Indexes**: `idx_merchant_location` (GiST index on lat/lon), `idx_merchant_cuisine` (GIN index on cuisine_types), `idx_merchant_active`

### MerchantCategory

Food categories a merchant can list.

| Field                | Type         | Constraints      | Description                      |
| -------------------- | ------------ | ---------------- | -------------------------------- |
| id                   | UUID         | PK               | Unique identifier                |
| merchant_id          | UUID         | FK → Merchant.id | Owning merchant                  |
| category_name        | VARCHAR(100) | NOT NULL         | e.g., "Pastries", "Chicken Rice" |
| default_quantity     | INTEGER      | NOT NULL         | Typical surplus quantity         |
| original_price       | DECIMAL(6,2) | NOT NULL         | Full retail price                |
| min_price            | DECIMAL(6,2) | NOT NULL         | Price floor (merchant set)       |
| default_discount_pct | DECIMAL(5,2) | NOT NULL         | Default discount percentage      |
| shelf_life_hours     | INTEGER      | NOT NULL         | Hours item remains safe to sell  |
| is_active            | BOOLEAN      | DEFAULT TRUE     | Category enabled/disabled        |
| created_at           | TIMESTAMP    | NOT NULL         | Creation timestamp               |

**Indexes**: `idx_merchant_cat_merchant`, unique constraint on (merchant_id, category_name)

### Listing

A surplus food item available for purchase.

| Field                 | Type                                              | Constraints                | Description                                |
| --------------------- | ------------------------------------------------- | -------------------------- | ------------------------------------------ |
| id                    | UUID                                              | PK                         | Unique listing identifier                  |
| merchant_id           | UUID                                              | FK → Merchant.id, NOT NULL | Owning merchant                            |
| category_id           | UUID                                              | FK → MerchantCategory.id   | Reference category                         |
| title                 | VARCHAR(200)                                      | NOT NULL                   | Listing title                              |
| description           | TEXT                                              | NULLABLE                   | Item description                           |
| item_type             | ENUM(specific, surprise_bag)                      | NOT NULL, DEFAULT specific | Known items or mystery bag                 |
| original_price        | DECIMAL(6,2)                                      | NOT NULL                   | Original retail price                      |
| current_price         | DECIMAL(6,2)                                      | NOT NULL                   | Current dynamic price                      |
| min_price             | DECIMAL(6,2)                                      | NOT NULL                   | Price floor                                |
| quantity_total        | INTEGER                                           | NOT NULL                   | Total items available                      |
| quantity_remaining    | INTEGER                                           | NOT NULL                   | Items still available                      |
| pickup_start          | TIMESTAMP                                         | NOT NULL                   | Pickup window start                        |
| pickup_end            | TIMESTAMP                                         | NOT NULL                   | Pickup window end                          |
| listing_type          | ENUM(predicted, manual)                           | NOT NULL                   | Auto-predicted or manually created         |
| prediction_confidence | DECIMAL(3,2)                                      | NULLABLE                   | ML confidence (0-1) for predicted listings |
| status                | ENUM(draft, active, sold_out, expired, cancelled) | NOT NULL, DEFAULT draft    | Listing lifecycle                          |
| dietary_tags          | VARCHAR[]                                         | DEFAULT '{}'               | Inherited from category/merchant           |
| image_urls            | VARCHAR[]                                         | DEFAULT '{}'               | Listing photos                             |
| view_count            | INTEGER                                           | DEFAULT 0                  | Number of consumer views                   |
| created_at            | TIMESTAMP                                         | NOT NULL                   | Listing creation time                      |
| updated_at            | TIMESTAMP                                         | NOT NULL                   | Last price/status update                   |
| expires_at            | TIMESTAMP                                         | NOT NULL                   | When listing becomes invalid               |

**Indexes**: `idx_listing_status`, `idx_listing_pickup_time`, `idx_listing_merchant`, `idx_listing_location` (join with merchant GiST)

### PriceHistory

Tracks dynamic price changes for a listing.

| Field      | Type         | Constraints               | Description                     |
| ---------- | ------------ | ------------------------- | ------------------------------- |
| id         | UUID         | PK                        | Unique identifier               |
| listing_id | UUID         | FK → Listing.id, NOT NULL | Associated listing              |
| old_price  | DECIMAL(6,2) | NOT NULL                  | Previous price                  |
| new_price  | DECIMAL(6,2) | NOT NULL                  | Updated price                   |
| reason     | VARCHAR(50)  | NOT NULL                  | time_decay, demand_drop, manual |
| created_at | TIMESTAMP    | NOT NULL, DEFAULT NOW()   | Price change timestamp          |

**Indexes**: `idx_price_history_listing`

### Order

A consumer purchase of a listing.

| Field           | Type                                                                    | Constraints                | Description                        |
| --------------- | ----------------------------------------------------------------------- | -------------------------- | ---------------------------------- |
| id              | UUID                                                                    | PK                         | Unique order identifier            |
| consumer_id     | UUID                                                                    | FK → User.id, NOT NULL     | Purchasing consumer                |
| listing_id      | UUID                                                                    | FK → Listing.id, NOT NULL  | Purchased listing                  |
| merchant_id     | UUID                                                                    | FK → Merchant.id, NOT NULL | Fulfilling merchant                |
| quantity        | INTEGER                                                                 | NOT NULL, CHECK > 0        | Number of items                    |
| unit_price      | DECIMAL(6,2)                                                            | NOT NULL                   | Price per unit at purchase time    |
| total_amount    | DECIMAL(6,2)                                                            | NOT NULL                   | Total charged                      |
| platform_fee    | DECIMAL(6,2)                                                            | NOT NULL                   | Commission charged                 |
| merchant_payout | DECIMAL(6,2)                                                            | NOT NULL                   | Amount to merchant                 |
| status          | ENUM(placed, preparing, ready, collected, expired, cancelled, refunded) | NOT NULL, DEFAULT placed   | Order lifecycle                    |
| payment_method  | VARCHAR(50)                                                             | NOT NULL                   | stripe_card, stripe_applepay, etc. |
| payment_id      | VARCHAR(255)                                                            | NOT NULL                   | External payment reference         |
| qr_code         | VARCHAR(500)                                                            | NOT NULL                   | QR code data for pickup            |
| pickup_start    | TIMESTAMP                                                               | NOT NULL                   | Pickup window start (snapshot)     |
| pickup_end      | TIMESTAMP                                                               | NOT NULL                   | Pickup window end (snapshot)       |
| collected_at    | TIMESTAMP                                                               | NULLABLE                   | When consumer collected            |
| created_at      | TIMESTAMP                                                               | NOT NULL                   | Order creation time                |
| updated_at      | TIMESTAMP                                                               | NOT NULL                   | Last status change                 |

**Indexes**: `idx_order_consumer`, `idx_order_merchant`, `idx_order_status`, `idx_order_created`

### Review

Consumer rating and feedback after order completion.

| Field       | Type      | Constraints                | Description                                    |
| ----------- | --------- | -------------------------- | ---------------------------------------------- |
| id          | UUID      | PK                         | Unique identifier                              |
| order_id    | UUID      | FK → Order.id, UNIQUE      | One review per order                           |
| consumer_id | UUID      | FK → User.id, NOT NULL     | Reviewing consumer                             |
| merchant_id | UUID      | FK → Merchant.id, NOT NULL | Reviewed merchant                              |
| rating      | INTEGER   | NOT NULL, CHECK 1-5        | Star rating                                    |
| review_text | TEXT      | NULLABLE                   | Written review                                 |
| tags        | VARCHAR[] | DEFAULT '{}'               | Quick tags: great_value, fresh, friendly, etc. |
| created_at  | TIMESTAMP | NOT NULL                   | Review timestamp                               |

**Indexes**: `idx_review_merchant`, `idx_review_consumer`

### ConsumerPreference

Stored consumer preferences for recommendation engine.

| Field                | Type         | Constraints          | Description                  |
| -------------------- | ------------ | -------------------- | ---------------------------- |
| id                   | UUID         | PK                   | Unique identifier            |
| consumer_id          | UUID         | FK → User.id, UNIQUE | Owning consumer              |
| preferred_cuisines   | VARCHAR[]    | DEFAULT '{}'         | Selected cuisine preferences |
| dietary_tags         | VARCHAR[]    | DEFAULT '{}'         | Dietary restrictions         |
| budget_max           | DECIMAL(6,2) | NULLABLE             | Maximum preferred meal price |
| home_lat             | DECIMAL(9,6) | NULLABLE             | Home location latitude       |
| home_lon             | DECIMAL(9,6) | NULLABLE             | Home location longitude      |
| work_lat             | DECIMAL(9,6) | NULLABLE             | Work location latitude       |
| work_lon             | DECIMAL(9,6) | NULLABLE             | Work location longitude      |
| notification_enabled | BOOLEAN      | DEFAULT TRUE         | Push notifications on/off    |
| created_at           | TIMESTAMP    | NOT NULL             | Creation timestamp           |
| updated_at           | TIMESTAMP    | NOT NULL             | Last update                  |

### SavedMerchant

Consumer's favorite merchants for notifications.

| Field       | Type      | Constraints      | Description       |
| ----------- | --------- | ---------------- | ----------------- |
| id          | UUID      | PK               | Unique identifier |
| consumer_id | UUID      | FK → User.id     | Saving consumer   |
| merchant_id | UUID      | FK → Merchant.id | Saved merchant    |
| created_at  | TIMESTAMP | NOT NULL         | When saved        |

**Unique constraint**: (consumer_id, merchant_id)

### ImpactRecord

Tracks sustainability impact per user for gamification.

| Field            | Type         | Constraints         | Description                    |
| ---------------- | ------------ | ------------------- | ------------------------------ |
| id               | UUID         | PK                  | Unique identifier              |
| user_id          | UUID         | FK → User.id        | User who made impact           |
| order_id         | UUID         | FK → Order.id       | Associated order               |
| meals_rescued    | INTEGER      | NOT NULL, DEFAULT 1 | Meals rescued count            |
| co2_prevented_kg | DECIMAL(8,2) | NOT NULL            | CO2 prevented in kg            |
| money_saved      | DECIMAL(6,2) | NOT NULL            | Money saved vs. original price |
| food_weight_kg   | DECIMAL(6,2) | NOT NULL            | Weight of food rescued         |
| created_at       | TIMESTAMP    | NOT NULL            | Impact timestamp               |

**Indexes**: `idx_impact_user`, `idx_impact_created`

### Notification

Stores in-app and push notifications for users.

| Field      | Type         | Constraints             | Description                                                         |
| ---------- | ------------ | ----------------------- | ------------------------------------------------------------------- |
| id         | UUID         | PK                      | Unique identifier                                                   |
| user_id    | UUID         | FK → User.id, NOT NULL  | Recipient user                                                      |
| type       | VARCHAR(50)  | NOT NULL                | Notification type (morning_prediction, new_order, price_drop, etc.) |
| title      | VARCHAR(200) | NOT NULL                | Notification title                                                  |
| body       | TEXT         | NOT NULL                | Notification body text                                              |
| data       | JSONB        | DEFAULT '{}'            | Deep link target, listing_id, order_id, etc.                        |
| is_read    | BOOLEAN      | NOT NULL, DEFAULT FALSE | Read status                                                         |
| created_at | TIMESTAMP    | NOT NULL, DEFAULT NOW() | Creation timestamp                                                  |
| expires_at | TIMESTAMP    | NOT NULL                | Auto-delete after 30 days                                           |

**Indexes**: `idx_notification_user_unread` (user_id, is_read), `idx_notification_expires`

### NotificationPreference

Per-user notification settings.

| Field             | Type      | Constraints          | Description                         |
| ----------------- | --------- | -------------------- | ----------------------------------- |
| id                | UUID      | PK                   | Unique identifier                   |
| user_id           | UUID      | FK → User.id, UNIQUE | Owning user                         |
| deal_alerts       | BOOLEAN   | DEFAULT TRUE         | New deal notifications              |
| price_drop_alerts | BOOLEAN   | DEFAULT TRUE         | Bookmarked listing price drops      |
| pickup_reminders  | BOOLEAN   | DEFAULT TRUE         | Order pickup reminders              |
| daily_summary     | BOOLEAN   | DEFAULT TRUE         | End-of-day merchant summary         |
| weekly_digest     | BOOLEAN   | DEFAULT TRUE         | Weekly consumer digest              |
| impact_milestones | BOOLEAN   | DEFAULT TRUE         | Badge/impact notifications          |
| quiet_hours_start | TIME      | DEFAULT '22:00'      | No non-critical notifications after |
| quiet_hours_end   | TIME      | DEFAULT '08:00'      | Resume notifications at             |
| max_daily         | INTEGER   | DEFAULT 5            | Max non-order notifications per day |
| updated_at        | TIMESTAMP | NOT NULL             | Last update                         |

### FCMToken

Firebase Cloud Messaging tokens for push notifications.

| Field         | Type         | Constraints             | Description                 |
| ------------- | ------------ | ----------------------- | --------------------------- |
| id            | UUID         | PK                      | Unique identifier           |
| user_id       | UUID         | FK → User.id, NOT NULL  | Owning user                 |
| token         | VARCHAR(500) | NOT NULL                | FCM registration token      |
| platform      | VARCHAR(20)  | NOT NULL                | ios, android, web           |
| device_id     | VARCHAR(200) | NULLABLE                | Device identifier for dedup |
| registered_at | TIMESTAMP    | NOT NULL, DEFAULT NOW() | Registration timestamp      |

**Indexes**: `idx_fcm_user`, unique on (user_id, token)

### SavedListing

Consumer bookmarked/watched listings for price drop alerts.

| Field       | Type      | Constraints               | Description       |
| ----------- | --------- | ------------------------- | ----------------- |
| id          | UUID      | PK                        | Unique identifier |
| consumer_id | UUID      | FK → User.id, NOT NULL    | Saving consumer   |
| listing_id  | UUID      | FK → Listing.id, NOT NULL | Saved listing     |
| created_at  | TIMESTAMP | NOT NULL                  | When saved        |

**Unique constraint**: (consumer_id, listing_id)
**Indexes**: `idx_saved_listing_consumer`, `idx_saved_listing_listing`

### MerchantPayout

Tracks weekly payout records for merchants.

| Field             | Type                                    | Constraints                | Description                  |
| ----------------- | --------------------------------------- | -------------------------- | ---------------------------- |
| id                | UUID                                    | PK                         | Unique identifier            |
| merchant_id       | UUID                                    | FK → Merchant.id, NOT NULL | Receiving merchant           |
| period_start      | DATE                                    | NOT NULL                   | Payout period start (Monday) |
| period_end        | DATE                                    | NOT NULL                   | Payout period end (Sunday)   |
| gross_amount      | DECIMAL(10,2)                           | NOT NULL                   | Total before refunds         |
| refund_deductions | DECIMAL(10,2)                           | NOT NULL, DEFAULT 0        | Refunds in period            |
| platform_fees     | DECIMAL(10,2)                           | NOT NULL                   | Total commission             |
| net_amount        | DECIMAL(10,2)                           | NOT NULL                   | Amount to be paid out        |
| status            | ENUM(pending, processing, paid, failed) | NOT NULL, DEFAULT pending  | Payout status                |
| stripe_payout_id  | VARCHAR(255)                            | NULLABLE                   | Stripe payout reference      |
| paid_at           | TIMESTAMP                               | NULLABLE                   | When payout completed        |
| created_at        | TIMESTAMP                               | NOT NULL                   | Record creation              |

**Indexes**: `idx_payout_merchant`, `idx_payout_status`, unique on (merchant_id, period_start)

### MerchantBankAccount

Merchant bank details for payouts.

| Field                    | Type         | Constraints              | Description                  |
| ------------------------ | ------------ | ------------------------ | ---------------------------- |
| id                       | UUID         | PK                       | Unique identifier            |
| merchant_id              | UUID         | FK → Merchant.id, UNIQUE | Owning merchant              |
| bank_name                | VARCHAR(100) | NOT NULL                 | Bank name (e.g., DBS, OCBC)  |
| bank_code                | VARCHAR(20)  | NOT NULL                 | Singapore bank code          |
| account_number_encrypted | VARCHAR(255) | NOT NULL                 | AES-encrypted account number |
| account_holder_name      | VARCHAR(200) | NOT NULL                 | Account holder name          |
| is_verified              | BOOLEAN      | DEFAULT FALSE            | Verification status          |
| created_at               | TIMESTAMP    | NOT NULL                 | Creation timestamp           |
| updated_at               | TIMESTAMP    | NOT NULL                 | Last update                  |

### Badge

Achievement badge definitions for gamification.

| Field           | Type                                                                 | Constraints      | Description                         |
| --------------- | -------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| id              | UUID                                                                 | PK               | Unique identifier                   |
| name            | VARCHAR(50)                                                          | UNIQUE, NOT NULL | Badge name (e.g., first_rescue)     |
| display_name    | VARCHAR(100)                                                         | NOT NULL         | Display name (e.g., "First Rescue") |
| description     | TEXT                                                                 | NOT NULL         | What earns this badge               |
| icon_url        | VARCHAR(500)                                                         | NOT NULL         | Badge icon image                    |
| threshold_type  | ENUM(meals_rescued, merchants_visited, cuisines_tried, streak_weeks) | NOT NULL         | What metric to track                |
| threshold_value | INTEGER                                                              | NOT NULL         | Value needed to earn                |
| created_at      | TIMESTAMP                                                            | NOT NULL         | Creation timestamp                  |

### UserBadge

User's earned badges and progress.

| Field     | Type      | Constraints             | Description                                |
| --------- | --------- | ----------------------- | ------------------------------------------ |
| id        | UUID      | PK                      | Unique identifier                          |
| user_id   | UUID      | FK → User.id, NOT NULL  | Owning user                                |
| badge_id  | UUID      | FK → Badge.id, NOT NULL | Badge definition                           |
| progress  | INTEGER   | NOT NULL, DEFAULT 0     | Current progress toward threshold          |
| earned_at | TIMESTAMP | NULLABLE                | When badge was earned (NULL = in progress) |

**Unique constraint**: (user_id, badge_id)
**Indexes**: `idx_user_badge_user`, `idx_user_badge_earned`

### MLSurplusPrediction

Stores ML surplus predictions for merchants.

| Field             | Type         | Constraints              | Description                        |
| ----------------- | ------------ | ------------------------ | ---------------------------------- |
| id                | UUID         | PK                       | Unique identifier                  |
| merchant_id       | UUID         | FK → Merchant.id         | Predicted merchant                 |
| category_id       | UUID         | FK → MerchantCategory.id | Predicted category                 |
| prediction_date   | DATE         | NOT NULL                 | Date being predicted               |
| predicted_surplus | INTEGER      | NOT NULL                 | Predicted surplus units            |
| confidence        | DECIMAL(3,2) | NOT NULL                 | Prediction confidence (0-1)        |
| suggested_price   | DECIMAL(6,2) | NOT NULL                 | Suggested discount price           |
| actual_surplus    | INTEGER      | NULLABLE                 | Actual surplus (filled end-of-day) |
| model_version     | VARCHAR(50)  | NOT NULL                 | Model that generated prediction    |
| created_at        | TIMESTAMP    | NOT NULL                 | Prediction creation time           |

**Indexes**: `idx_prediction_merchant_date`, unique on (merchant_id, category_id, prediction_date)

### MLUserInteraction

Tracks user interactions for recommendation model training.

| Field              | Type                                    | Constraints     | Description                     |
| ------------------ | --------------------------------------- | --------------- | ------------------------------- |
| id                 | UUID                                    | PK              | Unique identifier               |
| consumer_id        | UUID                                    | FK → User.id    | Interacting consumer            |
| listing_id         | UUID                                    | FK → Listing.id | Viewed/clicked listing          |
| interaction_type   | ENUM(view, click, purchase, skip, rate) | NOT NULL        | Type of interaction             |
| dwell_time_seconds | INTEGER                                 | NULLABLE        | Time spent on listing detail    |
| position_in_feed   | INTEGER                                 | NULLABLE        | Position when shown             |
| context            | JSONB                                   | DEFAULT '{}'    | Time, weather, location context |
| created_at         | TIMESTAMP                               | NOT NULL        | Interaction timestamp           |

**Indexes**: `idx_interaction_consumer`, `idx_interaction_listing`, `idx_interaction_type`, `idx_interaction_created`

## Enumeration Values

### UserRole

- `merchant` — F&B business owner/manager
- `consumer` — Deal-seeking diner
- `admin` — Platform administrator

### ListingStatus

- `draft` — Created but not yet published
- `active` — Live and available for purchase
- `sold_out` — All items purchased
- `expired` — Pickup window passed
- `cancelled` — Merchant cancelled listing

### OrderStatus

- `placed` — Consumer purchased, awaiting pickup window
- `preparing` — Merchant acknowledged, preparing order
- `ready` — Order ready for collection
- `collected` — Consumer collected (QR scanned)
- `expired` — Pickup window passed without collection
- `cancelled` — Order cancelled before pickup
- `refunded` — Payment refunded

### ItemType

- `specific` — Known items listed individually
- `surprise_bag` — Mystery bag curated by merchant

### InteractionType

- `view` — Listing appeared in feed
- `click` — Consumer tapped to view details
- `purchase` — Consumer bought the item
- `skip` — Consumer scrolled past
- `rate` — Consumer rated after purchase
