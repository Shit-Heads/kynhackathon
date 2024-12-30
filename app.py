from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'gowtham'  

app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'admin'  
app.config['MYSQL_DB'] = 'kyn' 

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Email is already registered!', 'danger')
        else:
            cursor.execute('INSERT INTO users (firstname, lastname, email, password, location) VALUES (%s, %s, %s, %s, %s)', (firstname, lastname, email, password, location))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            if account['password'] == password:
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('No account found. Please sign up first.', 'warning')
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/index')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)