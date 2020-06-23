from functools import wraps
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
session = db_session()


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


def rollback_failed(sess, func_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as ex:
                print(f'db.{func_name} error: {ex}')
                raise ex

        return wrapper
    return decorator


@rollback_failed(session, 'query')
def query(model_cls):
    return session.query(model_cls)


@rollback_failed(session, 'add')
def add(model_instance, commit=True):
    result = session.add(model_instance)
    if commit:
        session.commit()

    return result


@rollback_failed(session, 'delete')
def delete(model_cls, model_id, commit=True):
    result = session.query(model_cls).filter_by(id=model_id).delete()
    if commit:
        session.commit()

    return result


@rollback_failed(session, 'get_one')
def get_one(model_cls, **filter_by):
    return session.query(model_cls).filter_by(**filter_by).one()


@rollback_failed(session, 'get_by_id')
def get_by_id(model_cls, model_id):
    return session.query(model_cls).get(model_id)


@rollback_failed(session, 'commit')
def commit():
    print("Commiting successful transaction")
    return session.commit()


def rollback():
    print("Rolling back failed transaction")
    return session.rollback()


@rollback_failed(session, 'count')
def count(model_cls, **filter_by):
    return session.query(model_cls).filter_by(**filter_by).count()
