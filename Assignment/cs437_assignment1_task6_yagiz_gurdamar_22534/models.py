from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    age = db.Column(db.Integer)

    def get_id(self):
        return (self.id)

    def __repr__(self):
        return f'<User {self.username}>'
