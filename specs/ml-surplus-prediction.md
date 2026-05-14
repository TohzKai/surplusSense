# ML Surplus Prediction Specification

> **Phase 2 — Not part of final submitted MVP.** The detailed ML model architecture and feature engineering spec is Phase 2 planning. The actual implemented model (XGBoost, 46 features, temporal holdout) is documented in `src/train_model.py`, `src/feature_engineering.py`, and `outputs/model_metadata.json`.

## Overview

Predicts daily surplus quantities per merchant per food category to enable auto-generated listings and proactive waste reduction. The system learns from historical transaction data, weather, events, and merchant-specific patterns.

## Input Features

| Feature              | Type        | Source       | Engineering Notes                              |
| -------------------- | ----------- | ------------ | ---------------------------------------------- |
| day_of_week          | int (0-6)   | Calendar     | One-hot encoded                                |
| is_holiday           | bool        | Calendar API | Singapore public holidays                      |
| is_school_holiday    | bool        | Calendar API | MOE school holiday calendar                    |
| month                | int (1-12)  | Calendar     | Cyclical encoding (sin/cos)                    |
| temperature_avg      | float       | Weather API  | Degrees Celsius                                |
| rainfall_mm          | float       | Weather API  | Daily total                                    |
| humidity_avg         | float       | Weather API  | Percentage                                     |
| weather_category     | categorical | Weather API  | sunny, cloudy, rainy, thunderstorm             |
| sales_7d_avg         | float       | Platform     | Avg daily sales (same category, last 7 days)   |
| sales_same_day_lw    | float       | Platform     | Sales same day last week                       |
| surplus_7d_avg       | float       | Platform     | Avg daily surplus (same category, last 7 days) |
| surplus_same_day_lw  | float       | Platform     | Surplus same day last week                     |
| surplus_yesterday    | float       | Platform     | Yesterday's surplus for this category          |
| batch_size           | int         | Platform     | Merchant's typical batch size for category     |
| merchant_tenure_days | int         | Platform     | Days since merchant joined                     |
| nearby_events_count  | int         | Events API   | Events within 2km                              |
| is_payday_week       | bool        | Calendar     | Approximation: 1st and 15th ±3 days            |

## Target Variable

- `surplus_quantity` (integer, units per category per day)
- Alternative formulation: `surplus_ratio` = surplus / batch_size (float 0-1)

## Model Architecture

### Phase 1: Rule-Based Baseline

```
predicted_surplus = category_avg_surplus × day_of_week_multiplier × weather_multiplier
```

- Category averages from all merchants in same category
- Day-of-week multipliers from historical patterns
- Weather multiplier: rainy day = 1.2x surplus, sunny = 1.0x

### Phase 2: XGBoost (Primary Model)

- Objective: reg:squarederror
- Hyperparameters: max_depth=6, learning_rate=0.1, n_estimators=200
- Feature importance tracked for merchant trust
- Trained per-merchant after 4+ weeks of data
- Trained globally (all merchants) for cold start

### Phase 3: Prophet (Time-Series Component)

- Captures weekly seasonality and trend
- Provides prediction intervals (80% and 95% confidence)
- Used as secondary signal in ensemble

### Ensemble (Phase 2+)

```python
final_prediction = (
    0.65 × xgboost_prediction +
    0.35 × prophet_prediction
)
# Weights optimized per-merchant based on validation MAE
```

## Training Pipeline

### Data Requirements

| Stage      | Data                     | Quality                     |
| ---------- | ------------------------ | --------------------------- |
| Cold start | None (merchant-specific) | Rule-based only             |
| 2-4 weeks  | Limited merchant history | Rule-based + global XGBoost |
| 4-8 weeks  | Sufficient per-merchant  | Merchant-specific XGBoost   |
| 8+ weeks   | Rich history             | Ensemble model              |

### Training Schedule

- **Global model**: Retrained weekly (Sunday midnight)
- **Per-merchant model**: Retrained daily if merchant has 4+ weeks of data
- **Feature computation**: Daily batch job (6am SGT) computing all features for previous day

### Validation Strategy

- Time-series split: Train on first 80% of dates, validate on last 20%
- Walk-forward validation for final evaluation
- No random train/test split (time-series data requires temporal ordering)

## Serving

### Prediction Generation

- Nightly batch job generates predictions for next day
- Predictions stored in MLSurplusPrediction table
- Morning: Predictions pushed to merchant dashboard

### API

```
GET /api/v1/ml/surplus-prediction?merchant_id={id}&date={date}
→
{
  "predictions": [
    {
      "category_id": "uuid",
      "category_name": "Chicken Rice",
      "predicted_surplus": 12,
      "confidence": 0.82,
      "suggested_price": 3.50,
      "prediction_interval": {"low": 7, "high": 17}
    }
  ],
  "model_version": "xgboost_v2_prophet_v1",
  "generated_at": "2026-04-17T06:00:00+08:00"
}
```

### Actual Surplus Recording

- End of each pickup window: system calculates actual surplus
- `actual_surplus = quantity_total - quantity_sold`
- Stored in MLSurplusPrediction.actual_surplus
- Feeds back into training data for continuous improvement

## Evaluation Metrics and Targets

| Metric               | Phase 1 Target | Phase 2 Target | Phase 3 Target |
| -------------------- | -------------- | -------------- | -------------- |
| MAE (units)          | < 5            | < 3            | < 2            |
| MAPE (%)             | < 40           | < 25           | < 20           |
| Directional accuracy | > 70%          | > 80%          | > 85%          |
| Coverage             | 100% (rules)   | > 90%          | > 95%          |

## Edge Cases

| Case                              | Handling                                                           |
| --------------------------------- | ------------------------------------------------------------------ |
| New merchant, zero history        | Use category-level rule-based averages                             |
| Merchant closes unexpectedly      | Prediction for closed day = 0 (no listing generated)               |
| Holiday not in calendar           | Model detects anomaly, fallback to day-of-week average             |
| Extreme weather (typhoon warning) | Weather multiplier = 1.5x, merchant notified of unusual prediction |
| Model predicts zero surplus       | No listing generated, merchant can still create manual listing     |
| Prediction significantly wrong    | Merchant feedback tracked; model retrained with corrected data     |
