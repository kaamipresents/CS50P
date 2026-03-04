"""
logic.py — Core business logic for the Smart Expense Tracker (Web Version).
Storage backend: PostgreSQL via psycopg2.
Connection string is read from the DATABASE_URL environment variable.
"""

import os
from datetime import datetime

import psycopg2
import psycopg2.extras  # RealDictCursor

# ─────────────────────────────────────────────
#  STORAGE CONFIGURATION
# ─────────────────────────────────────────────

DATABASE_URL = os.environ.get("DATABASE_URL")

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
    """
    Open and return a new psycopg2 connection.
    Raises RuntimeError with a helpful message if DATABASE_URL is not set.
    """
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Add it in your Vercel project settings (or .env locally)."
        )
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def init_db():
    """
    Create the expenses table if it doesn't already exist.
    Called once at app startup (from app.py).
    """
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id          SERIAL PRIMARY KEY,
                    amount      NUMERIC(12, 2) NOT NULL,
                    category    TEXT           NOT NULL,
                    description TEXT           NOT NULL,
                    date        TEXT           NOT NULL
                )
            """)
        conn.commit()


def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _row_to_dict(row):
    """Convert a RealDictRow to a plain python dict with native types."""
    d = dict(row)
    # psycopg2 returns NUMERIC as Decimal — convert to float for consistency
    if "amount" in d and d["amount"] is not None:
        d["amount"] = float(d["amount"])
    return d


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
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO expenses (amount, category, description, date)
                   VALUES (%s, %s, %s, %s)
                   RETURNING *""",
                (amount, category, description, _get_timestamp()),
            )
            new_row = cur.fetchone()
        conn.commit()

    return _row_to_dict(new_row)


def get_all_expenses():
    """Return all expenses sorted by date descending."""
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM expenses ORDER BY date DESC")
            rows = cur.fetchall()
    return [_row_to_dict(r) for r in rows]


def get_expense_by_id(expense_id):
    """Return a single expense dict or None if not found."""
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
            row = cur.fetchone()
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
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE expenses
                   SET amount = %s, category = %s, description = %s
                   WHERE id = %s""",
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
        with conn.cursor() as cur:
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
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
    expenses = get_all_expenses()

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
    """Return expenses matching the given category, sorted by date descending."""
    category = validate_category(category)
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM expenses WHERE category = %s ORDER BY date DESC",
                (category,),
            )
            rows = cur.fetchall()
    return [_row_to_dict(r) for r in rows]
