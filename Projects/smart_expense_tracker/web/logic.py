"""
logic.py — Core business logic for the Smart Expense Tracker (Web Version).
This file is identical in structure to the CLI version — only the DATA_FILE
path differs. This is intentional: pure logic, zero framework dependencies.
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  STORAGE CONFIGURATION
# ─────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.json")

VALID_CATEGORIES = [
    "Food",
    "Transport",
    "Housing",
    "Entertainment",
    "Health",
    "Shopping",
    "Education",
    "Other",
]


# ─────────────────────────────────────────────
#  STORAGE LAYER
# ─────────────────────────────────────────────

def _ensure_data_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_expenses():
    _ensure_data_file()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Could not read expenses file: {e}")


def save_expenses(expenses):
    _ensure_data_file()
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
    except IOError as e:
        raise RuntimeError(f"Could not write expenses file: {e}")


def _generate_id(expenses):
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number (e.g. 12.50).")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_category(category):
    if not category or not category.strip():
        raise ValueError("Category cannot be empty.")
    normalized = category.strip().title()
    if normalized not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category. Choose from: {', '.join(VALID_CATEGORIES)}")
    return normalized


def validate_description(description):
    if not description or not description.strip():
        raise ValueError("Description cannot be empty.")
    cleaned = description.strip()
    if len(cleaned) > 200:
        raise ValueError("Description must be under 200 characters.")
    return cleaned


# ─────────────────────────────────────────────
#  CRUD OPERATIONS
# ─────────────────────────────────────────────

def add_expense(amount_str, category, description):
    """
    Validate inputs and persist a new expense.
    Returns:
        dict: The newly created expense.
    Raises:
        ValueError: On validation failure.
    """
    amount = validate_amount(amount_str)
    category = validate_category(category)
    description = validate_description(description)

    expenses = load_expenses()
    new_expense = {
        "id": _generate_id(expenses),
        "amount": amount,
        "category": category,
        "description": description,
        "date": _get_timestamp(),
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense


def get_all_expenses():
    expenses = load_expenses()
    return sorted(expenses, key=lambda e: e["date"], reverse=True)


def get_expense_by_id(expense_id):
    for expense in load_expenses():
        if expense["id"] == expense_id:
            return expense
    return None


def update_expense(expense_id, amount_str=None, category=None, description=None):
    expenses = load_expenses()
    target = next((e for e in expenses if e["id"] == expense_id), None)

    if target is None:
        raise ValueError(f"No expense found with ID {expense_id}.")

    if amount_str is not None:
        target["amount"] = validate_amount(amount_str)
    if category is not None:
        target["category"] = validate_category(category)
    if description is not None:
        target["description"] = validate_description(description)

    save_expenses(expenses)
    return target


def delete_expense(expense_id):
    expenses = load_expenses()
    filtered = [e for e in expenses if e["id"] != expense_id]
    if len(filtered) == len(expenses):
        raise ValueError(f"No expense found with ID {expense_id}.")
    save_expenses(filtered)
    return True


# ─────────────────────────────────────────────
#  SUMMARY & ANALYTICS
# ─────────────────────────────────────────────

def get_summary():
    """
    Compute aggregate statistics across all expenses.
    Returns:
        dict: total, count, by_category, highest_expense, average, percentages.
    """
    expenses = load_expenses()

    if not expenses:
        return {
            "total": 0.0,
            "count": 0,
            "by_category": {},
            "highest_expense": None,
            "average": 0.0,
            "category_percentages": {},
        }

    total = sum(e["amount"] for e in expenses)
    by_category = {}

    for expense in expenses:
        cat = expense["category"]
        by_category[cat] = round(by_category.get(cat, 0.0) + expense["amount"], 2)

    category_percentages = {
        cat: round((amount / total) * 100, 1)
        for cat, amount in by_category.items()
    }

    highest = max(expenses, key=lambda e: e["amount"])
    average = round(total / len(expenses), 2)

    return {
        "total": round(total, 2),
        "count": len(expenses),
        "by_category": by_category,
        "highest_expense": highest,
        "average": average,
        "category_percentages": category_percentages,
    }


def filter_by_category(category):
    category = validate_category(category)
    return [e for e in load_expenses() if e["category"] == category]
