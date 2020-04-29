from flask import Blueprint
from backend.common.decorators import api_validation, json_response
from backend.api.accounts.schema import LoginSchema, RegisterSchema, ForgotPasswordSchema
from backend.api.accounts import user_controller as controller
from backend.common.errors import Http400Error, Http404Error, Http401Error
from backend import config
from backend.common import mailer
from backend.common import jwt

blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')


@blueprint.route('/login', methods=['POST'])
@api_validation(LoginSchema)
def login(params):
    user = controller.get_user(params['email'])

    if not user:
        raise Http404Error(f'User not found by key {user_id}')

    if not user.active:
        raise Http401Error(f'User {user.email} deactivated')

    if not user.activated_at:
        raise Http401Error(f'User {user.email} accoutn inactive, please activate account by email')

    controller.validate_password(user.password, params['password'])

    return {
        'user': {
            'id': user.id,
            'name': user.name,
            'activated_at': user.activated_at
        },
        'token': controller.issue_token(user)
    }


@blueprint.route('/register', methods=['POST'])
@api_validation(RegisterSchema)
def register(params):
    if params['password'] != params['confirmation']:
        raise Http400Error('Password doesn\'t match confirmation')

    user = controller.create_user(
        email=params['email'],
        password=params['password'],
        name=params['name']
    )

    confirmation_url = config.get_url('verify', controller.issue_token(user))

    try:
        mailer.send(
            user.email,
            'email/email_confirmation',
            {'confirmation_url': confirmation_url},
            'Please verify your email'
        )
    except Exception as ex:
        print(f'Unable to send email to user {user.email}:', ex)

    return {
        'user': {
            'id': user.id,
            'name': user.name,
            'activated_at': user.activated_at
        }
    }


@blueprint.route('/forgot_password', methods=['POST'])
@api_validation(ForgotPasswordSchema)
def forgot_password(params):
    return {"message": params}


@blueprint.route('/reset_password', methods=['POST'])
@api_validation(ForgotPasswordSchema)
def reset_password(params):
    return {"message": params}


@blueprint.route('/verify/<token>', methods=['GET'])
@json_response
def verify_account(token):
    if not token:
        raise Http404Error()

    payload = jwt.deserialize(token)
    user = controller.get_user_by_id(payload['user_id'])

    user = controller.activate_user(user)

    return {
        'user': {
            'id': user.id,
            'name': user.name,
            'activated_at': user.activated_at
        }
    }
