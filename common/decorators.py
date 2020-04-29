from functools import wraps
from flask import make_response, request, session
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError


def apply_decorators(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def json_response(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        payload, *status = fn(*args, **kwargs)
        status = status[0] if status else 200

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
                print("ValidationError:", ex)
                status = 400
                payload = {'error': 'Field validation failed', 'validation_errors': ex.messages}
            except BadRequest as ex:
                print("BadRequest:", ex)
                status = 400
                payload = {'error': 'Malformed payload'}
            except Exception as ex:
                print("Exception:", ex)
                status = 500
                payload = {'error': 'Server error'}

            return payload, status

        return wrapper
    return decorator


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session['user'] or session['user'].role != role:
                return ({'message': 'Unauthorized'}, 401)

            return f(*args, **kwargs)
        return wrapper
    return decorator


api_validation = lambda schema: apply_decorators(json_response, validate_schema(schema))
