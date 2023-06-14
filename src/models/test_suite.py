from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.models import Base


class TestSuite(Base):
    __tablename__ = 'test_suite'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    name = Column(String)
    description = Column(String)

    project = relationship('Project', uselist=False)


class TestCaseTestSuite(Base):
    __tablename__ = 'test_case_test_suite'

    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey('test_case.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    test_suite_id = Column(Integer, ForeignKey('test_suite.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    order = Column(Integer)


class TestRun(Base):
    __tablename__ = 'test_run'

    id = Column(Integer, primary_key=True)
    test_suite_id = Column(Integer, ForeignKey('test_suite.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    result = Column(String)
    created = Column(DateTime, server_default=func.now())

    test_suite = relationship('TestSuite', uselist=False)


class TestCaseTestRun(Base):
    __tablename__ = 'test_case_test_run'

    id = Column(Integer, primary_key=True)
    test_run_id = Column(Integer, ForeignKey('test_run.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    test_case_id = Column(Integer, ForeignKey('test_case.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    status = Column(String)
