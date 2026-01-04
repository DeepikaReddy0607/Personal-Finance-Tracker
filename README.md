# Budget Bee

#### Video Demo: https://youtube.com/shorts/jX-3hyNdvLQ?si=GayBsJ8-DGAnIjM2

#### Description:

**Budget Bee** is a web-based personal finance tracker I built to help people manage their expenses, set monthly budgets, and better understand their spending habits. I wanted to create something that’s simple to use, visually appealing, and secure—all while helping students and young professionals who are trying to stay on top of their finances.

For this project, I used Python’s Flask framework for the backend, SQLite as the database, and Bootstrap to make the interface clean and responsive. The goal was to build a lightweight tool that anyone can set up quickly without worrying about complicated server configurations.

### Features:

- **User Authentication:** Users can register and log in with their username and password. The passwords are securely hashed using `Werkzeug` so that sensitive information isn’t stored in plain text.

- **Expense Tracking:** Users can easily add expenses by entering details like description, amount, and choosing a category such as Food, Travel, or Shopping. All the data is saved with a timestamp.

- **Budget Management:** Users can set and update their monthly budget. The app automatically calculates how much has been spent and how much is left for the month.

- **Data Visualization:** Using `Chart.js`, I added a pie chart to give users a clear view of how their money is being spent across different categories.

- **Filtering:** Users can filter expenses by category to see only the relevant transactions.

- **Responsive UI:** The app works smoothly on desktops, tablets, and smartphones thanks to Bootstrap.

### Files and Structure:

- **app.py:** This is where all the main functionality lives—routes, database interactions, and logic are defined here using Flask.

- **expenses.db:** The SQLite database file stores user information, expenses, categories, and budget data. It’s easy to set up and manage.

- **templates/:** Contains the HTML files like `home.html`, `login.html`, `register.html`, `tracker.html`, and `set_budget.html`. I used Jinja2 templating to display data dynamically.

- **static/:** Holds CSS files, JavaScript libraries like `Chart.js`, and any other resources needed for styling and interactivity.

- **requirements.txt:** Lists all the Python packages required to run the project, like Flask, Flask-WTF, and Werkzeug.

### Design Choices:

I chose Flask because it’s lightweight and flexible. It allowed me to structure the app in a way that’s both easy to expand and maintain. SQLite was the obvious choice because it doesn’t need any extra setup—perfect for small projects like this.

For forms and validation, I used `Flask-WTF`. It made sure users enter valid data and helped prevent bad inputs. Password security was a priority, so I used `Werkzeug’s` hashing tools to keep data safe.

For the interface, I used Bootstrap. It helped me design a neat and mobile-friendly layout without spending too much time on CSS. For charts, I picked `Chart.js` because it’s lightweight, looks great, and is easy to configure.

### Challenges:

One of the biggest challenges was making sure that user data stays private and secure. Managing sessions in Flask took some trial and error. I also had to learn how to handle real-time updates, especially when expenses are added or removed and the budget is recalculated.

Another challenge was filtering expenses by date. I needed to group expenses by month and category without making the app slow. SQLite’s `strftime` functions helped me a lot here.

### Future Improvements:

- Adding recurring expenses for things like subscriptions
- Adding notifications when the budget limit is close or exceeded
- Creating reports or trends to see expenses over multiple months
- Moving from SQLite to PostgreSQL for larger or production-ready environments
- Adding more encryption layers for sensitive data beyond just password hashing

### Conclusion:

Working on Budget Bee has been a really rewarding experience. It helped me practice web development, database management, and security. I learned a lot about building user-friendly apps that are both functional and secure. I’m proud of the final product and excited to keep improving it in the future!
