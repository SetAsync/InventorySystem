#// Globals
from flask import *
from datetime import datetime, timedelta
from models import *
from database import db
import bcrypt

#// Import App
blueprint = Blueprint('account', __name__)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Query the database for the user
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            # If the user exists and the password is correct, log them in
            session['user'] = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("account.profile"))
        else:
            # If the user doesn't exist or the password is incorrect, show error
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for("account.login"))
    else:
        return render_template("login.html")
    
@blueprint.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        # Register User
        existingUser = User.query.filter_by(email = request.form["email"]).first()
        if existingUser:
            flash("An account with that email exists!")
            return redirect(url_for("account.register"))

        salt = bcrypt.gensalt()

        password = request.form["password"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new User object and add it to the database
        new_user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=hashed_password  # Store the hashed password as bytes
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Created account!")
        return redirect(url_for("account.login"))
    else:
        return render_template("register.html")

@blueprint.route("/profile")
def profile():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))
    return render_template("profile.html", user = session["user"])