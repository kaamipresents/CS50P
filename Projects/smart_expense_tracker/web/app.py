"""
app.py — Flask web application for the Smart Expense Tracker.
All HTTP routing lives here. Business logic is delegated to logic.py.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
)

app = Flask(__name__)

# Secret key required for flash messages (session-based feedback)
app.secret_key = "postgresql://neondb_owner:npg_pkVjbDf5ETO7@ep-rapid-hat-ah12gt87-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Initialise the PostgreSQL database (creates expenses table if not present)
init_db()


# ─────────────────────────────────────────────
#  HOME / DASHBOARD
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """
    Main dashboard: show summary stats + recent expenses.
    """
    summary = get_summary()
    recent_expenses = get_all_expenses()[:10]  # Show last 10
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
def add():
    """
    GET:  Show the add expense form.
    POST: Validate + save the new expense.
    """
    if request.method == "POST":
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        try:
            expense = add_expense(amount, category, description)
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
def expenses():
    """
    Show full paginated list of expenses with optional category filter.
    """
    category_filter = request.args.get("category", "").strip()
    all_expenses = []

    try:
        if category_filter:
            all_expenses = filter_by_category(category_filter)
        else:
            all_expenses = get_all_expenses()
    except ValueError as e:
        flash(f"❌ {str(e)}", "error")
        all_expenses = get_all_expenses()

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
def edit(expense_id):
    """
    GET:  Show the edit form pre-filled with current values.
    POST: Validate + update the expense.
    """
    expense = get_expense_by_id(expense_id)

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
def delete(expense_id):
    """
    POST only: Delete an expense by ID.
    We use POST (not GET) to prevent accidental deletions via URL.
    """
    try:
        delete_expense(expense_id)
        flash(f"✅ Expense #{expense_id} deleted.", "success")
    except ValueError as e:
        flash(f"❌ {str(e)}", "error")

    return redirect(url_for("expenses"))


# ─────────────────────────────────────────────
#  SUMMARY PAGE
# ─────────────────────────────────────────────

@app.route("/summary")
def summary():
    """
    Full analytics summary page with category breakdown.
    """
    stats = get_summary()
    return render_template("summary.html", summary=stats, categories=VALID_CATEGORIES)


# ─────────────────────────────────────────────
#  API ENDPOINT (Bonus: JSON API)
# ─────────────────────────────────────────────

@app.route("/api/expenses", methods=["GET"])
def api_expenses():
    """
    JSON API endpoint — returns all expenses.
    Useful for future React/mobile frontends.
    """
    expenses = get_all_expenses()
    return jsonify({"expenses": expenses, "count": len(expenses)})


@app.route("/api/summary", methods=["GET"])
def api_summary():
    """JSON API endpoint — returns summary statistics."""
    stats = get_summary()
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
