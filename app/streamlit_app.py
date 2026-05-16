#!/usr/bin/env python3
"""
SurplusSense Streamlit Decision Cockpit
=====================================
Merchant-facing AI dashboard for F&B surplus decision support.

Features:
1. Merchant selector
2. Product category selector
3. Surplus prediction display
4. Model performance section
5. Baseline vs ML comparison
6. Discount recommendation panel
7. Food-safety status panel
8. Revenue recovery simulator
9. Phase 2 listing preview
10. Exportable recommendation table
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta, time
import sys
import plotly.express as px
import plotly.graph_objects as go

# Compute base directory (parent of app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add src to path
sys.path.insert(0, BASE_DIR)

from src.feature_engineering import engineer_features, get_feature_columns, get_target_column
from src.recommendation_engine import generate_recommendation, CATEGORY_EMOJI, predict_surplus_cold_start
from src.food_safety_rules import check_item_safety, format_safety_display

# SVG Icon constants (Lucide-style, 16x16 or 20x20)
ICONS = {
    "target": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "lightbulb": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "dollar": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "clock": '<svg xmlns="http://www.w.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "package": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 9.4 7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>',
    "eye": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>',
    "download": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "x": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "trending": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "store": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"/></svg>',
    "calendar": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "leaf": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
}

# Page config
st.set_page_config(
    page_title="SurplusSense",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Design System CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0B0F0E;
        --surface: #131918;
        --surface-elevated: #1A2220;
        --border: #1F2A28;
        --accent: #10B981;
        --accent-muted: #064E3B;
        --text-primary: #F3F4F6;
        --text-secondary: #9CA3AF;
        --text-tertiary: #6B7280;
        --warning: #F59E0B;
        --danger: #EF4444;
        --success: #10B981;
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    /* ===== Animations ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .stMarkdown, .element-container {
        animation: fadeInUp 0.4s ease-out;
    }

    /* ===== Responsive ===== */
    @media (max-width: 768px) {
        .three-col-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .rec-hero-savings {
            flex-wrap: wrap;
            gap: 16px;
        }

        .rec-hero-discount {
            font-size: 40px;
        }

        .app-header {
            padding: 0 16px;
        }

        .app-subtitle {
            display: none;
        }

        .rec-hero {
            padding: 20px;
        }
    }

    /* ===== App Header ===== */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        height: 64px;
        background: var(--surface);
        border-bottom: 1px solid var(--border);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .app-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .app-logo {
        width: 32px;
        height: 32px;
        flex-shrink: 0;
    }

    .app-header-titles {
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .app-wordmark {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.2;
    }

    .app-subtitle {
        font-size: 12px;
        color: var(--text-secondary);
        line-height: 1.2;
    }

    .app-header-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid var(--accent);
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        color: var(--accent);
    }

    .demo-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        background: #F59E0B22;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        color: #F59E0B;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: var(--accent);
        border-radius: 50%;
    }

    .app-header-separator {
        height: 1px;
        background: var(--border);
    }

    .sidebar-disclaimer {
        font-size: 11px;
        color: #6B7280;
        padding: 8px;
        border-top: 1px solid var(--border);
        line-height: 1.5;
        margin-top: 8px;
    }

    /* Tighten gap between app header and first main-content section */
    .main-content-tight {
        margin-top: 0px !important;
    }

    .stApp {
        background-color: var(--bg);
        color: var(--text-primary);
    }

    /* ===== Typography ===== */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    .metric-number {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* ===== Section Headers ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 12px;
    }

    .section-header svg {
        flex-shrink: 0;
    }

    /* ===== Metric Cards ===== */
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .metric-value.small {
        font-size: 20px;
    }

    .metric-delta {
        font-size: 13px;
        color: var(--text-secondary);
    }

    /* ===== Cards ===== */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
        border-color: var(--accent);
    }

    .card-elevated:hover {
        background: var(--surface-elevated);
    }

    /* ===== Recommendation Hero Hover ===== */
    .rec-hero {
        transition: box-shadow 0.2s ease;
    }

    .rec-hero:hover {
        box-shadow: 0 0 0 1px var(--accent), 0 4px 24px rgba(16, 185, 129, 0.2);
    }

    /* ===== Safety Badge Hover ===== */
    .safety-badge {
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .safety-badge:hover {
        transform: scale(1.03);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* ===== Status Dot Pulse ===== */
    .status-dot {
        animation: pulse-dot 2s ease-in-out infinite;
    }

    /* ===== Accent Card (Recommendation Hero) ===== */
    .accent-card {
        background: var(--accent-muted);
        border-left: 3px solid var(--accent);
        border-radius: 12px;
        padding: 24px;
    }

    /* ===== Recommendation Hero Card ===== */
    .rec-hero {
        background: linear-gradient(135deg, var(--accent-muted) 0%, rgba(6, 78, 59, 0.4) 100%);
        border: 1px solid var(--accent);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
    }

    .rec-hero-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .rec-hero-discount {
        font-family: 'JetBrains Mono', monospace;
        font-size: 56px;
        font-weight: 700;
        color: var(--accent);
        line-height: 1;
    }

    .rec-hero-label {
        font-size: 13px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    .rec-hero-prices {
        display: flex;
        align-items: baseline;
        gap: 16px;
        margin-top: 8px;
    }

    .rec-hero-original {
        font-size: 18px;
        color: var(--text-tertiary);
        text-decoration: line-through;
    }

    .rec-hero-discounted {
        font-size: 24px;
        font-weight: 600;
        color: var(--text-primary);
    }

    .rec-hero-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        background: var(--accent);
        color: #0B0F0E;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 700;
    }

    .rec-hero-savings {
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid var(--border);
        display: flex;
        gap: 32px;
    }

    .rec-hero-savings-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    /* ===== Three Column Grid ===== */
    .three-col-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    /* Consumer listing card now uses fully inline HTML — no CSS classes needed */

    /* ===== Safety Badges ===== */
    .safety-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
    }

    .safety-badge.safe {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid var(--success);
    }

    .safety-badge.caution {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning);
        border: 1px solid var(--warning);
    }

    .safety-badge.blocked {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger);
        border: 1px solid var(--danger);
    }

    /* ===== Info Box ===== */
    .info-box {
        background: var(--surface);
        border-left: 3px solid var(--accent);
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
    }

    /* ===== Impact KPI Cards (Emerald) ===== */
    .impact-kpi {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .impact-kpi:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
        border-color: #10B981;
    }

    .impact-kpi-accent {
        border-top: 3px solid #10B981;
    }

    .impact-kpi-icon {
        margin-bottom: 8px;
    }

    .impact-kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 700;
        color: #10B981;
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .impact-kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }

    .impact-kpi-caption {
        font-size: 11px;
        color: var(--text-tertiary);
        font-style: italic;
    }

    /* ===== Footer ===== */
    .footer {
        background: var(--surface);
        border-top: 1px solid var(--border);
        padding: 32px 24px;
        text-align: center;
        margin-top: 48px;
    }

    .footer-brand {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .footer-logo {
        width: 24px;
        height: 24px;
    }

    .footer-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
    }

    .footer-subtitle {
        font-size: 13px;
        color: var(--text-secondary);
        margin-bottom: 12px;
    }

    .footer-badge {
        display: inline-block;
        padding: 4px 12px;
        background: var(--accent-muted);
        border: 1px solid var(--accent);
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .footer-disclaimer {
        margin-top: 16px;
        font-size: 12px;
        color: var(--text-tertiary);
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }

    .footer-meta {
        margin-top: 12px;
        display: flex;
        justify-content: center;
        gap: 24px;
        font-size: 11px;
        color: var(--text-tertiary);
    }

    /* ===== Sidebar ===== */
    .css-1d391kg {
        background-color: var(--surface);
        border-right: 3px solid var(--accent);
    }

    /* Section labels */
    .sidebar-section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-tertiary);
        margin-bottom: 8px;
        padding-left: 4px;
    }

    /* Merchant info chip */
    .merchant-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: var(--surface-elevated);
        border: 1px solid var(--border);
        border-radius: 8px;
        font-size: 13px;
        color: var(--text-secondary);
    }

    /* ===== Streamlit Overrides ===== */
    .stMetric {
        background: var(--surface);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    .stSlider label, .stSelectbox label {
        color: var(--text-secondary) !important;
    }

    section {
        background: var(--bg) !important;
    }
</style>
""", unsafe_allow_html=True)


