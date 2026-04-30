#!/usr/bin/env python3
"""
SurplusSense Data Generator Module
==================================
Wrapper module that re-exports the data generation functionality.
Can be imported by other modules.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.generate_synthetic_data import generate_records, save_to_csv, RANDOM_SEED

__all__ = ["generate_records", "save_to_csv", "RANDOM_SEED"]
