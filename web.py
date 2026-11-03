from flask import Flask, render_template, request
from signal_engine import generate_signal
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            mines = int(request.form.get("mines", "5"))
            result = generate_signal(mines, 5)
        except (ValueError, TypeError):
            error = "Please choose a mine count from 3 to 10."
    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
