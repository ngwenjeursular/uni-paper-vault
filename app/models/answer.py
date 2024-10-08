from app.models.base import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime
from app.models.user import User


class Answer(BaseModel, db.Model):
	"""
	Answer model
	"""
	__tablename__ = 'answers'

	id = Column(Integer, primary_key=True, autoincrement=True)
	content = Column(String, nullable=False)
	upvotes = Column(Integer, default=0)
	downvotes = Column(Integer, default=0)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

	comments = relationship('Comment', backref='answer', lazy=True)
	comments = relationship('Comment', backref='commented_answer', lazy=True)

	def __init__(self, content, user_id, question_id):
		"""
		Constructor class
		"""
		print("answer model loaded 3")
		self.content = content
		self.user_id = user_id
		self.question_id = question_id

	def __repr__(self):
		"""
		Returns a string representation of the Answer object
		"""
		return f'<Answer: {self.content[:20]}>'

	def to_dict(self):
		"""
		Dict representation
		"""
		return {
			'id': self.id,
			'content': self.content,
			'upvotes': self.upvotes,
			'downvotes': self.downvotes,
			'user_id': self.user_id,
			'question_id': self.question_id
		}
