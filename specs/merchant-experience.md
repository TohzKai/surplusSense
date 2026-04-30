# Merchant Experience Specification

## Overview

Merchant-facing dashboard for managing surplus listings, processing orders, and viewing analytics. Web-based interface (responsive, mobile-friendly for tablet use in kitchen).

## Dashboard Pages

### 1. Home / Today View

**Purpose**: At-a-glance view of today's activity.

**Components**:

- **Prediction card**: ML surplus prediction for today with accept/adjust/reject buttons
- **Active listings**: Currently live listings with real-time sales count and revenue
- **Pending orders**: Orders awaiting preparation or ready for pickup
- **Quick stats**: Items sold today, revenue today, sell-through rate
- **Alert banner**: Low sell-through warning, expiring SFA license, system notifications

### 2. Listing Management

**Create listing flow**:

1. Tap "New Listing"
2. Select category from saved categories (or create new)
3. Enter: quantity, price (suggested price pre-filled from ML), pickup window (defaults from category)
4. Optional: description, photos, item_type (specific or surprise_bag)
5. Review → Publish

**Prediction flow**:

1. Morning prediction notification received
2. Open dashboard → see prediction cards per category
3. Each card shows: category name, predicted surplus, confidence (high/medium/low), suggested price
4. Quick actions: Accept (publishes immediately), Adjust (opens edit), Reject (dismisses)

**Listing management table**:

- Columns: Category, Quantity, Price, Sold, Remaining, Status, Pickup Window
- Row actions: Edit, Cancel, View orders
- Filters: Status (active, sold_out, expired), Date range

### 3. Order Management

**Order list view**:

- Incoming orders sorted by pickup time (soonest first)
- Order card shows: consumer name (or order ID), items, quantity, pickup window, status
- Status badges: placed (yellow), preparing (blue), ready (green), collected (gray)

**Order processing flow**:

1. New order notification → appears in order list
2. Tap order → see details + consumer pickup QR preview
3. "Mark Preparing" → consumer notified
4. "Mark Ready" → consumer notified to come pick up
5. Consumer arrives → merchant opens QR scanner
6. Scan QR → order auto-completes, both parties confirmed

**QR Scanner**:

- Accessible from top nav bar (always available)
- Full-screen camera view with scan overlay
- On successful scan: Green checkmark + order details
- On failed scan: Red X + error reason

**Manual order lookup** (fallback):

- Enter order ID manually
- Same validation as QR scan

### 4. Analytics Dashboard

See `ml-analytics.md` for full specification. Key views:

**Overview**: Waste metrics, trend lines, top categories
**Patterns**: Heatmaps, waste profile, correlations
**Recommendations**: Prescriptive insight cards with action buttons
**Impact**: Sustainability metrics, shareable reports

### 5. Settings

**Business profile**: Name, description, address, operating hours, cuisine types, dietary tags, logo
**Category management**: Add/edit/delete food categories with defaults (batch size, price, shelf life)
**Pricing preferences**: Price floors per category, dynamic pricing toggle, pricing mode (conservative/balanced/aggressive)
**Notification preferences**: Toggle notification types, set prediction delivery time
**Payment settings**: Bank account for payouts, view payout history
**Account settings**: Email, password, linked accounts

## Mobile Considerations

- Dashboard must be usable on tablet (iPad常见 in F&B kitchens)
- Large touch targets for kitchen environment (wet hands, gloves)
- High-contrast mode for bright kitchen environments
- Offline-resistant: Basic order list cached locally, syncs on reconnect
- QR scanner must work in varying lighting conditions

## Onboarding Experience

1. Welcome screen with platform overview (3 slides)
2. Business details form (pre-fills from Google Places if available)
3. Category setup: Select from common categories + customize
4. Pricing setup: Set original prices and floor prices per category
5. Tutorial overlay: Point-out key dashboard elements
6. First prediction: "We'll start sending predictions tomorrow morning!"

## Information Architecture

```
Merchant Dashboard
├── Home (Today)
│   ├── Prediction Cards
│   ├── Active Listings
│   ├── Pending Orders
│   └── Quick Stats
├── Listings
│   ├── All Listings (table)
│   ├── Create New Listing
│   └── Category Management
├── Orders
│   ├── Active Orders
│   ├── Order History
│   └── QR Scanner (global access)
├── Analytics
│   ├── Overview
│   ├── Patterns
│   ├── Recommendations
│   └── Impact
└── Settings
    ├── Business Profile
    ├── Categories
    ├── Pricing
    ├── Notifications
    ├── Payments
    └── Account
```
