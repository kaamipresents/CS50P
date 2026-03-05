from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    """Create table if it doesn't exist."""
    with sqlite3.connect("temporary.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temporary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        conn.commit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():

    message = ""

    with sqlite3.connect("temporary.db") as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")

            cursor.execute(
                "INSERT INTO temporary (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            message = "Form Submitted Successfully!"

            # 🔥 Redirect after POST
            return redirect(url_for("submit"))
        
        else:
            message = "Users List:"
            # Fetch users (for both GET and POST)
            cursor.execute("SELECT name, email FROM temporary")
            users_list = cursor.fetchall()

    return render_template("submit.html", users=users_list, message=message)

@app.route("/delete", methods=["POST"])
def delete():
    with sqlite3.connect("temporary.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM temporary")
        conn.commit()
    message = "All users deleted!"
    return redirect(url_for("submit", message=message))

if __name__ == "__main__":
    init_db()  # Create table once when app starts
    app.run(debug=True)