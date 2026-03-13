from flask import Flask, request
import sqlite3
import os
import hashlib
import subprocess
import config

app = Flask(__name__)

# Hardcoded secret
SECRET_KEY = "SUPER_SECRET_KEY_123456"

DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


@app.route("/")
def home():
    return "Vulnerable App Running"


# SQL Injection vulnerability
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = cursor.execute(query).fetchone()

    if result:
        return "Login Success"
    else:
        return "Login Failed"


# Command Injection
@app.route("/ping")
def ping():
    host = request.args.get("host")

    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)

    return result


# Path Traversal
@app.route("/readfile")
def read_file():
    filename = request.args.get("file")

    with open(filename, "r") as f:
        data = f.read()

    return data


# Weak hashing
@app.route("/hash")
def hash_password():
    pwd = request.args.get("password")
    hashed = hashlib.md5(pwd.encode()).hexdigest()

    return hashed


# Hardcoded credential endpoint
@app.route("/admin")
def admin():
    user = request.args.get("user")
    pwd = request.args.get("pwd")

    if user == "admin" and pwd == "admin123":
        return "Welcome Admin"
    else:
        return "Access denied"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
