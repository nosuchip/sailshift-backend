import asyncio
import traceback
from functools import wraps
from flask import make_response, request, g
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from backend.common.errors import HttpError, Http403Error, Http400Error
from backend.api.accounts.user_controller import load_user_from_token
from backend import config
from backend.db import enums
from backend.common.logger import logger


def apply_decorators(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def json_response(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        payload = {'data': {}}
        status = 200

        try:
            res = fn(*args, **kwargs)

            if type(res) == tuple or type(res) == list:
                if len(res) > 1:
                    status = res[1]

                payload = res[0]
            else:
                payload = res
        except HttpError as ex:
            # logger.exception("json_response HttpError:", ex)
            # traceback.print_exc()
            status = ex.status
            payload = {'error': ex.message, 'data': ex.payload or {}}
        except BadRequest as ex:
            logger.exception("json_response BadRequest:", ex)
            traceback.print_exc()
            status = 400
            payload = {'error': 'Malformed payload'}
        except Exception as ex:
            logger.exception("json_response Exception:", ex)
            traceback.print_exc()
            payload = {'error': 'Server error'}
            status = 500

        logger.debug("json_response ok", status, payload)

        return make_response(payload, status)
    return wrapper


def validate_schema(marshmallow_schema, source=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data_to_validate = source(request) if source else request.json
                params = marshmallow_schema().load(data_to_validate or {})
                return f(*args, **kwargs, params=params)
            except ValidationError as ex:
                logger.exception("validate_schema ValidationError:", ex)
                raise Http400Error('Field validation failed', ex.messages)

        return wrapper
    return decorator


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            token_type, token = request.headers.get('Authorization').split(' ')
        except Exception:
            raise Http403Error('Bad authorization token')

        if token_type != config.AUTH_TOKEN_TYPE:
            raise Http403Error('Bad authorization token')

        g.user = load_user_from_token(token)

        return fn(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not g.user or g.user.role != role:
                raise Http403Error('Insufficient privileges')

            return f(*args, **kwargs)
        return wrapper
    return decorator


def api_validation(schema):
    return apply_decorators(json_response, validate_schema(schema))


def user_required(fn):
    return apply_decorators(json_response, login_required)(fn)


def admin_required(fn):
    return apply_decorators(json_response, login_required, role_required(enums.UserRoles.Admin))(fn)


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped
