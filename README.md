# News Aggregator Flask Application

This is a news aggregator application built with Flask that combines news scraping, user authentication, community news posting, and fact-checking features. It uses MySQL for user data management and MongoDB (with GridFS) for storing community posts, including images.

---

## Features
- User registration and login with session and cookies.
- Scraping Google News based on user preferences and location.
- Community news posting with image upload.
- Fact-checking for headlines using a dedicated API.
- CSRF protection for sensitive operations.

---

## Prerequisites

Before running this application, ensure you have the following installed:

1. Python 3.7+
2. MySQL Server
3. MongoDB
4. Pip (Python package manager)

---

## Installation Guide

### 1. Clone the Repository

```bash
$ git clone https://github.com/your-username/news-aggregator.git
$ cd news-aggregator
```

### 2. Set Up a Virtual Environment

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Python Packages

```bash
$ pip install -r requirements.txt
```

### 4. Set Up MySQL Database

1. Create a MySQL database named `kyn`.
2. Execute the following SQL script to create necessary tables:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

CREATE TABLE favourites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    topic VARCHAR(255)
);
```

3. Update the MySQL connection configuration in `app.py`:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'kyn'
```

### 5. Set Up MongoDB

1. Start the MongoDB server.
2. Create a database named `newsAggregator`.
3. Create a collection named `communitynews`.

### 6. Configure CSRF Secret Key

Update the secret key in `app.py`:

```python
app.secret_key = 'your_secret_key'
```

### 7. Run the Application

Start the Flask development server:

```bash
$ flask run
```

The application will be available at `http://127.0.0.1:5000/`.

---

## Project Structure

```
news-aggregator/
|-- static/                # Static files (CSS, JS, images)
|-- templates/             # HTML templates
|-- webscrapping/          # Scraping scripts
|   |-- main.py
|-- factcheck.py           # Fact-checking logic
|-- app.py                 # Main Flask application
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
```

---

## Dependencies

The required Python packages are listed in `requirements.txt`:

```text
Flask
Flask-MySQLdb
pymongo
gridfs
werkzeug
```

Install them using:

```bash
$ pip install -r requirements.txt
```

---

## Usage

### 1. Register and Log In

Visit the `/register` route to create an account, then log in via the `/login` route.

### 2. Add Favourites

Navigate to the `/favourites` route to add topics of interest.

### 3. Dashboard

Access the `/index` route to view aggregated news based on preferences and location.

### 4. Community News

Visit `/post` to create a community news post. Uploaded images will be stored in MongoDB using GridFS.

### 5. Fact-Checking

Use the `/factcheck` API endpoint to validate news headlines.

---

## Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request.

