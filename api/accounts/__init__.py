from flask import Blueprint
from backend.common.decorators import api_validation
from backend.api.accounts.schema import LoginSchema, RegisterSchema, ForgotPasswordSchema

blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')


@blueprint.route('/login', methods=['POST'])
@api_validation(LoginSchema)
def login(params):
    return {"message": params}


@blueprint.route('/register', methods=['POST'])
@api_validation(RegisterSchema)
def register(params):
    return {"message": params}


@blueprint.route('/forgot_password', methods=['POST'])
@api_validation(ForgotPasswordSchema)
def forgot_password(params):
    return {"message": params}


@blueprint.route('/reset_password', methods=['POST'])
@api_validation(ForgotPasswordSchema)
def reset_password(params):
    return {"message": params}
