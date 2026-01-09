from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'database.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/')
def index():
    expenses = load_data()
    total = sum(item['amount'] for item in expenses)
    
    # Calculate totals per category for the Chart
    categories = {}
    for item in expenses:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + item['amount']
    
    return render_template('index.html', 
                           expenses=expenses[::-1], 
                           total=total, 
                           cat_labels=list(categories.keys()), 
                           cat_values=list(categories.values()))

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    amount = float(request.form.get('amount'))
    category = request.form.get('category')
    
    expenses = load_data()
    expenses.append({"title": title, "amount": amount, "category": category})
    save_data(expenses)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)