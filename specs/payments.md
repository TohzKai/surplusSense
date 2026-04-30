# Payments Specification

## Overview

Payment processing via Stripe for consumer purchases and merchant payouts. QR-based pickup confirmation flow.

## Payment Methods (Singapore)

| Method                               | Supported By     | Priority |
| ------------------------------------ | ---------------- | -------- |
| Credit/Debit Card (Visa, Mastercard) | Stripe           | Required |
| Apple Pay                            | Stripe           | Required |
| Google Pay                           | Stripe           | Required |
| PayNow                               | Manual (Phase 2) | Deferred |

## Payment Flow

### Consumer Purchase

1. Consumer confirms order → Stripe PaymentIntent created
2. Amount = total (unit_price × quantity)
3. Stripe processes payment → returns payment_intent_id
4. On success: Order created with status=placed, QR generated
5. On failure: Order not created, consumer sees error with retry option

### Payment Breakdown

```
Sale Price:        S$5.00
Platform Fee (15%): S$0.75
Merchant Payout:   S$4.25
```

### Refunds

- **Full refund**: Consumer cancels before pickup window, or order expires uncollected
- **Partial refund**: Not supported in MVP (all-or-nothing)
- **Refund processing**: Stripe refund initiated immediately, takes 3-5 business days to appear
- **Refund reason**: Logged for analytics (consumer_cancel, expired, merchant_cancel, safety_issue)

## Merchant Payouts

### Payout Schedule

- Weekly payout every Monday for previous week (Mon-Sun) transactions
- Minimum payout: S$10 (accumulates if below threshold)
- Payout method: Bank transfer (merchant provides bank details during onboarding)

### Payout Calculation

```
Weekly payout = SUM(merchant_payout) for all completed orders in period
              - SUM(refunded amounts) for orders refunded in period
```

### Payout Dashboard

- Current period earnings (running total)
- Pending payout amount
- Payout history with breakdown by order
- Export as CSV

## QR-Based Pickup

### QR Code Generation

- Generated server-side upon successful payment
- Contains: order_id + verification_hash
- Format: JSON string encoded in QR
- Displayed on order confirmation screen in consumer app

### QR Code Scanning (Merchant Side)

1. Merchant opens scanner in dashboard
2. Scans consumer's QR code.
3. System validates:
   - Order exists and belongs to this merchant
   - Order status is placed or ready
   - Current time is within pickup window (with 15-min grace period)
4. On valid scan: Order status → collected, confirmation to both parties
5. On invalid scan: Error message with reason

### Manual Confirmation (Fallback)

- If QR scanning fails, merchant can manually enter order ID
- Same validation as QR scan
- Merchant confirms with button tap

## Security

### Payment Security

- All payment processing through Stripe (PCI DSS compliant)
- No card details stored on our servers
- Stripe.js for frontend tokenization
- Webhook for async payment confirmation

### QR Security

- Verification hash prevents QR forgery
- Hash = HMAC(order_id, secret_key)
- Single-use: QR becomes invalid after scan (order moves to collected)
- Time-bound: QR invalid outside pickup window (with grace period)

## Stripe Configuration

### Stripe Connect (Phase 2)

- Each merchant gets a Stripe Connect account
- Automatic split: platform fee to platform, remainder to merchant
- Simplifies payout management

### Stripe Webhooks

- `payment_intent.succeeded` → confirm order
- `payment_intent.failed` → notify consumer
- `charge.refunded` → update order status
- `payout.paid` → update merchant payout status

## API Endpoints

| Method | Path                               | Description                             |
| ------ | ---------------------------------- | --------------------------------------- |
| POST   | /api/v1/payments/create-intent     | Create Stripe PaymentIntent             |
| POST   | /api/v1/payments/confirm           | Confirm payment after Stripe processing |
| POST   | /api/v1/payments/refund/{order_id} | Initiate refund                         |
| GET    | /api/v1/payments/payouts           | Merchant payout history                 |
| GET    | /api/v1/payments/earnings          | Merchant current earnings               |
| POST   | /api/v1/payments/webhook           | Stripe webhook receiver                 |
