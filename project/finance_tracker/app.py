from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import extract


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'user_transactions'  # Rename the table to avoid conflicts
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Transaction {self.id}>'



# Create the database
with app.app_context():
    db.create_all()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get the current date
    current_date = datetime.now()

    # Default to current month and year
    if request.method == 'POST':
        selected_month = int(request.form.get('month'))
        selected_year = int(request.form.get('year'))
    else:
        selected_month = current_date.month
        selected_year = current_date.year

    # Get the transactions for the selected month and year
    transactions = Transaction.query.filter(
        db.extract('month', Transaction.date) == selected_month,
        db.extract('year', Transaction.date) == selected_year,
        Transaction.user_id == session['user_id']
    ).all()

    # Calculate total income and expenses for the selected month
    # Calculate total income (only Salary)
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income' and t.category.lower() == 'salary')
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    net_balance = total_income - total_expenses
    total_money = net_balance + sum(t.amount for t in transactions if t.transaction_type == 'income' and t.category.lower() == 'saving')

    # Prepare month names and years for the dropdown
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years = list(range(current_date.year, current_date.year - 6, -1))  # Last 6 years

    # Aggregate expenses by category
    category_expenses = {
        "apartment": 0,
        "tv": 0,
        "bills": 0,
        "education": 0,
        "food_and_drink": 0,
        "groceries": 0,
        "health_and_fitness": 0,
        "investments": 0,
        "borrow": 0,
        "vehicle_and_transports": 0,
        "travel": 0,
        "shopping": 0,
        "entertainment": 0,
        "other": 0
    }

    # Define a mapping for category keys to display names
    category_display_names = {
        "apartment": "Apartment",
        "tv": "TV",
        "bills": "Bills",
        "education": "Education",
        "food_and_drink": "Food & Drink",
        "groceries": "Groceries",
        "health_and_fitness": "Health & Fitness",
        "investments": "Investments",
        "borrow": "Borrow",
        "vehicle_and_transports": "Vehicle & Transports",
        "travel": "Travel",
        "shopping": "Shopping",
        "entertainment": "Entertainment",
        "other": "Other"
    }

    # Normalize category names and aggregate expenses
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            category = transaction.category.lower().replace(" ", "_")
            if category in category_expenses:
                category_expenses[category] += transaction.amount
            else:
                # Dynamically add any new categories that are not predefined
                category_expenses[category] = transaction.amount

    return render_template(
        'index.html',
        transactions=transactions,
        category_display_names=category_display_names,
        selected_month=selected_month,
        selected_year=selected_year,
        month_names=month_names,
        years=years,
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        total_money=total_money,
        category_expenses=category_expenses)




@app.route('/add_income', methods=['POST'])
def add_income():
    amount = request.form.get('amount')
    category = request.form.get('category')
    description = request.form.get('description')
    # Get month and year from the form
    month = int(request.form.get('month'))
    year = int(request.form.get('year'))
    # Use the current day
    current_day = datetime.now().day  # Get the current day
    # Create a date from month and year (using the first day of the month)
    transaction_date = datetime(year, month, current_day)

    # Ensure amount is converted to float
    if amount and category:
        try:
            amount = float(amount)
            db.session.execute(
                text("INSERT INTO user_transactions (user_id, amount, category, description, transaction_type, date) VALUES (:user_id, :amount, :category, :description, :transaction_type, :date)"),
                {
                    'user_id': session['user_id'],
                    'amount': amount,
                    'category': category,
                    'description': description,
                    'transaction_type': 'income',
                    'date': transaction_date  # Add the date here
                }
            )
            db.session.commit()
            flash("Income added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"Failed to add income: {str(e)}", "danger")
    else:
        flash("Please provide amount and category.", "danger")

    return redirect(url_for('index'))



@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = request.form.get('amount')
    category = request.form.get('category')
    description = request.form.get('description')
    # Get month and year from the form
    month = int(request.form.get('month'))
    year = int(request.form.get('year'))
    # Use the current day
    current_day = datetime.now().day  # Get the current day
    # Create a date from month and year (using the first day of the month)
    transaction_date = datetime(year, month, current_day)

    # Ensure amount is converted to float
    if amount and category:
        try:
            amount = float(amount)
            db.session.execute(
                text("INSERT INTO user_transactions (user_id, amount, category, description, transaction_type, date) VALUES (:user_id, :amount, :category, :description, :transaction_type, :date)"),
                {
                    'user_id': session['user_id'],
                    'amount': amount,
                    'category': category,
                    'description': description,
                    'transaction_type': 'expense',
                    'date': transaction_date  # Add the date here
                }
            )
            db.session.commit()
            flash("Expense added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"Failed to add expense: {str(e)}", "danger")
    else:
        flash("Please provide amount and category.", "danger")

    return redirect(url_for('index'))


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    transaction = Transaction.query.get_or_404(transaction_id)

    if request.method == 'POST':
        # Update transaction details
        transaction.amount = float(request.form['amount'])
        transaction.category = request.form['category']
        transaction.description = request.form['description']
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('history'))

    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('history'))