def load_model():
    """Load trained model."""
    model_path = os.path.join(BASE_DIR, "outputs/surplus_model.pkl")
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None


def load_data():
    """Load synthetic data."""
    data_path = os.path.join(BASE_DIR, "data/synthetic_fnb_data.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None


def load_results():
    """Load model evaluation results."""
    results_path = os.path.join(BASE_DIR, "outputs/model_results.csv")
    importance_path = os.path.join(BASE_DIR, "outputs/feature_importance.csv")
    model_path = os.path.join(BASE_DIR, "outputs/surplus_model.pkl")

    results = None
    importance = None
    model_type = None

    if os.path.exists(results_path):
        results = pd.read_csv(results_path)
    if os.path.exists(importance_path):
        importance = pd.read_csv(importance_path)
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
            model_type = model_data.get("model_type", "ML Model")

    return results, importance, model_type


@st.cache_data
def load_merchant_clusters():
    """Load merchant cluster assignments."""
    cluster_path = os.path.join(BASE_DIR, "data/merchant_clusters.csv")
    if os.path.exists(cluster_path):
        return pd.read_csv(cluster_path)
    return None


@st.cache_data
def load_multi_seed_results():
    """Load multi-seed validation results (5-seed means)."""
    path = os.path.join(BASE_DIR, "outputs/multi_seed_validation.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def calculate_impact_metrics(df, date_filter=None, merchant_filter=None):
    """
    Calculate aggregate impact metrics from loaded data.

    Uses a default 35% discount assumption for revenue recovery estimation
    (typical midpoint of the recommendation engine's discount range).
    CO2 estimate: 2.5 kg CO2e per kg food (F&B sector average, WWF estimate).
    """
    data = df.copy()
    if date_filter is not None:
        data = data[data["date"] == date_filter]
    if merchant_filter is not None:
        data = data[data["merchant_id"] == merchant_filter]

    if len(data) == 0:
        return None

    # Surplus units recovered (i.e. surplus that would be listed/donated)
    total_surplus = data["surplus_quantity"].sum()

    # Estimate revenue recovery using 35% average discount
    avg_discount = 0.35
    data["estimated_recovery"] = data["original_price"] * (1 - avg_discount) * data["surplus_quantity"]
    total_recovery = data["estimated_recovery"].sum()

    # Original value (what would be lost without action)
    data["original_value"] = data["original_price"] * data["surplus_quantity"]
    total_original = data["original_value"].sum()

    # CO2 avoided: assume avg 0.4 kg per surplus unit (F&B portion of 2.5 kg/kg food estimate)
    # Industry avg for prepared F&B is ~0.4-0.6 kg CO2e per unit
    co2_per_unit_kg = 0.4
    total_co2 = total_surplus * co2_per_unit_kg

    # Meals saved: 1 surplus unit ≈ 1 meal equivalent
    meals_saved = int(total_surplus)

    return {
        "surplus_recovered": int(total_surplus),
        "revenue_recovered": round(total_recovery, 2),
        "co2_avoided_kg": round(total_co2, 1),
        "meals_saved": meals_saved,
        "record_count": len(data),
        "date_label": date_filter if date_filter else "all dates",
        "scope_label": f"this merchant" if merchant_filter else f"all merchants ({len(data['merchant_id'].unique())} operators)",
    }


@st.cache_data
def get_merchant_list(df):
    """Get unique merchants for selector."""
    if df is None:
        return []
    return sorted(df["merchant_id"].unique())


@st.cache_data
def get_category_list(df):
    """Get unique categories for selector."""
    if df is None:
        return []
    return sorted(df["product_category"].unique())


def create_prediction_features(df, merchant_id, category, date=None):
    """Create features for a single prediction."""
    # Filter to merchant and category
    subset = df[(df["merchant_id"] == merchant_id) & (df["product_category"] == category)].copy()

    if len(subset) == 0:
        return None

    # Get the most recent record as template
    if date:
        template = subset[subset["date"] <= date].iloc[-1] if len(subset[subset["date"] <= date]) > 0 else subset.iloc[-1]
    else:
        template = subset.iloc[-1]

    return template


def get_selected_record_or_fallback(df, merchant_id, category, product, selected_date=None):
    """
    Return a safe record-like dict for the selected merchant/category/product/date.

    Fallback order:
    1. Exact merchant + category + product + date match
    2. Exact merchant + category + product (any date), tail(1)
    3. Exact merchant + category (any product/date), tail(1)
    4. Category + product global average row
    5. Merchant global average row
    6. Hardcoded safe default (all numeric fields set to sensible defaults)

    Also returns a fallback_label string describing which fallback was used.
    """
    # Guard: if DataFrame is empty or has no columns, return hardcoded defaults immediately
    if df is None or len(df.columns) == 0 or len(df) == 0:
        return {
            "surplus_quantity": 5.0,
            "preparation_time": 30,
            "holding_time_hours": 2.0,
            "storage_type": "Refrigerated",
            "shelf_life_hours": 48.0,
            "original_price": 10.0,
            "weekend_flag": False,
            "promotion_flag": False,
        }, "fallback: hardcoded defaults"

    SAFE_DEFAULTS = {
        "surplus_quantity": 5.0,
        "preparation_time": 30,
        "holding_time_hours": 2.0,
        "storage_type": "Refrigerated",
        "shelf_life_hours": 48.0,
        "original_price": 10.0,
        "weekend_flag": False,
        "promotion_flag": False,
    }

    if selected_date is not None:
        exact = df[
            (df["merchant_id"] == merchant_id) &
            (df["product_category"] == category) &
            (df["product_name"] == product) &
            (df["date"] == selected_date)
        ]
        if len(exact) > 0:
            return exact.iloc[-1].to_dict(), "exact merchant/category/product/date"

    mcp = df[
        (df["merchant_id"] == merchant_id) &
        (df["product_category"] == category) &
        (df["product_name"] == product)
    ]
    if len(mcp) > 0:
        return mcp.tail(1).iloc[-1].to_dict(), "fallback: merchant/category/product (latest date)"

    mc = df[
        (df["merchant_id"] == merchant_id) &
        (df["product_category"] == category)
    ]
    if len(mc) > 0:
        return mc.tail(1).iloc[-1].to_dict(), "fallback: merchant/category (latest record)"

    cp = df[df["product_category"] == category]
    if len(cp) > 0:
        avg = cp.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in cp.columns:
            mode_vals = cp["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: category average"

    m = df[df["merchant_id"] == merchant_id]
    if len(m) > 0:
        avg = m.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in m.columns:
            mode_vals = m["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: merchant average"

    if len(df) > 0:
        avg = df.mean(numeric_only=True)
        result = SAFE_DEFAULTS.copy()
        result["surplus_quantity"] = float(avg.get("surplus_quantity", 5.0))
        result["original_price"] = float(avg.get("original_price", 10.0))
        result["preparation_time"] = int(avg.get("preparation_time", 30))
        result["holding_time_hours"] = float(avg.get("holding_time_hours", 2.0))
        result["shelf_life_hours"] = float(avg.get("shelf_life_hours", 48.0))
        if "storage_type" in df.columns:
            mode_vals = df["storage_type"].mode()
            result["storage_type"] = mode_vals.iloc[0] if len(mode_vals) > 0 else "Refrigerated"
        return result, "fallback: global average"

    return SAFE_DEFAULTS.copy(), "fallback: hardcoded defaults"


def _safe_get(record, key, default):
    """Safely get a value from a dict-like record, returning default if key missing."""
    try:
        val = record[key]
        if pd.isna(val):
            return default
        return val
    except (KeyError, TypeError, ValueError):
        return default


def main():
    # Header — sticky app bar
    st.markdown("""
    <div class="app-header">
        <div class="app-header-left">
            <svg class="app-logo" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="32" height="32" rx="8" fill="#064E3B"/>
                <path d="M16 6C16 6 10 10 10 17C10 20.3137 12.6863 23 16 23C19.3137 23 22 20.3137 22 17C22 10 16 6 16 6Z" fill="#10B981"/>
                <circle cx="16" cy="17" r="3" fill="#064E3B"/>
            </svg>
            <div class="app-header-titles">
                <span class="app-wordmark">SurplusSense</span>
                <span class="app-subtitle">AI Decision Cockpit for F&B Merchants</span>
            </div>
        </div>
        <div class="app-header-right">
            <span class="status-pill">
                <span class="status-dot"></span>Live
            </span>
            <span class="demo-pill" title="This MVP uses synthetic data. Production deployment requires real merchant data and pilot validation.">
                Demo data
            </span>
        </div>
    </div>
    <div class="app-header-separator"></div>
    """, unsafe_allow_html=True)

    # ===== DECISION WORKFLOW HEADER =====
    st.markdown("""
    <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px 24px; margin: 16px 0 24px 0;">
        <div style="font-size: 13px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">Decision Workflow</div>
        <div style="display: flex; gap: 0; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: var(--accent); color: #0B0F0E; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0;">1</div>
                <div style="font-size: 13px; color: var(--text-primary); font-weight: 500;">Enter Context</div>
            </div>
            <div style="flex: 1; height: 2px; background: var(--border); margin: 0 12px;"></div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: var(--accent); color: #0B0F0E; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0;">2</div>
                <div style="font-size: 13px; color: var(--text-primary); font-weight: 500;">Predict</div>
            </div>
            <div style="flex: 1; height: 2px; background: var(--border); margin: 0 12px;"></div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: var(--accent); color: #0B0F0E; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0;">3</div>
                <div style="font-size: 13px; color: var(--text-primary); font-weight: 500;">Recommend</div>
            </div>
            <div style="flex: 1; height: 2px; background: var(--border); margin: 0 12px;"></div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: var(--accent); color: #0B0F0E; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0;">4</div>
                <div style="font-size: 13px; color: var(--text-primary); font-weight: 500;">Screen Safety</div>
            </div>
            <div style="flex: 1; height: 2px; background: var(--border); margin: 0 12px;"></div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: var(--accent); color: #0B0F0E; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0;">5</div>
                <div style="font-size: 13px; color: var(--text-primary); font-weight: 500;">Estimate Recovery</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()
    model_metadata = load_model()
    results_df, importance_df, model_type = load_results()
    clusters_df = load_merchant_clusters()
    multi_seed_df = load_multi_seed_results()

    if df is None:
        st.error("No data found. Please run the data generator first: `python data/generate_synthetic_data.py`")
        return

    # Sidebar - all content under one with block so dividers stay in sidebar scope
    with st.sidebar:
        merchants = get_merchant_list(df)
        categories = get_category_list(df)

        st.markdown('<p class="sidebar-section-label">Merchant</p>', unsafe_allow_html=True)
        merchant_id = st.selectbox("Select Merchant", merchants, label_visibility="collapsed")
        merchant_info = df[df["merchant_id"] == merchant_id].iloc[-1]
        merchant_type = merchant_info["merchant_type"]
        st.markdown(f'<div class="merchant-chip">{ICONS["store"]} {merchant_type}</div>', unsafe_allow_html=True)

        st.markdown('<p class="sidebar-section-label" style="margin-top: 8px;">Category</p>', unsafe_allow_html=True)
        merchant_categories = get_category_list(df[df["merchant_id"] == merchant_id])
        selected_category = st.selectbox("Select Category", merchant_categories, label_visibility="collapsed")

        st.markdown('<p class="sidebar-section-label" style="margin-top: 8px;">Product</p>', unsafe_allow_html=True)
        products = df[(df["merchant_id"] == merchant_id) & (df["product_category"] == selected_category)]["product_name"].unique()
        selected_product = st.selectbox("Select Product", list(products), label_visibility="collapsed")

        st.markdown('<p class="sidebar-section-label" style="margin-top: 8px;">Date</p>', unsafe_allow_html=True)
        merchant_dates = df[(df["merchant_id"] == merchant_id) & (df["product_category"] == selected_category)]["date"].unique()
        selected_date = st.selectbox("Select Date", sorted(merchant_dates)[-30:], label_visibility="collapsed")

        st.markdown('<p class="sidebar-section-label" style="margin-top: 8px;">Time</p>', unsafe_allow_html=True)
        _time_options = [f"{h:02d}:00" for h in range(6, 23)]  # 06:00 to 22:00
        # Only set default on first load; preserve user selection on reruns
        if "time_selector" not in st.session_state:
            st.session_state["time_selector"] = "10:00"
        current_time_str = st.selectbox(
            "Time",
            _time_options,
            label_visibility="collapsed",
            key="time_selector",
        )

        st.markdown('<p class="sidebar-section-label" style="margin-top: 8px;">Demo Mode</p>', unsafe_allow_html=True)
        cold_start_mode = st.checkbox(
            "Simulate new merchant (no history)",
            value=False,
            help="When enabled, surplus predictions use cluster-level patterns instead of merchant-specific history."
        )

        # Food safety disclaimer
        st.markdown("""
        <div class="sidebar-disclaimer">
            ⚠ Advisory only. Food safety recommendations are based on general principles and have not
            been validated by SFA or food safety experts. Merchants remain responsible for food
            safety compliance, storage, and handling decisions.
        </div>
        """, unsafe_allow_html=True)

    # Get selected record — robust with multiple fallback levels (never raises IndexError)
    # This must be computed BEFORE the early prediction block because cold-start prediction
    # and safety check use record values.
    record, record_fallback_label = get_selected_record_or_fallback(
        df, merchant_id, selected_category, selected_product, selected_date
    )

    # Compute surplus prediction early (before Impact Today and Executive Decision Summary)
    selected_dt = datetime.strptime(selected_date, "%Y-%m-%d")
    is_weekend = selected_dt.weekday() >= 5

    if cold_start_mode:
        cold_result = predict_surplus_cold_start(
            merchant_type=merchant_type,
            product_category=selected_category,
            avg_daily_production=None,
            dominant_storage=record.get("storage_type", "Refrigerated"),
            is_weekend=is_weekend,
        )
        avg_prediction = cold_result["predicted_surplus"]
        cold_start_note = cold_result
    else:
        if model_metadata is not None:
            # Scope feature engineering to merchant + category for relevant lag/rolling features.
            # If insufficient history (< 10 records), fall back to merchant-only scope.
            df_mc = df[(df["merchant_id"] == merchant_id) & (df["product_category"] == selected_category)]
            if len(df_mc) >= 10:
                features = engineer_features(df_mc.tail(30))
            else:
                # Insufficient merchant+category history — fall back to merchant scope
                features = engineer_features(df[df["merchant_id"] == merchant_id].tail(30))
            features = features.dropna(subset=["prev_day_surplus", "same_weekday_last_week_surplus"])
            if len(features) > 0:
                model = model_metadata["model"]
                feature_names = model_metadata["feature_names"]
                categorical_cols = ["product_category", "merchant_type", "storage_type"]
                all_categories = {
                    "product_category": ["Bento Sets", "Bread", "Cakes", "Coffee & Beverages", "Cookies",
                                        "Desserts", "Noodle Dishes", "Pastries", "Rice Dishes",
                                        "Salads", "Sandwiches", "Soup & Sides", "Tarts"],
                    "merchant_type": ["Bakery", "Café", "Small F&B"],
                    "storage_type": ["Ambient", "Frozen", "Refrigerated"]
                }
                for col in categorical_cols:
                    if col in features.columns:
                        dummies = pd.get_dummies(features[col], prefix=col)
                        for cat in all_categories.get(col, []):
                            dummy_col = f"{col}_{cat}"
                            if dummy_col not in dummies.columns:
                                dummies[dummy_col] = 0
                        features = pd.concat([features, dummies], axis=1)
                X = pd.DataFrame(columns=feature_names)
                for col in feature_names:
                    if col in features.columns:
                        X[col] = features[col]
                    else:
                        X[col] = 0
                X = X.fillna(0)
                if len(X) > 0:
                    predictions = model.predict(X)
                    avg_prediction = predictions.mean()
                else:
                    # Safe fallback — no model data; use category mean surplus
                    cat_mean = df[df["product_category"] == selected_category]["surplus_quantity"].mean() if len(df[df["product_category"] == selected_category]) > 0 else 5.0
                    avg_prediction = float(cat_mean) * 1.1
            else:
                cat_mean = df[df["product_category"] == selected_category]["surplus_quantity"].mean() if len(df[df["product_category"] == selected_category]) > 0 else 5.0
                avg_prediction = float(cat_mean) * 1.1
        else:
            cat_mean = df[df["product_category"] == selected_category]["surplus_quantity"].mean() if len(df[df["product_category"] == selected_category]) > 0 else 5.0
            avg_prediction = float(cat_mean) * 1.1
        cold_start_note = None

    avg_prediction = round(avg_prediction, 1)

    # Compute safety and recommendation for Executive Decision Summary
    safety_result = check_item_safety(
        product_category=selected_category,
        preparation_time=_safe_get(record, "preparation_time", 30),
        holding_time_hours=_safe_get(record, "holding_time_hours", 2.0),
        storage_type=_safe_get(record, "storage_type", "Refrigerated"),
        shelf_life_hours=_safe_get(record, "shelf_life_hours", 48.0),
    )

    recommendation = generate_recommendation(
        merchant_id=merchant_id,
        merchant_type=merchant_type,
        product_category=selected_category,
        product_name=selected_product,
        original_price=_safe_get(record, "original_price", 10.0),
        predicted_surplus=avg_prediction,
        shelf_life_hours=_safe_get(record, "shelf_life_hours", 48.0),
        preparation_time=_safe_get(record, "preparation_time", 30),
        storage_type=_safe_get(record, "storage_type", "Refrigerated"),
        holding_time_hours=_safe_get(record, "holding_time_hours", 2.0),
        current_time=current_time_str,
        safety_status=safety_result.status,
        safety_flags=safety_result.flags,
    )

    # ===== EXECUTIVE DECISION SUMMARY — appears near top for immediate visibility =====
    discount_pct = recommendation['recommended_discount_pct']
    if discount_pct >= 0.6:
        action_label = "DEEP DISCOUNT"
        action_color = "#EF4444"
    elif discount_pct >= 0.4:
        action_label = "DISCOUNT"
        action_color = "#F59E0B"
    elif discount_pct >= 0.2:
        action_label = "MONITOR"
        action_color = "#3B82F6"
    else:
        action_label = "HOLD"
        action_color = "#10B981"

    surplus_qty = recommendation['predicted_surplus']
    shelf_life = _safe_get(record, 'shelf_life_hours', 48.0)
    holding = _safe_get(record, 'holding_time_hours', 2.0)
    remaining = shelf_life - holding
    recovery = recommendation['estimated_merchant_recovery']
    original = recommendation['original_value']

    if safety_result.status == "SAFE":
        safety_label = "SAFE"
        safety_color = "#10B981"
        safety_icon = "✓"
    elif safety_result.status == "CAUTION":
        safety_label = "CAUTION"
        safety_color = "#F59E0B"
        safety_icon = "⚠"
    else:
        safety_label = "BLOCKED"
        safety_color = "#EF4444"
        safety_icon = "✕"

    st.markdown("""
    <div style="background: var(--surface-elevated); border: 1px solid var(--accent); border-radius: 16px; padding: 28px 32px; margin: 16px 0 24px 0;">
        <div style="font-size: 13px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 16px;">Executive Decision Summary</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px;">
            <div style="text-align: center;">
                <div style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Recommended Action</div>
                <div style="font-size: 18px; font-weight: 700; color: """ + action_color + """; background: """ + action_color + """22; border: 1px solid """ + action_color + """; border-radius: 8px; padding: 8px 16px; display: inline-block;">""" + action_label + """</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Why</div>
                <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.5;">""" + f"{surplus_qty:.0f} units predicted · {discount_pct*100:.0f}% discount recommended" + """</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Safety Status</div>
                <div style="font-size: 14px; font-weight: 700; color: """ + safety_color + """; background: """ + safety_color + """22; border: 1px solid """ + safety_color + """; border-radius: 8px; padding: 8px 16px; display: inline-block;">""" + safety_icon + """ """ + safety_label + """</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 11px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Estimated Recovery</div>
                <div style="font-size: 14px; font-weight: 700; color: var(--accent);">SGD """ + f"{recovery:.2f}" + """</div>
                <div style="font-size: 11px; color: var(--text-tertiary);">vs SGD """ + f"{original:.2f}" + """ potential loss</div>
            </div>
        </div>
        <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-secondary);">
            <strong style="color: var(--text-primary);">Recommended next step:</strong> Apply the suggested discount only after reviewing safety warnings and confirming in-store handling compliance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Impact Today Strip — sustainability KPIs (calculated from all merchants on selected date)
    impact = calculate_impact_metrics(df, date_filter=selected_date)
    if impact:
        st.markdown(f'<div class="section-header" style="margin-top: 0px;">{ICONS["leaf"]} Impact Today</div>', unsafe_allow_html=True)
        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
        with col_i1:
            st.markdown(f'''
            <div class="impact-kpi impact-kpi-accent">
                <div class="impact-kpi-icon">{ICONS["leaf"]}</div>
                <div class="impact-kpi-value">{impact["surplus_recovered"]:,}</div>
                <div class="impact-kpi-label">Surplus Recovered</div>
                <div class="impact-kpi-caption">units redirected from waste</div>
            </div>''', unsafe_allow_html=True)
        with col_i2:
            st.markdown(f'''
            <div class="impact-kpi impact-kpi-accent">
                <div class="impact-kpi-icon">{ICONS["dollar"]}</div>
                <div class="impact-kpi-value">SGD {impact["revenue_recovered"]:,.2f}</div>
                <div class="impact-kpi-label">Revenue Recovered</div>
                <div class="impact-kpi-caption">vs potential loss</div>
            </div>''', unsafe_allow_html=True)
        with col_i3:
            st.markdown(f'''
            <div class="impact-kpi impact-kpi-accent">
                <div class="impact-kpi-icon">{ICONS["leaf"]}</div>
                <div class="impact-kpi-value">{impact["co2_avoided_kg"]:,} kg</div>
                <div class="impact-kpi-label">CO₂ Avoided</div>
                <div class="impact-kpi-caption">estimated, F&amp;B sector avg</div>
            </div>''', unsafe_allow_html=True)
        with col_i4:
            st.markdown(f'''
            <div class="impact-kpi impact-kpi-accent">
                <div class="impact-kpi-icon">{ICONS["package"]}</div>
                <div class="impact-kpi-value">{impact["meals_saved"]:,}</div>
                <div class="impact-kpi-label">Meals Saved</div>
                <div class="impact-kpi-caption">equivalent meals</div>
            </div>''', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:11px; color: var(--text-tertiary); text-align:center; margin-top: 4px; margin-bottom: 16px;">Aggregate: {impact["scope_label"]} on {impact["date_label"]}</p>', unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<div class="section-header">{ICONS["target"]} Surplus Prediction</div>', unsafe_allow_html=True)
        st.caption("Updates with the selected merchant, product, date, and time.")
        st.info("**Prediction scoping:** SurplusSense recalculates features using the selected merchant and product/category context. Where there is insufficient history (fewer than 10 records for this merchant + category), it falls back to a broader merchant-level scope.")

        # Determine if weekend based on selected date
        selected_dt = datetime.strptime(selected_date, "%Y-%m-%d")
        is_weekend = selected_dt.weekday() >= 5

        if cold_start_mode:
            # Cold-start: display variables (prediction already computed above)
            prediction_display = f"{avg_prediction:.0f} units"
            prediction_subtitle = f"Based on {merchant_type.lower()} cluster patterns"
            starter_pill = '<span style="display:inline-flex;align-items:center;gap:4px;padding:3px 8px;background:#F59E0B22;border-radius:9999px;font-size:11px;font-weight:600;color:#F59E0B;">Starter estimate</span>'
            prediction_badge = f"&nbsp;{starter_pill}"
            prediction_ratio = cold_start_note["surplus_ratio_used"] if cold_start_note else None
        else:
            # Standard: display variables (prediction already computed above)
            prediction_display = f"{avg_prediction:.0f} units"
            prediction_subtitle = f"Based on {merchant_type} patterns"
            prediction_badge = ""
            prediction_ratio = None

        # Calculate historical average
        historical_avg = df[(df["merchant_id"] == merchant_id) & (df["product_category"] == selected_category)]["surplus_quantity"].mean()

        # Display prediction with custom styling
        bar_width = min(100, avg_prediction / (historical_avg * 1.5) * 100) if historical_avg > 0 else 50
        st.markdown(f'''
        <div class="card">
            <div style="display: flex; align-items: flex-start; gap: 2rem;">
                <div>
                    <div class="metric-label">Predicted Surplus</div>
                    <div class="metric-value">{prediction_display}{prediction_badge}</div>
                    <div class="metric-delta">{prediction_subtitle}</div>
                </div>
                <div style="flex: 1;">
                    <div class="metric-label" style="margin-bottom: 0.25rem;">Surplus Level</div>
                    <div style="background: var(--neutral-200); border-radius: 8px; height: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, var(--green-500), var(--green-700)); height: 100%; width: {bar_width:.0f}%; border-radius: 8px;"></div>
                    </div>
                </div>
            </div>
        </div>''', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f'''
            <div class="card">
                <div class="metric-label">Historical Average</div>
                <div class="metric-value">{historical_avg:.1f}</div>
                <div class="metric-label">units/day</div>
            </div>''', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'''
            <div class="card">
                <div class="metric-label">Today's Actual</div>
                <div class="metric-value">{_safe_get(record, 'surplus_quantity', 5.0)}</div>
                <div class="metric-label">units</div>
            </div>''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="section-header">{ICONS["store"]} Merchant Details</div>', unsafe_allow_html=True)
        st.write(f"**Merchant:** {merchant_id}")
        st.write(f"**Type:** {merchant_type}")
        st.write(f"**Category:** {selected_category}")
        st.write(f"**Product:** {selected_product}")
        st.write(f"**Date:** {selected_date}")
        st.write(f"**Weekend:** {'Yes' if _safe_get(record, 'weekend_flag', False) else 'No'}")
        st.write(f"**Promotion:** {'Yes' if _safe_get(record, 'promotion_flag', False) else 'No'}")

    # ===== MERCHANT PROFILE CARD — placed below Surplus Prediction, above Model Performance =====
    if clusters_df is not None and merchant_id in clusters_df["merchant_id"].values:
        cluster_row = clusters_df[clusters_df["merchant_id"] == merchant_id].iloc[0]
        cluster_name = cluster_row["cluster_name"]
        cluster_id = int(cluster_row["cluster_id"])
        n_in_cluster = int((clusters_df["cluster_id"] == cluster_id).sum())
        n_others = n_in_cluster - 1
    else:
        cluster_name = None
        cluster_id = None
        n_in_cluster = 0
        n_others = 0

    st.markdown("---")
    st.markdown('<div class="section-header">{} Operating Profile</div>'.format(ICONS["store"]), unsafe_allow_html=True)

    if cluster_name:
        st.markdown(f'''
        <div class="card">
            <div style="margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Operating Profile</span>
            </div>
            <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">
                {cluster_name}
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 8px;">
                Grouped with {n_others} other merchants by operating pattern
            </div>
            <div style="font-size: 11px; color: var(--text-tertiary);">
                Calibrated against merchants with similar volume, shelf life, and surplus patterns.
            </div>
        </div>''', unsafe_allow_html=True)

        # Cold-start: show synthetic data note as expandable "Why am I seeing this?" link
        if cold_start_mode and cold_start_note is not None:
            with st.expander("Why am I seeing this?"):
                st.markdown(f'<span style="font-size: 13px; color: var(--text-secondary);">{cold_start_note["synthetic_data_note"]}</span>', unsafe_allow_html=True)

    # Model Performance Section
    st.markdown("---")
    st.subheader("Model Performance")

    # Use temporal holdout values from the final model (consistent with executive report)
    # Historical Average MAE: 1.49 (from model_results.csv)
    # XGBoost MAE: 0.64 / RMSE: 0.81 (from temporal holdout, model_metadata.json)
    # Earlier 5-seed mean evaluation is retained in multi_seed_validation.csv for robustness checks
    if results_df is not None:
        baselines = results_df[results_df["is_baseline"] == True]
        if len(baselines) > 0:
            best_baseline_row = baselines.loc[baselines["MAE"].idxmin()]
            baseline_mae = best_baseline_row["MAE"]   # Historical Average: 1.49
            baseline_rmse = best_baseline_row["RMSE"]  # Historical Average RMSE

        # Temporal holdout values (authoritative — used in executive report and README)
        xgb_mae = 0.6355  # XGBoost temporal holdout MAE
        xgb_rmse = 0.8131  # XGBoost temporal holdout RMSE
        improvement_pct = (baseline_mae - xgb_mae) / baseline_mae * 100  # 57.2% vs Historical Average

        # Metric cards in a row
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        with perf_col1:
            st.metric("Best Baseline MAE", f"{baseline_mae:.2f}", best_baseline_row["model"])
        with perf_col2:
            st.metric("XGBoost MAE", f"{xgb_mae:.2f}", "Temporal holdout")
        with perf_col3:
            st.metric("Improvement vs Baseline", f"{improvement_pct:.1f}%", "Temporal holdout")
        with perf_col4:
            st.metric("XGBoost RMSE", f"{xgb_rmse:.2f}", "Temporal holdout")

        st.caption(
            "Model performance is calculated on the final temporal holdout set and remains fixed as a global reliability benchmark. "
            "Sidebar selections change the case-level prediction, recommendation, safety status, and recovery estimate. "
            "Earlier 5-seed mean evaluation (MAE 0.68) is retained in model logs for robustness checks."
        )

        # Baseline comparison chart — XGBoost uses temporal holdout value
        st.markdown(f'<div class="section-header">{ICONS["chart"]} Baseline vs Model Comparison</div>', unsafe_allow_html=True)

        chart_data = results_df[results_df["is_baseline"] == True].copy()
        # Add XGBoost temporal holdout row
        xgb_row = pd.DataFrame([{
            "model": "XGBoost (Temporal Holdout)",
            "MAE": float(xgb_mae),
            "RMSE": float(xgb_rmse),
            "is_baseline": False,
        }])
        chart_data = pd.concat([chart_data, xgb_row], ignore_index=True)

        fig = px.bar(
            chart_data,
            x="model",
            y=["MAE", "RMSE"],
            barmode="group",
            color_discrete_sequence=["#10B981", "#6B7280"],
        )
        fig.update_layout(
            plot_bgcolor="rgba(19,25,24,1)",
            paper_bgcolor="rgba(19,25,24,1)",
            font_color="#9CA3AF",
            xaxis=dict(
                title=None,
                tickfont=dict(color="#9CA3AF", size=12),
                linecolor="#1F2A28",
                showgrid=False,
            ),
            yaxis=dict(
                title=None,
                tickfont=dict(color="#6B7280", size=11),
                linecolor="#1F2A28",
                showgrid=True,
                gridcolor="rgba(31,42,40,0.8)",
            ),
            legend=dict(
                title=None,
                font=dict(color="#9CA3AF", size=12),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
            margin=dict(l=40, r=20, t=40, b=40),
            barmode="group",
            bargap=0.15,
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, width='stretch')
        st.caption(
            "Model metrics are shown for transparency. Merchant action should be based on the recommendation, "
            "safety status, and business context — not MAE alone."
        )
    else:
        st.info("Run evaluation to see model performance metrics")

    # Feature Importance
    if importance_df is not None:
        st.markdown(f'<div class="section-header">{ICONS["trending"]} Top 10 Feature Importances</div>', unsafe_allow_html=True)
        top_features = importance_df.head(10)
        st.data_editor(
            top_features[["feature", "importance"]].rename(columns={"feature": "Feature", "importance": "Importance"}),
            disabled=True,
            hide_index=True,
            width='stretch',
        )

    # Recommendation Panel
    st.markdown("---")
    st.subheader("Discount Recommendation")

    # (Safety and recommendation already computed above for Executive Decision Summary)
    st.markdown("---")

    # Hero card — main recommendation
    emoji = CATEGORY_EMOJI.get(selected_category, "🍽️")
    savings = _safe_get(record, "original_price", 10.0) - recommendation["discounted_price"]
    st.markdown(f'''
    <div class="rec-hero">
        <div class="rec-hero-header">
            <div>
                <div class="rec-hero-label">{emoji} Recommended Discount</div>
                <div class="rec-hero-discount">{recommendation['recommended_discount_pct']*100:.0f}%</div>
                <div class="rec-hero-prices">
                    <span class="rec-hero-original">SGD {_safe_get(record, 'original_price', 10.0):.2f}</span>
                    <span class="rec-hero-discounted">SGD {recommendation['discounted_price']:.2f}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div class="rec-hero-badge">{ICONS["zap"]} Save SGD {savings:.2f}</div>
                <div style="margin-top: 12px;">
                    <div class="rec-hero-label">Revenue Recovery</div>
                    <div class="metric-value" style="font-size: 28px; color: var(--accent);">SGD {recommendation['estimated_merchant_recovery']:.2f}</div>
                </div>
            </div>
        </div>
        <div class="rec-hero-savings">
            <div class="rec-hero-savings-item">
                <span class="metric-label">Potential Loss</span>
                <span style="font-size: 15px; color: var(--text-secondary);">SGD {recommendation['original_value']:.2f}</span>
            </div>
            <div class="rec-hero-savings-item">
                <span class="metric-label">Recovery Rate</span>
                <span style="font-size: 15px; color: var(--accent);">{recommendation['estimated_merchant_recovery'] / recommendation['original_value'] * 100:.0f}%</span>
            </div>
            <div class="rec-hero-savings-item">
                <span class="metric-label">Listing Time</span>
                <span style="font-size: 15px; color: var(--text-primary);">{recommendation['recommended_listing_time']}</span>
            </div>
            <div class="rec-hero-savings-item">
                <span class="metric-label">Pickup Window</span>
                <span style="font-size: 15px; color: var(--text-primary);">{recommendation['recommended_pickup_window']}</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ===== WHY THIS RECOMMENDATION? =====
    # Build action label based on discount tier
    discount_pct = recommendation['recommended_discount_pct']
    if discount_pct >= 0.6:
        action_label = "DEEP DISCOUNT"
        action_color = "#EF4444"
    elif discount_pct >= 0.4:
        action_label = "DISCOUNT"
        action_color = "#F59E0B"
    elif discount_pct >= 0.2:
        action_label = "MONITOR"
        action_color = "#3B82F6"
    else:
        action_label = "HOLD"
        action_color = "#10B981"

    surplus_qty = recommendation['predicted_surplus']
    shelf_life = _safe_get(record, 'shelf_life_hours', 48.0)
    holding = _safe_get(record, 'holding_time_hours', 2.0)
    remaining = shelf_life - holding
    recovery = recommendation['estimated_merchant_recovery']
    original = recommendation['original_value']

    st.markdown(f"""
    <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px 24px; margin: 16px 0;">
        <div style="display: flex; align-items: flex-start; gap: 16px;">
            <div style="background: {action_color}22; border: 1px solid {action_color}; border-radius: 8px; padding: 8px 16px; flex-shrink: 0;">
                <div style="font-size: 11px; font-weight: 700; color: {action_color}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Recommended Action</div>
                <div style="font-size: 18px; font-weight: 700; color: {action_color};">{action_label}</div>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px;">Why this recommendation?</div>
                <div style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
                    <strong>{surplus_qty:.0f} units</strong> predicted surplus for <strong>{selected_category}</strong> at <strong>{merchant_id}</strong> ·
                    <strong>{remaining:.0f}h remaining</strong> shelf life ({holding:.0f}h already held) ·
                    <strong>{discount_pct*100:.0f}% discount</strong> recommended ·
                    Estimated recovery: <strong>SGD {recovery:.2f}</strong> vs potential loss of SGD {original:.2f}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== SAFETY CONFIDENCE NOTE =====
    if safety_result.status == "SAFE":
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 12px 16px; margin: 0 0 16px 0;">
            <div style="font-size: 12px; color: #10B981; font-weight: 600; margin-bottom: 4px;">✓ Safety Confidence: Item passed all 5 safety checks</div>
            <div style="font-size: 11px; color: var(--text-tertiary);">Food safety screening is advisory. Merchant assumes responsibility for compliance with SFA regulations and in-store handling procedures.</div>
        </div>
        """, unsafe_allow_html=True)
    elif safety_result.status == "CAUTION":
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 12px 16px; margin: 0 0 16px 0;">
            <div style="font-size: 12px; color: #F59E0B; font-weight: 600; margin-bottom: 4px;">⚠ Safety Confidence: Caution advised — review warnings before listing</div>
            <div style="font-size: 11px; color: var(--text-tertiary);">Food safety screening is advisory. Merchant assumes responsibility for compliance with SFA regulations and in-store handling procedures.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 12px 16px; margin: 0 0 16px 0;">
            <div style="font-size: 12px; color: #EF4444; font-weight: 600; margin-bottom: 4px;">✕ Safety Confidence: Item blocked — cannot be recommended for listing</div>
            <div style="font-size: 11px; color: var(--text-tertiary);">Food safety screening is advisory. Merchant assumes responsibility for compliance with SFA regulations and in-store handling procedures.</div>
        </div>
        """, unsafe_allow_html=True)

    # Three-column grid: Food Safety | Listing Schedule | Product Details
    col_safety, col_schedule, col_details = st.columns(3)

    with col_safety:
        st.markdown(f'<div class="section-header">{ICONS["eye"]} Food Safety</div>', unsafe_allow_html=True)
        if safety_result.status == "SAFE":
            st.markdown('''
            <div class="safety-badge safe">
                <span class="safety-icon">✓</span>
                <span>SAFE — Item can be listed</span>
            </div>''', unsafe_allow_html=True)
        elif safety_result.status == "CAUTION":
            st.markdown('''
            <div class="safety-badge caution">
                <span class="safety-icon">!</span>
                <span>CAUTION — List with warnings</span>
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="safety-badge blocked">
                <span class="safety-icon">✕</span>
                <span>BLOCKED — Cannot be listed</span>
            </div>''', unsafe_allow_html=True)
        with st.expander("View Safety Checks"):
            for check in safety_result.checks:
                if check.severity == "BLOCK":
                    st.error(f"❌ {check.message}")
                elif check.severity == "CAUTION":
                    st.warning(f"⚠️ {check.message}")
                else:
                    st.success(f"✓ {check.message}")
        st.markdown(
            '<p style="font-size:11px; color:#6B7280; margin-top:8px;">'
            '⚠ Advisory only — not SFA validated. Merchants remain responsible for food safety compliance.</p>',
            unsafe_allow_html=True
        )

    with col_schedule:
        st.markdown(f'<div class="section-header">{ICONS["calendar"]} Listing Schedule</div>', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="card">
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div>
                    <div class="metric-label">List At</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{recommendation['recommended_listing_time']}</div>
                </div>
                <div>
                    <div class="metric-label">Pickup Window</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{recommendation['recommended_pickup_window']}</div>
                </div>
                <div>
                    <div class="metric-label">Latest Pickup</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{recommendation['latest_pickup_time']}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col_details:
        st.markdown(f'<div class="section-header">{ICONS["package"]} Product Details</div>', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="card">
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div>
                    <div class="metric-label">Storage</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{_safe_get(record, 'storage_type', 'Refrigerated')}</div>
                </div>
                <div>
                    <div class="metric-label">Shelf Life</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{_safe_get(record, 'shelf_life_hours', 48.0):.0f} hours</div>
                </div>
                <div>
                    <div class="metric-label">Holding Time</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{_safe_get(record, 'holding_time_hours', 2.0):.1f} hours</div>
                </div>
                <div>
                    <div class="metric-label">Preparation</div>
                    <div style="font-size: 15px; color: var(--text-primary);">{_safe_get(record, 'preparation_time', 30)} min</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Recommendation explanation
    rec_explanation = recommendation["recommendation_explanation"]
    if cold_start_mode and cold_start_note is not None:
        rec_explanation += f"\n\n> **Cold-start note:** This prediction uses cluster-level surplus ratios calibrated against merchants with similar operating patterns. It will refine as this merchant's own data accumulates."
    st.markdown(f'<div class="section-header" style="margin-top: 24px;">{ICONS["lightbulb"]} Recommendation</div>', unsafe_allow_html=True)
    st.markdown(rec_explanation)

    # Phase 2 Listing Preview
    st.markdown("---")
    st.markdown(f'<div class="section-header" style="margin-bottom: 16px;">{ICONS["clock"]} Phase 2 Listing Preview</div>', unsafe_allow_html=True)
    st.caption("Optional preview only. Consumer marketplace listing is a Phase 2 extension and is not part of the submitted MVP.")

    preview_col1, preview_col2 = st.columns([1, 2])

    with preview_col1:
        savings = _safe_get(record, "original_price", 10.0) - recommendation["discounted_price"]
        listing_html = f"""
<div style="background: #FFFFFF; border-radius: 12px; overflow: hidden; max-width: 480px;">
  <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 16px 20px; display: flex; justify-content: space-between; align-items: center;">
    <div>
      <div style="color: #FFFFFF; font-size: 12px; opacity: 0.85; margin-bottom: 2px;">{merchant_type}</div>
      <div style="color: #FFFFFF; font-size: 18px; font-weight: 700;">{merchant_id}</div>
    </div>
    <div style="background: rgba(255,255,255,0.2); color: #FFFFFF; padding: 6px 12px; border-radius: 999px; font-weight: 700; font-size: 13px;">{recommendation["recommended_discount_pct"]*100:.0f}% OFF</div>
  </div>
  <div style="padding: 20px; background: #FFFFFF;">
    <div style="color: #111827; font-size: 24px; font-weight: 700; margin: 0 0 4px 0; line-height: 1.2;">{selected_product}</div>
    <div style="color: #6B7280; font-size: 14px; margin-bottom: 16px;">{selected_category}</div>
    <div style="margin-bottom: 16px;">
      <span style="color: #9CA3AF; font-size: 14px; text-decoration: line-through; margin-right: 8px;">SGD {_safe_get(record, "original_price", 10.0):.2f}</span>
      <span style="color: #059669; font-size: 22px; font-weight: 700;">SGD {recommendation["discounted_price"]:.2f}</span>
    </div>
    <div style="color: #059669; font-size: 13px; font-weight: 600; margin-bottom: 16px;">You save SGD {savings:.2f}</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px; padding-top: 12px; border-top: 1px solid #E5E7EB;">
      <div>
        <div style="color: #9CA3AF; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Pickup By</div>
        <div style="color: #111827; font-size: 14px; font-weight: 600;">{recommendation["recommended_pickup_window"]}</div>
      </div>
      <div>
        <div style="color: #9CA3AF; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Listed At</div>
        <div style="color: #111827; font-size: 14px; font-weight: 600;">{recommendation["recommended_listing_time"]}</div>
      </div>
      <div>
        <div style="color: #9CA3AF; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Storage</div>
        <div style="color: #111827; font-size: 14px; font-weight: 600;">{_safe_get(record, "storage_type", "Refrigerated")}</div>
      </div>
    </div>
    <div style="margin-bottom: 16px;">
      <div style="color: #9CA3AF; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Freshness</div>
      <div style="color: #111827; font-size: 14px; font-weight: 600;">{_safe_get(record, "shelf_life_hours", 48.0) - _safe_get(record, "holding_time_hours", 2.0):.0f}h remaining</div>
    </div>
    <div style="background: #ECFDF5; border-radius: 8px; padding: 12px;">
      <span style="color: #059669; font-weight: 600; font-size: 13px;">Consumer Tip:</span>
      <span style="color: #064E3B; font-size: 13px;"> Best consumed today. Help reduce food waste while saving money.</span>
    </div>
  </div>
</div>
"""
        st.markdown(listing_html, unsafe_allow_html=True)

    with preview_col2:
        st.markdown(f'<div class="section-header">{ICONS["dollar"]} Listing Details</div>', unsafe_allow_html=True)

        item_details = pd.DataFrame({
            "Attribute": [
                "Product",
                "Merchant",
                "Original Price",
                "Discounted Price",
                "You Save",
                "Pickup Window",
                "Storage",
                "Shelf Life Remaining",
                "Safety Status"
            ],
            "Value": [
                selected_product,
                f"{merchant_id} ({merchant_type})",
                f"SGD {_safe_get(record, 'original_price', 10.0):.2f}",
                f"SGD {recommendation['discounted_price']:.2f}",
                f"SGD {_safe_get(record, 'original_price', 10.0) - recommendation['discounted_price']:.2f}",
                recommendation['recommended_pickup_window'],
                _safe_get(record, 'storage_type', 'Refrigerated'),
                f"{_safe_get(record, 'shelf_life_hours', 48.0) - _safe_get(record, 'holding_time_hours', 2.0):.0f} hours",
                safety_result.status
            ]
        })

        st.data_editor(
            item_details,
            disabled=True,
            hide_index=True,
            width='stretch',
        )

    # Revenue Recovery Simulator
    st.markdown("---")
    st.subheader("Revenue Recovery Simulator")

    st.markdown("Adjust parameters to see how different discount levels affect recovery:")

    sim_col1, sim_col2, sim_col3 = st.columns(3)

    with sim_col1:
        sim_discount = st.slider("Discount Level", 0, 70, int(recommendation['recommended_discount_pct']*100)) / 100

    with sim_col2:
        sim_quantity = st.slider("Surplus Quantity", 0, 50, int(recommendation['predicted_surplus']))

    with sim_col3:
        sim_price = st.number_input("Original Price (SGD)", 1.0, 50.0, _safe_get(record, 'original_price', 10.0), 0.5)

    # Calculate simulation
    original_value = sim_price * sim_quantity
    discounted_price = sim_price * (1 - sim_discount)
    recovery = discounted_price * sim_quantity
    loss_prevention = recovery / original_value * 100 if original_value > 0 else 0

    sim_col4, sim_col5, sim_col6 = st.columns(3)
    with sim_col4:
        st.markdown(f'''
        <div class="sim-card">
            <div class="metric-label">Original Value</div>
            <div class="metric-value">SGD {original_value:.2f}</div>
        </div>''', unsafe_allow_html=True)
    with sim_col5:
        st.markdown(f'''
        <div class="sim-card">
            <div class="metric-label">Estimated Recovery</div>
            <div class="metric-value">SGD {recovery:.2f}</div>
            <div class="metric-delta">{loss_prevention:.1f}% recovered</div>
        </div>''', unsafe_allow_html=True)
    with sim_col6:
        st.markdown(f'''
        <div class="sim-card">
            <div class="metric-label">Discount per Unit</div>
            <div class="metric-value">SGD {sim_price * sim_discount:.2f}</div>
        </div>''', unsafe_allow_html=True)

    # Export Section
    st.markdown("---")
    st.subheader("Export Recommendation")

    # Create export dataframe
    export_data = {
        "Merchant ID": [merchant_id],
        "Merchant Type": [merchant_type],
        "Category": [selected_category],
        "Product": [selected_product],
        "Predicted Surplus": [recommendation['predicted_surplus']],
        "Recommended Discount %": [recommendation['recommended_discount_pct']*100],
        "Discounted Price": [recommendation['discounted_price']],
        "Estimated Recovery (SGD)": [recommendation['estimated_merchant_recovery']],
        "Listing Time": [recommendation['recommended_listing_time']],
        "Pickup Window": [recommendation['recommended_pickup_window']],
        "Safety Status": [safety_result.status],
        "Safety Flags": [", ".join(safety_result.flags) if safety_result.flags else "None"],
    }

    export_df = pd.DataFrame(export_data)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(export_df, width='stretch')

    with col2:
        csv = export_df.to_csv(index=False)
        st.download_button(
            "📥 Download as CSV",
            csv,
            f"surplus_recommendation_{merchant_id}_{selected_date}.csv",
            "text/csv",
            key='download-csv'
        )

        # Also offer to save sample recommendations
        if st.button("Save to Sample Recommendations"):
            sample_path = os.path.join(BASE_DIR, "outputs/sample_recommendations.csv")
            if os.path.exists(sample_path):
                existing = pd.read_csv(sample_path)
                combined = pd.concat([existing, export_df], ignore_index=True)
            else:
                combined = export_df
            combined.to_csv(sample_path, index=False)
            st.success(f"Saved to {sample_path}")

    # Professional Footer
    st.markdown("---")
    st.markdown(f'''
    <div class="footer">
        <div class="footer-brand">
            <svg class="footer-logo" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="32" height="32" rx="8" fill="#064E3B"/>
                <path d="M16 6C16 6 10 10 10 17C10 20.3137 12.6863 23 16 23C19.3137 23 22 20.3137 22 17C22 10 16 6 16 6Z" fill="#10B981"/>
                <circle cx="16" cy="17" r="3" fill="#064E3B"/>
            </svg>
            <span class="footer-title">SurplusSense</span>
        </div>
        <div class="footer-subtitle">AI Decision Cockpit for F&B Merchants</div>
        <div class="footer-badge">MVP Prototype</div>
        <div class="footer-disclaimer">
            For educational purposes only. Synthetic data demonstration — not real merchant data or financial advice.
        </div>
        <div class="footer-meta">
            <span>SMU MBA Machine Learning Project</span>
            <span>•</span>
            <span>SurplusSense v1.0</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Production Considerations
    st.caption("**Production Considerations:** PDPA compliance (consent, access/correction rights, breach notification) required before any real merchant or consumer deployment. ESG/reporting metrics (NEA waste reporting, full GHG accounting) are Phase 3+ scope.")


if __name__ == "__main__":
    main()
