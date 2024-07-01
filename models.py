from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, email, password, role=0):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    claimed = db.Column(db.Integer, nullable = True)
    location_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name, claimed=None, location_id=None):
        self.name = name
        self.claimed = claimed
        self.location_id = location_id

    def delete(self):
        db.session.delete(self)
        db.session.commit()