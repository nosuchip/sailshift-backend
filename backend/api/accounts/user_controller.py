import hashlib
import binascii
import os
import datetime

from backend.db.models.user import User
# from backend.db import get_session
from flask import g
from backend.common.errors import HttpError, Http404Error, Http403Error, Http401Error, Http409Error
from backend.common import jwt
from backend.db import enums
from backend.common.logger import logger


def get_user(email):
    try:
        return g.session.query(User).filter_by(email=email).one()
    except Exception:
        raise Http404Error(f'User "{email}" not found')


def get_user_by_id(user_id):
    try:
        return g.session.query(User).get(user_id)
    except Exception:
        raise Http404Error(f'User not found')


def load_user_from_token(token):
    try:
        payload = jwt.deserialize(token)
        user_id = payload['user_id']

        user = get_user_by_id(user_id)

        if not user:
            raise Http404Error(f'User not found by key {user_id}')

        if not user.active:
            raise Http403Error(f'User {user.email} deactivated')

        if not user.activated_at:
            raise Http401Error(f'User {user.email} accoutn inactive, please activate account by email')

        return user
    except HttpError as ex:
        logger.exception(f'load_user_from_token HttpError error: ${ex.status} ${ex.message}')
        raise ex
    except Exception as ex:
        logger.exception(f'load_user_from_token unhandled error: {ex}')
        raise Http401Error(f'Login required')


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hashed = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    hashed = binascii.hexlify(hashed)
    return (salt + hashed).decode('ascii')


def validate_password(stored_password, password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    hashed = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'),  100000)
    hashed = binascii.hexlify(hashed).decode('ascii')

    if hashed != stored_password:
        raise Http403Error('Password or username incorrect')


def create_user(**kwargs):
    email = kwargs['email']

    count = g.session.query(User).filter_by(email=email).count()

    if count:
        raise Http409Error(f'User with email "{email}"" already exists')

    user = User()

    user.email = kwargs['email']
    user.name = kwargs['name']
    user.active = True
    user.activated_at = None
    user.role = enums.UserRoles.User
    user.password = hash_password(kwargs['password'])

    g.session.add(user)
    g.session.commit()

    return user


def update_user(user, **kwargs):
    if 'name' in kwargs:
        user.name = kwargs['name']

    if 'password' in kwargs:
        user.password = hash_password(kwargs['password'])

    is_admin = kwargs.get('is_admin', None)

    if is_admin:
        if 'role' in kwargs:
            user.role = kwargs['role']

        if 'active' in kwargs:
            user.active = bool(kwargs['active'])

        if 'email' in kwargs:
            user.email = kwargs['email']

    g.session.commit()

    return user


def verify_user(user):
    if not user.active:
        raise Http403Error('User deactivated')

    if user.activated_at:
        raise Http409Error('User already activated')

    user.activated_at = datetime.datetime.now()
    g.session.commit()

    return user


def issue_token(user):
    payload = {'user_id': user.id}
    return jwt.serialize(payload)


def delete_user(user_id):
    g.session.query(User).filter_by(id=user_id).delete()


def list_users(page=0, page_size=10):
    return g.session.query(User).order_by(
        User.id.asc()
    ).limit(page_size).offset(page * page_size).all()
