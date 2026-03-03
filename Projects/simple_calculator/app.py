from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            num1 = float(request.form.get("num1"))
            num2 = float(request.form.get("num2"))
        except (ValueError, TypeError):
            error = "Please enter valid numbers."
            return render_template("index.html", error=error)
        result = num1 + num2
        return render_template("index.html", result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)