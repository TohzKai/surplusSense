# Consumer Experience Specification

> **Phase 2 — Not part of final submitted MVP.** Consumer-facing mobile app is a Phase 2 extension. The submitted MVP is the merchant-side decision cockpit only.

## Overview

Consumer-facing mobile app (Flutter, iOS + Android) for discovering, purchasing, and picking up surplus food deals. Focus on fast, personalized deal discovery and a delightful purchase experience.

## App Structure

### Bottom Navigation

| Tab     | Icon      | Purpose                                 |
| ------- | --------- | --------------------------------------- |
| Home    | House     | Personalized feed, deals, sections      |
| Search  | Magnifier | Search, browse by category, filters     |
| Orders  | Bag       | Active orders, order history, QR codes  |
| Profile | Person    | Impact dashboard, preferences, settings |

## Screens

### 1. Onboarding Flow

**Splash screen**: App logo + tagline ("Rescue great food, save money, help the planet")

**Sign up / Login screen**:

- Email + password fields
- "Continue with Google" / "Continue with Apple" buttons
- "Already have an account? Log in" toggle

**Preference quiz** (3 screens):

1. "What do you like to eat?" — Grid of cuisine tiles (multi-select with icons)
2. "What's your budget?" — Slider S$3 to S$15 with meal illustrations
3. "Any dietary needs?" — Toggle chips: Halal, Vegetarian, Vegan, Gluten-free, None

**Location permission**: "Find deals near you" → system permission dialog
**Home/work setup** (optional): "Where do you spend most of your time?" → map pin

**Transition to home**: "Great! We found X deals near you"

### 2. Home Tab

**Top section**:

- Greeting: "Good morning, [name]!" with weather icon
- Location indicator: "Near [neighborhood]" (tappable to change)

**Hero banner** (rotating):

- "8 deals expiring within 2 hours!"
- "New: Surprise bags available near you"
- "You've rescued 5 meals this week — keep going!"

**Feed sections** (vertical scroll):

**"For You" section** (ML-ranked):

- Horizontal scroll of deal cards (3-4 visible)
- Each card: merchant image, name, distance, original→current price, discount badge, quantity remaining

**"Expiring Soon" section**:

- Vertical list with countdown timers
- Urgency indicators: red (<30min), orange (<1hr), yellow (<2hr)

**"Nearby" section**:

- Map view (compact, expandable) with deal pins
- List view below map

**"Popular This Week" section**:

- Most purchased deals across platform
- Social proof: "X people rescued this today"

### 3. Deal Card Component

**Card anatomy** (list view):

```
┌─────────────────────────────────────────┐
│ [Image]  Merchant Name        1.2 km    │
│          Cuisine tags                   │
│          S$6.00  S$3.00    Save 50%     │
│          Pickup: 5-9pm  ● 5 left        │
│          ★★★★☆ (42)  Halal             │
└─────────────────────────────────────────┘
```

**Card anatomy** (detail page):

- Full-width merchant image / photos
- Merchant name + rating + distance + dietary tags
- Original price (strikethrough) → Current price (large, green)
- Discount percentage badge
- Item description (or surprise bag hints)
- Pickup window with countdown timer
- Remaining quantity bar (visual: X of Y remaining)
- Price trend indicator: "Price may drop" or "Price just dropped ↓"
- "What you might get" section (for surprise bags)
- Merchant location map with directions button
- Reviews section (last 5 reviews)
- "Buy Now" button (sticky at bottom)

### 4. Search Tab

**Search bar**: Full-width, auto-focus on tab selection

- Autocomplete suggestions as user types
- Recent searches shown below bar when empty
- Trending searches: "bakery near me", "halal", "under $5"

**Browse categories** (grid of tiles):

- Chinese, Malay, Indian, Western, Japanese, Korean, Thai, Bakery, Cafe, Healthy, Desserts, All

**Filters panel** (bottom sheet):

- Price range slider
- Distance selector (500m, 1km, 3km, 5km, 10km)
- Dietary toggles
- Pickup time (Now, Lunch, Dinner, Late Night)
- Rating (Any, 3+, 4+, 4.5+)
- Sort by: Relevance, Distance, Price (low-high), Discount (high-low), Rating

### 5. Orders Tab

**Active orders section**:

- Order cards with: merchant, items, pickup window countdown, QR code button
- Status indicator: Placed (yellow dot), Ready (green dot)
- "Show QR" button → full-screen QR code for merchant scan
- Directions button → opens map navigation

**Order history section** (below active):

- Past orders sorted by date (newest first)
- Each: merchant name, items, amount, date, rating given
- Filter by date range, merchant

### 6. Profile Tab

**Impact dashboard** (top section):

- Circular progress ring showing meals rescued vs. next badge
- Stats row: Meals rescued, Money saved (S$), CO2 prevented (kg)
- Current badge level with next badge progress
- "Share Impact" button → generates shareable card image

**Quick links**:

- My Preferences (cuisine, dietary, budget, locations)
- Saved Merchants (favorite merchants list)
- Payment Methods (saved cards, add new)
- Notification Settings (toggle categories, quiet hours)
- Transaction History (detailed purchase history)
- Help & Support
- About & Terms

**Achievement badges section**:

- Grid of earned and locked badges
- Each badge: icon, name, description, progress bar
- Badges: First Rescue, Regular Rescuer (10), Waste Warrior (50), Neighborhood Hero (10 merchants), Cuisine Explorer (5 cuisines), Early Bird (purchase within 1hr), Green Champion (100+)

## Purchase Flow (Detailed)

1. **Deal detail** → Tap "Buy Now"
2. **Order summary sheet** (bottom sheet):
   - Item name, quantity selector (+/-), price breakdown
   - Pickup window confirmation
   - Merchant name + mini map
   - Payment method (default selected, tap to change)
   - Total amount
3. **"Confirm & Pay"** button
4. **Processing overlay** (2-3 seconds): Animated food icon
5. **Confirmation screen**:
   - Green checkmark + "Order Confirmed!"
   - QR code (large, centered)
   - Pickup details: merchant, address, time window
   - "Get Directions" button
   - "View Order" button
6. **Auto-return to Home** after 10 seconds (or tap to dismiss)

## Animations and Micro-interactions

- Deal card: Subtle bounce on tap
- Purchase confirmation: Confetti animation on first purchase
- Impact dashboard: Count-up animation on stats
- Badge unlock: Celebration animation with sound (optional)
- Price drop: Gentle pulse animation on new price
- Quantity low: Blinking badge when <3 remaining

## Accessibility

- Minimum touch target: 44×44pt
- Color contrast: WCAG AA minimum
- Screen reader support for all interactive elements
- Dynamic text sizing support
- High contrast mode support

## Error States

| Scenario        | Display                                                                                |
| --------------- | -------------------------------------------------------------------------------------- |
| No deals nearby | Friendly illustration + "No deals right now — check back later!" + notification signup |
| Deal sold out   | "This deal just sold out!" + suggest similar deals                                     |
| Payment failed  | "Payment didn't go through" + retry button + change payment option                     |
| Network error   | Offline banner + cached content where possible                                         |
| Location denied | Manual location entry + reduced personalization                                        |
