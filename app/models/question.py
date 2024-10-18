from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime



class Question(BaseModel, db.Model):
	"""
	Question model
	"""
	__tablename__ = 'questions'

	id = Column(Integer, primary_key=True, autoincrement=True)
	content = Column(String, nullable=False)
	unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

	answers = relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")

	# Relationship to User
	#author = db.relationship('User', back_populates='questions')
	user = relationship('User', back_populates='questions')

	def __init__(self, content, unit_id, user_id):
		"""
		Constructor class
		"""
		print("question model loaded 4")

		self.content = content
		self.unit_id = unit_id
		self.user_id = user_id
		self.created_at = datetime.utcnow()

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
			'unit_id': self.unit_id,
			'user_id': self.user_id,
			'created_at': self.created_at
		}
