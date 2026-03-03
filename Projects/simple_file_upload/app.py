from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        file = request.files.get("file")
        if file:
            if not os.path.exists(os.path.join("uploads")):
                os.makedirs(os.path.join("uploads"))
            if os.path.exists(os.path.join("uploads", file.filename)):
                return "File already exists. Please choose a different file."
            else:
                file.save(os.path.join("uploads", file.filename))
            return f"File '{file.filename}' uploaded successfully!"
        else:
            return "No file uploaded."

if __name__ == "__main__":
    app.run(debug=True)