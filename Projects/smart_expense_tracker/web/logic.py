"""
logic.py — Core business logic for the Smart Expense Tracker (Web Version).
Storage backend: PostgreSQL via psycopg2.
Connection string is read from the DATABASE_URL environment variable.
"""

import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file FIRST
load_dotenv()

import psycopg2
import psycopg2.extras  # RealDictCursor
from psycopg2 import pool
from contextlib import contextmanager

# ─────────────────────────────────────────────
#  STORAGE CONFIGURATION
# ─────────────────────────────────────────────

DATABASE_URL = os.environ.get("DATABASE_URL")

# Create a global connection pool (min 1 connection, max 10 connections)
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
    db_pool = None

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

@contextmanager
def _get_connection():
    """
    Yield a psycopg2 connection from the connection pool.
    Ensures the connection is returned to the pool after use.
    Raises RuntimeError with a helpful message if DB URL is missing or pool failed.
    """
    if not DATABASE_URL or not db_pool:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set or pool failed to initialize. "
            "Add it in your Vercel project settings (or .env locally)."
        )
    
    conn = db_pool.getconn()
    try:
        # Set the row factory for this connection session
        conn.cursor_factory = psycopg2.extras.RealDictCursor
        yield conn
    finally:
        # Give back the connection when the `with` block finishes
        db_pool.putconn(conn)


def init_db():
    """
    Create the users and expenses tables if they don't already exist.
    Called once at app startup (from app.py).
    """
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id          SERIAL PRIMARY KEY,
                    google_id   TEXT UNIQUE NOT NULL,
                    email       TEXT UNIQUE NOT NULL,
                    name        TEXT NOT NULL,
                    picture     TEXT
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id          SERIAL PRIMARY KEY,
                    user_id     INTEGER REFERENCES users(id),
                    amount      NUMERIC(12, 2) NOT NULL,
                    category    TEXT           NOT NULL,
                    description TEXT           NOT NULL,
                    date        TEXT           NOT NULL
                )
            """)
            
            # For existing databases: add user_id column if it doesn't exist.
            try:
                cur.execute("""
                    ALTER TABLE expenses 
                    ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)
                """)
            except psycopg2.Error:
                pass # Column might already exist or error handling
            
            # Create indexes for extreme performance scaling
            cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date DESC)")
            
        conn.commit()

# ─────────────────────────────────────────────
#  USER MANAGEMENT
# ─────────────────────────────────────────────

def get_or_create_user(google_info):
    """
    Fetch user by google_id. If not found, create new user.
    Also, if this is the first user, assign all orphan expenses to them.
    Returns user dict.
    """
    # Google openid returns the unique ID in the 'sub' field
    google_id = google_info.get('sub') or google_info.get('id')
    
    if not google_id:
        raise ValueError("Could not find user ID in Google's response.")

    with _get_connection() as conn:
        with conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
            user = cur.fetchone()
            
            if not user:
                # Check if it's the very first user
                cur.execute("SELECT COUNT(*) as cnt FROM users")
                is_first_user = cur.fetchone()['cnt'] == 0
                
                # Create user
                cur.execute(
                    """INSERT INTO users (google_id, email, name, picture)
                       VALUES (%s, %s, %s, %s)
                       RETURNING *""",
                    (google_id, google_info['email'], google_info['name'], google_info.get('picture'))
                )
                user = cur.fetchone()
                
                # If first user, claim orphan expenses
                if is_first_user:
                    cur.execute("UPDATE expenses SET user_id = %s WHERE user_id IS NULL", (user['id'],))
            else:
                # Update picture/name if changed
                cur.execute(
                    """UPDATE users SET name = %s, picture = %s, email = %s WHERE google_id = %s RETURNING *""",
                    (google_info['name'], google_info.get('picture'), google_info['email'], google_id)
                )
                user = cur.fetchone()
                
        conn.commit()
    
    return _row_to_dict(user)

def get_user_by_id(user_id):
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
    return _row_to_dict(user) if user else None


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

def add_expense(user_id, amount_str, category, description):
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
                """INSERT INTO expenses (user_id, amount, category, description, date)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING *""",
                (user_id, amount, category, description, _get_timestamp()),
            )
            new_row = cur.fetchone()
        conn.commit()

    return _row_to_dict(new_row)


def get_all_expenses(user_id, limit=None):
    """Return expenses sorted by date descending for a specific user, with an optional limit."""
    query = """
        SELECT *, ROW_NUMBER() OVER (ORDER BY date ASC, id ASC) as display_id 
        FROM expenses 
        WHERE user_id = %s 
        ORDER BY date DESC
    """
    params = [user_id]
    
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)
        
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
    return [_row_to_dict(r) for r in rows]


def get_expense_by_id(expense_id, user_id):
    """Return a single expense dict or None if not found or doesn't belong to matched user."""
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM (
                       SELECT *, ROW_NUMBER() OVER (ORDER BY date ASC, id ASC) as display_id
                       FROM expenses
                       WHERE user_id = %s
                   ) x WHERE id = %s""", (user_id, expense_id)
            )
            row = cur.fetchone()
    return _row_to_dict(row) if row else None


def update_expense(expense_id, user_id, amount_str=None, category=None, description=None):
    """
    Update one or more fields of an expense.
    Raises ValueError if not found or validation fails.
    Returns the updated expense dict.
    """
    existing = get_expense_by_id(expense_id, user_id)
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
                   WHERE id = %s AND user_id = %s""",
                (new_amount, new_category, new_description, expense_id, user_id),
            )
        conn.commit()

    return get_expense_by_id(expense_id, user_id)


