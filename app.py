from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Path to the Excel file (change it if needed)
FILE_PATH = "data.xlsx"

# Load Excel data (Make sure the file is in your project folder)
if os.path.exists(FILE_PATH):
    data = pd.read_excel(FILE_PATH)
else:
    data = pd.DataFrame(columns=["Vehicle Number", "Total Round", "Total Overload", "Total CF"])

@app.route("/")
def welcome():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    results = None
    if request.method == "POST":
        query = request.form.get("query")
        results = data[data["Vehicle Number"].astype(str).str.contains(query, na=False, case=False)]

    return render_template("search.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use PORT from Render, default to 10000
    app.run(host="0.0.0.0", port=port, debug=True)
