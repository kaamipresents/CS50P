# Hello User App — Complete Python + Flask SaaS Foundation

> A fully documented, production-style "Hello World" Flask application built to
> teach real SaaS architecture patterns to junior developers.

---

## ═══════════════════════════════════════
## PART 1 — SYSTEM DESIGN
## ═══════════════════════════════════════

### What the app does

A visitor enters their name, receives a time-aware personalised greeting
(e.g. "Good morning, Alice!"), and every greeting is persisted to disk.
Past visitors are displayed on a /history page. A JSON API endpoint is
included so the data is consumable by any future frontend or mobile client.

### Core features

| Feature           | Description                                      |
|-------------------|--------------------------------------------------|
| Greet user        | POST name → receive personalised message         |
| History view      | GET /history → list all past greetings           |
| JSON API          | GET /api/greetings → machine-readable output     |
| Input validation  | Length, character whitelist, empty-check         |
| File persistence  | All data stored in data/greetings.json           |
| CSV export        | logic.export_greetings_csv() → data/greetings.csv|
| Error handling    | Custom 404 + 500 pages                           |

### Data structure

Every greeting is stored as a Python dict and serialised as a JSON object:

```json
{
  "name":      "Alice",
  "message":   "Good morning, Alice! Welcome to the Hello App.",
  "timestamp": "2025-01-15 09:32:11"
}
```

The file is a JSON array of these objects:

```json
[
  {
    "name": "Alice",
    "message": "Good morning, Alice! Welcome to the Hello App.",
    "timestamp": "2025-01-15 09:32:11"
  },
  {
    "name": "Bob",
    "message": "Good afternoon, Bob! Welcome to the Hello App.",
    "timestamp": "2025-01-15 14:05:43"
  }
]
```

### File storage structure

```
data/
├── greetings.json   ← all greetings (created automatically on first run)
└── greetings.csv    ← export output (created on demand)
```

The `data/` directory is created automatically by `logic.ensure_data_dir()`.
No manual setup is required.


---

## ═══════════════════════════════════════
## PART 2 — CLI VERSION
## ═══════════════════════════════════════

### Folder structure

```
hello-user-app/
├── cli.py           ← command-line interface
├── logic.py         ← pure business logic (no Flask)
├── test_logic.py    ← unit tests (21 tests, stdlib only)
├── data/            ← runtime-generated JSON/CSV storage
└── requirements.txt
```

### How to run the CLI app

```bash
# No dependencies needed for CLI — just Python 3.8+
python cli.py
```

**Menu options:**
```
[1] Greet me           — enter name, receive greeting
[2] View history       — list all past greetings
[3] Export to CSV      — writes data/greetings.csv
[4] Clear all history  — prompts for confirmation
[0] Exit
```

### Running the unit tests

```bash
# With pytest (recommended)
pip install pytest
pytest test_logic.py -v

# Without pytest (stdlib only)
python test_logic.py
```

**Test coverage:**
- `TestValidateName`   — 7 tests covering all validation rules
- `TestBuildGreeting`  — 4 tests for greeting construction
- `TestRecordGreeting` — 10 tests for persistence + retrieval

All 21 tests pass. ✅


---

## ═══════════════════════════════════════
## PART 3 — FLASK WEB APP
## ═══════════════════════════════════════

### Folder structure

```
hello-user-app/
├── app.py              ← Flask routes (HTTP layer only)
├── logic.py            ← business logic (shared with CLI)
├── cli.py              ← standalone CLI entry-point
├── test_logic.py       ← unit tests
├── templates/
│   ├── base.html       ← shared layout, nav, global CSS
│   ├── index.html      ← home page + name form
│   ├── greet.html      ← greeting result page
│   ├── history.html    ← all-greetings table
│   └── error.html      ← 404 / 500 error page
├── data/
│   ├── .gitkeep        ← ensures directory is tracked by git
│   ├── greetings.json  ← (auto-created)
│   └── greetings.csv   ← (auto-created on export)
├── vercel.json         ← Vercel deployment config
├── requirements.txt
└── .gitignore
```

### Flask routes

