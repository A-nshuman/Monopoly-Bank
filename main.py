# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector

# app = Flask(__name__)

# # Database connection details
# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         port=3306,
#         user="root",
#         passwd="123456789",
#         database="bus"
#     )

# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         try:
#             # Insert the new user with a default balance of 10000
#             cursor.execute(
#                 "INSERT INTO users (name, password, balance) VALUES (%s, %s, %s)",
#                 (name, password, 10000)
#             )
#             connection.commit()

#             # Get the ID of the newly created user
#             user_id = cursor.lastrowid
#         finally:
#             cursor.close()
#             connection.close()

#         # Redirect to the login page or dashboard
#         return redirect(url_for('dashboard', user_id=user_id))  # Adjust based on desired behavior
#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         try:
#             # Check user credentials
#             cursor.execute(
#                 "SELECT * FROM users WHERE name = %s AND password = %s",
#                 (name, password)
#             )
#             user = cursor.fetchone()
#         finally:
#             cursor.close()
#             connection.close()

#         if user:
#             return redirect(url_for('dashboard', user_id=user['id']))
#     return render_template('login.html')

# @app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
# def dashboard(user_id):
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         # Fetch user details
#         cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#         user = cursor.fetchone()
#         if not user:
#             return "User not found", 404

#         if request.method == 'POST':
#             receiver_name = request.form['receiver_name']
#             amount = int(request.form['amount'])

#             # Fetch receiver details
#             cursor.execute("SELECT * FROM users WHERE name = %s", (receiver_name,))
#             receiver = cursor.fetchone()

#             if receiver and amount > 0 and user['balance'] >= amount:
#                 # Update balances
#                 cursor.execute(
#                     "UPDATE users SET balance = balance - %s WHERE id = %s",
#                     (amount, user['id'])
#                 )
#                 cursor.execute(
#                     "UPDATE users SET balance = balance + %s WHERE id = %s",
#                     (amount, receiver['id'])
#                 )
#                 connection.commit()
#                 return redirect(url_for('dashboard', user_id=user_id))
#     finally:
#         cursor.close()
#         connection.close()

#     return render_template('dashboard.html', user=user)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="123456789",
        database="bus"
    )

# Function to check and create tables if not exist
def ensure_tables_exist():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Check if 'users' table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                balance INT DEFAULT 10000
            )
        """)
        # Check if 'statements' table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statements (
                statement TEXT
            )
        """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def calcLoan(amount):
    percent = 0.15 * amount
    return amount, int(percent), int(amount + percent)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Insert the new user with a default balance of 10000
            cursor.execute(
                "INSERT INTO users (name, password, balance) VALUES (%s, %s, %s)",
                (name, password, 10000)
            )
            connection.commit()

            # Get the ID of the newly created user
            user_id = cursor.lastrowid
        finally:
            cursor.close()
            connection.close()

        # Redirect to the dashboard page with the new user's ID
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('register.html')

'''
# @app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
# def dashboard(user_id):
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         # Fetch user details
#         cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#         user = cursor.fetchone()
#         if not user:
#             return "User not found", 404

#         if request.method == 'POST':
#             sender_name = user['name']
#             receiver_name = request.form['receiver_name']
#             amount = int(request.form['amount'])

#             # Fetch receiver details
#             cursor.execute("SELECT * FROM users WHERE name = %s", (receiver_name,))
#             receiver = cursor.fetchone()

#             if receiver and amount > 0 and user['balance'] >= amount:
#                 # Update balances
#                 cursor.execute(
#                     "UPDATE users SET balance = balance - %s WHERE id = %s",
#                     (amount, user['id'])
#                 )
#                 cursor.execute(
#                     "UPDATE users SET balance = balance + %s WHERE id = %s",
#                     (amount, receiver['id'])
#                 )
#                 # Add a statement to the statements table
#                 statement = f"{sender_name} sent {amount} to {receiver_name}"
#                 cursor.execute("INSERT INTO statements (statement) VALUES (%s)", (statement,))
#                 connection.commit()
#                 return redirect(url_for('dashboard', user_id=user_id))

#         # Fetch all statements
#         cursor.execute("SELECT * FROM statements order by id desc")
#         statements = cursor.fetchall()

#     finally:
#         cursor.close()
#         connection.close()

#     return render_template('dashboard.html', user=user, statements=statements)
'''

@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    loan_result = None
    try:
        # Fetch user details
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return "User not found", 404

        if request.method == 'POST':
            if 'receiver_name' in request.form and 'amount' in request.form:
                # Handle transaction
                sender_name = user['name']
                receiver_name = request.form['receiver_name']
                amount = int(request.form['amount'])

                # Fetch receiver details
                cursor.execute("SELECT * FROM users WHERE name = %s", (receiver_name,))
                receiver = cursor.fetchone()

                if receiver and amount > 0 and user['balance'] >= amount:
                    # Update balances
                    cursor.execute(
                        "UPDATE users SET balance = balance - %s WHERE id = %s",
                        (amount, user['id'])
                    )
                    cursor.execute(
                        "UPDATE users SET balance = balance + %s WHERE id = %s",
                        (amount, receiver['id'])
                    )
                    # Add a statement to the statements table
                    statement = f"{sender_name} sent {amount} to {receiver_name}"
                    cursor.execute("INSERT INTO statements (statement) VALUES (%s)", (statement,))
                    connection.commit()
                    return redirect(url_for('dashboard', user_id=user_id))
            elif 'loanINP' in request.form:
                # Handle loan calculation
                loan_amount = int(request.form['loanINP'])
                amt, per, tot = calcLoan(loan_amount)
                loan_result = f"{amt} + {per} = {tot}"

            elif 'loanGiveAmt' in request.form:
                loan_amount = int(request.form['loanGiveAmt'])
                loan_user = request.form['loanGiveName']
                statement = f"{loan_user} loaned out {loan_amount}"
                cursor.execute("INSERT INTO statements (statement) VALUES (%s)", (statement,))
                connection.commit()
                return redirect(url_for('dashboard', user_id=user_id))

        # Fetch all statements
        cursor.execute("SELECT * FROM statements ORDER BY id DESC")
        statements = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template('dashboard.html', user=user, statements=statements, loan_result=loan_result)


if __name__ == '__main__':
    # Ensure tables exist before running the app
    ensure_tables_exist()
    app.run(host="0.0.0.0", port=5000, debug=True)