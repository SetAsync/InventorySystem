#// Globals
from flask import *

import config
from database import db
from models import *

#// Create App
app = Flask(__name__)

#// Handle Configs
app.secret_key = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME

#// Database
db.init_app(app)

#// Routes / App
from route import index
from route import account
from route import account_api
from route import admin
from route import inventory

app.register_blueprint(index.blueprint)
app.register_blueprint(account.blueprint)
app.register_blueprint(account_api.blueprint)
app.register_blueprint(admin.blueprint)
app.register_blueprint(inventory.blueprint)

#// Context Processors
@app.context_processor
def inject_admin():
    admin = False
    if 'user' in session and session['user'].get('role', 0) > 1:
        admin = True
    return dict(admin=admin)

#// Start App

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(email='admin@setasync.me').first()
        if not admin:
            import bcrypt
            default_password = 'admin'
            hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
            # Create the admin user
            admin = User(
                name='Admin',
                email='admin@setasync.me',
                password=hashed_password,
                role=3
            )

            # Add admin to the database
            db.session.add(admin)
            db.session.commit()
            print("Default admin account created.")

    app.run(debug=True)