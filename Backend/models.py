'''This file contains the models for the database'''
from . import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    '''Creates User table in DB'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    messages = db.relationship("Message", backref="user")

class Message(db.Model, UserMixin):
    '''Creates Message table in DB'''
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    is_ai = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    session_id = db.Column(db.String(150), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    def __repr__(self):
        return f"Message('{self.content}')"