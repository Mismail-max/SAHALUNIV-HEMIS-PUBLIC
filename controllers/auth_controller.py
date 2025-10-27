from flask import Blueprint, render_template, request, redirect, session, flash
from models.user_model import create_user, get_user_by_username, update_password
import bcrypt
import re 

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if "username" not in session:
        flash("You must be logged in to register a new user.", "warning")
        return redirect("/login")

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        #  Password strength validation
        password_regex = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        )
        if not password_regex.match(password):
            flash("Password must meet all requirements: uppercase, lowercase, number, special character, and at least 8 characters.", "danger")
            return render_template("register.html")
        if create_user(first_name, last_name, email, username, password):
            flash("Registration successful. Please login.", "success")
            return redirect("/login")
        else:
            flash("Username already taken or error occurred.", "danger")
    return render_template("register.html")


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            session["name"] = f"{user['first_name']} {user['last_name']}"
            session["username"] = user["username"]
            flash("Login successful. Welcome!", "success")
            return redirect("/")
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")


@auth_routes.route("/register", methods=["GET", "POST"])
def register_user():
    # ✅ Ensure the requester is authenticated
    if "username" not in session:
        flash("You must be logged in to register a new user.", "warning")
        return redirect("/login")

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # ✅ Password strength validation
        password_regex = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        )
        if not password_regex.match(password):
            flash("Password must meet all requirements: uppercase, lowercase, number, special character, and at least 8 characters.", "danger")
            return render_template("register.html")

        # ✅ Attempt to create user
        if create_user(first_name, last_name, email, username, password):
            flash("Registration successful. Please login.", "success")
            return redirect("/login")
        else:
            flash("Username already taken or error occurred.", "danger")

    return render_template("register.html")



@auth_routes.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "warning")
    return redirect("/")
