"""
storage.py — File-based JSON persistence layer for the Expense Tracker.
All read/write operations on expenses.json live here.
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.json")


def _ensure_data_file():
    """Create the data directory and JSON file if they don't exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_expenses():
    """
    Load all expenses from the JSON file.
    Returns a list of expense dicts.
    """
    _ensure_data_file()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Could not read expenses file: {e}")


def save_expenses(expenses):
    """
    Overwrite the JSON file with the given list of expenses.
    Args:
        expenses (list): Full list of expense dicts to persist.
    """
    _ensure_data_file()
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
    except IOError as e:
        raise RuntimeError(f"Could not write expenses file: {e}")


def generate_id(expenses):
    """
    Generate a simple incrementing integer ID.
    Args:
        expenses (list): Existing expenses list.
    Returns:
        int: Next available ID.
    """
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def get_timestamp():
    """Return current datetime as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
