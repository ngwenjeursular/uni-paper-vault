from app.models.base import BaseModel
from app import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(BaseModel, UserMixin, db.Model):
    """
    User model for managing user information
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    #password_hash = Column(String(128), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = relationship('Answer', backref='user', lazy=True)

    def __init__(self, username, email, password):
        """
        Constructor class
        """
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        """
        This method is used to hash the password before storing it
        """
        self.password = generate_password_hash(password)


    def check_password(self, password):
        """
        Check hashed password
        """
        return check_password_hash(self.password, password)
    

    def __repr__(self):
        """
        String representation
        """
        return f'<User {self.username}>'

    def to_dict(self):
        """
        Dict representation
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    