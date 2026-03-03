from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route("/form", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    return render_template("submit.html", name=name, email=email)  

if __name__ == "__main__":
    app.run(debug=True)