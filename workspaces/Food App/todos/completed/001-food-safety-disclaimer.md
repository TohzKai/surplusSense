# Food Safety Disclaimer

**Priority**: CRITICAL
**Status**: DONE
**Type**: Product Gap

## Task

Add explicit food safety disclaimer to the Streamlit dashboard and executive report.

## Requirement

Display prominently:

> "The food-safety status shown by SurplusSense is a decision-support indicator based on the information entered by the merchant. It does not certify or guarantee food safety. Merchants remain responsible for proper food handling, storage, labelling, and compliance with applicable food-safety requirements."

## Files Updated

- `app/streamlit_app.py` — sidebar banner + Food Safety card caption
- `docs/executive_report_notes.md` — food safety limitations section updated

## Verification

### Sidebar banner

- Location: bottom of sidebar, after Time selector
- CSS class `.sidebar-disclaimer`: font-size 11px, color #6B7280, padding 8px, border-top in var(--border)
- Text: "⚠ Advisory only. Food safety recommendations are based on general principles..."

### Food Safety card caption

- Location: inside `col_safety`, below `st.expander("View Safety Checks")`
- Text: same disclaimer as inline caption

### Executive report

- `docs/executive_report_notes.md` § Food Safety Limitations — disclaimer text added verbatim
- Model performance table also updated to reflect XGBoost results (was stale "Random Forest" entry)
