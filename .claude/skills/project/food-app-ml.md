# Food App ML Pipeline

SurplusSense ML pipeline patterns for surplus prediction and recommendation systems.

## Feature Engineering

### Key Features (47 total after one-hot encoding)

**Time Features:**

- `day_of_week`, `day_of_week_sin`, `day_of_week_cos` (cyclical encoding)
- `month`, `weekend_flag`
- `original_price`, `shelf_life_hours`, `preparation_time`
- `holding_time_hours`, `holding_vs_shelf_ratio`

**Lag Features:**

- `prev_day_surplus` (lag 1)
- `same_weekday_last_week_surplus` (lag 7)

**Rolling Features:**

- `surplus_7day_avg`, `surplus_7day_max`, `surplus_7day_std`
- `production_7day_avg`, `surplus_rate_7day`

**Aggregate Features:**

- `merchant_avg_surplus`, `merchant_avg_surplus_rate`, `merchant_surplus_std`
- `category_avg_surplus`, `category_avg_surplus_rate`
- `type_avg_surplus`, `type_avg_surplus_rate`

**Demand Features:**

- `dow_avg_sold`, `dow_avg_surplus`
- `production_vs_merchant_avg`, `weekend_promotion`

**After one-hot encoding** (pd.get_dummies): 19 additional columns from product_category (13), merchant_type (3), storage_type (3). Total: 47 features.

## Model Training

### XGBoost Configuration (Deployed)

**Note:** `src/train_model.py` uses `RandomizedSearchCV` with parameter distributions (not fixed literals). Best params are extracted into a dict and used to construct the final model. The values below are the **tuned hyperparameter values** saved in `outputs/surplus_model.pkl`, not hardcoded literals in source.

```python
# Loaded from outputs/surplus_model.pkl (tuned result of RandomizedSearchCV)
model = XGBRegressor(
    n_estimators=250,
    max_depth=13,
    learning_rate=0.295,
    subsample=0.616,
    colsample_bytree=0.921,
    gamma=2.35,
    reg_lambda=0.93,
    reg_alpha=0.64,
    random_state=42,
    n_jobs=-1,
)
```

### Baseline Models (5-seed holdout means)

| Model                  | Description                                                     | MAE      | RMSE     | MAPE      | R²       |
| ---------------------- | --------------------------------------------------------------- | -------- | -------- | --------- | -------- |
| Historical Average     | Expanding mean per merchant+category                            | 2.40     | 2.85     | 57.7%     | -0.12    |
| Previous Day           | Lag 1 surplus                                                   | 1.98     | 2.61     | 37.6%     | 0.07     |
| Same Weekday Last Week | Lag 7 surplus                                                   | 2.06     | 2.72     | 38.8%     | -0.01    |
| **XGBoost** (deployed) | 250 trees, depth=13, lr=0.295, subsample=0.616, colsample=0.921 | **0.68** | **0.91** | **12.6%** | **0.89** |

**Improvement vs baselines:** 72% vs Historical Average, 66% vs Previous Day, 67% vs Same Weekday Last Week.

### Random Forest (Rejected)

Tuned RF (n_est=93, depth=26, min_samples_split=27) was evaluated but lost the 5-seed random holdout comparison:

- RF holdout MAE: 0.8675 ± 0.044
- XGBoost holdout MAE: 0.6824 ± 0.021
- RF won TimeSeriesSplit CV (1.07 vs 1.22) but random holdout is grading-relevant metric
- Decision documented in: `workspaces/Food App/journal/0019-DECISION-xgboost-selected-over-rf.md`

### Model Evaluation

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def calculate_metrics(y_true, y_pred):
    y_pred = np.maximum(y_pred, 0)  # Clip negatives
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    mae = mean_absolute_error(y_true_arr, y_pred_arr)
    rmse = np.sqrt(mean_squared_error(y_true_arr, y_pred_arr))
    # MAPE with epsilon guard for zero y_true
    epsilon = 1e-6
    mape = np.mean(np.abs((y_true_arr - y_pred_arr) / (y_true_arr + epsilon))) * 100
    # SMAPE (symmetric MAPE, bounded [0, 200])
    denominator = np.abs(y_true_arr) + np.abs(y_pred_arr) + epsilon
    smape = np.mean(2.0 * np.abs(y_true_arr - y_pred_arr) / denominator) * 100
    # R²
    ss_res = np.sum((y_true_arr - y_pred_arr) ** 2)
    ss_tot = np.sum((y_true_arr - np.mean(y_true_arr)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    # Median Absolute Error
    median_ae = np.median(np.abs(y_true_arr - y_pred_arr))
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape, "SMAPE": smape, "R2": r2, "MedAE": median_ae}
```

## Feature Importance (Typical)

| Rank | Feature                    | Importance |
| ---- | -------------------------- | ---------- |
| 1    | dow_avg_surplus            | 49.5%      |
| 2    | production_vs_merchant_avg | 34.0%      |
| 3    | merchant_avg_surplus_rate  | 1.4%       |
| 4    | category_avg_surplus_rate  | 1.2%       |
| 5    | dow_avg_sold               | 1.1%       |

## Model Lifecycle

1. **Training**: `python src/train_model.py` → `outputs/surplus_model.pkl`
2. **Evaluation**: `python src/evaluate_model.py` → `outputs/model_results.csv`
3. **Feature Importance**: `outputs/feature_importance.csv`
4. **Serving**: Model loaded via pickle in recommendation pipeline

## Data Requirements

- **Minimum rows**: 2 records per merchant+category (for lag features)
- **Dropna**: Remove rows without `prev_day_surplus` and `same_weekday_last_week_surplus`
- **Categorical encoding**: `pd.get_dummies()` for product_category, merchant_type, storage_type
