import datetime
from flask import Blueprint, render_template, make_response, request, g
from backend.common.decorators import api_validation, json_response, admin_required, user_required
from backend.api.accounts.schema import (
    LoginSchema,
    RegisterSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    UpdateUserSchema
)
from backend.api.accounts import user_controller
from backend.common.errors import Http400Error, Http404Error, Http401Error
from backend.db import enums
from backend import config
from backend.common import mailer
from backend.common import jwt
from backend.common.logger import logger

blueprint = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@blueprint.route('/login', methods=['POST'])
@api_validation(LoginSchema)
def login(params):
    user = user_controller.get_user(params['email'])

    if not user:
        raise Http404Error(f'User not found by key {params["email"]}')

    if not user.active:
        raise Http401Error(f'User {user.email} deactivated')

    if not user.activated_at:
        raise Http401Error(f'User {user.email} accoutn inactive, please activate account by email')

    user_controller.validate_password(user.password, params['password'])

    return {
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'activated_at': user.activated_at,
            'role': user.role.value if user.role else ''
        },
        'token': user_controller.issue_token(user)
    }


@blueprint.route('/register', methods=['POST'])
@api_validation(RegisterSchema)
def register(params):
    if params['password'] != params['confirmation']:
        raise Http400Error('Password doesn\'t match confirmation')

    user = user_controller.create_user(
        email=params['email'],
        password=params['password'],
        name=params.get('name')
    )

    confirmation_url = config.get_url('verify', user_controller.issue_token(user))

    try:
        mailer.send(
            user.email,
            'email/email_confirmation',
            {'confirmation_url': confirmation_url},
            'Please verify your email'
        )
    except Exception as ex:
        logger.exception(f'Unable to send email to user {user.email}')
        logger.exception(ex)

    return {
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'activated_at': user.activated_at
        }
    }


@blueprint.route('/forgot_password', methods=['POST'])
@api_validation(ForgotPasswordSchema)
def forgot_password(params):
    user = user_controller.get_user(params['email'])
    forgot_password_url = config.get_url('reset_password', user_controller.issue_token(user))

    try:
        mailer.send(
            user.email,
            'email/forgot_password',
            {'forgot_password_url': forgot_password_url},
            'Password restore'
        )
    except Exception as ex:
        logger.exception(f'Unable to send email to user {user.email}')
        logger.exception(ex)

    return {}


@blueprint.route('/reset_password', methods=['POST'])
@api_validation(ResetPasswordSchema)
def reset_password(params):
    if params['password'] != params['confirmation']:
        raise Http400Error('Password must match confirmation')

    payload = jwt.deserialize(params['token'])
    user = user_controller.get_user_by_id(payload['user_id'])

    payload = {
        'password': params['password']
    }

    if not user.activated_at:
        user.activated_at = datetime.datetime.now()

    user_controller.update_user(user, **payload)

    return {}


@blueprint.route('/verify/<token>', methods=['GET'])
def verify_account(token):
    is_xhr = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    try:
        if not token:
            raise Http404Error()

        payload = jwt.deserialize(token)
        user = user_controller.get_user_by_id(payload['user_id'])

        user = user_controller.verify_user(user)

        if not is_xhr:
            return render_template(
                'verify.jinja2',
                message='Your account is activated not. Please ' +
                '<a href="/account/login">login.</a>',
                type='success')

        return make_response({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'activated_at': user.activated_at
            }
        }, 200)
    except Exception as ex:
        print('Verify exception:', ex)
        print('is XHR:', is_xhr)
        if not is_xhr:
            return render_template('verify.jinja2',
                                   message='Token is invalid or already used',
                                   type='error')

        return make_response({'message': 'Token is invalid or already used', 'success': False})


@blueprint.route('/users', methods=['GET'])
@admin_required
def list_users():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('perPage', 10))
    users = user_controller.list_users(page, page_size)

    return {'data': [user.to_json() for user in users]}


@blueprint.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_account(user_id):
    user_controller.delete_user(user_id)

    return {}


@blueprint.route('/<user_id>', methods=['PUT'])
@api_validation(UpdateUserSchema)
@user_required
def update_account(user_id, params):
    user = user_controller.get_user_by_id(user_id)

    if not user:
        raise Http404Error('User not found')

    is_admin = g.user.role.value == enums.UserRoles.Admin.value

    user = user_controller.update_user(user, is_admin, **params)

    return {'user': user.to_json()}
