# create database tables
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(90), nullable=False, unique=True)
    password=db.Column(db.Text, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())
    tasks=db.Relationship('Task', backref='user')
    def __repr__(self) -> str:
        return f'User>>> {self.email}'
    
class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    reminder_time = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    create_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())
    def __repr__(self) -> int:
        return f'Task>>> {self.id}'