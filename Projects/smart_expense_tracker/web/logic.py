"""
logic.py — Core business logic for the Smart Expense Tracker (Web Version).
Storage backend: SQLite (via Python's built-in sqlite3 module).
Business logic is cleanly separated from Flask routing (app.py).
"""

import json
import os
import sqlite3
from datetime import datetime

# ─────────────────────────────────────────────
#  STORAGE CONFIGURATION
# ─────────────────────────────────────────────

DB_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.db")

# Legacy JSON file — used only for one-time migration on first boot
_LEGACY_JSON = os.path.join(os.path.dirname(__file__), "data", "expenses.json")

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
#  DATABASE HELPERS
# ─────────────────────────────────────────────

def _get_connection():
    """Return a configured SQLite connection with Row factory."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row          # allows dict-like column access
    conn.execute("PRAGMA journal_mode=WAL") # safe concurrent writes
    return conn


def init_db():
    """
    Create the expenses table if it doesn't exist, then migrate any
    legacy JSON data into SQLite (runs once automatically).
    """
    with _get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                description TEXT    NOT NULL,
                date        TEXT    NOT NULL
            )
        """)
        conn.commit()

    _migrate_legacy_json()


def _migrate_legacy_json():
    """
    If a legacy expenses.json exists and the DB is empty, import the
    JSON records into SQLite, then rename the JSON file so migration
    doesn't run again.
    """
    if not os.path.exists(_LEGACY_JSON):
        return

    try:
        with open(_LEGACY_JSON, "r") as f:
            records = json.load(f)
    except (json.JSONDecodeError, IOError):
        return  # silently skip a corrupt file

    if not records:
        return

    with _get_connection() as conn:
        # Only migrate when the table is empty to avoid duplicates
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        if count > 0:
            return

        conn.executemany(
            """INSERT INTO expenses (id, amount, category, description, date)
               VALUES (:id, :amount, :category, :description, :date)""",
            records,
        )
        conn.commit()

    # Rename so future starts skip migration
    os.rename(_LEGACY_JSON, _LEGACY_JSON + ".migrated")


def _row_to_dict(row):
    """Convert a sqlite3.Row to a plain dict."""
    return dict(row)


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

    with _get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO expenses (amount, category, description, date)
               VALUES (?, ?, ?, ?)""",
            (amount, category, description, _get_timestamp()),
        )
        conn.commit()
        new_id = cursor.lastrowid

    return get_expense_by_id(new_id)


def get_all_expenses():
    """Return all expenses sorted by date descending."""
    with _get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC"
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_expense_by_id(expense_id):
    """Return a single expense dict or None if not found."""
    with _get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
    return _row_to_dict(row) if row else None


def update_expense(expense_id, amount_str=None, category=None, description=None):
    """
    Update one or more fields of an expense.
    Raises ValueError if not found or validation fails.
    Returns the updated expense dict.
    """
    existing = get_expense_by_id(expense_id)
    if existing is None:
        raise ValueError(f"No expense found with ID {expense_id}.")

    new_amount = validate_amount(amount_str) if amount_str is not None else existing["amount"]
    new_category = validate_category(category) if category is not None else existing["category"]
    new_description = validate_description(description) if description is not None else existing["description"]

    with _get_connection() as conn:
        conn.execute(
            """UPDATE expenses
               SET amount = ?, category = ?, description = ?
               WHERE id = ?""",
            (new_amount, new_category, new_description, expense_id),
        )
        conn.commit()

    return get_expense_by_id(expense_id)


def delete_expense(expense_id):
    """
    Delete an expense by ID.
    Raises ValueError if not found.
    """
    if get_expense_by_id(expense_id) is None:
        raise ValueError(f"No expense found with ID {expense_id}.")

    with _get_connection() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

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
    with _get_connection() as conn:
        rows = conn.execute("SELECT * FROM expenses").fetchall()

    expenses = [_row_to_dict(r) for r in rows]

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
    """Return expenses matching the given category."""
    category = validate_category(category)
    with _get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC",
            (category,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]
