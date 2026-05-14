---
type: DISCOVERY
date: 2026-04-17
created_at: 2026-04-17T12:00:00+08:00
author: agent
session_id: analyze-phase
project: Food App
topic: ML data moat as primary differentiator in food waste marketplace
phase: analyze
tags: [ml, competitive-advantage, data-moat, food-waste]
---

> **Historical note:** This journal was written during early project exploration under the "Food App" working title. The project was later renamed to SurplusSense and narrowed to a merchant-side decision-support cockpit. This entry is retained as process evidence.

# ML Data Moat as Primary Differentiator

## Finding

The food waste reduction app market globally has no player combining marketplace functionality with ML-driven surplus prediction, dynamic pricing, and prescriptive analytics. Too Good To Go (global leader, 75M+ users) uses a completely manual approach — merchants set quantities and prices with zero ML assistance. This creates a clear window for an ML-first entrant.

The key insight is that the **data moat is self-reinforcing**: more transactions → better surplus predictions → higher sell-through rates → more merchant trust → more merchants → more transactions. Each prediction cycle improves accuracy, creating compounding advantage that is expensive for competitors to replicate.

However, the cold-start problem is severe. New merchants need 4-8 weeks of data before ML predictions outperform simple rules. The platform must provide immediate value through rule-based features while collecting data to activate ML.

## For Discussion

1. What if a well-funded competitor (Grab, Deliveroo) added food surplus as a feature — how does the data moat hold against their existing merchant network and transaction data?
2. Should the MVP focus entirely on merchant-side value (surplus prediction + analytics) before building the consumer marketplace, to ensure data collection starts before needing consumer demand?
3. Is the 10-week timeline realistic for delivering all 4 ML capabilities with meaningful accuracy, or should we cut to 2 (surplus prediction + recommendations) for the course project?
