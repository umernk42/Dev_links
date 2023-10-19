import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from werkzeug.utils import secure_filename

# setting upload path for userimages
UPLOAD_FOLDER = 'static/uploads/'

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///links.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    if request.method == "POST":
        formData = []
        index = 0
        requestFormIndex = 0

        # Adding the form data in a list of objects to use later
        for key, val in request.form.items():
            if requestFormIndex % 2 == 0:
                formData.append({
                    "website": val
                })
            else:
                formData[index]["url"] = val
                index += 1

            requestFormIndex += 1

        # Deleting all the existing links for this user to make database consistent
        db.execute("DELETE FROM links_data WHERE user_id = ?", user_id)

        # Now adding all the links submitted in the form to the database for this user
        for item in formData:
            website = item["website"]
            url = item["url"]
            db.execute("INSERT INTO links_data (user_id, website, url) VALUES (?, ?, ?)", user_id, website, url)

        return redirect("/")


    else:
        existingLinks = db.execute("SELECT website, url FROM links_data WHERE user_id=?", user_id)

        return render_template(
            "index.html", existingLinks=enumerate(existingLinks)
        )

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

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
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must type password again")

        # Storing the values in variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checking if username already exists
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("Username Already Exists")

        # Checking if passwords and confirmation match
        elif password != confirmation:
            return apology("Password and confirm password dont match")

        # Generate a has for the password
        hash = generate_password_hash(password)

        # Store the user in the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Login the user automatically after registering
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    if request.method == "POST":

        # Checks if the user has uploaded an image or not
        if request.files["picture"]:
            file = request.files["picture"]

            # Find the list of exiting images in the upload folder
            existingFiles = os.listdir(app.config["UPLOAD_FOLDER"])

            for f in existingFiles:
                if f.split(".")[0] == str(user_id):
                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"],f))
                    break

            # Saving the filename using the user_id as the name of the file for better access
            filename = file.filename
            file_ext = filename.split(".")[1]
            filename = secure_filename(str(user_id) + "." + file_ext)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        # Gathering the rest of the parameters from the profile form
        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        email = request.form.get("email")

        exists = db.execute("SELECT * FROM user_profiles WHERE user_id=?",user_id)

        if exists:
            db.execute("UPDATE user_profiles SET first_name=?, last_name=?, email=?", firstName, lastName, email)
        else:
            db.execute("INSERT INTO user_profiles(user_id, first_name, last_name, email) VALUES(?, ?, ?, ?)", user_id, firstName, lastName, email)


        return redirect("/")
    else:
        files = os.listdir(app.config["UPLOAD_FOLDER"])
        fileExists = False
        fileLoc = ""
        first_name = ""
        last_name = ""
        email = ""

        for file in files:
            if file.split(".")[0] == str(user_id):
                fileExists = True
                filename = file
                break

        if fileExists:
            fileLoc = "../static/uploads/" + filename


        exists = db.execute("SELECT * FROM user_profiles WHERE user_id=?",user_id)

        if exists:
            first_name = exists[0]["first_name"]
            last_name = exists[0]["last_name"]
            email = exists[0]["email"]

        return render_template("profile.html", first_name=first_name, last_name=last_name, email=email, fileLoc=fileLoc)


@app.route("/preview", methods=["GET", "POST"])
@login_required
def preview():
    user_id = session["user_id"]
    if request.method == "POST":
        return render_template("shared.html")
    else:
        # Querying the profile details from the database
        profile = db.execute("SELECT * FROM user_profiles WHERE user_id = ?", user_id)
        name = ""
        email = ""
        filename = ""
        fileExists = False
        name = profile[0]["first_name"].capitalize() + " " + profile[0]["last_name"].capitalize()
        email = profile[0]["email"]

        # Finding the picture from local directory
        files = os.listdir(app.config["UPLOAD_FOLDER"])

        for file in files:
            if file.split(".")[0] == str(user_id):
                fileExists = True
                filename = file
                break

        if fileExists:
            fileLoc = "../static/uploads/" + filename


        # Quering the links of the user from the database
        links = []
        links = db.execute("SELECT * FROM links_data WHERE user_id = ?", user_id)

        return render_template("preview.html", name=name, email=email, links=links, fileLoc=fileLoc)