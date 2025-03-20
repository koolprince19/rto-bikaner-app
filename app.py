from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random string
PASSWORD = "Rtobikaner"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Data (Google Sheets or Excel file)
EXCEL_FILE = 'D:/rto_bikaner_project/erawana.xlsx'  # Updated file path
data_df = pd.read_excel(EXCEL_FILE)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('search_page'))
        else:
            return "Invalid Password", 403
    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        search_query = request.form.get('query')
        if search_query:
            results = data_df[data_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)]
    
    return render_template('search.html', results=results)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
