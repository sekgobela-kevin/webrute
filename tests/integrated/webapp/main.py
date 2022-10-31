from flask import Flask, redirect, url_for
from flask import render_template
from flask import session
from flask import request
from flask import g

from typing import Dict
import json
import os

import logging


logger = logging.getLogger('werkzeug')
logger.disabled = True


app = Flask(__name__)
app.secret_key = "!)#*EODKCMT"

@app.before_request
def setup_accounts():
    folder_path = os.path.split(os.path.abspath(__file__))[0]
    file_path = os.path.join(folder_path, "accounts.json")
    with open(file_path) as f:
        g.accounts: Dict[str, str] = json.load(f)


@app.before_request
def setupt_account():
    if "user_id" in session:
        username: str = session["user_id"]
        password: str = g.accounts[username]
        g.account = {username: password}
        g.username = username

@app.route('/', methods=["Get"])
def home():
    if "user_id" in session:
        responce= "Welcome back " + g.username
        return render_template('/responce.html', responce_text=responce)
    return render_template('/home.html')


@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username not in g.accounts:
        responce= "No such username exists in the server"
        return render_template('/responce.html', responce_text=responce)
    elif g.accounts[username] == password:
        session["user_id"] = username
        responce= "Login successful, welcome " + username
        return render_template('/responce.html', responce_text=responce)
    else:
        responce= "Failed to login with provided credentials"
        return render_template('/responce.html', responce_text=responce)

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
