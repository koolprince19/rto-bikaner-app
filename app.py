from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Define the path to the Excel file (inside the same directory as app.py)
FILE_PATH = os.path.join(os.path.dirname(__file__), "erawana.xlsx")

# Load Excel data
if os.path.exists(FILE_PATH):
    data = pd.read_excel(FILE_PATH)
else:
    data = None  # Handle the case if the file is missing

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    results = None
    if request.method == "POST":
        query = request.form["query"].strip().upper()  # Convert input to uppercase for consistency
        if data is not None:
            results = data[data.iloc[:, 0].astype(str) == query]  # Filter by first column (Vehicle Number)
    
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
