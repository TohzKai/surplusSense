# DECISION: Codified Food App ML Patterns

**Type**: DECISION
**Date**: 2026-04-26
**Status**: Closed

## Decision

Created project-specific agents and skills for SurplusSense Food App ML patterns:

### Agents Created

| Agent               | File                                          | Purpose                                                                      |
| ------------------- | --------------------------------------------- | ---------------------------------------------------------------------------- |
| `food-app-analyst`  | `.claude/agents/project/food-app-analyst.md`  | ML pipeline analysis, food safety compliance, recommendation system analysis |
| `food-app-reviewer` | `.claude/agents/project/food-app-reviewer.md` | Code review, quality verification, ML implementation correctness             |

### Skills Created/Updated

| Skill              | File                                         | Purpose                                                                                        |
| ------------------ | -------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `food-app-ml`      | `.claude/skills/project/food-app-ml.md`      | Feature engineering (29 features), Random Forest training, baseline models, evaluation metrics |
| `food-app-safety`  | `.claude/skills/project/food-app-safety.md`  | SFA compliance rules, holding/pickup thresholds, check_item_safety API                         |
| `food-app-pricing` | `.claude/skills/project/food-app-pricing.md` | Discount tiers, recovery calculations, listing time recommendations                            |

### SKILL.md Updated

Updated `.claude/skills/project/SKILL.md` with quick reference guide including:

- Core import patterns
- Safety thresholds table
- Discount tiers table
- MVP scope clarification

## Rationale

The Food App is a downstream USE repo requiring project-specific knowledge capture for:

1. ML pipeline patterns (unique to this codebase)
2. Food safety compliance (Singapore SFA-specific)
3. Discount recommendation logic (business-specific rules)

## Notes

- This is a downstream USE repo - no upstream proposal created
- Learning digest updated at `.claude/learning/learning-codified.json`
- All artifacts validated with correct frontmatter and within line limits

---

_Created during /codify phase_
