#!/usr/bin/env python3
"""
SurplusSense Food Safety Rule Engine
=====================================
Rule-based food safety checks before surplus food is listed or recommended.

Safety checks:
- preparation_time: Maximum allowed prep time for surplus listing
- holding_time: Maximum allowed holding time before listing
- storage_type: Appropriate storage for food type
- shelf_life: Remaining shelf life must be sufficient
- pickup_window: Consumer pickup must occur within safe window

Status levels:
- SAFE: Item can be listed
- CAUTION: Item can be listed with warnings
- BLOCK: Item should not be listed for safety reasons
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

# Maximum holding times by storage type (hours)
# After this, food safety cannot be guaranteed
MAX_HOLDING_TIMES = {
    "Ambient": 4,      # Room temperature food must be sold quickly
    "Refrigerated": 8,  # Refrigerated items have more time
    "Frozen": 24,      # Frozen items are most flexible
}

# Maximum pickup windows by storage type (hours)
# Time from listing to consumer pickup
MAX_PICKUP_WINDOWS = {
    "Ambient": 2,
    "Refrigerated": 4,
    "Frozen": 12,
}

# Minimum remaining shelf life by category (hours)
# Food must have at least this much shelf life left when listed
MIN_REMAINING_SHELF_LIFE = {
    "Coffee & Beverages": 2,
    "Pastries": 4,
    "Sandwiches": 3,
    "Salads": 4,
    "Desserts": 4,
    "Bread": 6,
    "Cakes": 8,
    "Cookies": 12,
    "Tarts": 4,
    "Rice Dishes": 2,
    "Noodle Dishes": 2,
    "Bento Sets": 3,
    "Soup & Sides": 3,
}

# High-risk categories requiring extra scrutiny
HIGH_RISK_CATEGORIES = [
    "Rice Dishes",
    "Noodle Dishes",
    "Bento Sets",
    "Salads",
    "Sandwiches",
]

# Temperature danger zone (hours)
# Time food can spend between 4°C and 60°C before becoming unsafe
DANGER_ZONE_HOURS = 2


@dataclass
class SafetyCheck:
    """Individual safety check result."""
    name: str
    passed: bool
    severity: str  # "BLOCK", "CAUTION", "INFO"
    message: str
    details: str = ""


@dataclass
class SafetyResult:
    """Overall safety assessment result."""
    status: str  # "SAFE", "CAUTION", "BLOCK"
    overall_message: str
    checks: List[SafetyCheck]
    flags: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "overall_message": self.overall_message,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "severity": c.severity,
                    "message": c.message,
                    "details": c.details,
                }
                for c in self.checks
            ],
            "flags": self.flags,
        }


def check_holding_time(
    holding_time_hours: float,
    storage_type: str,
) -> SafetyCheck:
    """
    Check if holding time is within safe limits.

    Ambient food should not be held more than 4 hours.
    Refrigerated food should not be held more than 8 hours.
    Frozen food should not be held more than 24 hours.
    """
    max_holding = MAX_HOLDING_TIMES.get(storage_type, 4)

    if holding_time_hours > max_holding:
        return SafetyCheck(
            name="holding_time",
            passed=False,
            severity="BLOCK",
            message=f"Holding time {holding_time_hours:.1f}h exceeds maximum {max_holding}h for {storage_type}",
            details=f"Food held at {storage_type.lower()} temperature for {holding_time_hours:.1f} hours. "
                    f"Maximum safe holding time is {max_holding}h.",
        )
    elif holding_time_hours > max_holding * 0.75:
        return SafetyCheck(
            name="holding_time",
            passed=True,
            severity="CAUTION",
            message=f"Holding time {holding_time_hours:.1f}h is approaching limit ({max_holding}h max)",
            details="Food should be listed and sold soon.",
        )
    else:
        return SafetyCheck(
            name="holding_time",
            passed=True,
            severity="INFO",
            message=f"Holding time {holding_time_hours:.1f}h is within safe limits ({max_holding}h max)",
            details="No safety concern.",
        )


def check_remaining_shelf_life(
    shelf_life_hours: float,
    holding_time_hours: float,
    product_category: str,
) -> SafetyCheck:
    """
    Check if remaining shelf life is sufficient for listing and consumer use.
    """
    remaining_life = shelf_life_hours - holding_time_hours
    min_required = MIN_REMAINING_SHELF_LIFE.get(product_category, 4)

    if remaining_life <= 0:
        return SafetyCheck(
            name="remaining_shelf_life",
            passed=False,
            severity="BLOCK",
            message=f"Product shelf life EXPIRED ({remaining_life:.1f}h remaining)",
            details=f"Shelf life: {shelf_life_hours:.0f}h, Holding time: {holding_time_hours:.1f}h. "
                    f"Product is no longer safe for sale.",
        )
    elif remaining_life < min_required:
        return SafetyCheck(
            name="remaining_shelf_life",
            passed=False,
            severity="BLOCK",
            message=f"Insufficient remaining shelf life ({remaining_life:.1f}h < {min_required}h required)",
            details=f"Category {product_category} requires minimum {min_required}h shelf life. "
                    f"Consumer needs time to transport and consume before expiry.",
        )
    elif remaining_life < min_required * 1.5:
        return SafetyCheck(
            name="remaining_shelf_life",
            passed=True,
            severity="CAUTION",
            message=f"Remaining shelf life {remaining_life:.1f}h is acceptable but limited",
            details=f"Recommend immediate listing and fast consumer pickup.",
        )
    else:
        return SafetyCheck(
            name="remaining_shelf_life",
            passed=True,
            severity="INFO",
            message=f"Remaining shelf life {remaining_life:.1f}h is adequate",
            details=f"{remaining_life - min_required:.1f}h buffer beyond minimum.",
        )


def check_pickup_window(
    pickup_window_hours: float,
    storage_type: str,
) -> SafetyCheck:
    """
    Check if the proposed pickup window is safe.
    """
    max_pickup = MAX_PICKUP_WINDOWS.get(storage_type, 2)

    if pickup_window_hours > max_pickup:
        return SafetyCheck(
            name="pickup_window",
            passed=False,
            severity="BLOCK",
            message=f"Pickup window {pickup_window_hours:.1f}h exceeds safe limit ({max_pickup}h) for {storage_type}",
            details=f"Consumer must pickup within {max_pickup}h for {storage_type.lower()} items.",
        )
    elif pickup_window_hours > max_pickup * 0.7:
        return SafetyCheck(
            name="pickup_window",
            passed=True,
            severity="CAUTION",
            message=f"Pickup window {pickup_window_hours:.1f}h is acceptable but tight",
            details=f"Recommend setting pickup window to {max_pickup}h maximum.",
        )
    else:
        return SafetyCheck(
            name="pickup_window",
            passed=True,
            severity="INFO",
            message=f"Pickup window {pickup_window_hours:.1f}h is appropriate for {storage_type}",
            details="No safety concern.",
        )


def check_storage_type_appropriateness(
    product_category: str,
    storage_type: str,
) -> SafetyCheck:
    """
    Check if storage type is appropriate for the product category.
    """
    # Define appropriate storage for each category
    APPROPRIATE_STORAGE = {
        "Coffee & Beverages": ["Ambient", "Refrigerated"],
        "Pastries": ["Ambient", "Refrigerated"],
        "Sandwiches": ["Refrigerated"],
        "Salads": ["Refrigerated"],
        "Desserts": ["Refrigerated", "Frozen"],
        "Bread": ["Ambient", "Refrigerated"],
        "Cakes": ["Refrigerated", "Ambient"],
        "Cookies": ["Ambient", "Refrigerated"],
        "Tarts": ["Refrigerated", "Ambient"],
        "Rice Dishes": ["Ambient"],  # Typically served ambient but time-critical
        "Noodle Dishes": ["Ambient"],
        "Bento Sets": ["Refrigerated"],
        "Soup & Sides": ["Refrigerated", "Ambient"],
    }

    appropriate = APPROPRIATE_STORAGE.get(product_category, ["Ambient", "Refrigerated"])

    if storage_type not in appropriate:
        return SafetyCheck(
            name="storage_type",
            passed=False,
            severity="CAUTION",
            message=f"{storage_type} storage may not be optimal for {product_category}",
            details=f"Recommended storage: {', '.join(appropriate)}.",
        )
    else:
        return SafetyCheck(
            name="storage_type",
            passed=True,
            severity="INFO",
            message=f"{storage_type} storage is appropriate for {product_category}",
            details="No concern.",
        )


def check_preparation_time(product_category: str, preparation_time: int) -> SafetyCheck:
    """
    Check if preparation time introduces safety concerns.

    Long prep times (e.g., foods that sit assembled for long periods)
    can be a risk indicator.
    """
    # Maximum safe assembly-to-sale time (rough indicator)
    MAX_ASSEMBLY_TIME = 60  # minutes

    if preparation_time > MAX_ASSEMBLY_TIME:
        return SafetyCheck(
            name="preparation_time",
            passed=True,
            severity="CAUTION",
            message=f"Long preparation time ({preparation_time}min) - verify freshness",
            details="Food prepared far in advance may have reduced shelf life.",
        )
    else:
        return SafetyCheck(
            name="preparation_time",
            passed=True,
            severity="INFO",
            message=f"Preparation time {preparation_time}min is normal",
            details="No concern.",
        )


def check_item_safety(
    product_category: str,
    preparation_time: int,
    holding_time_hours: float,
    storage_type: str,
    shelf_life_hours: float,
    pickup_window_hours: float = 2,
) -> SafetyResult:
    """
    Perform comprehensive safety check on a surplus item.

    Parameters:
        product_category: Product category name
        preparation_time: Prep time in minutes
        holding_time_hours: Hours food has been held
        storage_type: Storage condition (Ambient/Refrigerated/Frozen)
        shelf_life_hours: Total shelf life in hours
        pickup_window_hours: Proposed consumer pickup window

    Returns:
        SafetyResult with overall status and individual checks
    """
    checks = []

    # Run all checks
    checks.append(check_holding_time(holding_time_hours, storage_type))
    checks.append(check_remaining_shelf_life(shelf_life_hours, holding_time_hours, product_category))
    checks.append(check_pickup_window(pickup_window_hours, storage_type))
    checks.append(check_storage_type_appropriateness(product_category, storage_type))
    checks.append(check_preparation_time(product_category, preparation_time))

    # Determine overall status
    statuses = [c.severity for c in checks]
    flags = [c.message for c in checks if not c.passed or c.severity == "CAUTION"]

    if "BLOCK" in statuses:
        overall_status = "BLOCK"
        overall_message = "ITEM BLOCKED: Cannot be listed for safety reasons"
    elif "CAUTION" in statuses:
        overall_status = "CAUTION"
        overall_message = "CAUTION ADVISED: Item can be listed with warnings"
    else:
        overall_status = "SAFE"
        overall_message = "Item is safe to list"

    return SafetyResult(
        status=overall_status,
        overall_message=overall_message,
        checks=checks,
        flags=flags,
    )


def format_safety_display(safety_result: SafetyResult) -> str:
    """Format safety result for display in dashboard."""
    lines = []

    if safety_result.status == "BLOCK":
        lines.append("🔴 **BLOCKED** - " + safety_result.overall_message)
    elif safety_result.status == "CAUTION":
        lines.append("🟡 **CAUTION** - " + safety_result.overall_message)
    else:
        lines.append("🟢 **SAFE** - " + safety_result.overall_message)

    lines.append("")
    for check in safety_result.checks:
        if check.severity == "BLOCK":
            icon = "❌"
        elif check.severity == "CAUTION":
            icon = "⚠️"
        else:
            icon = "✓"
        lines.append(f"{icon} {check.message}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test safety engine
    print("Testing food safety engine...\n")

    test_cases = [
        {
            "name": "Fresh pastry (SAFE)",
            "product_category": "Pastries",
            "preparation_time": 5,
            "holding_time_hours": 2,
            "storage_type": "Ambient",
            "shelf_life_hours": 48,
        },
        {
            "name": "Day-old rice dish (CAUTION)",
            "product_category": "Rice Dishes",
            "preparation_time": 20,
            "holding_time_hours": 6,
            "storage_type": "Ambient",
            "shelf_life_hours": 8,
        },
        {
            "name": "Expired sandwich (BLOCK)",
            "product_category": "Sandwiches",
            "preparation_time": 10,
            "holding_time_hours": 10,
            "storage_type": "Refrigerated",
            "shelf_life_hours": 12,
        },
    ]

    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print("="*60)

        result = check_item_safety(**test)
        print(format_safety_display(result))
