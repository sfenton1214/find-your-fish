# Import and configuration code from CS50 Finance pset

import csv
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Reads from questions.csv and loads into tree, displays question html
with open("Findyourfish.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fishes.db")


@app.route("/", methods=["GET", "POST"])
def get_index():
    """ Index page is the first page of the key"""

    # If it is the first time index is rendered with GET method, display the first question
    if request.method == "GET":
        row = rows[0]

    # For subsequent rendering with POST, use the submitted form to get the id of the next csv item
    else:
        id = int(request.form.get("id"))
        row = rows[id - 1]

    # Check if the next csv item in the key is a question or a fish
    if row['a']:

        return render_template("question.html", row=row)

    else:
        fish = row['text']

        # Check if the user is logged in
        if not session:
            verify = -1
        # Check to see if the fish is one of the user's favorites already.
        else:
            verify = len(db.execute("SELECT fishname FROM favorites WHERE user_id = :user_id AND fishname = :fishname",
                                    user_id=session["user_id"], fishname=fish))
        return render_template("fish.html", fish=fish, verify=verify)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    if rows:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/fishinsert", methods=["POST"])
@login_required
def fishinsert():
    """Insert a fish into favorites"""

    # Insert selected fish into database with user's id
    db.execute("INSERT INTO favorites (user_id, fishname) VALUES (:user_id, :fishname)",
               user_id=session["user_id"], fishname=request.form.get("fishname"))

    return redirect("/favorites")


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """Show favorite fish of a user"""

    # Select the current user's favorited fish
    rows = db.execute("SELECT fishname FROM favorites WHERE user_id = :user_id",
                      user_id=session["user_id"])

    # If GET, show the users favotited fish
    if request.method == "GET":

        return render_template("favorites.html", rows=rows)

    # If POST, render the selected fish's HTML page
    else:

        fish = request.form.get("fishname")
        return render_template("fish.html", fish=fish, verify=1)

#login, log out, and register functions from Skye's CS50 Finance Pset

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("you must provide a username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("you must provide a password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("you must provide a password confirmation")

        # check if password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("the password must match password confirmation")

        # Encrypt password
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into database if username isn't already present
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("this username is taken")

        else:
            # Remember which user has logged in
            session["user_id"] = result

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")