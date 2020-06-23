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


# @contextmanager
def get_session():
    return db_session()
    # _session = db_session()
    # try:
    #     yield _session
    #     _session.commit()
    # except Exception:
    #     _session.rollback()
    #     raise
    # finally:
    #     _session.close()


Base = declarative_base()
Base.query = db_session.query_property()


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



# def query(model_cls):
#     return session.query(model_cls)


# def add(model_instance, commit=True):
#     result = session.add(model_instance)
#     if commit:
#         session.commit()

#     return result


# def delete(model_cls, model_id, commit=True):
#     result = session.query(model_cls).filter_by(id=model_id).delete()
#     if commit:
#         session.commit()

#     return result


# def get_one(model_cls, **filter_by):
#     return session.query(model_cls).filter_by(**filter_by).one()


# def get_by_id(model_cls, model_id):
#     return session.query(model_cls).get(model_id)


# def commit():
#     print("Commiting successful transaction")
#     return session.commit()


# def rollback():
#     print("Rolling back failed transaction")
#     return session.rollback()


# def count(model_cls, **filter_by):
#     return session.query(model_cls).filter_by(**filter_by).count()
