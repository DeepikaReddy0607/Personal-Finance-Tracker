from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf.csrf import CSRFProtect
import calendar

app = Flask(__name__)
app.secret_key = "super_secret_key"
csrf = CSRFProtect(app)

DB_NAME = "expenses.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_NAME, check_same_thread=False)
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA journal_mode = WAL")  # Enable WAL for better concurrency
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, params=(), fetch=False, commit=False):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, params)
    data = cur.fetchall() if fetch else None
    if commit:
        db.commit()
    cur.close()
    return data

def init_db():
    query_db("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""", commit=True)

    query_db("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )""", commit=True)

    query_db("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )""", commit=True)

    query_db("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        month INTEGER,
        year INTEGER,
        UNIQUE(user_id, month, year),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""", commit=True)

    # Insert default categories if not exists
    default_categories = ["Food", "Travel", "Shopping", "Bills", "Other"]
    for cat in default_categories:
        query_db("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,), commit=True)

with app.app_context():
    init_db()

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class BudgetForm(FlaskForm):
    amount = FloatField('Monthly Budget', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Set Budget')

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('tracker'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        hashed_pw = generate_password_hash(password)

        try:
            query_db("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw), commit=True)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
    return render_template('Register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = query_db("SELECT id, password FROM users WHERE username=?", (username,), fetch=True)
        if user and check_password_hash(user[0][1], password):
            session['user_id'] = user[0][0]
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('tracker'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Fetch categories for the form
    categories = query_db("SELECT id, name FROM categories", fetch=True)
    form = ExpenseForm()
    form.category.choices = [(cat[0], cat[1]) for cat in categories]

    # Add expense
    if form.validate_on_submit():
        desc = form.description.data
        amount = form.amount.data
        category_id = form.category.data
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_db("INSERT INTO expenses (user_id, description, amount, category_id, date) VALUES (?, ?, ?, ?, ?)",
                 (user_id, desc, amount, category_id, date), commit=True)
        flash("Expense added successfully!", "success")
        return redirect(url_for('tracker'))

    # Fetch expenses with filter
    selected_category = request.args.get('category')
    if selected_category:
        expenses = query_db("""
            SELECT e.id, e.description, e.amount, c.name, e.date 
            FROM expenses e JOIN categories c ON e.category_id = c.id 
            WHERE e.user_id=? AND c.id=? ORDER BY e.date DESC
        """, (user_id, selected_category), fetch=True)
    else:
        expenses = query_db("""
            SELECT e.id, e.description, e.amount, c.name, e.date 
            FROM expenses e JOIN categories c ON e.category_id = c.id 
            WHERE e.user_id=? ORDER BY e.date DESC
        """, (user_id,), fetch=True)

    # Calculate budget & spent amount
    now = datetime.now()
    month, year = now.month, now.year
    budget_data = query_db("SELECT amount FROM budget WHERE user_id=? AND month=? AND year=?", 
                           (user_id, month, year), fetch=True)
    budget = budget_data[0][0] if budget_data else None
    spent_data = query_db("""
        SELECT SUM(amount) FROM expenses 
        WHERE user_id=? AND strftime('%m', date)=? AND strftime('%Y', date)=?
    """, (user_id, f"{month:02}", str(year)), fetch=True)
    spent = spent_data[0][0] if spent_data[0][0] else 0

    remaining = budget - spent if budget else None

    return render_template('tracker.html', username=session['username'], form=form,
                           expenses=expenses, categories=categories, selected_category=selected_category,
                           budget=budget, spent=spent, remaining=remaining)

@app.route('/set-budget', methods=['GET', 'POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    form = BudgetForm()
    now = datetime.now()
    month, year = now.month, now.year

    if form.validate_on_submit():
        amount = form.amount.data
        # Insert or update budget for this month
        query_db("""
            INSERT INTO budget (user_id, amount, month, year) 
            VALUES (?, ?, ?, ?) 
            ON CONFLICT(user_id, month, year) 
            DO UPDATE SET amount=excluded.amount
        """, (user_id, amount, month, year), commit=True)
        flash("Budget updated successfully!", "success")
        return redirect(url_for('tracker'))

    return render_template('set_budget.html', form=form)

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    query_db("DELETE FROM expenses WHERE id=?", (expense_id,), commit=True)
    flash("Expense deleted.", "info")
    return redirect(url_for('tracker'))

@app.route('/chart-data')
def chart_data():
    if 'user_id' not in session:
        return jsonify([])
    user_id = session['user_id']
    now = datetime.now()
    month, year = now.month, now.year
    data = query_db("""
        SELECT c.name, SUM(e.amount) 
        FROM expenses e JOIN categories c ON e.category_id = c.id 
        WHERE e.user_id=? AND strftime('%m', e.date)=? AND strftime('%Y', e.date)=? 
        GROUP BY c.name
    """, (user_id, f"{month:02}", str(year)), fetch=True)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)