#// Globals
from flask import *
from datetime import datetime, timedelta
from models import *
from database import db
import bcrypt

#// Import App
blueprint = Blueprint('account_api', __name__)

@blueprint.route('/delete_account', methods=['POST'])
def delete_account():
    # Check if user is logged in
    if 'user' not in session:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('account.login'))

    # Retrieve user from session
    user_id = session['user']['id']
    user = User.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('account.login'))

    try:
        # Delete the user account
        db.session.delete(user)
        db.session.commit()

        # Clear the session
        session.pop('user', None)
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('account.login'))

    except Exception as e:
        flash(f'An error occurred while deleting your account: {str(e)}', 'danger')
        return redirect(url_for('account.profile'))

@blueprint.route('/logout')
def logout():
    # Clear the session
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index.home'))