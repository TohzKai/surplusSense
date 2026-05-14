---
type: CONNECTION
date: 2026-04-17
created_at: 2026-04-17T12:15:00+08:00
author: agent
session_id: analyze-phase
project: Food App
topic: ML features create both revenue and retention flywheels
phase: analyze
tags: [ml, retention, flywheel, merchant-value]
---

> **Historical note:** This journal was written during early project exploration under the "Food App" working title. The project was later renamed to SurplusSense and narrowed to a merchant-side decision-support cockpit. This entry is retained as process evidence.

# ML Features Connect Revenue to Retention

## Finding

The analysis treats ML features as separate capabilities, but their real power is in how they connect to create a retention flywheel:

1. **Surplus prediction** → reduces merchant effort → increases merchant engagement → generates more data
2. **Dynamic pricing** → increases sell-through → increases merchant revenue → increases merchant retention
3. **Waste analytics** → provides prescriptive insights → reduces waste at source → increases merchant dependency on platform
4. **Recommendations** → increases consumer conversion → increases sell-through → feeds back into pricing and prediction data

The key connection: **prescriptive waste analytics** is more valuable than marketplace sales because it addresses the root cause. A merchant who follows ML recommendations to reduce waste at source saves money even on days when no surplus is sold through the platform. This makes the platform valuable even without consumer demand, solving the chicken-and-egg marketplace bootstrapping problem.

This means the merchant experience should lead with analytics, not listings. The dashboard should open on insights, not on today's sales.

## For Discussion

1. If prescriptive analytics is the real value driver, should the platform offer a free "analytics only" tier to merchants, with marketplace sales as a premium feature?
2. Does reducing waste at source conflict with marketplace revenue? (If merchants waste less, they have less surplus to sell.)
3. Counterfactual: What if we built analytics-only (no marketplace) — would that be a viable standalone product for the SMU ML project?
