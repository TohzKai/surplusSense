#!/usr/bin/env python3
"""
Generate report figures for SurplusSense executive report.
Saves 4 PNG files to outputs/:
  - workflow_diagram.png
  - eda_surplus_by_category.png
  - eda_dow_heatmap.png
  - eda_pred_vs_actual.png

Run: python scripts/generate_report_figures.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

from src.feature_engineering import engineer_features
from src.train_model import load_data
from src.recommendation_engine import generate_recommendation

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. WORKFLOW DIAGRAM
# ─────────────────────────────────────────────────────────────────────────────
def generate_workflow_diagram():
    """Merchant decision flow with real example outputs (BAK001, Ciabatta, 2026-02-10)."""
    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Stage boxes
    boxes = [
        {
            "title": "1. Merchant Input",
            "body": "Merchant: BAK001 (Bakery)\nProduct: Ciabatta\nDate: 2026-02-10\nStorage: Refrigerated",
            "xy": (0.6, 1.5),
        },
        {
            "title": "2. Surplus Prediction",
            "body": "Predicted: 11 units\n(Actual: 10 units)\nConfidence: cluster-calibrated",
            "xy": (3.0, 1.5),
        },
        {
            "title": "3. Discount Recommendation",
            "body": "Discount: 50% off\nListed at SGD 3.24\n(from SGD 6.47)",
            "xy": (5.4, 1.5),
        },
        {
            "title": "4. Food Safety Check",
            "body": "Result: SAFE\nHolding: 2h / 93h shelf life\nStorage: Refrigerated ✓",
            "xy": (7.8, 1.5),
        },
        {
            "title": "5. Recovery Estimate",
            "body": "Recovery: SGD 34.29\n(vs SGD 68.58 potential loss)\nRecovery rate: 50%",
            "xy": (10.2, 1.5),
        },
    ]

    box_w, box_h = 2.1, 2.2
    colors = ["#1E3A5F", "#1E5C3A", "#5C3A1E", "#3A1E5C", "#5C1E3A"]
    light_colors = ["#EBF3FB", "#EBF5EE", "#FBF3EB", "#F3EBFB", "#FBEBF3"]

    for i, box in enumerate(boxes):
        x, y = box["xy"]
        # Outer colored border
        rect = mpatches.FancyBboxPatch(
            (x, y), box_w, box_h,
            boxstyle="round,pad=0.08",
            linewidth=2,
            edgecolor=colors[i],
            facecolor=light_colors[i],
            zorder=2,
        )
        ax.add_patch(rect)

        # Title bar
        title_rect = mpatches.FancyBboxPatch(
            (x, y + box_h - 0.45), box_w, 0.45,
            boxstyle="round,pad=0.04",
            linewidth=0,
            edgecolor=colors[i],
            facecolor=colors[i],
            zorder=3,
        )
        ax.add_patch(title_rect)

        ax.text(
            x + box_w / 2, y + box_h - 0.22,
            box["title"],
            ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white",
            zorder=4,
        )
        ax.text(
            x + box_w / 2, y + box_h / 2 - 0.1,
            box["body"],
            ha="center", va="center",
            fontsize=7.5, color="#1a1a1a",
            multialignment="left",
            linespacing=1.5,
            zorder=4,
        )

    # Arrows between boxes
    arrow_y = 2.6
    for i in range(len(boxes) - 1):
        x1 = boxes[i]["xy"][0] + box_w
        x2 = boxes[i + 1]["xy"][0]
        ax.annotate(
            "", xy=(x2 - 0.08, arrow_y), xytext=(x1 + 0.08, arrow_y),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#555555",
                lw=1.5,
                shrinkA=0,
                shrinkB=0,
            ),
            zorder=5,
        )

    fig.text(0.5, 0.96, "Figure 1: End-to-end merchant decision flow with example outputs (BAK001, Ciabatta, 2026-02-10)",
             ha="center", fontsize=8.5, style="italic", color="#444444")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(OUTPUT_DIR, "workflow_diagram.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 2. EDA — SURPLUS DISTRIBUTION BY CATEGORY
# ─────────────────────────────────────────────────────────────────────────────
def generate_surplus_by_category():
    """Box plot: surplus_quantity by product_category."""
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_fnb_data.csv"))

    # Sort by median surplus for ordering
    order = (
        df.groupby("product_category")["surplus_quantity"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F8F8")

    bp = ax.boxplot(
        [df[df["product_category"] == cat]["surplus_quantity"].values for cat in order],
        labels=order,
        patch_artist=True,
        medianprops=dict(color="#E74C3C", lw=1.5),
        whiskerprops=dict(color="#888888"),
        flierprops=dict(marker="o", markersize=2, alpha=0.4),
        boxprops=dict(linewidth=0.8),
    )
    colors = plt.cm.Blues(np.linspace(0.35, 0.75, len(order)))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    ax.set_ylabel("Surplus Quantity (units)", fontsize=10)
    ax.set_xlabel("Product Category", fontsize=10)
    ax.tick_params(axis="x", rotation=30, labelsize=8.5)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.4, linewidth=0.5)

    fig.text(0.5, 0.01,
              "Surplus quantity varies substantially by category; Bento Sets and Rice Dishes show highest median surplus.",
              ha="center", fontsize=7.5, style="italic", color="#666666")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = os.path.join(OUTPUT_DIR, "eda_surplus_by_category.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 3. EDA — DAY-OF-WEEK HEATMAP
# ─────────────────────────────────────────────────────────────────────────────
def generate_dow_heatmap():
    """Heatmap: mean surplus_quantity by merchant_type × day_of_week."""
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_fnb_data.csv"))

    DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    pivot = (
        df.groupby(["merchant_type", "day_of_week"])["surplus_quantity"]
        .mean()
        .unstack("day_of_week")
    )
    pivot = pivot[[0, 1, 2, 3, 4, 5, 6]]  # reorder Mon–Sun
    pivot.columns = DOW_NAMES

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F8F8")

    im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(7))
    ax.set_xticklabels(DOW_NAMES, fontsize=9)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    ax.set_xlabel("Day of Week", fontsize=10)
    ax.set_ylabel("Merchant Type", fontsize=10)

    # Annotate cells
    for r in range(len(pivot.index)):
        for c in range(7):
            val = pivot.values[r, c]
            color = "white" if val > pivot.values.max() * 0.65 else "#333333"
            ax.text(c, r, f"{val:.1f}", ha="center", va="center",
                    fontsize=8, color=color)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Mean Surplus (units)", fontsize=9)

    fig.text(0.5, 0.01,
             "Bakery merchants show elevated surplus mid-week; Small F&B peaks on weekends.",
             ha="center", fontsize=7.5, style="italic", color="#666666")
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    path = os.path.join(OUTPUT_DIR, "eda_dow_heatmap.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 4. EDA — PREDICTED VS ACTUAL (HOLDOUT SPLIT)
# ─────────────────────────────────────────────────────────────────────────────
def generate_pred_vs_actual():
    """Scatter plot: predicted vs actual surplus on single-seed holdout (seed=42)."""
    from sklearn.model_selection import train_test_split

    df = load_data(os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_fnb_data.csv"))
    df = engineer_features(df)

    # Load model
    with open(os.path.join(os.path.dirname(__file__), "..", "outputs", "surplus_model.pkl"), "rb") as f:
        meta = pickle.load(f)
    model = meta["model"]
    feature_names = meta["feature_names"]

    # Keep only rows with valid lag features, reset index for clean iloc
    df_lagged = df.dropna(subset=["prev_day_surplus", "same_weekday_last_week_surplus"]).copy()
    df_lagged = df_lagged.reset_index(drop=True)

    # Encode categoricals on full df
    for col in ["product_category", "merchant_type", "storage_type"]:
        dummies = pd.get_dummies(df_lagged[col], prefix=col)
        df_lagged = pd.concat([df_lagged, dummies], axis=1)

    # Build feature matrix
    feature_cols = [c for c in feature_names if c in df_lagged.columns]
    X_all = df_lagged[feature_cols].fillna(0)
    y_all = df_lagged["surplus_quantity"].values

    # CRITICAL: use sklearn train_test_split (not numpy shuffle) to replicate
    # the EXACT same split used during model training. sklearn uses its own RNG,
    # independent of numpy's global RNG — np.random.seed(42) gives DIFFERENT
    # shuffle results than sklearn's random_state=42.
    _, X_test, _, y_actual = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42
    )
    y_pred = model.predict(X_test)

    # Clip negative predictions at 0
    y_pred = np.maximum(y_pred, 0)

    mae = np.mean(np.abs(y_actual - y_pred))

    # DEBUG
    print(f"\n[pred_vs_actual debug] Test samples: {len(y_actual)}")
    print(f"[pred_vs_actual debug] MAE = {mae:.4f}")
    print(f"[pred_vs_actual debug] First 10 (predicted, actual):")
    for i in range(min(10, len(y_pred))):
        print(f"  row {i}: pred={y_pred[i]:.4f}, actual={y_actual[i]:.4f}, diff={abs(y_pred[i]-y_actual[i]):.4f}")

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F8F8")

    ax.scatter(y_pred, y_actual, alpha=0.25, s=12, color="#2980B9", rasterized=True)

    # Diagonal reference line
    max_val = max(y_pred.max(), y_actual.max())
    ax.plot([0, max_val], [0, max_val], "r--", lw=1.5, label="Perfect prediction")

    # Add MAE annotation
    ax.text(
        0.05, 0.93,
        f"Single-seed holdout (seed=42): MAE = {mae:.2f}",
        transform=ax.transAxes,
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    ax.set_xlabel("Predicted Surplus (units)", fontsize=10)
    ax.set_ylabel("Actual Surplus (units)", fontsize=10)
    ax.legend(fontsize=9, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.3, linewidth=0.5)

    fig.text(0.5, 0.01,
             "Points near the diagonal indicate accurate predictions; red dashed line = perfect.",
             ha="center", fontsize=7.5, style="italic", color="#666666")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = os.path.join(OUTPUT_DIR, "eda_pred_vs_actual.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("Generating SurplusSense report figures...")
    paths = {
        "workflow_diagram.png": generate_workflow_diagram(),
        "eda_surplus_by_category.png": generate_surplus_by_category(),
        "eda_dow_heatmap.png": generate_dow_heatmap(),
    }
    print("\nAll figures generated:")
    for name, path in paths.items():
        size_kb = os.path.getsize(path) / 1024
        print(f"  {name}: {size_kb:.0f} KB")


if __name__ == "__main__":
    main()
