# from deepface import DeepFace
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from datetime import datetime
import sqlite3

# setting up our application
app = Flask(__name__)
app.secret_key = "grtyui"

# Saving the date today
now = datetime.now()
current_date = now.strftime("%d-%m-%y")


def check_if_user_exists(username, password):
    """Function checks if the user exists
    and if the password entered matches
    with the one that is stored in our database.
    """
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=:NAME",
                {'NAME': username})

    user_pass = cur.fetchone()
    if user_pass is None:
        return False
    elif user_pass[0] == password:
        return True
    return False


@app.route('/')
def root():
    return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]
        email = request.form["email"]
        conn = get_db_connection()
        # users = conn.execute()
        conn.execute('INSERT INTO users(username, password, email) VALUES (?,?,?)',
                     (username, password,  email))

        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/signin', methods=["GET", "POST"])
def signin():
    error = None
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]

        if check_if_user_exists(username, password):
            flash('Login successful')
            return redirect(url_for('home'))
        else:

            flash('Invalid username or password. Please try again!', 'error')
            return redirect(url_for('signin'))

    return render_template('login.html', error=error)


@app.route('/home')
def home():
    return render_template('home.html')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# @app.route('/login', methods=["Get", "POST"])
# def login():
#     if request.method == "POST":
#         # getting input with name in html form
#         username = request.form.get("usrname")
#         return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