@app.route('/history', methods=['GET', 'POST'])  # Added POST to methods
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_date = datetime.now()

    # Default to current month and year or use selected month and year from form
    if request.method == 'POST':
        selected_month = int(request.form.get('month'))
        selected_year = int(request.form.get('year'))
    else:
        selected_month = current_date.month
        selected_year = current_date.year

    # Get transactions for the selected month and year
    transactions = Transaction.query.filter(
        db.extract('month', Transaction.date) == selected_month,
        db.extract('year', Transaction.date) == selected_year,
        Transaction.user_id == session['user_id']
    ).all()

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income' and t.category.lower() == 'salary')
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    net_balance = total_income - total_expenses

    
    # Create a dictionary to hold expenses by category
    category_expenses = {
        "apartment": 0,
        "tv": 0,
        "bills": 0,
        "education": 0,
        "food_and_drink": 0,
        "groceries": 0,
        "health_and_fitness": 0,
        "investments": 0,
        "borrow": 0,
        "vehicle_and_transports": 0,
        "travel": 0,
        "shopping": 0,
        "entertainment": 0,
        "other": 0
    }

    # Define a mapping for category keys to display names
    category_display_names = {
        "apartment": "Apartment",
        "tv": "TV",
        "bills": "Bills",
        "education": "Education",
        "food_and_drink": "Food & Drink",
        "groceries": "Groceries",
        "health_and_fitness": "Health & Fitness",
        "investments": "Investments",
        "borrow": "Borrow",
        "vehicle_and_transports": "Vehicle & Transports",
        "travel": "Travel",
        "shopping": "Shopping",
        "entertainment": "Entertainment",
        "other": "Other"
    }

    # Initialize total expenses
    total_expenses = 0

    # Aggregate expenses for each transaction
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            # Normalize category by making it lowercase and replacing spaces with underscores
            category = transaction.category.lower().replace(" ", "_")
            if category in category_expenses:
                category_expenses[category] += transaction.amount
                total_expenses += transaction.amount  # Aggregate total expenses
            else:
                # Dynamically add any new categories that are not predefined
                category_expenses[category] = transaction.amount  # Initialize if not present
                total_expenses += transaction.amount  # Aggregate total expenses

    # Calculate total income
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income' and t.category.lower() == 'salary')

    return render_template(
        'history.html',
        transactions=transactions,
        category_display_names=category_display_names,
        category_expenses=category_expenses,
        total_income=total_income,         # Pass total_income to template
        total_expenses=total_expenses,     # Pass total_expenses to template
        net_balance=net_balance,
        selected_month=selected_month,
        selected_year=selected_year,
        month_names=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        years=list(range(current_date.year, current_date.year - 6, -1))
    )









@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.get(session['user_id'])
        if user.password == old_password and new_password == confirm_password:
            user.password = new_password
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid old password or new passwords do not match.', 'danger')

    return render_template('change_password.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
