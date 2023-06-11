from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from src.config import SQLALCHEMY_DATABASE_URI


Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
DBSession = scoped_session(sessionmaker(bind=engine))
