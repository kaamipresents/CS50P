"""
logic.py — Core business logic for the Smart Expense Tracker.
Pure functions: no Flask, no CLI concerns. Reusable in both CLI and Web.
"""

from storage import load_expenses, save_expenses, generate_id, get_timestamp

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
#  VALIDATION
# ─────────────────────────────────────────────

def validate_amount(amount_str):
    """
    Validate that amount is a positive number.
    Args:
        amount_str (str or float): Raw amount input.
    Returns:
        float: Validated amount.
    Raises:
        ValueError: If amount is invalid.
    """
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number (e.g. 12.50).")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_category(category):
    """
    Validate that category is in the allowed list.
    Args:
        category (str): Raw category input.
    Returns:
        str: Validated, title-cased category.
    Raises:
        ValueError: If category is not recognized.
    """
    if not category or not category.strip():
        raise ValueError("Category cannot be empty.")
    normalized = category.strip().title()
    if normalized not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category '{normalized}'. "
            f"Choose from: {', '.join(VALID_CATEGORIES)}"
        )
    return normalized


def validate_description(description):
    """
    Validate that description is a non-empty string under 200 chars.
    Args:
        description (str): Raw description input.
    Returns:
        str: Cleaned description.
    Raises:
        ValueError: If description fails validation.
    """
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
    Add a new expense entry.
    Args:
        amount_str (str): Raw amount string from user input.
        category (str): Expense category.
        description (str): Short description of the expense.
    Returns:
        dict: The newly created expense record.
    Raises:
        ValueError: If any field fails validation.
    """
    amount = validate_amount(amount_str)
    category = validate_category(category)
    description = validate_description(description)

    expenses = load_expenses()

    new_expense = {
        "id": generate_id(expenses),
        "amount": amount,
        "category": category,
        "description": description,
        "date": get_timestamp(),
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense


def get_all_expenses():
    """
    Retrieve all expenses, sorted by most recent first.
    Returns:
        list: All expense dicts.
    """
    expenses = load_expenses()
    return sorted(expenses, key=lambda e: e["date"], reverse=True)


def get_expense_by_id(expense_id):
    """
    Find a single expense by its ID.
    Args:
        expense_id (int): The expense ID to search for.
    Returns:
        dict or None: The matching expense, or None if not found.
    """
    expenses = load_expenses()
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


def update_expense(expense_id, amount_str=None, category=None, description=None):
    """
    Update fields of an existing expense.
    Only provided (non-None) fields are updated.
    Args:
        expense_id (int): ID of the expense to update.
        amount_str (str, optional): New amount.
        category (str, optional): New category.
        description (str, optional): New description.
    Returns:
        dict: Updated expense record.
    Raises:
        ValueError: If expense not found or validation fails.
    """
    expenses = load_expenses()
    target = None

    for expense in expenses:
        if expense["id"] == expense_id:
            target = expense
            break

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
    """
    Delete an expense by ID.
    Args:
        expense_id (int): ID of the expense to delete.
    Returns:
        bool: True if deleted successfully.
    Raises:
        ValueError: If expense is not found.
    """
    expenses = load_expenses()
    original_count = len(expenses)
    expenses = [e for e in expenses if e["id"] != expense_id]

    if len(expenses) == original_count:
        raise ValueError(f"No expense found with ID {expense_id}.")

    save_expenses(expenses)
    return True


# ─────────────────────────────────────────────
#  SUMMARY & ANALYTICS
# ─────────────────────────────────────────────

def get_summary():
    """
    Calculate spending summary grouped by category.
    Returns:
        dict: {
            "total": float,
            "count": int,
            "by_category": { "Food": 45.50, ... },
            "highest_expense": dict or None,
            "average": float,
        }
    """
    expenses = load_expenses()

    if not expenses:
        return {
            "total": 0.0,
            "count": 0,
            "by_category": {},
            "highest_expense": None,
            "average": 0.0,
        }

    total = sum(e["amount"] for e in expenses)
    by_category = {}

    for expense in expenses:
        cat = expense["category"]
        by_category[cat] = round(by_category.get(cat, 0.0) + expense["amount"], 2)

    highest = max(expenses, key=lambda e: e["amount"])
    average = round(total / len(expenses), 2)

    return {
        "total": round(total, 2),
        "count": len(expenses),
        "by_category": by_category,
        "highest_expense": highest,
        "average": average,
    }


def filter_by_category(category):
    """
    Filter expenses by a specific category.
    Args:
        category (str): Category to filter on.
    Returns:
        list: Matching expense dicts.
    Raises:
        ValueError: If category is invalid.
    """
    category = validate_category(category)
    expenses = load_expenses()
    return [e for e in expenses if e["category"] == category]
