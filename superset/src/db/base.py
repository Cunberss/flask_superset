from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from superset.src.config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()