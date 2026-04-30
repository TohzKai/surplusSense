# SurplusSense: Product Hardening Plan

**Date**: 2026-04-25
**Purpose**: Guardrail the MVP against overclaiming and document the path from prototype to production

---

## Executive Summary

This document addresses the key gaps between the Week 9 MVP and a production-ready commercial product. It clearly separates:

1. What is **implemented** in the Week 9 MVP
2. What is **designed but not implemented**
3. What belongs to the **commercial roadmap**

The MVP demonstrates the core AI/ML decision-support logic: predicting surplus, recommending discount actions, estimating recovery value, and applying food-safety constraints. Production features (authentication, API integrations, model registry, CI/CD, notifications, A/B testing) are acknowledged as necessary for commercialization but are not required for the assignment MVP.

---

## Stage 1: Week 9 MVP (Current)

### Implemented

- Synthetic F&B data generator (cafés, bakeries, small F&B)
- ML pipeline with 3 baselines + XGBoost
- Rule-based discount recommendation engine
- Food-safety rule layer (blocks/cautions unsafe items)
- Streamlit decision cockpit dashboard
- COC decision log documenting all product choices

### Synthetic Data Position

> "Synthetic data is used as a controlled starting point to demonstrate the ML pipeline, not as proof of real-world accuracy. Real merchant pilots will be required before production deployment."

---

## Stage 2: Merchant Pilot

### To Implement

- Real merchant onboarding
- Actual sales and surplus data
- Merchant feedback loop
- Outcome tracking
- Manual retraining
- Basic account persistence

### Key Questions to Answer

| Gap                          | Resolution                                                              |
| ---------------------------- | ----------------------------------------------------------------------- |
| Cold start for new merchants | Use merchant profile + category benchmarks with lower confidence labels |
| No drift monitoring          | Track prediction error trend; flag when error exceeds threshold         |
| No retraining pipeline       | Weekly during pilot, monthly after stabilization                        |
| No outcome tracking          | Record actual surplus, quantity listed, sold, discarded, recovery       |

---

## Stage 3: Commercial Platform

### To Implement

- Authentication (email/password, MFA for larger chains)
- Production database (PostgreSQL)
- API endpoints (FastAPI)
- Notifications (email, WhatsApp, Telegram, in-app)
- Model registry (MLflow or equivalent)
- Scheduled retraining + error-triggered retraining
- Legal terms of service
- Merchant SaaS pricing

### Pricing Hypothesis

| Plan       | Target                  | Price Point       |
| ---------- | ----------------------- | ----------------- |
| Free pilot | 30-60 days              | Free              |
| Basic      | Single-outlet merchants | SGD 49-99/month   |
| Pro        | Multi-outlet merchants  | SGD 149-299/month |
| Enterprise | Chains with reporting   | Custom            |

---

## Stage 4: Marketplace Expansion

### To Implement

- Consumer listings
- Payment integration (PayNow, cards, wallets)
- Consumer demand validation
- Marketplace transaction flow
- Personalisation

### Validation Roadmap

1. Merchant-side surplus prediction MVP ✓
2. Small closed pilot with selected merchants
3. Manual consumer demand test (WhatsApp, Telegram, landing page)
4. Measure click-through, reservation, pickup rate
5. Add marketplace only after demand validated

---

## Stage 5: Advanced Optimisation

### Future Roadmap

- A/B testing for model versions
- Drift monitoring (prediction error, feature drift, outcome drift)
- Automated retraining
- POS integration
- Multi-outlet benchmarking
- Bandit or reinforcement learning pricing

---

## Detailed Gap Analysis

### 1. Data & Model Gaps

#### 1.1 Synthetic Data Only

- **Status**: MVP limitation acknowledged
- **Real calibration needed**: Compare predicted vs actual surplus, adjust weights, retrain, measure improvement over baselines
- **Positioning**: MVP development tool, not real-world validation

#### 1.2 90-Day Training Window

- **Status**: Sufficient for MVP, insufficient for seasonality
- **Production need**: 12-24 months of data + external calendar features (public holidays, festive periods)
- **Roadmap**: Add seasonal features in Phase 3

#### 1.3 No Drift Monitoring

- **Status**: Not implemented
- **Production design**: Track prediction error trend, feature drift, outcome drift
- **Threshold**: Flag for retraining when error exceeds baseline by X% for N consecutive days

#### 1.4 No Retraining Pipeline

