#!/usr/bin/env python3
"""
Demo utilities for importing DevTrackr modules
"""

import sys
import os


def setup_demo_imports():
    """Add the parent directory to Python path for imports"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
