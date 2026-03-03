from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            words = text.split()
            word_count = len(words)
            char_count = len(text)
            analysis = {
                "word_count": word_count,
                "character_count": char_count,
            }
        else:
            analysis = None
        return render_template("index.html", analysis=analysis)
    else:   
        return render_template("index.html", analysis=None)

if __name__ == "__main__":
    app.run(debug=True)