- **Status**: Manual single training
- **Production design**:
  - Weekly retraining during early pilot
  - Monthly once patterns stabilize
  - Trigger-based when error exceeds threshold
  - Immediate after major operational changes

#### 1.5 Cold Start for New Merchants

- **Status**: Handled via merchant profile + benchmarks
- **Approach**:
  - Use merchant type, category, operating hours, production quantity
  - Label as "starter estimate" not high-confidence
  - Shift to merchant-specific as data accumulates

---

### 2. Product Gaps

#### 2.1 No Real Merchant Onboarding

- **Status**: Dashboard selectors simulate selection
- **Production design**: Account creation, outlet setup, product catalogue, optional CSV/POS upload

#### 2.2 No User Authentication

- **Status**: Not required for MVP prototype
- **Production design**:
  - Email/password login or SSO
  - MFA for business accounts
  - Role-based access (outlet manager, area manager, admin)

#### 2.3 No Session Persistence

- **Status**: CSV/SQLite acceptable for MVP
- **Production design**: Database-backed merchant profile table

#### 2.4 No Actual Transactions

- **Status**: Deliberate scope decision
- **Current**: Mock consumer listing preview
- **Future**: Full marketplace transactions in Phase 4

#### 2.5 No Notifications

- **Status**: Not implemented
- **Production design**:
  - Morning alert: expected surplus risk
  - Midday alert: early warning if sales below forecast
  - Late afternoon: recommended discount action
  - Pickup window: listing expiry warning
  - Safety alert: item should no longer be listed

---

### 3. Technical Gaps

#### 3.1 No Production Database

- **Status**: CSV/SQLite for MVP
- **Production**: PostgreSQL

#### 3.2 No API Endpoints

- **Status**: Streamlit direct calls
- **Production**: FastAPI endpoints for merchant, prediction, recommendation, safety, feedback, outcomes

#### 3.3 No Authentication Mechanism

- **Status**: Out of scope for MVP
- **Production**: Email/password, OAuth, managed identity provider

#### 3.4 No Model Registry

- **Status**: Simple model metadata file
- **Production**: MLflow or equivalent

#### 3.5 No CI/CD

- **Status**: Out of scope for MVP
- **Production**: Git, automated testing, Docker, staging, production, rollback

---

### 4. Food Safety Gaps

#### 4.1 Rules Not Expert-Validated

- **Status**: Prototype rules based on general food-safety principles
- **Required**: Expert review before production
- **Disclaimer**: "Decision-support indicator, not regulatory certification"

#### 4.2 No SFA Integration

- **Status**: No direct SFA integration
- **Required**: Review against SFA guidelines, legal counsel
- **No claim**: Not claiming formal regulatory compliance

#### 4.3 No Legal Disclaimers

- **Required disclaimer**:
  > "The food-safety status shown by SurplusSense is a decision-support indicator based on merchant-provided information. It does not certify or guarantee food safety. Merchants remain responsible for proper food handling, storage, labelling, and compliance with applicable food-safety requirements."

#### 4.4 Assumed Storage Conditions

- **Status**: Rules assume proper storage
- **Required**: Merchant must explicitly confirm storage conditions
- **Unknown = manual review required**

---

### 5. Business Model

#### 5.1 Pricing Not Set

- **Status**: Hypothesis to validate during merchant pilots
- **Approach**: Conservative/base/optimistic scenarios

#### 5.2 No Merchant Contracts

- **Required for production**:
  - Merchant responsibility for food safety
  - Accuracy of information
  - Limitation of platform liability
  - Data usage and privacy
  - Payment and refund terms

#### 5.3 Revenue Projections

- **Basis**:
  - Average deal value
  - Weekly transactions per merchant
  - Merchant payout percentage
  - Platform commission
  - Subscription fee assumptions
- **Separation**: Merchant recovery value ≠ Platform revenue

#### 5.4 Hawker Deferral

- **Phase 3 approach**:
  - Start with digitally ready stalls using QR payments
  - Partner with hawker centres, town councils
  - Mobile-first interface
  - Pre-set product templates
  - Group onboarding workshops

---

### 6. Evaluation Gaps

#### 6.1 No A/B Testing Framework

- **Production design**: Parallel model runs, compare prediction error, acceptance rate, recovery value

#### 6.2 No Merchant Feedback Loop

