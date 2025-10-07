from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    borrows = db.relationship('Borrow', backref='user', lazy=True)

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  author = db.Column(db.String(200))
  description = db.Column(db.Text)
  stock = db.Column(db.Integer, default=1)
  borrows = db.relationship('Borrow', backref='book', lazy=True)

    

class Borrow(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
 borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
 returned = db.Column(db.Boolean, default=False)
 returned_at = db.Column(db.DateTime)