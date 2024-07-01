#// Index
# /

#// Globals
from flask import *
from datetime import datetime, timedelta
from models import *
from database import db
import bcrypt

#// Import App
blueprint = Blueprint('index', __name__)

@blueprint.route("/")
def index():
    return redirect(url_for("index.home"))

@blueprint.route("/home")
def home():
    return render_template("index.html")

@blueprint.route("/<x>")
def notFound(x):
    return render_template("404.html", page = x)