from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend import config

engine = create_engine(config.DATABASE_URI, convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
session = db_session()
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from backend.db.models.user import User
    from backend.db.models.document import Document
    from backend.db.models.purchase import Purchase

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        print("Unable to create DB models:")
        print(ex)
