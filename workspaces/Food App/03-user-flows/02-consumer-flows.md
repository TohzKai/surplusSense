# User Flows: Consumer Journey

## C1: Consumer Onboarding

```
App store → Download → Splash screen → Sign up (email/Google/Apple)
→ Quick preference quiz (3 questions) → Location permission
→ Home feed with personalized deals → First purchase
```

### Step-by-step:

**1a. Sign up**

- Options: Email + password, Google Sign-In, Apple Sign-In
- Phone number optional (for pickup notifications)
- Age confirmation (13+)

**1b. Quick preference quiz (3 questions)**

1. "What cuisines do you enjoy?" — Multi-select: Chinese, Malay, Indian, Western, Japanese, Thai, Korean, Bakery, Cafe, Other
2. "What's your typical lunch budget?" — Slider: S$3 to S$15
3. "Any dietary preferences?" — Multi-select: No restrictions, Halal, Vegetarian, Vegan, Gluten-free

**1c. Location permission**

- Request location access for nearby deal discovery
- Fallback: Manual postal code entry
- Home/work location setup (optional): "Set home" and "Set office" for commute-based recommendations

**1d. First experience**

- Personalized home feed showing nearby deals matching preferences
- Educational banner: "How it works" — 3 steps (Browse → Buy → Pick up)
- First-purchase incentive: "Get S$3 off your first order!"

**Onboarding time target**: < 2 minutes

---

## C2: Deal Discovery (Home Feed)

```
Open app → Personalized home feed → Browse by category/filter
→ Tap deal card → View deal details → Decision point
```

### Home feed layout:

**2a. Hero section**

- Time-sensitive: "X deals expiring in the next 2 hours near you!"
- Weather-aware: "Rainy day? These cozy spots have great deals"

**2b. Personalized deal cards (ML-ranked)**
Each card shows:

- Merchant name + cuisine tag + distance
- Original price → Discounted price (with savings %)
- Items included (category description or specific items)
- Pickup window (e.g., "Pickup 5-9pm")
- Remaining quantity badge (e.g., "5 left")
- Live price indicator (showing if price is dropping)
- Rating (star average)
- Dietary tags (halal, vegetarian)

**2c. Feed sections (tabbed or scrollable)**

- "For You" — ML-personalized recommendations
- "Nearby" — Deals sorted by distance
- "Expiring Soon" — Deals with closing pickup windows
- "Best Value" — Highest discount percentage
- "Surprise Bags" — Mystery deals at deep discounts

**2d. Filters**

- Cuisine type
- Price range
- Distance (within 500m, 1km, 3km, 5km)
- Dietary requirements
- Pickup time (now, lunch, dinner)
- Rating (4+ stars)

**ML integration**: Feed is ranked by the recommendation engine considering user preferences, location, time of day, weather, and behavioral history. Ordering updates in near-real-time as deals sell out or prices change.

---

## C3: Deal Purchase Flow

```
Deal card → "Buy Now" → Confirm order → Payment → QR code generated
→ Navigate to merchant → Show QR → Collect food → Rate experience
```

### Step-by-step:

**3a. Deal detail page**

- Full item description (or "Surprise Bag — merchant curates contents")
- Merchant info: name, address, map, operating hours, rating
- Pricing breakdown: Original price, discount %, final price
- Pickup window: Start time, end time, time remaining
- Remaining quantity
- Reviews from other consumers
- "What you might get" (category examples for surprise bags)

**3b. Purchase confirmation**

- Order summary: Items, price, pickup window, merchant location
- Payment method selection (saved methods + add new)
- Total amount charged
- "Confirm Purchase" button

**3c. Payment processing**

- PayNow, credit/debit card, Apple Pay, Google Pay, GrabPay
- Instant confirmation
- Digital receipt generated

**3d. Post-purchase**

- QR code / order confirmation screen
- Map directions to merchant
- Pickup instructions ("Show this QR code at the counter")
- Countdown timer to pickup window
- "Add to calendar" option for pickup reminder

**3e. Pickup**

