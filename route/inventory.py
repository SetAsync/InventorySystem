#// Index
# /

#// Globals
from flask import *
from datetime import datetime, timedelta
from models import *
from database import db
import bcrypt

#// Import App
blueprint = Blueprint('inventory', __name__)

@blueprint.route("/inventory")
def inventory():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"] == 0:
        flash("Your account needs to be activated by an admin!")
        return redirect(url_for("index.home"))
    
    locations = Location.query.all()
    return render_template("inventory.html", user = session["user"], locations = locations)

@blueprint.route("/inventory/create_location", methods = ["GET", "POST"])
def create_location():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"] < 2:
        flash("Access denied!")
        return redirect(url_for("index.home"))
    
    if request.method == "POST":
        newLocation = Location(request.form["locationname"])
        db.session.add(newLocation)
        db.session.commit()
        flash("Created new location.")
        return redirect(url_for("admin.admin_panel"))
    else:
        return render_template("create_location.html", user = session["user"])
    
@blueprint.route("/inventory/create_item", methods = ["GET", "POST"])
def create_item():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"] < 2:
        flash("Access denied!")
        return redirect(url_for("index.home"))
    
    if request.method == "POST":
        newLocation = Item(request.form["itemname"])
        db.session.add(newLocation)
        db.session.commit()
        flash("Created new item.")
        return redirect(url_for("admin.admin_panel"))
    else:
        return render_template("create_item.html", user = session["user"])
    
@blueprint.route("/inventory/view_items/<location_id>", methods=["POST", "GET"])
def view_items(location_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"] == 0:
        flash("Your account needs to be activated by an admin!")
        return redirect(url_for("index.home"))


    itemsInLocation = []
    if location_id == "all":
        itemsInLocation = Item.query.all()
    else:
        itemsInLocation = Item.query.filter_by(location_id = location_id).all()
    
    locations = Location.query.all()
    return render_template("items.html", items=itemsInLocation, locations = locations)

@blueprint.route("/inventory/delete_item/<item_id>", methods=["POST"])
def delete_item(item_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"] < 2:
        flash("Access denied!")
        return redirect(url_for("index.home"))

    item = Item.query.filter_by(id = item_id).first()
    if item:
        item.delete()
        flash("Item deleted.")
    else:
        flash("Failed to remove item!")
    return redirect(url_for("admin.admin_panel"))

@blueprint.route("/inventory/claim_item/<item_id>", methods=["POST", "GET"])
def claim_item(item_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"]  == 0:
        flash("Access denied!")
        return redirect(url_for("index.home"))

    item = Item.query.filter_by(id = item_id).first()
    if item:
        if item.claimed:
            flash("Cannot claim a claimed item!")
        else:
            item.claimed = session["user"]["id"]
            db.session.commit()
            flash("Claimed item.")
    else:
        flash("Failed to claim item!")

    return redirect(request.referrer or url_for("inventory.view_items"))

@blueprint.route("/inventory/update_item_location/<item_id>", methods=["POST"])
def update_item_location(item_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"]  == 0:
        flash("Access denied!")
        return redirect(url_for("index.home"))

    item = Item.query.filter_by(id = item_id).first()
    if item:
        if item.claimed:
            flash("Cannot claim a claimed item!")
        else:
            item.claimed = session["user"]["id"]
            db.session.commit()
            flash("Claimed item.")
    else:
        flash("Failed to claim item!")

    return redirect(request.referrer or url_for("inventory.view_items"))

@blueprint.route("/inventory/user/<user_id>", methods=["POST", "GET"])
def view_user(user_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"]  == 0:
        flash("Access denied!")
        return redirect(url_for("index.home"))

    user = User.query.filter_by(id = user_id).first()
    if not user:
        flash("Failed to find the user!")
        return redirect(request.referrer or url_for("index.home"))
    
    items = Item.query.filter_by(claimed = user.id).all()
    return render_template("user.html", user = user, claimed_items = items)

@blueprint.route("/inventory/assign_location/<item_id>", methods=["POST", "GET"])
def assign_location(item_id):
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("account.login"))

    if session["user"]["role"]  == 0:
        flash("Access denied!")
        return redirect(url_for("index.home"))

    item = Item.query.filter_by(id = item_id).first()
    if not item:
        flash("Invalid Item!")
        return redirect(url_for("inventory.inventory"))
    
    if request.method == "POST":
        location_id = request.form.get('location_id')
        if location_id:
            item.location_id = location_id
            db.session.commit()
        else:
            flash("Invalid location!")

        return redirect(url_for("inventory.inventory"))
    else:
        locations = Location.query.all()
        return render_template("assign_location.html", item = item, locations = locations)
