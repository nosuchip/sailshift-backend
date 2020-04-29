from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend import config

engine = create_engine(config.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from backend.db.models.user import User

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        print("Unable to create DB models:")
        print(ex)
