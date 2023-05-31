from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models import Base


class TestCase(Base):
    __tablename__ = 'test_case'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    name = Column(String)
    description = Column(String)
    precondition = Column(String)
    postcondition = Column(String)

    project = relationship('Project', uselist=False)
    test_steps = relationship('TestStep', back_populates='test_case', uselist=True)


class TestStep(Base):
    __tablename__ = 'test_step'

    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey('test_case.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    content = Column(String)
    order = Column(Integer)

    test_case = relationship('TestCase', back_populates='test_steps', uselist=False)







