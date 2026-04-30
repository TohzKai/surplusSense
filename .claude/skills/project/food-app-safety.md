# Food App Safety Rules

SurplusSense food safety rules for SFA compliance in Singapore.

## Safety Thresholds

### Maximum Holding Times (hours)

| Storage Type | Max Holding | Notes               |
| ------------ | ----------- | ------------------- |
| Ambient      | 4           | Room temperature    |
| Refrigerated | 8           | Cold chain items    |
| Frozen       | 24          | Longest flexibility |

### Maximum Pickup Windows (hours)

| Storage Type | Max Pickup Window |
| ------------ | ----------------- |
| Ambient      | 2                 |
| Refrigerated | 4                 |
| Frozen       | 12                |

### Minimum Shelf Life by Category (hours)

| Category           | Min Remaining |
| ------------------ | ------------- |
| Rice Dishes        | 2             |
| Noodle Dishes      | 2             |
| Coffee & Beverages | 2             |
| Sandwiches         | 3             |
| Bento Sets         | 3             |
| Soup & Sides       | 3             |
| Pastries           | 4             |
| Salads             | 4             |
| Desserts           | 4             |
| Tarts              | 4             |
| Bread              | 6             |
| Cakes              | 8             |
| Cookies            | 12            |

## Safety Check Types

### `check_holding_time`

Verifies food hasn't been held too long before listing.

```python
def check_holding_time(holding_time_hours: float, storage_type: str) -> SafetyCheck:
    # Ambient > 4h = BLOCK
    # Ambient > 3h (75%) = CAUTION
```

### `check_remaining_shelf_life`

Verifies sufficient shelf life remains for consumer pickup.

```python
def check_remaining_shelf_life(
    shelf_life_hours: float,
    holding_time_hours: float,
    product_category: str,
) -> SafetyCheck:
    # remaining = shelf_life - holding_time
    # If remaining <= 0 or < category_min = BLOCK
```

### `check_pickup_window`

Verifies pickup window is safe for storage type.

```python
def check_pickup_window(pickup_window_hours: float, storage_type: str) -> SafetyCheck:
    # Ambient > 2h = BLOCK
    # Refrigerated > 4h = BLOCK
```

### `check_storage_type_appropriateness`

Verifies storage type matches food category requirements.

```python
# Appropriate storage examples:
# Rice Dishes: Ambient only
# Sandwiches: Refrigerated only
# Bento Sets: Refrigerated only
# Pastries: Ambient or Refrigerated
```

### `check_preparation_time`

Flags long preparation times as safety indicators.

```python
# > 60 minutes = CAUTION
# Long assembly time may indicate reduced shelf life
```

## Usage Pattern

```python
from src.food_safety_rules import check_item_safety, format_safety_display

result = check_item_safety(
    product_category="Pastries",
    preparation_time=5,
    holding_time_hours=2,
    storage_type="Ambient",
    shelf_life_hours=48,
    pickup_window_hours=2,
)

# result.status: "SAFE", "CAUTION", or "BLOCK"
# result.checks: List[SafetyCheck]
# result.flags: List[str] of warning messages
```

## Return Values

### SafetyResult

```python
@dataclass
class SafetyResult:
    status: str           # "SAFE", "CAUTION", "BLOCK"
    overall_message: str  # Human-readable summary
    checks: List[SafetyCheck]  # Individual check results
    flags: List[str]     # Warning messages
```

### SafetyCheck

```python
@dataclass
class SafetyCheck:
    name: str      # e.g., "holding_time", "remaining_shelf_life"
    passed: bool   # True if check passed
    severity: str  # "BLOCK", "CAUTION", "INFO"
    message: str  # Human-readable message
    details: str  # Detailed explanation
```

## High-Risk Categories

These require extra scrutiny:

```python
HIGH_RISK_CATEGORIES = [
    "Rice Dishes",
    "Noodle Dishes",
    "Bento Sets",
    "Salads",
    "Sandwiches",
]
```

## Danger Zone

Food safety danger zone: **2 hours** between 4°C and 60°C.

```python
DANGER_ZONE_HOURS = 2
```

## SFA Compliance Notes

- Use-by dates: **BLOCK** if expired
- Best-before dates: Consumer disclosure required if past
- SFA license verification at merchant onboarding
- Temperature control confirmation for cold chain items
