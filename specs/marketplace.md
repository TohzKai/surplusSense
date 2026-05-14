# Marketplace Specification

> **Phase 2 — Not part of final submitted MVP.** The consumer marketplace is a Phase 2 extension. The submitted MVP is the merchant-side decision cockpit only. See `grading-self-assessment-v6-final.md` for the final MVP scope.

## Overview

The marketplace connects merchant surplus listings with consumer demand. Core flows: listing creation (predicted and manual), search and discovery, purchase, and fulfillment.

## Listing Lifecycle

```
draft → active → sold_out
                → expired
                → cancelled
```

### Draft

- Created by merchant or auto-generated from ML prediction
- Not visible to consumers
- Merchant reviews and publishes

### Active

- Visible in consumer feed
- Dynamic pricing in effect
- Consumers can purchase
- Price may decrease over time per price curve

### Sold Out

- All items purchased
- No longer visible in feed
- Pending orders still valid for pickup

### Expired

- Pickup window passed
- Unsold items marked expired
- No further purchases possible
- Actual surplus recorded for ML training

### Cancelled

- Merchant cancels before any purchases
- Existing orders refunded
- Reason logged for analytics

## Listing Creation

### ML-Predicted Listing

1. Nightly batch job generates predictions for each active merchant
2. Prediction stored in MLSurplusPrediction table
3. Morning (merchant's local time): prediction notification sent
4. Merchant reviews in dashboard: sees category, predicted quantity, suggested price, confidence
5. Merchant actions per prediction:
   - **Accept**: Draft listing auto-created and published
   - **Adjust**: Modify quantity or price, then publish
   - **Reject**: Dismiss prediction, no listing created
   - **Snooze**: Reminder sent later in the day

### Manual Listing

1. Merchant navigates to "Create Listing" in dashboard
2. Selects category from MerchantCategory list
3. Sets quantity, price (within floor/ceiling bounds), pickup window
4. Optionally adds description, photos
5. Publishes → goes active immediately

## Search and Discovery

### Consumer Feed Algorithm

Deals ranked by ML recommendation score, combining:

- Content relevance (cuisine match, dietary match, price match)
- Collaborative signal (similar users purchased)
- Contextual relevance (time of day, weather, location proximity)
- Listing urgency (time remaining, quantity low)
- Quality signal (merchant rating, review count)

Feed sections:

1. **For You**: Personalized ML ranking
2. **Nearby**: Distance-sorted within configurable radius
3. **Expiring Soon**: Sorted by time remaining (ascending)
4. **Best Value**: Sorted by discount percentage (descending)
5. **Surprise Bags**: Filtered to surprise_bag type only

### Filters

- Cuisine type (multi-select)
- Price range (slider: S$0-S$15)
- Distance (500m, 1km, 3km, 5km, 10km)
- Dietary tags (halal, vegetarian, vegan, gluten-free)
- Pickup time (now, lunch 11am-2pm, dinner 5-9pm, late night)
- Rating (4+ stars)

### Search

- Full-text search on listing title, description, merchant name
- Ranked by relevance + personalization score
- Autocomplete suggestions from popular queries

## Purchase Flow

### Pre-Purchase Validation

1. Listing is active and not expired
2. Quantity remaining >= requested quantity
3. Pickup window has not closed
4. Consumer does not already have active order for this listing (prevent double-purchase)

### Purchase Steps

1. Consumer taps "Buy" on listing detail
2. Order summary shown: items, price, pickup window, merchant location
3. Payment method selection
4. Payment processed via Stripe
5. Order created with status=placed
6. Listing quantity_remaining decremented
7. QR code generated for pickup
8. Consumer sees confirmation with QR code and directions

### Concurrent Purchase Handling

- Use database row lock on listing during quantity decrement
- If quantity reaches 0 mid-purchase: refund and notify consumer ("Sorry, this deal just sold out")

### Order Status Machine

```
placed → preparing (merchant acknowledges)
       → ready (merchant marks ready)
       → collected (QR scanned) ← terminal state
       → expired (pickup window passed) → refunded ← terminal
       → cancelled (before pickup window) → refunded ← terminal
```

## Pickup Flow

1. Consumer arrives at merchant during pickup window
2. Shows QR code on phone
3. Merchant scans QR (or manually enters order ID)
4. System verifies: order is placed/ready, pickup window is active, correct merchant
5. Order status → collected
6. Consumer and merchant both see confirmation
7. Rating prompt sent to consumer (30 min later)

### Expired Pickup

- If pickup window closes without collection: order → expired
- Automatic refund initiated
- Merchant and consumer both notified

## Commission and Payouts

### Commission Structure

- Platform commission: 15% of sale price
- Merchant receives 85% of sale price
- Minimum commission: S$0.30 per transaction

### Payout

- Payouts accumulated and settled weekly (Monday for previous week)
- Merchant can view pending payout balance in dashboard
- Payout via Stripe Connect (or bank transfer for MVP)
- Payout history available in merchant settings

## API Endpoints

### Listings

| Method | Path                    | Description            | Auth                               |
| ------ | ----------------------- | ---------------------- | ---------------------------------- |
| GET    | /api/v1/listings        | Search/browse listings | Optional (better if authenticated) |
| GET    | /api/v1/listings/{id}   | Listing detail         | Optional                           |
| POST   | /api/v1/listings        | Create listing         | Merchant                           |
| PATCH  | /api/v1/listings/{id}   | Update listing         | Merchant (own)                     |
| DELETE | /api/v1/listings/{id}   | Cancel listing         | Merchant (own)                     |
| GET    | /api/v1/listings/feed   | Personalized feed      | Consumer                           |
| GET    | /api/v1/listings/search | Text search            | Optional                           |

### Orders

| Method | Path                        | Description             | Auth                     |
| ------ | --------------------------- | ----------------------- | ------------------------ |
| POST   | /api/v1/orders              | Create order (purchase) | Consumer                 |
| GET    | /api/v1/orders              | List own orders         | Consumer/Merchant        |
| GET    | /api/v1/orders/{id}         | Order detail            | Consumer/Merchant (own)  |
| PATCH  | /api/v1/orders/{id}/status  | Update status           | Merchant                 |
| POST   | /api/v1/orders/{id}/collect | QR scan confirmation    | Merchant                 |
| POST   | /api/v1/orders/{id}/cancel  | Cancel order            | Consumer (before pickup) |

### Reviews

| Method | Path                           | Description      | Auth                       |
| ------ | ------------------------------ | ---------------- | -------------------------- |
| POST   | /api/v1/reviews                | Create review    | Consumer (post-collection) |
| GET    | /api/v1/merchants/{id}/reviews | Merchant reviews | Public                     |
| PATCH  | /api/v1/reviews/{id}           | Update review    | Consumer (own)             |

## Standard API Contracts

### Error Response Format

All API errors return a consistent JSON shape:

```json
{
  "error": {
    "code": "LISTING_SOLD_OUT",
    "message": "This deal just sold out",
    "details": {}
  }
}
```

| HTTP Status | Error Code       | When                                          |
| ----------- | ---------------- | --------------------------------------------- |
| 400         | VALIDATION_ERROR | Invalid request body or parameters            |
| 401         | AUTH_REQUIRED    | Missing or invalid authentication             |
| 403         | FORBIDDEN        | Authenticated but not authorized for resource |
| 404         | NOT_FOUND        | Resource does not exist                       |
| 409         | CONFLICT         | Concurrent modification, sold out             |
| 422         | BUSINESS_RULE    | Order cancelled, listing expired, etc.        |
| 429         | RATE_LIMITED     | Too many requests                             |
| 500         | INTERNAL_ERROR   | Unexpected server error                       |

### Pagination

All collection endpoints use cursor-based pagination:

**Request**: `GET /api/v1/listings?cursor={cursor}&limit={limit}`

- `cursor`: Opaque cursor from previous response (omit for first page)
- `limit`: Page size (default: 20, max: 50)

**Response**:

```json
{
  "items": [...],
  "pagination": {
    "has_next": true,
    "next_cursor": "eyJpZCI6ImFiYzEyMyJ9",
    "total_count": 142
  }
}
```

### Concurrent Purchase Handling

Order creation uses a reserve-then-pay pattern:

1. **Reserve**: `SELECT quantity_remaining FROM listings WHERE id = ? FOR UPDATE` (row lock)
2. **Check**: Verify quantity_remaining >= requested quantity
3. **Decrement**: `UPDATE listings SET quantity_remaining = quantity_remaining - ? WHERE id = ?`
4. **Process payment**: Create Stripe PaymentIntent
5. **Create order**: Insert order record
6. **Commit transaction**
7. **On payment failure**: Roll back reservation (increment quantity_remaining)
8. **Lock timeout**: 5 seconds; if lock not acquired, return 409 CONFLICT
