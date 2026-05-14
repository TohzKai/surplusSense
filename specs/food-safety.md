# Food Safety Specification

> **Phase 2 — Not part of final submitted MVP.** Full SFA regulatory compliance documentation is Phase 2. The submitted MVP implements food safety rules in `src/food_safety_rules.py` with simplified Singapore F&B context.

## Overview

Singapore-specific food safety requirements for selling surplus and near-expiry food. Compliance with SFA (Singapore Food Agency) and NEA regulations is mandatory.

## Use-By vs Best-Before Enforcement

### Use-By Date (SAFETY CRITICAL)

- Items with use-by dates CANNOT be sold after the use-by date
- System must prevent listing items past their use-by date
- Merchant must enter use-by date when creating listings for applicable items
- Validation: `use_by_date > NOW()` at listing creation time
- Monitoring: Scheduled check every 30 minutes — auto-expire any listing where `use_by_date <= NOW()`

### Best-Before Date (QUALITY INDICATOR)

- Items past best-before date MAY be sold if merchant confirms food is safe
- System requires explicit merchant confirmation: "I confirm this item is safe for consumption despite being past its best-before date"
- Consumer disclosure: Listing must show "Past best-before date: [date]"
- No restriction on selling — but disclosure is mandatory

### Items Without Dates

- Prepared food (cooked meals, baked goods): Shelf life based on MerchantCategory.shelf_life_hours
- System calculates effective expiry: `listing.created_at + category.shelf_life_hours`
- Pickup window must be within shelf life

## Listing Safety Validation

### Mandatory Checks at Listing Creation

1. **Use-by date validation** (if applicable):
   - If category has `requires_use_by_date = true`: merchant must provide use-by date
   - Use-by date must be after pickup end time
   - Rejected if: use-by date is today AND pickup window extends past midnight

2. **Shelf life validation**:
   - Pickup end time must be within `shelf_life_hours` of food preparation time
   - If merchant sets pickup end beyond shelf life: warning shown, listing blocked

3. **Temperature control categories**:
   - Items requiring cold chain (dairy, meat, prepared meals): merchant must confirm temperature control maintained
   - Confirmation checkbox at listing creation
   - Consumer sees "Temperature-controlled item" tag

4. **Allergen disclosure**:
   - Merchant must declare common allergens for each category
   - Consumer filters work based on allergen data

## Merchant Safety Requirements

### Onboarding Verification

- SFA license number required and verified
- License must be active and in good standing
- Merchant type determines applicable safety rules:
  - Restaurant/Cafe: Full SFA food establishment requirements
  - Bakery: SFA requirements + specific baked goods rules
  - Supermarket: SFA retail food shop requirements
  - Hawker stall: SFA hawker stall requirements

### Ongoing Compliance

- SFA license renewal monitoring (annual check)
- Merchant can be suspended if license lapses
- Consumer complaints about food safety → immediate investigation → potential suspension

## Consumer Safety Features

### Trust Signals

- SFA verified badge on merchant profile
- Food safety rating (based on NEA hygiene grading if available)
- Consumer reviews include food quality tags
- Listing shows: preparation time, shelf life remaining, storage conditions

### Complaint and Refund

- Consumer reports food safety issue → immediate order flag
- Merchant notified, investigation initiated
- Consumer receives full refund
- Repeated complaints → merchant suspended pending review
- Serious food safety violations → reported to SFA

## Data Tracking for Safety

### Fields Tracked

- Listing creation timestamp
- Use-by / best-before dates (if applicable)
- Shelf life hours per category
- Pickup window start/end
- Consumer collection timestamp
- Any safety-related consumer feedback

### Audit Trail

- Every listing has a complete timestamp chain: created → published → purchased → collected
- Temperature control confirmations logged
- Use-by date validations logged
- Safety complaints logged with resolution status

## Edge Cases

| Scenario                                      | Resolution                                          |
| --------------------------------------------- | --------------------------------------------------- |
| Merchant lists item past use-by date          | System blocks creation — validation error           |
| Use-by date passes during active listing      | Auto-expire listing, refund any uncollected orders  |
| Consumer reports food safety issue            | Immediate refund, merchant flag, investigation      |
| Merchant SFA license expires                  | Platform suspension, pending renewal verification   |
| Shelf life expires before pickup window       | System blocks listing creation                      |
| Surprise bag contains allergens not disclosed | Merchant violation → warning → suspension on repeat |
