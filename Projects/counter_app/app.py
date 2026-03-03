from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    global error
    error = None
    with open("count.txt", "r") as f:
        try:
            count = int(f.read())
        except ValueError:
            count = 0
            error = "Count file is corrupted" 
    count += 1
    with open("count.txt", "w") as f:
        f.write(str(count))
    return render_template("index.html", count=count, error=error)

if __name__ == "__main__":
    app.run(debug=True)