from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection from Render
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return f"Welcome, {username}!"
    else:
        return "Invalid credentials", 401

if __name__ == '__main__':
    app.run(debug=True)
