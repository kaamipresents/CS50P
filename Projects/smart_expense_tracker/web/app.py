"""
app.py — Flask web application for the Smart Expense Tracker.
All HTTP routing lives here. Business logic is delegated to logic.py.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from authlib.integrations.flask_client import OAuth
import os

from logic import (
    init_db,
    add_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_summary,
    filter_by_category,
    VALID_CATEGORIES,
    get_or_create_user,
    get_user_by_id
)

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback-secret-for-dev")

# Initialise the PostgreSQL database (creates expenses table if not present)
init_db()

# ─────────────────────────────────────────────
#  OAUTH SETUP
# ─────────────────────────────────────────────

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# ─────────────────────────────────────────────
#  AUTHENTICATION
# ─────────────────────────────────────────────

@app.route("/login-page")
def login_page():
    """Landing page for unauthenticated users."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/login')
def login():
    """Redirect to Google's OAuth consent screen."""
    redirect_uri = url_for('auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/callback')
def auth():
    """Handle the callback from Google."""
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        user = get_or_create_user(user_info)
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_picture'] = user.get('picture')
        session['user_email'] = user['email']
        flash(f"Welcome back, {user['name']}!", "success")
        
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Clear the session."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login_page'))

@app.route('/profile')
@login_required
def profile():
    """Display user profile page."""
    user = {
        'name': session.get('user_name'),
        'email': session.get('user_email'),
        'picture': session.get('user_picture')
    }
    stats = get_summary(session['user_id'])
    return render_template('profile.html', user=user, stats=stats)


# ─────────────────────────────────────────────
#  HOME / DASHBOARD
# ─────────────────────────────────────────────

@app.route("/")
@login_required
def index():
    """
    Main dashboard: show summary stats + recent expenses.
    """
    user_id = session['user_id']
    summary = get_summary(user_id)
    recent_expenses = get_all_expenses(user_id, limit=10)
    return render_template(
        "index.html",
        summary=summary,
        recent_expenses=recent_expenses,
        categories=VALID_CATEGORIES,
    )


# ─────────────────────────────────────────────
#  ADD EXPENSE
# ─────────────────────────────────────────────

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """
    GET:  Show the add expense form.
    POST: Validate + save the new expense.
    """
    user_id = session['user_id']
    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        try:
            expense = add_expense(user_id, amount, category, description)
            flash(f"✅ Expense of ${expense['amount']:.2f} added successfully!", "success")
            return redirect(url_for("index"))
        except ValueError as e:
            flash(f"❌ {str(e)}", "error")
            return render_template(
                "add.html",
                categories=VALID_CATEGORIES,
                form_data={"amount": amount, "category": category, "description": description},
            )

    return render_template("add.html", categories=VALID_CATEGORIES, form_data={})


# ─────────────────────────────────────────────
#  VIEW ALL EXPENSES
# ─────────────────────────────────────────────

@app.route("/expenses")
@login_required
def expenses():
    """
    Show full paginated list of expenses with optional category filter.
    """
    user_id = session['user_id']
    category_filter = request.args.get("category", "").strip()
    all_expenses = []

    try:
        if category_filter:
            all_expenses = filter_by_category(category_filter, user_id)
        else:
            all_expenses = get_all_expenses(user_id)
    except ValueError as e:
        flash(f"❌ {str(e)}", "error")
        all_expenses = get_all_expenses(user_id)

    return render_template(
        "expenses.html",
        expenses=all_expenses,
        categories=VALID_CATEGORIES,
        active_filter=category_filter,
    )


# ─────────────────────────────────────────────
#  EDIT EXPENSE
# ─────────────────────────────────────────────

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):
    """
    GET:  Show the edit form pre-filled with current values.
    POST: Validate + update the expense.
    """
    user_id = session['user_id']
    expense = get_expense_by_id(expense_id, user_id)

    if expense is None:
        flash(f"❌ Expense #{expense_id} not found.", "error")
        return redirect(url_for("expenses"))

    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        try:
            updated = update_expense(
                expense_id,
                user_id,
                amount_str=amount or None,
                category=category or None,
                description=description or None,
            )
            flash(f"✅ Expense #{expense_id} updated successfully!", "success")
            return redirect(url_for("expenses"))
        except ValueError as e:
            flash(f"❌ {str(e)}", "error")

    return render_template(
        "edit.html",
        expense=expense,
        categories=VALID_CATEGORIES,
    )


# ─────────────────────────────────────────────
#  DELETE EXPENSE
# ─────────────────────────────────────────────

@app.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):
    """
    POST only: Delete an expense by ID.
    We use POST (not GET) to prevent accidental deletions via URL.
    """
    user_id = session['user_id']
    try:
        delete_expense(expense_id, user_id)
        flash(f"✅ Expense #{expense_id} deleted.", "success")
    except ValueError as e:
        flash(f"❌ {str(e)}", "error")

    return redirect(url_for("expenses"))


# ─────────────────────────────────────────────
#  SUMMARY PAGE
# ─────────────────────────────────────────────

@app.route("/summary")
@login_required
def summary():
    """
    Full analytics summary page with category breakdown.
    """
    user_id = session['user_id']
    stats = get_summary(user_id)
    return render_template("summary.html", summary=stats, categories=VALID_CATEGORIES)


# ─────────────────────────────────────────────
#  API ENDPOINT (Bonus: JSON API)
# ─────────────────────────────────────────────

@app.route("/api/expenses", methods=["GET"])
@login_required
def api_expenses():
    """
    JSON API endpoint — returns all expenses.
    Useful for future React/mobile frontends.
    """
    user_id = session['user_id']
    expenses = get_all_expenses(user_id)
    return jsonify({"expenses": expenses, "count": len(expenses)})


@app.route("/api/summary", methods=["GET"])
@login_required
def api_summary():
    """JSON API endpoint — returns summary statistics."""
    user_id = session['user_id']
    stats = get_summary(user_id)
    return jsonify(stats)


# ─────────────────────────────────────────────
#  ERROR HANDLERS
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="Page not found (404)."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", error="Internal server error (500). Please try again."), 500


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # debug=True only for local development — NEVER in production
    app.run(debug=True, host="0.0.0.0", port=5000)
