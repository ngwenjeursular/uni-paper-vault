from app.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from app import db


class Unit(BaseModel, db.Model):
    """
    Units class
    """
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_name = Column(String(50), nullable=False)
    year_id = Column(Integer, ForeignKey('years.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)
    description = Column(String(255), nullable=True)


    def __init__(self, unit_name, year_id, semester_id, description):
        """
        constructor class
        """
        self.unit_name = unit_name
        self.year_id = year_id
        self.semester_id = semester_id
        self.description = description


    def to_dict(self):
        """
        dict representation
        """
        return {
            'id': self.id,
            'unit_name': self.unit_name,
            'year_id': self.year_id,
            'semester_id': self.semester_id,
            'description': self.description
        }
