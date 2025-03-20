from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "Rtobikaner"

# Load the Excel file permanently
FILE_PATH = r"C:\Users\RTO\Desktop\erawana 19032025.xlsx"
data = pd.read_excel(FILE_PATH)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "Rtobikaner":
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html', message="RTO BIKANER")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        query = request.form.get('query')
        results = data[data.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
    
    return render_template('search.html', results=results)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
