from app import db
from datetime import datetime
from flask_login import UserMixin
from app import bcrypt

class User(db.Model, UserMixin):


    def __init__(self, username, email, password, admin):
        self.username=username
        self.email=email
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')
        self.admin = admin


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    about_me = db.Column(db.String(400),  nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, server_default='default.jpg')
    admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.admin

    def veryfy_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
