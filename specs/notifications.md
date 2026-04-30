# Notifications Specification

## Overview

Push notification system for timely, relevant alerts to merchants and consumers. Notification timing optimized by ML based on user engagement patterns.

## Notification Types

### Merchant Notifications

| Type                 | Trigger                                | Priority | Example                                                      |
| -------------------- | -------------------------------------- | -------- | ------------------------------------------------------------ |
| Morning prediction   | Daily at merchant's start time         | High     | "Predicted surplus: 12 chicken rice, 8 nasi lemak"           |
| New order            | Consumer purchases                     | High     | "New order! 2× chicken rice — pickup 5-9pm"                  |
| Low sell-through     | 50% of window passed, <30% sold        | Medium   | "Only 3 of 12 items sold — consider price reduction?"        |
| Price drop accepted  | Price auto-reduced per dynamic pricing | Low      | "Price reduced to S$3.50 for remaining pastries"             |
| End-of-day summary   | After pickup window closes             | Medium   | "Today: 10/12 sold, S$45 recovered, 83% sell-through"        |
| SFA license reminder | 30 days before expiry                  | High     | "Your SFA license expires in 30 days — renew to stay active" |
| Weekly analytics     | Monday morning                         | Low      | "Weekly report: S$320 revenue, 85% sell-through, -12% waste" |

### Consumer Notifications

| Type              | Trigger                                     | Priority | Example                                               |
| ----------------- | ------------------------------------------- | -------- | ----------------------------------------------------- |
| Personalized deal | New listing matching preferences            | Medium   | "New deal: Chicken rice 60% off near your office!"    |
| Price drop        | Bookmarked listing price decreased          | High     | "Price dropped! Pastries now S$2 (was S$4)"           |
| Expiring soon     | Deals near consumer expiring within 2 hours | Medium   | "5 great deals expiring near you in the next 2 hours" |
| Order confirmed   | After successful purchase                   | High     | "Order confirmed! Pick up from [merchant] by 9pm"     |
| Pickup reminder   | 30 minutes before pickup window starts      | High     | "Ready to pick up! [Merchant] is waiting for you"     |
| Pickup ending     | 30 minutes before pickup window closes      | High     | "Last chance! Pick up your order in the next 30 min"  |
| Rating prompt     | 30 minutes after collection                 | Low      | "How was your meal? Rate [merchant]"                  |
| Impact milestone  | Meals rescued hits threshold                | Low      | "You've rescued 25 meals! You're a Waste Warrior"     |
| Weekly digest     | Monday morning                              | Low      | "You saved S$32 last week! See this week's deals"     |

## Notification Delivery

### Channels (Priority Order)

1. **Push notification** (Firebase Cloud Messaging) — primary
2. **In-app notification center** — always stored
3. **Email** — optional, for weekly digest and critical alerts only

### Delivery Rules

- Maximum 5 notifications per consumer per day (don't spam)
- Maximum 3 non-order notifications per consumer per day
- Merchant notifications unlimited (operational necessity)
- Quiet hours: 10pm - 8am (no non-critical notifications)
- Duplicate suppression: Same listing won't trigger >1 notification per consumer per day

## ML-Optimized Timing

### When to Send (Consumer)

- Track when each user typically opens the app (engagement time distribution)
- Send personalized deal alerts during user's peak engagement window
- Pre-meal timing: lunch deals sent 10am-11am, dinner deals sent 4pm-5pm
- Weather-reactive: Send more notifications on rainy days (more likely to plan ahead)

### When to Send (Merchant)

- Morning prediction: Aligned with merchant's operating start time
- Order alerts: Immediate (no delay)
- Daily summary: 30 minutes after merchant's closing time

## Notification Preference Management

### Consumer Controls

- Toggle categories: deal alerts, price drops, pickup reminders, weekly digest, impact milestones
- Set quiet hours (custom start/end time)
- Set max notifications per day (1, 3, 5, 10, unlimited)
- Pause all notifications (vacation mode)

### Merchant Controls

- Toggle categories: predictions, order alerts, sell-through alerts, daily summary, weekly report
- Prediction notification time (when to receive morning prediction)
- Cannot disable: order alerts, pickup confirmations (operational)

## In-App Notification Center

### Storage

- All notifications stored in database with read/unread status
- Retained for 30 days
- Badge count on app icon shows unread count

### UI

- Bell icon with badge in app header
- Tapping opens notification list (sorted by time, newest first)
- Swipe to dismiss or mark as read
- Tap notification to navigate to relevant content (deal detail, order, etc.)

## Implementation

### Push Notification Service

- Firebase Cloud Messaging (FCM) for mobile push
- Store FCM tokens per user (updated on app open)
- Fallback: If push fails, notification still stored in notification center

### Notification Queue

- Notifications queued in database table
- Background worker processes queue and sends via FCM
- Rate limiting enforced at worker level
- Retry on transient failure (max 3 retries, exponential backoff)

## API Endpoints

| Method | Path                                 | Description               |
| ------ | ------------------------------------ | ------------------------- |
| GET    | /api/v1/notifications                | List user's notifications |
| PATCH  | /api/v1/notifications/{id}/read      | Mark as read              |
| PATCH  | /api/v1/notifications/read-all       | Mark all as read          |
| GET    | /api/v1/notifications/preferences    | Get notification settings |
| PATCH  | /api/v1/notifications/preferences    | Update settings           |
| POST   | /api/v1/notifications/register-token | Register FCM token        |
