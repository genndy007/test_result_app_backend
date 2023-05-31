from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models import Base


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    name = Column(String)
    description = Column(String)

    user = relationship('User', uselist=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    active_project_id = Column(Integer, nullable=True)
    first_name = Column(String)
    last_name = Column(String)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
