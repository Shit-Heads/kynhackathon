from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
from webscrapping.main import *
from webscrapping.trending import *
import pymongo
import gridfs
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import base64
import os
from factcheck import check_fact  

app = Flask(__name__)
app.secret_key = 'gowtham'

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["newsAggregator"]
collection = db["communitynews"]
fs = gridfs.GridFS(db)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bingus'
app.config['MYSQL_DB'] = 'kyn'

mysql = MySQL(app)

@app.route('/')
def index():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (username, ))
    account = cursor.fetchone()
    if account:
        if account['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            resume = make_response(redirect(url_for('dashboard')))
            return resume
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/picfav')
def picfav():
    return render_template('picfav.html')

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
            session['loggedin'] = True
            session['username'] = email
            return redirect(url_for('picfav'))

    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('checkbox')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            if account['password'] == password:
                session['loggedin'] = True
                session['username'] = email
                if remember_me:
                    res = make_response(redirect(url_for('dashboard')))
                    res.set_cookie('username', f'{email}', max_age=60*60*24*7)
                    res.set_cookie('password', f'{password}', max_age=60*60*24*7)
                    flash('Login successful!', 'success')
                    return res
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('No account found. Please sign up first.', 'warning')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    res = make_response(redirect('/'))
    res.delete_cookie('username')
    res.delete_cookie('password')
    return res

@app.route('/favourites', methods=['GET', 'POST'])
def favourites():
    if request.method == 'POST':
        topics = request.form.getlist('topics')
        username = session['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for topic in topics:
            cursor.execute('INSERT INTO favourites (username, topic) VALUES (%s, %s)', (username, topic.strip()))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    return render_template('favourites.html')

@app.route('/index')
def dashboard():
    if 'loggedin' in session:
        username = session['username'] # if users name is needed use this variable
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"select * from users where email = '{username}'")
        account = cursor.fetchone()
        location = account['location']
        category = 'f1'
        news = scrape_google_news(location, category)
        trending = scrape_trending_news(category)
        communitypost = collection.find().sort("_id", pymongo.DESCENDING)

        posts_with_images = []
        for post in communitypost:
            if post.get('image_id'):
                image = fs.get(post['image_id']).read()
                image_url = f"data:image/jpeg;base64,{base64.b64encode(image).decode('utf-8')}"
                post['image_url'] = image_url
            else:
                post['image_url'] = None
            posts_with_images.append(post)

        return render_template('index.html', news=news, communitypost=posts_with_images, trending=trending)
    return redirect(url_for("login"))

@app.route('/index/<news_category>')
def categorydashboard(news_category):
    if 'loggedin' in session:
        username = session['username'] # if users name is needed use this variable
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"select * from users where email = '{username}'")
        account = cursor.fetchone()
        location = account['location']
        category = news_category
        news = scrape_google_news(location, category)
        trending = scrape_trending_news(category)
        communitypost = collection.find().sort("_id", pymongo.DESCENDING)

        posts_with_images = []
        for post in communitypost:
            if post.get('image_id'):
                image = fs.get(post['image_id']).read()
                image_url = f"data:image/jpeg;base64,{base64.b64encode(image).decode('utf-8')}"
                post['image_url'] = image_url
            else:
                post['image_url'] = None
            posts_with_images.append(post)

        return render_template('index.html', news=news, communitypost=posts_with_images,  trending=trending)
    return redirect(url_for("login"))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        headline = request.form['headline']
        date = request.form['date']
        location = request.form['location']
        category = request.form['category']
        description = request.form['description']
        username = session['username']

        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            file_id = fs.put(image, filename=filename)
        else:
            file_id = None

        collection.insert_one({"username": username, "headline": headline, "date": date, "location": location, "category": category, "description": description, "image_id": file_id})
        return redirect(url_for('dashboard'))
    return render_template('post.html')

@app.route('/factcheck', methods=['POST'])
def factcheck_route():
    data = request.json
    headline = data.get('headline')
    results = check_fact(headline)
    is_true = any(result['claim_conclusion'].lower() in ['true', 'correct'] for result in results)
    no_matching_claims = len(results) == 0
    return jsonify({'is_true': is_true, 'no_matching_claims': no_matching_claims})

@app.route('/viewpost/<post_id>')
def viewpost(post_id):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post.get('image_id'):
        image = fs.get(post['image_id']).read()
        image_url = f"data:image/jpeg;base64,{base64.b64encode(image).decode('utf-8')}"
    else:
        image_url = None
    return render_template("viewpost.html", post=post, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)