| Method | Route             | Purpose                              |
|--------|-------------------|--------------------------------------|
| GET    | /                 | Home page with name-entry form       |
| POST   | /greet            | Process form, show greeting          |
| GET    | /history          | Table of all past greetings          |
| GET    | /api/greetings    | JSON list of all greetings           |
| POST   | /api/greet        | JSON API endpoint (body: {"name":…}) |

### Architecture principle

`app.py` contains ONLY routing logic.
`logic.py` contains ONLY business logic.

This separation means:
- The CLI and Flask app share the exact same logic.py without modification.
- You can test logic.py without starting a Flask server.
- Migrating to a different framework (FastAPI, Django) only requires rewriting app.py.


---

## ═══════════════════════════════════════
## PART 4 — DEPLOYMENT GUIDE
## ═══════════════════════════════════════

### Local development

```bash
# 1. Clone the repo
git clone https://github.com/your-username/hello-user-app.git
cd hello-user-app

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask development server
python app.py

# App is now live at: http://127.0.0.1:5000
```

### Deploy to Vercel (recommended — free tier)

Vercel supports Python/Flask via its serverless runtime.
The `vercel.json` in this repo is pre-configured.

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy (from the project root)
vercel

# 4. Follow the prompts. Your app will be live at:
#    https://your-project.vercel.app
```

**Important note on Vercel + file storage:**
Vercel runs Flask as a serverless function. The filesystem is ephemeral —
writes may not persist between function invocations. For a production app
you should replace file I/O with a persistent store (see Part 5).

For a simple demo / learning project this is perfectly fine.

### Deploy to Railway (persistent filesystem)

Railway gives you a persistent container, so file-based storage works reliably.

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and initialise
railway login
railway init

# 3. Deploy
railway up

# 4. Open in browser
railway open
```

Add a `Procfile` for Railway:
```
web: python app.py
```

And update `app.py` to read the PORT environment variable:
```python
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

### Environment variables

This app currently has no secrets. When you add them (API keys, etc.),
use a `.env` file locally and set them as environment variables in
Vercel/Railway dashboards — never commit them to git.


---

## ═══════════════════════════════════════
## PART 5 — FUTURE IMPROVEMENTS
## ═══════════════════════════════════════

### 1. Add SQLite (persistent database)

**Why:** File-based JSON breaks on concurrent users and doesn't scale.

**How:** Replace `load_greetings()` / `save_greetings()` in `logic.py` with
SQLite calls using Python's built-in `sqlite3` module. No ORM needed for
a simple app. The rest of the code (app.py, templates) stays identical.

```python
import sqlite3
conn = sqlite3.connect("data/app.db")
```

### 2. Add user authentication

**Why:** Protect the /history page; let users see only their own greetings.

**How:** Add `flask-login` and a simple `users.json` store (or SQLite users
table). Each greeting gets a `user_id` field. The /history route checks
`current_user` before returning data.

### 3. Add a payment system

**Why:** Gate premium features (e.g., CSV export, greeting analytics).

**How:** Integrate Stripe Checkout. Add a `subscriptions.json` to track
which user_id has an active plan. Use a webhook endpoint to update
subscription status when Stripe events fire.

### 4. Build a REST API

**Why:** Decouple frontend from backend; support mobile clients.

**How:** The `/api/greetings` and `/api/greet` routes already exist in
`app.py`. Extend them with:
- Pagination (`?page=1&per_page=20`)
- Filtering (`?name=alice`)
- API key authentication via `Authorization: Bearer <token>` headers

### 5. Add a React frontend

**Why:** Richer interactivity — real-time greeting feed, animated counters.

**How:**
1. Keep `app.py` but convert it to a pure JSON API (remove HTML routes).
2. Create a separate `frontend/` directory with a Vite + React project.
3. The React app fetches from `/api/greetings` and `/api/greet`.
4. Deploy frontend to Vercel, backend to Railway (or combine with FastAPI).

### Upgrade path summary

```
Phase 1  →  File JSON (you are here)
Phase 2  →  SQLite (same Python, just swap storage)
Phase 3  →  Auth + sessions
Phase 4  →  Payments + subscription tiers
Phase 5  →  REST API + React SPA
Phase 6  →  PostgreSQL + Docker + CI/CD
```

Each phase builds on the last without throwing away what you have.
This is how real SaaS products are built: iteratively, not all at once.
