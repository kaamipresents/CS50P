# 💰 Smart Expense Tracker — Complete Developer Guide

> **Audience:** Junior-to-intermediate Python developers building their first real SaaS project.
> **Stack:** Python · Flask · JSON file storage · HTML/CSS
> **Constraint:** No databases, no ORM, no async — beginner-friendly, production-clean.

---

## Table of Contents

1. [Part 1 — System Design](#part-1--system-design)
2. [Part 2 — CLI Version](#part-2--cli-version)
3. [Part 3 — Flask Web App](#part-3--flask-web-app)
4. [Part 4 — Deployment Guide](#part-4--deployment-guide)
5. [Part 5 — Future Improvements](#part-5--future-improvements)

---

# PART 1 — SYSTEM DESIGN

## 1. What the App Does

The **Smart Expense Tracker** lets users log, view, edit, and delete personal spending records. It provides a real-time dashboard with category breakdowns, total spent, average per expense, and the highest single expense. Both a command-line interface and a web interface are provided — sharing the exact same business logic.

---

## 2. Core Features

| Feature | CLI | Web |
|---|---|---|
| Add expense (amount, category, description) | ✅ | ✅ |
| View all expenses | ✅ | ✅ |
| View expense by ID | ✅ | ✅ |
| Edit expense | ✅ | ✅ |
| Delete expense | ✅ | ✅ |
| Spending summary with totals | ✅ | ✅ |
| Filter by category | ✅ | ✅ |
| Visual category breakdown | text bar | CSS bar |
| JSON API endpoint | ❌ | ✅ |

---

## 3. Data Structure

Each expense is a Python dict / JSON object:

```json
{
    "id": 1,
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at restaurant",
    "date": "2025-06-15 13:45:22"
}
```

**Field rules:**

- `id` — auto-incrementing integer, never reused
- `amount` — positive float, rounded to 2 decimal places
- `category` — one of 8 fixed options (Food, Transport, Housing, Entertainment, Health, Shopping, Education, Other)
- `description` — non-empty string, max 200 characters
- `date` — auto-set on creation using `datetime.now()`

The full data store is a **JSON array** of these objects.

---

## 4. File Storage Structure

```
data/
└── expenses.json       ← All expense records
```

- On first run, the `data/` directory and `expenses.json` are **auto-created**.
- The entire JSON array is read on every operation and fully rewritten on every save. This is the correct approach for file-based storage at small-to-medium scale (< ~10,000 records).
- **Why not SQLite?** Using JSON keeps the project constraint-compliant and teaches the core pattern. When you need queries/joins, upgrade to SQLite or PostgreSQL.

---

## 5. Example of Stored JSON

```json
[
    {
        "id": 1,
        "amount": 45.00,
        "category": "Food",
        "description": "Weekly grocery run",
        "date": "2025-06-15 09:30:00"
    },
    {
        "id": 2,
        "amount": 12.50,
        "category": "Transport",
        "description": "Bus pass top-up",
        "date": "2025-06-15 11:00:00"
    },
    {
        "id": 3,
        "amount": 200.00,
        "category": "Housing",
        "description": "Electricity bill",
        "date": "2025-06-16 08:15:00"
    }
]
```

---

# PART 2 — CLI VERSION

## 1. Folder Structure

```
smart_expense_tracker/
└── cli/
    ├── main.py           ← Entry point, all menus and user I/O
    ├── logic.py          ← Business logic (validate, CRUD, summary)
    ├── storage.py        ← File I/O: read/write JSON
    ├── data/
    │   └── expenses.json ← Auto-created on first run
    └── tests/
        └── test_logic.py ← Unit tests
```

**Separation of concerns:**

| File | Responsibility |
|---|---|
| `storage.py` | Load / save JSON. Nothing else. |
| `logic.py` | Validate input. Build expense dicts. Call storage. Compute summaries. |
| `main.py` | Print menus. Accept input. Call logic. Display results. |

This structure means you can swap out the storage layer (e.g., to SQLite) without touching `logic.py` or `main.py`.

---

## 2. Key Code Patterns

### Validation in logic.py

```python
def validate_amount(amount_str):
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number (e.g. 12.50).")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)
```

**Why this pattern?**
- It raises `ValueError` with a human-readable message.
- The caller (either CLI or Flask) catches it and decides how to display the error.
- Logic never knows whether it's a terminal or a browser.

### Safe File I/O in storage.py

```python
def load_expenses():
    _ensure_data_file()           # create file if missing
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Could not read expenses file: {e}")
```

**Why wrap in try/except?**
- `json.JSONDecodeError` — file got corrupted or is empty
- `IOError` — disk full, permissions issue
- We convert both to `RuntimeError` so callers handle one exception type for storage failures.

---

## 3. Running the CLI App

```bash
# 1. Navigate to the CLI folder
cd smart_expense_tracker/cli

# 2. Run directly (no dependencies needed — standard library only)
python main.py
```

**What you see:**

```
  Welcome to the Smart Expense Tracker 💰

==================================================
  SMART EXPENSE TRACKER
==================================================
  [1] Add Expense
  [2] View All Expenses
  [3] View Expense by ID
  [4] Update Expense
  [5] Delete Expense
  [6] View Summary
  [7] Filter by Category
  [0] Exit

  Select option:
```

---

## 4. Unit Tests

```bash
# Install pytest
pip install pytest

# Run all tests with verbose output
cd smart_expense_tracker/cli
python -m pytest tests/ -v
```

**Expected output:**

```
tests/test_logic.py::TestValidation::test_valid_amount PASSED
tests/test_logic.py::TestValidation::test_invalid_amount_zero PASSED
tests/test_logic.py::TestValidation::test_invalid_amount_negative PASSED
tests/test_logic.py::TestCRUD::test_add_expense PASSED
tests/test_logic.py::TestCRUD::test_add_multiple_expenses_unique_ids PASSED
tests/test_logic.py::TestCRUD::test_update_expense_amount PASSED
tests/test_logic.py::TestCRUD::test_delete_expense PASSED
tests/test_logic.py::TestSummary::test_summary_totals PASSED
...
```

> **The tests use a separate `test_expenses.json` file** so they never pollute your real data.

---

# PART 3 — FLASK WEB APP

## 1. Folder Structure

```
smart_expense_tracker/
└── web/
    ├── app.py                  ← Flask routes (HTTP layer only)
    ├── logic.py                ← Business logic (identical pattern to CLI)
    ├── requirements.txt        ← Flask + Gunicorn
    ├── Procfile                ← For Railway/Render deployment
    ├── render.yaml             ← Render.com config
    ├── data/
    │   └── expenses.json       ← Auto-created on first run
    ├── static/
    │   └── css/
    │       └── style.css       ← All styles
    └── templates/
        ├── base.html           ← Navbar, flash messages, footer
        ├── index.html          ← Dashboard
        ├── add.html            ← Add expense form
        ├── expenses.html       ← Full list with filter
        ├── edit.html           ← Edit form
        ├── summary.html        ← Full analytics
        └── error.html          ← 404/500 pages
```

---

## 2. Flask Route Architecture

```
GET  /                   → Dashboard (summary + recent 10)
GET  /expenses           → All expenses (with ?category= filter)
GET  /add                → Show add form
POST /add                → Save new expense
GET  /edit/<id>          → Show edit form
POST /edit/<id>          → Update expense
POST /delete/<id>        → Delete expense
GET  /summary            → Full analytics page
GET  /api/expenses       → JSON API: all expenses
GET  /api/summary        → JSON API: summary stats
```

**Key design decisions:**

- **DELETE uses POST, not GET.** Never allow data deletion via a GET request — it can be triggered accidentally by link prefetchers or bots.
- **Flash messages** provide user feedback after redirects (the Post/Redirect/Get pattern prevents duplicate form submissions on page refresh).
- **API endpoints** are bonus routes — they let you later add a React frontend without rewriting the backend.

---

## 3. The Post/Redirect/Get Pattern

This is a web development best practice used in `app.py`:

```python
@app.route("/add", methods=["POST"])
def add():
    try:
        expense = add_expense(amount, category, description)
        flash("Expense added!", "success")
        return redirect(url_for("index"))   # ← REDIRECT after POST
    except ValueError as e:
        flash(str(e), "error")
        return render_template("add.html", ...)  # ← re-render form on error
```

**Why?** If you just `return render_template(...)` after a POST, the user can hit browser refresh and the form submits again (duplicate record). Redirecting prevents this.

---

## 4. Form Validation Flow

```
User submits form
    │
    ▼
Flask route receives form data (request.form)
    │
    ▼
Calls logic.add_expense(amount, category, description)
    │
    ├─ ValueError raised?
    │       ├── YES → flash error, re-render form WITH user's previous values
    │       └── NO  → flash success, redirect to dashboard
    │
    ▼
logic.py validates each field independently
    ├── validate_amount()
    ├── validate_category()
    └── validate_description()
```

---

## 5. Template Inheritance

All pages extend `base.html`:

```
base.html
├── index.html     (extends base)
├── add.html       (extends base)
├── expenses.html  (extends base)
├── edit.html      (extends base)
├── summary.html   (extends base)
└── error.html     (extends base)
```

`base.html` provides: navbar, flash messages, container, footer. Child templates only define `{% block content %}`.

---

# PART 4 — DEPLOYMENT GUIDE

## 1. requirements.txt

```
flask==3.0.3
gunicorn==22.0.0
```

`gunicorn` is a production WSGI server. Never use Flask's built-in dev server (`flask run`) in production.

---

## 2. Run Locally

```bash
# Step 1: Go to the web folder
cd smart_expense_tracker/web

# Step 2: Create a virtual environment
python -m venv venv

# Step 3: Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Run the app
python app.py

# OR using Flask CLI:
flask --app app run --debug
```

Open `http://localhost:5000` in your browser.

---

## 3. Deploy to Render (Free Tier)

**Step 1: Create a GitHub repository**

```bash
git init
git add .
git commit -m "Initial commit: Smart Expense Tracker"
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git push -u origin main
```

**Step 2: Sign up at render.com**

**Step 3: Create a new Web Service**
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository
- Configure:

| Setting | Value |
|---|---|
| Name | `smart-expense-tracker` |
| Root Directory | `web` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| Plan | Free |

**Step 4: Add Environment Variables**

| Key | Value |
|---|---|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | (click "Generate" for a random value) |

**Step 5: Click "Create Web Service"**

Render will build and deploy. Your app will be live at `https://smart-expense-tracker.onrender.com` in ~2 minutes.

---

## 4. Deploy to Railway

**Step 1: Sign up at railway.app**

**Step 2: Create a new project**
- Click **"New Project"** → **"Deploy from GitHub repo"**
- Select your repository

**Step 3: Configure the service**

Railway auto-detects Python. It will use your `Procfile`:

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Step 4: Add environment variables**
- Go to your service → **Variables tab**
- Add `SECRET_KEY` = any long random string

**Step 5: Set the root directory to `web`** in Railway's settings.

Railway provides a URL like `https://expense-tracker-production.up.railway.app`.

---

## 5. Important: Data Persistence on Cloud

> ⚠️ **Both Render and Railway use ephemeral filesystems on the free tier.** This means your `expenses.json` file will be **wiped when the service restarts** (which can happen every 24 hours on the free tier).

**For a real production deployment, upgrade the storage layer:**

- **Render:** Use a Render Disk (persistent volume) — available on paid plans.
- **Railway:** Same — use a persistent volume add-on.
- **Best solution:** Migrate to SQLite (a single file database) or PostgreSQL (free tier available on both platforms). This is covered in Part 5.

For learning and demos, the free tier is perfectly fine.

---

## 6. Environment Variables in Flask

Update `app.py` to read `SECRET_KEY` from the environment:

```python
import os

app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
```

This means:
- **Locally:** Falls back to the dev key string.
- **In production:** Reads the secure key you set in Render/Railway.

Never hardcode a real secret key in source code.

---

# PART 5 — FUTURE IMPROVEMENTS

## 1. Upgrade Storage to SQLite

**When to do this:** When your JSON file exceeds ~1,000 records, or when you need to query/sort data efficiently.

```python
# logic.py changes:
import sqlite3

def get_db():
    conn = sqlite3.connect("data/expenses.db")
    conn.row_factory = sqlite3.Row   # returns dicts instead of tuples
    return conn

def add_expense(amount, category, description):
    db = get_db()
    db.execute(
        "INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)",
        (amount, category, description)
    )
    db.commit()
```

Everything else stays the same — routes, templates, and validation don't change at all. This is why we separated logic from storage from the beginning.

---

## 2. Add User Authentication

Currently, all users share the same `expenses.json`. To make it multi-user:

**Simple approach (no external libraries):**
```python
# Store sessions as JSON files:
# data/sessions/abc123.json  → { "user_id": 5, "expires": "2025-07-01" }
# data/users.json            → [{ "id": 1, "email": "...", "password_hash": "..." }]
```

Use `hashlib` (standard library) for password hashing:
```python
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

**Better approach (when ready):** Use `flask-login` + `werkzeug.security` for production-grade auth.

---

## 3. Add a Budget / Alert System

```python
# config.json:
{
    "monthly_budget": 500.00,
    "category_budgets": {
        "Food": 150.00,
        "Entertainment": 50.00
    }
}

# In logic.py:
def check_budget_alerts(summary):
    alerts = []
    config = load_config()
    if summary["total"] > config["monthly_budget"]:
        alerts.append(f"⚠️ You've exceeded your monthly budget of ${config['monthly_budget']:.2f}!")
    return alerts
```

---

## 4. Build a REST API

Add a full JSON API so a React or mobile app can connect:

```python
# Current bonus endpoints (already in app.py):
GET  /api/expenses        → list all
GET  /api/summary         → analytics

# Add these next:
POST   /api/expenses      → create
PUT    /api/expenses/<id> → update
DELETE /api/expenses/<id> → delete
```

Add API key authentication:
```python
def require_api_key(f):
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if key != os.environ.get("API_KEY"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper
```

---

## 5. React Frontend

Once the REST API is complete, replace the Jinja2 templates with a React app:

```
expense-tracker/
├── backend/           ← Your Flask API (app.py, logic.py)
└── frontend/          ← React app
    ├── src/
    │   ├── App.jsx
    │   ├── pages/
    │   │   ├── Dashboard.jsx
    │   │   ├── AddExpense.jsx
    │   │   └── Summary.jsx
    │   └── api/
    │       └── expenses.js   ← fetch() calls to Flask API
    └── package.json
```

The Flask backend becomes a pure API, and the React frontend handles all UI. Deploy them separately (Flask on Render, React on Vercel).

---

## 6. Add Payment System (SaaS Monetization)

Turn this into a paid SaaS with **Stripe**:

```python
# Free plan: max 50 expenses
# Pro plan ($5/month): unlimited expenses, CSV export, charts

import stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": "price_YOUR_PRICE_ID", "quantity": 1}],
        mode="subscription",
        success_url=url_for("index", _external=True) + "?subscribed=true",
        cancel_url=url_for("index", _external=True),
    )
    return redirect(session.url)
```

---

## 7. CSV Export

A highly-requested feature that requires only the standard library:

```python
import csv
from io import StringIO
from flask import Response

@app.route("/export/csv")
def export_csv():
    expenses = get_all_expenses()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "amount", "category", "description", "date"])
    writer.writeheader()
    writer.writerows(expenses)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"}
    )
```

---

## Upgrade Roadmap Summary

```
Phase 1 (Now)       → JSON + CLI + Flask + HTML/CSS       ← You are here ✅
Phase 2 (Next)      → SQLite + Multi-user auth + Budget alerts
Phase 3 (Growth)    → REST API + React frontend + CSV export
Phase 4 (SaaS)      → Stripe payments + user tiers + PostgreSQL
Phase 5 (Scale)     → Redis caching + Docker + CI/CD pipeline
```

Each phase builds on the previous one without requiring a full rewrite — because the logic layer was kept clean and separate from the start.

---

*Built with ❤️ for junior developers learning real SaaS architecture.*
