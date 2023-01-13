from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

def get_db_sessionmaker(db_uri, **kvargs):
    engine = create_engine(db_uri, **kvargs)
    db_session = sessionmaker(bind=engine)
    db_session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return db_session
