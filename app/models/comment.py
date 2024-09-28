from app.models.base import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime

class Comment(BaseModel, db.Model):
    """
    Comment model to store comments on answers
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False)
    created_at = Column(db.DateTime, default=datetime.utcnow)
    

    def __init__(self, content, user_id, answer_id):
        """
        Constructor for Comment model
        """
        self.content = content
        self.user_id = user_id
        self.answer_id = answer_id

    def __repr__(self):
        """
        String representation of the comment
        """
        return f'<Comment {self.content[:20]}>'

    def to_dict(self):
        """
        Dictionary representation of the comment
        """
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'answer_id': self.answer_id,
            'created_at': self.created_at
        }
