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
altair==5.4.1
attrs==24.3.0
blinker==1.8.2
cachetools==5.5.0
certifi==2024.12.14
cffi==1.17.1
charset-normalizer==3.4.1
click==8.0.3
colorama==0.4.4
dnspython==2.6.1
exceptiongroup==1.2.2
Flask==2.0.2
Flask-MySQLdb==0.2.0
gitdb==4.0.11
GitPython==3.1.43
greenlet==3.1.1
gunicorn==20.1.0
h11==0.14.0
idna==3.10
importlib_metadata==8.5.0
importlib_resources==6.4.5
iniconfig==2.0.0
itsdangerous==2.0.1
Jinja2==3.0.2
jsonschema==4.23.0
jsonschema-specifications==2023.12.1
markdown-it-py==3.0.0
MarkupSafe==2.0.1
mdurl==0.1.2
mysql-connector==2.2.9
mysqlclient==2.0.3
narwhals==1.20.1
newsapi-python==0.2.7
numpy==1.24.4
outcome==1.3.0.post0
packaging==24.2
pandas==2.0.3
pillow==10.4.0
pkgutil_resolve_name==1.3.10
playwright==1.48.0
pluggy==1.5.0
protobuf==5.29.2
pyarrow==17.0.0
pycparser==2.22
pydeck==0.9.1
pyee==12.0.0
Pygments==2.18.0
pymongo==4.10.1
PySocks==1.7.1
pytest==8.3.4
pytest-base-url==2.1.0
pytest-playwright==0.5.2
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-slugify==8.0.4
pytz==2024.2
referencing==0.35.1
requests==2.32.3
rich==13.9.4
rpds-py==0.20.1
selenium==4.27.1
six==1.17.0
smmap==5.0.1
sniffio==1.3.1
sortedcontainers==2.4.0
streamlit==1.40.1
tenacity==9.0.0
text-unidecode==1.3
toml==0.10.2
tomli==2.2.1
tornado==6.4.2
trio==0.27.0
trio-websocket==0.11.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
watchdog==4.0.2
webdriver-manager==4.0.2
websocket-client==1.8.0
Werkzeug==2.0.2
wsproto==1.2.0
zipp==3.20.2

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