- **Required**: Feedback field for prediction accuracy
  - Too high / Too low
  - Useful / Not useful
  - Item not available
  - Discount too aggressive
  - Safety flag too strict

#### 6.3 No Outcome Tracking

- **Required**: Actual surplus, listed, sold, discarded, recovery, reason for unsold

#### 6.4 No Consumer Data

- **Positioning**: Consumer demand is Phase 4 validation, not MVP claim

---

### 7. Competitive Positioning

#### 7.1 Differentiation from Treatsure/Yindii

- Merchant-first cockpit (not consumer-first marketplace)
- Surplus prediction before listing
- Discount recommendation logic
- Food-safety rule gating
- Recovery simulation
- Merchant learning loop
- Upstream operating system for surplus decisions

#### 7.2 Switching Cost

- Accumulated merchant-specific data
- Historical sales and surplus patterns
- Discount preferences
- Recovery history
- Food-safety logs
- Outlet-level benchmarks
- Monthly waste and recovery reports

#### 7.3 Network Effects

- MVP value: single-sided merchant decision-support
- Consumer network: later growth accelerator, not starting requirement

---

## Disclaimer

This product hardening plan is part of the SurplusSense COC documentation. The MVP is not intended to be a full production system. It demonstrates the core AI/ML decision-support logic and establishes a credible roadmap toward a scalable platform.

---

## Final Decisions on Additional Gaps

### 1. PDPA Compliance

- **Decision**: MVP uses synthetic data only
- **Requirement**: Any real merchant or consumer pilot must comply with Singapore Personal Data Protection Act (PDPA)
- **Action**: Document PDPA requirements for production

### 2. POS Integration

- **Decision**: CSV upload for MVP; POS integration is future roadmap
- **Rationale**: Automated data capture is significant moat but requires partnership negotiations
- **Future**: Square, Lightspeed, iCHEF integration

### 3. Multi-tenancy

- **Decision**: Single-user prototype for MVP
- **Production design**:
  - `merchant_id` and `outlet_id` as isolation keys
  - Data isolation at database level
  - Role-based access control (admin, manager, staff)

### 4. Disaster Recovery

- **Decision**: Not implemented in MVP
- **Production requirements**:
  - Automated backups
  - Point-in-time recovery
  - Model artifact backup
  - Restore testing
  - Rollback procedures

### 5. Support Model

- **MVP**: Basic help text, tooltips, simple documentation
- **Production**: Email, in-app chat, WhatsApp support, enterprise SLA

### 6. Accessibility

- **Decision**: Apply basic principles; no formal WCAG claim
- **Requirement**: Full WCAG 2.2 AA compliance requires formal testing

### 7. Localization

- **Decision**: English only for MVP
- **Production**: EN/CN/MY/TA multilingual support as future requirement

### 8. Technical Stack

- **MVP**: Streamlit (fast interactive dashboard)
- **Production**: React/Next.js frontend, FastAPI backend, PostgreSQL, cloud deployment

### 9. MVP Success Metrics

- **Decision**: ML model must outperform simple baselines; dashboard must produce usable recommendations; target merchants can understand output and see business value
- **Metrics**:
  - Model beats baseline by measurable MAE improvement
  - Dashboard runs end-to-end without manual fixes
  - Food-safety rules working correctly
  - Merchants can test workflow with sample data

### 10. Exit Criteria for Phase 2

- **Decision**: MVP ready for merchant pilots when:
  - Model beats baseline performance
  - Dashboard runs end-to-end without manual fixes
  - Food-safety rules working
  - Merchants can test workflow using their own sample data

### 11. Key Assumptions

- Merchants are willing to share sales or surplus data
- Merchants see value in prediction-based decision support
- Cafés and bakeries have predictable surplus patterns
- Merchants may eventually pay for waste reduction, recovery tracking, or reporting features

### 12. ESG/Sustainability Reporting

- **Decision**: MVP includes basic waste-reduction and recovery metrics
- **Future**: Full NEA waste reporting or ESG disclosure automation in Phase 3+
- **MVP**: Basic metrics that can support sustainability reporting

### 13. Incumbent Response

- **Assumption**: Treatsure/Yindii may add merchant-side features if SurplusSense gains traction
- **Differentiation**: Deeper merchant intelligence, surplus prediction, discount recommendation, food-safety gating, recovery analytics
- **Positioning**: Not another consumer marketplace - upstream operating intelligence

---

_Document created 2026-04-25_
