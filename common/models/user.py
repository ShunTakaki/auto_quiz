from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mail = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64))
    pass_hash = db.Column(db.String(128))

    def set_pass(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.pass_hash, password)