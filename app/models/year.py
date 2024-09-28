from sqlalchemy import Column, ForeignKey, String, Integer, Text
from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app import db


class Year(BaseModel, db.Model):
    """
    Year category
    """
    __tablename__ = 'years'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)

    semesters = relationship('Semester', backref='year', lazy=True)
    units = relationship('Unit', backref='year', lazy=True)


    def __init__(self, title):
        """
        constructor for the year class
        """
        self.title = title

    def __repr__(self):
        """
        returns a string representation of the year object
        """
        return f'<Year {self.title}>'
    
    def __str__(self):
        """
        returns a string representation of the year object
        """
        return f'{self.title}'
    
    def to_dict(self):
        """
        returns a dict representation of the year class
        """
        return {
            'id': self.id,
            'title': self.title
        }

    
