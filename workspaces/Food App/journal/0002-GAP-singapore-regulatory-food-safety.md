---
type: GAP
date: 2026-04-17
created_at: 2026-04-17T12:10:00+08:00
author: agent
session_id: analyze-phase
project: Food App
topic: Singapore regulatory and food safety compliance for surplus food sales
phase: analyze
tags: [food-safety, sfa, regulations, singapore, gap]
---

# Singapore Food Safety Regulatory Gaps

## Finding

While the analysis identifies that selling near-expiry food is legal in Singapore (with use-by vs. best-before distinction), several regulatory details need validation:

1. **SFA license verification**: The spec assumes automated verification against an SFA database. It's unclear if SFA provides a public API for license validation, or if this must be manual.
2. **Hawker stall licensing**: Hawker stalls operate under different SFA rules than restaurants. The platform's merchant onboarding must handle these differences.
3. **Temperature control liability**: If a merchant sells a temperature-sensitive item and it causes food poisoning, the platform's liability is unclear. The food safety spec requires merchant confirmation of temperature control, but doesn't address platform liability.
4. **PDPA compliance**: Consumer location data, purchase history, and behavioral data for ML training must comply with Singapore's Personal Data Protection Act. The specs don't address consent, data retention, or anonymization requirements.

## For Discussion

1. Should we require merchants to carry food liability insurance as a platform condition, or is merchant self-certification sufficient for MVP?
2. Can we defer PDPA compliance documentation until after MVP, or should data collection consent be designed into the onboarding flow from day one?
3. Is hawker stall inclusion worth the additional regulatory complexity for MVP, or should we target restaurants/cafes/bakeries first?