def delete_expense(expense_id, user_id):
    """
    Delete an expense by ID.
    Raises ValueError if not found.
    """
    if get_expense_by_id(expense_id, user_id) is None:
        raise ValueError(f"No expense found with ID {expense_id}.")

    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id))
        conn.commit()

    return True


# ─────────────────────────────────────────────
#  SUMMARY & ANALYTICS
# ─────────────────────────────────────────────

def get_summary(user_id):
    """
    Compute aggregate statistics using optimized PostgreSQL queries.
    Returns:
        dict: total, count, by_category, highest_expense, average, percentages.
    """
    with _get_connection() as conn:
        with conn.cursor() as cur:
            # 1. Get totals and counts
            cur.execute(
                "SELECT SUM(amount) as total, COUNT(id) as cnt, AVG(amount) as avg FROM expenses WHERE user_id = %s",
                (user_id,)
            )
            agg = cur.fetchone()
            
            total = float(agg['total'] or 0.0)
            count = agg['cnt'] or 0
            average = float(agg['avg'] or 0.0)
            
            if count == 0:
                return {
                    "total": 0.0,
                    "count": 0,
                    "by_category": {},
                    "highest_expense": None,
                    "average": 0.0,
                    "category_percentages": {},
                }
            
            # 2. Get highest expense
            cur.execute(
                "SELECT * FROM expenses WHERE user_id = %s ORDER BY amount DESC LIMIT 1",
                (user_id,)
            )
            highest_raw = cur.fetchone()
            highest_expense = _row_to_dict(highest_raw) if highest_raw else None
            
            # 3. Get category breakdown
            cur.execute(
                "SELECT category, SUM(amount) as cat_total FROM expenses WHERE user_id = %s GROUP BY category",
                (user_id,)
            )
            cat_rows = cur.fetchall()
            
    by_category = {row['category']: float(row['cat_total']) for row in cat_rows}
    
    category_percentages = {
        cat: round((amount / total) * 100, 1)
        for cat, amount in by_category.items()
    }

    return {
        "total": round(total, 2),
        "count": count,
        "by_category": by_category,
        "highest_expense": highest_expense,
        "average": round(average, 2),
        "category_percentages": category_percentages,
    }


def filter_by_category(category, user_id):
    """Return expenses matching the given category, sorted by date descending."""
    category = validate_category(category)
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM (
                    SELECT *, ROW_NUMBER() OVER (ORDER BY date ASC, id ASC) as display_id
                    FROM expenses
                    WHERE user_id = %s
                ) x WHERE category = %s ORDER BY date DESC
                """,
                (user_id, category),
            )
            rows = cur.fetchall()
    return [_row_to_dict(r) for r in rows]
