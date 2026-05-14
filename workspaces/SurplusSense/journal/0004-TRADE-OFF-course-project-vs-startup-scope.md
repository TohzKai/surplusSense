---
type: TRADE-OFF
date: 2026-04-17
created_at: 2026-04-17T13:00:00+08:00
author: co-authored
session_id: analyze-phase
project: Food App
topic: Course project scope vs startup ambition — right-sizing ML for a 10-week timeline
phase: analyze
tags: [scope, ml, timeline, trade-off, mvp]
---

> **Historical note:** This journal was written during early project exploration under the "Food App" working title. The project was later renamed to SurplusSense and narrowed to a merchant-side decision-support cockpit. This entry is retained as process evidence.

# Course Project Scope vs Startup Ambition

## Decision

The red team surfaced a critical contradiction: the ML architecture describes a 14-20 week production roadmap, while the implementation plan allocates 4 weeks for ML in a 10-week course project. We chose to keep all four ML capabilities but right-size each to its simplest viable demonstration.

**What we keep**: Surplus prediction (XGBoost on synthetic data), recommendations (content-based filtering), dynamic pricing (rule-based time-decay), waste analytics (clustering + pattern detection).

**What we defer**: Ensemble models, reinforcement learning for pricing, collaborative filtering with contextual bandits, real-time model serving infrastructure, MLOps monitoring pipeline.

**Why this trade-off**: A course project needs to demonstrate ML depth across multiple capabilities (shows breadth of learning) while keeping each implementable. The production architecture serves as the "future vision" in the business presentation.

## For Discussion

1. Would the course be better served by going deep on one ML system (e.g., surplus prediction with full ensemble) rather than demonstrating four at surface level?
2. How do we present synthetic data results honestly — as "here's what the model would achieve" rather than "here's what it achieves"?
3. If a real merchant were recruited for the demo, would that change which ML capability to prioritize?
