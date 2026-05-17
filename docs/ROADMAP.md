# SurplusSense Roadmap

This roadmap documents planned enhancements beyond the current pilot-ready submission.

---

## Current Submission Scope

- Working Streamlit decision-support app
- XGBoost surplus prediction model with temporal holdout validation
- Merchant-facing 6-step recommendation workflow
- Food-safety gating (BLOCK/CAUTION/SAFE)
- Synthetic pilot dataset (4,027 records, 15 merchants, 13 categories, 90-day window)
- Executive report and COC decision log

---

## Pilot Enhancements (Post-Submission)

These are the logical next steps for a merchant pilot:

| Enhancement | Description | Priority |
|-------------|-------------|----------|
| POS / inventory integration | Connect to merchant POS or inventory system for automated item entry | HIGH |
| Real merchant data evaluation | Run SurplusSense on real merchant records; compare predictions against actual surplus | HIGH |
| Recommendation feedback loop | Merchant indicates whether prediction/recommendation was accurate; log for model improvement | MEDIUM |
| Food-safety expert review | Validate safety rules against SFA guidance; refine BLOCK/CAUTION thresholds | CRITICAL |
| Cold-start profile form | Merchant profile input form for new outlets without historical data | MEDIUM |
| Price sensitivity survey | Test SGD 99–299/month price points with pilot merchants | MEDIUM |

---

## Production Enhancements (Beyond Pilot)

| Enhancement | Description |
|-------------|-------------|
| User authentication | Multi-tenant login for merchant teams |
| Data connectors | Pre-built integrations for common POS/inventory systems |
| Forecast drift monitoring | Alert when model accuracy degrades below threshold |
| Human override audit log | Track when merchants override recommendations and why |
| Merchant-specific retraining | Periodic model retraining on accumulated real merchant data |
| Annual seasonality features | 12–24 months of data for CNY, Ramadan, school holidays, weather patterns |

---

## Assumptions

- All current estimates are from synthetic data; pilot validation required before commercial deployment
- Safety rules are prototype-level; expert review required before production
- Pricing (SGD 99–299/month) is a pilot-stage hypothesis, not an audited figure
