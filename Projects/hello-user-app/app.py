"""
app.py — Flask application.
All HTTP routing lives here. Business logic is delegated to logic.py.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import logic

app = Flask(__name__)


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """
    GET /
    Render the landing page with the name-entry form.
    Passes visitor count so the UI can show social proof.
    """
    count = logic.get_visitor_count()
    return render_template("index.html", visitor_count=count)


@app.route("/greet", methods=["POST"])
def greet():
    """
    POST /greet
    Accept the submitted name, validate it, build a greeting,
    persist it, and render the greeting page.
    On validation failure, redirect back to home with an error.
    """
    name = request.form.get("name", "").strip()

    success, result, clean_name = logic.record_greeting(name)

    if not success:
        # result is the error message when success=False
        error_message = result
        count = logic.get_visitor_count()
        return render_template("index.html", error=error_message, visitor_count=count), 400

    # result is the greeting string when success=True
    return render_template("greet.html", name=clean_name, greeting=result)


@app.route("/history")
def history():
    """
    GET /history
    Show all past greetings, newest first.
    """
    greetings = logic.get_all_greetings()
    count = logic.get_visitor_count()
    return render_template("history.html", greetings=greetings, visitor_count=count)


@app.route("/api/greetings")
def api_greetings():
    """
    GET /api/greetings
    JSON endpoint — returns all greetings.
    Useful for future React / mobile front-ends.
    """
    greetings = logic.get_all_greetings()
    return jsonify({
        "count": len(greetings),
        "greetings": greetings,
    })


@app.route("/api/greet", methods=["POST"])
def api_greet():
    """
    POST /api/greet  (JSON body: {"name": "..."})
    JSON API version of the greeting endpoint.
    """
    body = request.get_json(silent=True) or {}
    name = body.get("name", "")

    success, result, clean_name = logic.record_greeting(name)

    if not success:
        return jsonify({"error": result}), 400

    return jsonify({"name": clean_name, "greeting": result}), 201


# ─────────────────────────────────────────────
# Error handlers
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="Something went wrong on our end."), 500


# ─────────────────────────────────────────────
# Dev entry-point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # debug=True is for local development only.
    # Vercel / production uses a WSGI server (gunicorn).
    app.run(debug=True, port=5000)
