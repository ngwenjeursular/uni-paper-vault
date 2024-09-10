
from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from app.models.year import Year
from app import db


class Semester(BaseModel, db.Model):
    """
    the semester class object
    """
    __tablename__ = 'semesters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sem_number = Column(Integer, nullable=False)
    year_id = Column(Integer, ForeignKey('years.id'), nullable=False)

    units = relationship('Unit', backref='semester', lazy=True)

    def __init__(self, sem_number, year_id):
        """
        constructor class
        """
        self.sem_number = sem_number
        self.year_id = year_id

    def __repr__(self):
        return f'<semester {self.sem_number}>'
    
    def __str__(self):
        return f'<semester {self.sem_number}>'

    def to_dict(self):
        """
        dict representation
        """
        return {
            'id': self.id,
            'sem_number': self.sem_number,
            'year_id': self.year_id
        }