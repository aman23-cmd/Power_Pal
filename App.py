from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'energy_dashboard'

mysql = MySQL(app)

# 🧑 Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('User already exists. Please login.')
            return redirect('/login')
        else:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                           (name, email, password))
            mysql.connection.commit()
            flash('Signup successful! Please login.')
            return redirect('/login')
    return render_template('signup.html')

# 🔐 Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            session['email'] = user[2]
            flash('Login successful!')
            return redirect('/dashboard')
        else:
            flash('Invalid credentials')
            return redirect('/login')
    return render_template('login.html')

# 📊 Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html')  # ← apna dashboard yaha
    return redirect('/login')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
