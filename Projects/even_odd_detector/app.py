from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            number = int(request.form.get("number"))
        except (ValueError, TypeError):
            error = "Please enter a valid integer."
            return render_template("index.html", error=error)
        result = "Even" if number % 2 == 0 else "Odd"
        return render_template("index.html", result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)