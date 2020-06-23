from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend import config
from backend.common.logger import logger

engine_config = {
    'pool_pre_ping': True,
    'convert_unicode': False,
    'echo': True
}

session_config = {
    'autocommit': False,
    'autoflush': False
}

engine = create_engine(config.DATABASE_URI, **engine_config)

session_factory = sessionmaker(bind=engine, **session_config)
db_session = scoped_session(session_factory)


Base = declarative_base()
Base.query = db_session.query_property()


@contextmanager
def session():
    session = db_session()

    try:
        yield session
    except Exception as ex:
        print('DB session error:')
        print(ex)
        session.rollback()
    else:
        session.commit()


def init_db():
    from backend.db.models.user import User
    from backend.db.models.document import Document
    from backend.db.models.purchase import Purchase
    from backend.db.models.prerender import Prerender

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        logger.exception("Unable to create DB models:")
        logger.exception(ex)
