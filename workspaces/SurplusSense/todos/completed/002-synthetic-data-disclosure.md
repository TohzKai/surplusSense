# Synthetic Data Disclosure

**Priority**: HIGH
**Status**: DONE
**Type**: Product Gap

## Task

Add "Demo data" pill/badge to the top header bar next to the "● Live" status pill.

## Requirement

- Background: warning color tint (#F59E0B22)
- Text: warning color (#F59E0B)
- Content: "Demo data"
- 11px, rounded-full, padding 4px 10px
- Hover tooltip: "This MVP uses synthetic data. Production deployment requires real merchant data and pilot validation."

## Files Updated

- `app/streamlit_app.py` — CSS class `.demo-pill` + HTML span in app header + hover tooltip
- `docs/executive_report_notes.md` — synthetic data limitation already documented (no change needed)

## Verification

- `.demo-pill` CSS: `background: #F59E0B22`, `color: #F59E0B`, `border-radius: 9999px`, `font-size: 11px`, `padding: 4px 10px`
- HTML: `<span class="demo-pill" title="This MVP uses synthetic data...">Demo data</span>`
- Placed in `.app-header-right` alongside existing `.status-pill`
- Both pills sit side-by-side via `gap: 16px` in `.app-header-right`
- Executive report already had synthetic data limitation section — no duplicate needed
