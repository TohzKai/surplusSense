# ML Waste Analytics Specification

## Overview

Provides merchants with prescriptive waste analytics that go beyond descriptive dashboards. The system detects patterns, identifies anomalies, and generates actionable recommendations to reduce waste at source.

## Data Foundation

### Input Data

| Source                | Data                                           | Granularity          |
| --------------------- | ---------------------------------------------- | -------------------- |
| Platform transactions | Listing quantities, sell-through rates, prices | Per listing per day  |
| Surplus predictions   | Predicted vs. actual surplus                   | Per category per day |
| Merchant categories   | Batch sizes, shelf life, pricing               | Per category         |
| Weather               | Temperature, rainfall, humidity                | Daily                |
| Calendar              | Holidays, school holidays, events              | Daily                |

### Aggregated Metrics (computed daily per merchant per category)

| Metric             | Computation                                          |
| ------------------ | ---------------------------------------------------- |
| total_waste_units  | SUM(batch_size - quantity_sold) for expired listings |
| waste_ratio        | total_waste_units / SUM(batch_size)                  |
| revenue_lost       | SUM(original_price × waste_units) for expired items  |
| revenue_recovered  | SUM(current_price × quantity_sold) via platform      |
| sell_through_rate  | SUM(quantity_sold) / SUM(batch_size)                 |
| avg_discount_given | AVG(discount_pct) for sold items                     |
| avg_days_to_sell   | AVG(time from listing to last purchase)              |

## Analytics Capabilities

### 1. Waste Breakdown

- By category: What percentage of waste comes from each food category
- By day: Which days have highest waste
- By time period: Weekly, monthly trends

**Output example**:

```
Waste Breakdown (Last 30 Days)
├── Pastries: 42% (38 kg, S$520 lost)
├── Rice dishes: 28% (25 kg, S$340 lost)
├── Beverages: 15% (14 kg, S$95 lost)
└── Other: 15% (13 kg, S$120 lost)

Total: 90 kg wasted, S$1,075 potential revenue lost
```

### 2. Temporal Pattern Detection

- K-Means clustering on daily waste vectors (category × waste_quantity)
- Identifies merchant's "waste profile" from 4-6 standard profiles:
  - **Consistent over-producer**: High waste every day
  - **Weekend spike**: Waste concentrated on weekends
  - **Mid-week lull**: Tuesday-Thursday higher waste
  - **Weather-sensitive**: Waste correlates with weather
  - **Event-driven**: Waste spikes during nearby events
  - **Declining trend**: Waste decreasing over time (improving)

**Output example**:

```
Your waste profile: Weather-Sensitive + Weekend Spike
- Rainy days increase your waste by 35%
- Saturdays produce 40% more waste than average
```

### 3. Anomaly Detection

- Isolation Forest on daily waste quantities per category
- Flags days where waste significantly exceeded expected range
- Correlates anomalies with potential causes:
  - Weather events (rain, extreme heat)
  - Calendar events (holiday, school break)
  - Operational changes (new menu item, different batch size)
  - Listing issues (late listing creation, poor pricing)

**Output example**:

```
⚠ Anomaly Detected: April 12
Pastries waste: 28 units (expected: 12-18)
Possible causes:
- Heavy rain forecasted (70% above normal)
- No prediction listing created (manual listing at 4pm instead of 8am)
Recommendation: On rainy days, reduce pastry batch by 30% and list early
```

### 4. Prescriptive Recommendations

Recommendation types and confidence levels:

| Type                    | Example                                                                 | Confidence Required |
| ----------------------- | ----------------------------------------------------------------------- | ------------------- |
| **Batch optimization**  | "Reduce chicken rice batch on Tue/Thu by 3 portions"                    | High (>0.8)         |
| **Timing adjustment**   | "List pastries at 3pm instead of 5pm for better sell-through"           | Medium (>0.6)       |
| **Pricing suggestion**  | "Your pastries sell best at 55% discount — consider starting there"     | Medium (>0.6)       |
| **Weather-linked**      | "On rainy days, reduce all batch sizes by 15%"                          | High (>0.8)         |
| **Category focus**      | "Pastries account for 42% of waste — prioritize reducing this category" | High (>0.8)         |
| **Seasonal adjustment** | "December waste is typically 20% higher — prepare accordingly"          | Medium (>0.6)       |

**Recommendation format**:

```json
{
  "type": "batch_optimization",
  "category": "Pastries",
  "action": "Reduce batch size by 20% on weekdays",
  "expected_savings": "S$180/month",
  "confidence": 0.85,
  "evidence": "Based on 45 days of data. Weekday pastry waste averages 15 units (30% of batch). Reducing batch from 50 to 40 would maintain 95% order fulfillment.",
  "data_points": 45
}
```

### 5. Benchmarking

- Anonymous comparison against similar merchants
- Merchant segments by: cuisine type, size category, location type
- Percentile ranking: "Your waste rate is in the top 30% of similar bakeries"
- No raw data from other merchants shared — only aggregated benchmarks

## Dashboard Layout

### Overview Tab

- Key metrics: total waste (kg), waste ratio (%), revenue lost, revenue recovered
- Trend line: waste ratio over time (7-day moving average)
- Top 3 waste categories by volume

### Patterns Tab

- Day-of-week heatmap (category × day)
- Waste profile classification with explanation
- Correlation factors: what drives your waste

### Recommendations Tab

- Priority-sorted recommendation cards
- Each card: action, expected savings, confidence, evidence
- "Apply" button to track adoption (merchant marks as "Will do" / "Already doing" / "Not applicable")
- Adopted recommendations tracked for outcome measurement

### Impact Tab

- Cumulative waste reduction over time
- Revenue recovered through platform
- CO2 prevented, meals rescued
- Shareable impact report

## API Endpoints

| Method | Path                                                          | Description                    |
| ------ | ------------------------------------------------------------- | ------------------------------ |
| GET    | /api/v1/ml/analytics/{merchant_id}/overview                   | Key waste metrics              |
| GET    | /api/v1/ml/analytics/{merchant_id}/patterns                   | Detected patterns              |
| GET    | /api/v1/ml/analytics/{merchant_id}/anomalies                  | Anomaly list                   |
| GET    | /api/v1/ml/analytics/{merchant_id}/recommendations            | Prescriptive recommendations   |
| POST   | /api/v1/ml/analytics/{merchant_id}/recommendations/{id}/adopt | Mark recommendation adopted    |
| GET    | /api/v1/ml/analytics/{merchant_id}/impact                     | Sustainability impact metrics  |
| GET    | /api/v1/ml/analytics/{merchant_id}/benchmark                  | Anonymous benchmark comparison |

## Model Retraining

- Pattern detection: Monthly re-clustering with new data
- Anomaly detection: Continuous (Isolation Forest applied to each new day's data)
- Recommendations: Weekly regeneration with updated patterns and feedback
- Benchmarking: Quarterly recalculation of merchant segments
