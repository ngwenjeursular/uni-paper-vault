from app.models.base import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from app import db
from sqlalchemy.orm import relationship

class Paper(BaseModel, db.Model):
    """
    paper model
    """
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_name = Column(String(1000), nullable=False)
    year_id = Column(Integer, ForeignKey('years.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    latex_content = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)

    questions = relationship('Question', backref='paper', lazy=True)


    def __init__(self, paper_name, year_id, semester_id, unit_id, latex_content=None, pdf_path=None):
        """
        constructor class
        """
        self.paper_name = paper_name
        self.year_id = year_id
        self.semester_id = semester_id
        self.unit_id = unit_id
        self.latex_content = latex_content
        self.pdf_path = pdf_path

    def __repr__(self):
        """
        Returns a string representation of the Paper object
        """
        return f'<paper: {self.paper_name}>'
    
    def __str__(self):
        """
        Returns a string representation of the Paper object
        """
        return self.paper_name
    
    def to_dict(self):
        """
        Dict representation
        """
        return {
            'id' : self.id,
            'paper_name': self.paper_name,
            'year_id': self.year_id,
            'semester_id': self.semester_id,
            'unit_id': self.unit_id,
            'latex_content': self.latex_content,
			'pdf_path': self.pdf_path
        }