from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


Base = declarative_base()
DBSession = scoped_session(sessionmaker())
