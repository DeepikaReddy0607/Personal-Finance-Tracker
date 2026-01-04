Budget Bee — Personal Finance Tracker

A secure, responsive web application to track expenses, manage monthly budgets, and visualize spending patterns.

Tech Stack: Flask · Python · SQLite · Bootstrap · Chart.js

🔹 Key Features

User authentication with secure password hashing (Werkzeug)

Add, edit, and categorize expenses (Food, Travel, Shopping, etc.)

Monthly budget setup with automatic remaining balance calculation

Category-wise expense visualization using Chart.js (pie chart)

Expense filtering by category and month

Mobile-responsive UI using Bootstrap

🔹 Tech Stack
Layer	Technology
Backend	Flask (Python)
Database	SQLite
Frontend	HTML, CSS, Bootstrap
Charts	Chart.js
Security	Werkzeug password hashing
Forms	Flask-WTF
🔹 Project Structure
Budget-Bee/
├── app.py
├── expenses.db
├── requirements.txt
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── tracker.html
│   └── set_budget.html
└── static/
    ├── css/
    └── js/

🔹 Setup Instructions
git clone https://github.com/DeepikaReddy0607/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py


Visit: http://127.0.0.1:5000

🔹 Highlights

Designed lightweight architecture for fast local deployment

Implemented session-based authentication and role isolation

Used SQL date functions for efficient monthly filtering

Focused on usability and performance for student use-cases

🔹 Future Enhancements

Recurring expenses

Multi-month analytics and reports

Budget alerts & notifications

PostgreSQL migration for scalability

🔹 Author

Rudru Deepika Reddy
B.Tech CSE Student
GitHub: https://github.com/DeepikaReddy0607