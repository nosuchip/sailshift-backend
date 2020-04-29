import traceback
from functools import wraps
from flask import make_response, request, session
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from backend.common.errors import HttpError, Http403Error
from backend.api.accounts.user_controller import load_user_from_token
from backend import config
from backend.db import enums


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
            payload = res
        except HttpError as ex:
            print("json_response HttpError:", ex)
            traceback.print_exc()
            status = ex.status
            payload = {'error': ex.message, 'data': ex.payload or {}}
        except BadRequest as ex:
            print("json_response BadRequest:", ex)
            traceback.print_exc()
            status = 400
            payload = {'error': 'Malformed payload'}
        except Exception as ex:
            print("json_response Exception:", ex)
            traceback.print_exc()
            payload = {'error': 'Server error'}
            status = 500

        print("json_response ok", status, payload)

        return make_response(payload, status)
    return wrapper


def validate_schema(marshmallow_schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            status = 200
            payload = {}

            try:
                params = marshmallow_schema().load(request.json)
                return f(*args, **kwargs, params=params)
            except ValidationError as ex:
                print("validate_schema ValidationError:", ex)
                status = 400
                payload = {'error': 'Field validation failed', 'validation_errors': ex.messages}

            return payload, status

        return wrapper
    return decorator


def login_required(fn):
    authorization = request.headers.get('Authorization')

    token_type, token = authorization.split(' ')

    if token_type != config.AUTH_TOKEN_TYPE:
        raise Http403Error('Bad authorization token')

    session['user'] = load_user_from_token(token)


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session['user'] or session['user'].role != role:
                raise Http403Error('Insufficient privileges')

            return f(*args, **kwargs)
        return wrapper
    return decorator


def api_validation(schema):
    return apply_decorators(json_response, validate_schema(schema))


def user_required():
    return apply_decorators(json_response, login_required)


def admin_required():
    return apply_decorators(json_response, login_required, role_required(enums.UserRoles.Admin))
