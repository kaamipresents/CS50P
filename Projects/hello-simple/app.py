from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Where we save greetings
GREETINGS_FILE = "greetings.json"


# ── Helper: load greetings from file ──────────────────────
def load_greetings():
    if not os.path.exists(GREETINGS_FILE):
        return []
    with open(GREETINGS_FILE, "r") as f:
        return json.load(f)


# ── Helper: save greetings to file ────────────────────────
def save_greeting(name):
    greetings = load_greetings()
    greetings.append(name)
    with open(GREETINGS_FILE, "w") as f:
        json.dump(greetings, f)


# ── Route 1: Home page ─────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


# ── Route 2: Handle form, show greeting ───────────────────
@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name")

    if not name or name.strip() == "":
        error = "Please enter your name."
        return render_template("index.html", error=error)

    name = name.strip().title()
    save_greeting(name)
    greeting = f"Hello, {name}! Welcome to the app."
    return render_template("greet.html", name=name, greeting=greeting)


# ── Route 3: History page ──────────────────────────────────
@app.route("/history")
def history():
    greetings = load_greetings()
    return render_template("history.html", greetings=greetings)


# ── Run the app ────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
