#// Globals
from flask import *
from datetime import datetime, timedelta
from models import *
from database import db

#// Import App
blueprint = Blueprint('admin', __name__)

@blueprint.route('/admin')
def admin_panel():
    # Check if user is admin
    if 'user' not in session or session['user'].get('role', 0) <= 1:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index.home'))  # Redirect to a suitable page

    # Fetch users (assuming User is your model)
    users = User.query.all()
    locations = Location.query.all()
    items = Item.query.all()

    return render_template('admin.html', users=users, locations = locations, items = items)

# Admin API
def validateAuthorisedRequest():
    if 'user' not in session or session['user'].get('role', 0) <= 1:
        flash('You do not have permission to do this!', 'danger')
        return redirect(url_for('index.home'))
    return False

@blueprint.route("/admin/delete_user/<int:user_id>", methods = ["post"])
def delete_user(user_id):
    shouldRedirect = validateAuthorisedRequest()
    if shouldRedirect:
        return shouldRedirect
    
    targetDelete = User.query.filter_by(id = user_id).first()
    if not targetDelete:
        flash("Failed to locate the account!")
    else:
        if targetDelete.role > 2:
            flash("Cannot delete a superadmin!")
        else:
            targetDelete.delete()
            flash("The account has been removed.")
    return redirect(url_for("admin.admin_panel"))


@blueprint.route("/admin/make_staff/<int:user_id>", methods = ["post"])
def make_staff(user_id):
    shouldRedirect = validateAuthorisedRequest()
    if shouldRedirect:
        return shouldRedirect
    
    targetUser = User.query.filter_by(id = user_id).first()
    if not targetUser:
        flash("Failed to locate the account!")
    else:
        if targetUser.role > 2:
            flash("Cannot demote a superadmin!")
        else:
            targetUser.role = 1
            db.session.commit()
            flash("Successfully assigned role.")

    return redirect(url_for("admin.admin_panel"))

@blueprint.route("/admin/make_admin/<int:user_id>", methods = ["post"])
def make_admin(user_id):
    shouldRedirect = validateAuthorisedRequest()
    if shouldRedirect:
        return shouldRedirect
    
    targetUser = User.query.filter_by(id = user_id).first()
    if not targetUser:
        flash("Failed to locate the account!")
    else:
        if targetUser.role > 2:
            flash("Cannot demote a superadmin!")
        else:
            targetUser.role = 2
            db.session.commit()
            flash("Successfully assigned role.")

    return redirect(url_for("admin.admin_panel"))

@blueprint.route("/admin/remove_claim/<item_id>", methods = ["post"])
def remove_claim(item_id):
    shouldRedirect = validateAuthorisedRequest()
    targetItem = Item.query.filter_by(id = item_id).first()
    if shouldRedirect:
        if targetItem.claimed != session["user"]["id"]:
            flash("Unauthorised!")
            return redirect(url_for("index.home"))

    if not targetItem:
        flash("Failed to locate the item!")
    else:
        targetItem.claimed = None
        db.session.commit()
        flash("Claim removed.")

    return redirect(request.referrer or url_for("index.home"))

@blueprint.route("/admin/delete_location/<location_id>", methods = ["post"])
def delete_location(location_id):
    shouldRedirect = validateAuthorisedRequest()
    if shouldRedirect:
        return shouldRedirect
    
    targetLocation = Location.query.filter_by(id = location_id).first()
    if not targetLocation:
        flash("Failed to locate the location!")
    else:
        targetLocation.delete()
        flash("Location removed.")

    return redirect(url_for("admin.admin_panel"))