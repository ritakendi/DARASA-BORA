# from deepface import DeepFace
from flask import Flask, render_template, request, redirect, url_for, flash
import base64
import os
import csv
import numpy as np
import sys
from datetime import datetime
import sqlite3
from deepface import DeepFace

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
        student_no = request.form['Student_No']
        name = request.form['Name']
        course_name = request.form['Course Name']
        photo = request.files['photo']
        # Time = request.form['Time']
        # print(type(photo), photo)

        conn = get_db_connection()
        # users = conn.execute()
        conn.execute('INSERT INTO users(username, password, email, name, student_no, course_name, photo) VALUES (?,?,?,?,?,?,?)',
                     (username, password,  email, name, student_no, course_name, photo.read()))

        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/signin', methods=["GET", "POST"])
def signin():
    error = None
    if request.method == "POST":
        # with open("test.log", "w") as sys.stdout:
        print("Sign in request")
        user_data = request.json
        # print(user_data)
        username = user_data["username"]
        password = user_data["password"]
        user_photo = user_data["user_photo"]

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('SELECT photo FROM users WHERE username=:NAME',
                    {'NAME': username})
        database_photo = cur.fetchone()[0]
        with open("./tmp/user_tmp.png", "wb") as fp:
            fp.write(database_photo)
        df_verification = DeepFace.verify(
            "./tmp/user_tmp.png", user_photo)

        print(df_verification)

        if check_if_user_exists(username, password):
            flash('Login successful')
            return redirect(url_for('home'))
        else:

            flash('Invalid username or password. Please try again!', 'error')
            return redirect(url_for('signin'))

    return render_template('login.html', error=error)


@ app.route('/home', methods=['GET', 'POST'])
def home():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT student_no, name, course_name, time FROM users')
    records = cur.fetchall()
    conn.close()

    return render_template('home.html', records=records)


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
