# Dynamic Pricing Specification

> **Phase 2 — Not part of final submitted MVP.** Dynamic real-time pricing is Phase 2. The submitted MVP uses the 10-tier static discount recommendation engine documented in `src/recommendation_engine.py`.

## Overview

Dynamic pricing optimizes surplus food prices in real-time to maximize sell-through rate while respecting merchant-defined price floors and maintaining consumer trust through transparency.

## Pricing Model

### Price Curve Formula

```
price(t) = base_price × (floor_ratio + (1 - floor_ratio) × decay(t))

decay(t) = e^(-λ × t_normalized)
t_normalized = (current_time - listing_created) / (pickup_end - listing_created)
λ = decay_rate (category-specific, learned from historical data)
```

### Three-Tier Structure (MVP)

| Tier        | Time Range               | Price              | Example (S$10 base, S$3 floor) |
| ----------- | ------------------------ | ------------------ | ------------------------------ |
| **Initial** | Listing to 40% of window | 60-70% of original | S$6.00                         |
| **Mid**     | 40% to 75% of window     | 40-50% of original | S$4.50                         |
| **Final**   | 75% to end of window     | Floor price        | S$3.00                         |

### Demand Modifiers

Adjust the decay rate λ based on real-time demand signals:

| Signal                                 | Effect                                | Modifier |
| -------------------------------------- | ------------------------------------- | -------- |
| High views, zero purchases             | Price too high → accelerate decay     | λ × 1.5  |
| Purchases keeping pace with views      | Price is right → maintain             | λ × 1.0  |
| Rapid sell-through (>50% in first 30%) | Price could be higher → slow decay    | λ × 0.7  |
| Very low views (<5 in first hour)      | Visibility issue → don't change price | λ × 1.0  |

## Merchant Controls

### Price Floor (Mandatory)

- Every category has a minimum price set by the merchant
- System NEVER prices below floor, regardless of demand
- Merchant can adjust floor at any time (affects new listings only)

### Pricing Mode

- **Conservative**: Slow decay, higher prices maintained longer. Best for premium merchants.
- **Balanced** (default): Standard decay curve. Good for most merchants.
- **Aggressive**: Fast decay, prioritize sell-through over revenue. Best for perishable items.

### Dynamic Pricing Toggle

- Merchant can disable dynamic pricing per category
- When disabled: price stays at initial listing price for the entire window
- Default: Enabled for all categories

## Price Updates

### Update Frequency

- Check and potentially update every 5 minutes for active listings
- Immediate update on purchase (quantity remaining change)
- No update in last 15 minutes before pickup end (price stability for last-minute buyers)

### Price History

- Every price change logged to PriceHistory table
- Consumer can see price trend chart on listing detail (optional Phase 2)
- Merchant can see price curve analytics in dashboard

## Consumer Experience

### Price Transparency

- Original price always shown with strikethrough
- Current price shown prominently
- Savings percentage badge: "Save 55%!"
- "Price may decrease" disclaimer on active listings
- No surprise price increases — price only decreases

### Price Drop Notifications

- If consumer bookmarked/watched a listing: notified on price drop
- "Price dropped on [item]! Now S$X.XX (was S$Y.YY)"
- One notification per listing per session (don't spam)

## Pricing API

| Method | Path                                 | Description                             |
| ------ | ------------------------------------ | --------------------------------------- |
| GET    | /api/v1/pricing/{listing_id}         | Current price for listing               |
| GET    | /api/v1/pricing/{listing_id}/history | Price change history                    |
| POST   | /api/v1/ml/pricing/optimize          | Get optimal price suggestion (merchant) |

## Constraints and Guards

1. **No price increases**: `new_price <= previous_price` always enforced
2. **Floor enforcement**: `new_price >= listing.min_price` always enforced
3. **Round to S$0.50**: Final price rounded to nearest 50 cents for simplicity
4. **Stability window**: No price changes in last 15 minutes before pickup end
5. **Max daily changes**: Maximum 8 price adjustments per listing per day (prevent perceived volatility)
6. **Purchased price frozen**: Once a consumer purchases, their price is locked — no further changes affect completed orders