- Consumer arrives at merchant during pickup window
- Shows QR code to merchant staff
- Merchant scans → order confirmed → consumer collects food
- Push notification: "Enjoy your meal! Don't forget to rate."

**3f. Rating and review**

- Post-pickup notification (30 min after pickup window)
- Quick rating: 1-5 stars + optional review
- Category tags: "Great value", "Fresh food", "Friendly staff", "Easy pickup"
- Impact update: "You saved X kg of food and prevented Y kg of CO2 emissions!"

---

## C4: Search and Discovery

```
Search bar → Type query or voice search → Results displayed
→ Filter and sort → Select deal → Purchase flow
```

**Search capabilities**:

- Text search: "bakery near me", "halal food under $5", "chicken rice"
- Voice search (optional Phase 2)
- Autocomplete suggestions
- Recent searches
- Trending searches ("Popular near you right now")

**Search ranking**: ML-powered — considers relevance, user preferences, proximity, deal quality, and availability.

---

## C5: Notifications and Alerts

```
Push notification → Tap → Relevant deal or update
```

**Notification types**:

- **Deal alert**: New deal from a favorited merchant or matching preference
- **Price drop**: A deal you bookmarked just dropped in price
- **Expiring soon**: "3 great deals expiring near you in the next hour!"
- **Pickup reminder**: "Your order from [merchant] is ready for pickup until [time]"
- **Weekly digest**: "You saved S$XX this week! Here are your personalized deals for the weekend"
- **Impact milestone**: "You've rescued 50 meals! You're a Food Rescue Hero"

**ML-driven timing**: Notifications sent at optimal time based on user's past engagement patterns (when they typically open the app).

---

## C6: Consumer Profile and Impact Dashboard

```
Profile tab → Impact dashboard → View stats → Share achievements
→ Manage preferences → Transaction history
```

### Profile sections:

**6a. Impact dashboard**

- Total meals rescued (count)
- Total money saved (S$)
- CO2 emissions prevented (kg)
- Food waste equivalent (meals / kg)
- Streak: "X consecutive weeks of food rescue!"
- Level / badge system (Bronze → Silver → Gold → Platinum based on meals rescued)
- Shareable impact card ("I've rescued 50 meals and saved S$200!")

**6b. Preference management**

- Saved cuisines, dietary tags, price range
- Saved locations (home, office, school)
- Notification preferences
- Favorite merchants
- Connected payment methods

**6c. Transaction history**

- Past orders with dates, merchants, amounts, ratings
- Filterable by date range, merchant, cuisine
- Export as CSV

**6d. Achievement badges**

- "First Rescue" — Made first purchase
- "Regular Rescuer" — 10 purchases
- "Waste Warrior" — 50 purchases
- "Neighborhood Hero" — Rescued food from 10 different merchants
- "Cuisine Explorer" — Tried 5+ cuisine categories
- "Early Bird" — Purchased within 1 hour of listing
- "Green Champion" — Rescued 100+ meals

---

## C7: Surprise Bag Flow

```
Home feed → "Surprise Bags" section → Select merchant
→ View price and category hints → Purchase → Collect → Unbox!
```

**Surprise bag details**:

- Consumer sees: merchant, price, category hints ("Baked goods", "Asian meals", "Mixed items"), pickup window
- Consumer does NOT see: exact items (that's the surprise)
- Merchants curate bags from actual surplus at pickup time
- Value guarantee: "Worth at least 2x the purchase price in retail value"

**Post-unbox experience**:

- Encourage sharing: "Show off your surprise bag! Tag us @foodapp"
- Rate: "What did you get? Rate your surprise bag"
- Feedback loop: Item-level feedback improves future bag composition

---

## C8: Social and Community Features (Phase 2)

```
Deal detail → Share with friend → Friend receives link → Opens app → Views deal
```

**Social features**:

- Share deal link via WhatsApp, Telegram, social media
- Group buying: "Get extra 10% off if 3 friends also buy from this merchant today"
- Leaderboard: Top food rescuers by neighborhood (optional, gamification)
- Community feed: See what others are rescuing nearby (anonymized aggregate)
- Merchant reviews and tips
