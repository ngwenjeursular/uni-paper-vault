from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Question(BaseModel, db.Model):
	"""
	Question model
	"""
	__tablename__ = 'questions'

	id = Column(Integer, primary_key=True, autoincrement=True)
	content = Column(String, nullable=False)
	paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False)

	answers = relationship('Answer', backref='question', lazy=True)

	def __init__(self, content, paper_id):
		"""
		Constructor class
		"""
		self.content = content
		self.paper_id = paper_id

	def __repr__(self):
		"""
		Returns a string representation of the Question object
		"""
		return f'<Question: {self.content[:20]}>'

	def __str__(self):
		"""
		Returns a string representation of the Question object
		"""
		return self.content

	def to_dict(self):
		"""
		Dict representation
		"""
		return {
			'id': self.id,
			'content': self.content,
			'paper_id': self.paper_id
		}
