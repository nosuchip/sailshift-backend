from flask import Blueprint
from backend.api.validators import validate_schema, role_required
from .params import LoginSchema, RegisterSchema, ForgotPasswordSchema

blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')


@blueprint.route('/login', methods=['POST'])
@validate_schema()
@role_required('admimn')
def upload_document(params):
    return {"message": params}


@blueprint.route('/register', methods=['POST'])
@validate_schema(RegisterSchema)
def register(params):
    return {"message": params}


@blueprint.route('/forgot_password', methods=['POST'])
@validate_schema(ForgotPasswordSchema)
def forgot_password(params):
    return {"message": params}


@blueprint.route('/reset_password', methods=['POST'])
@validate_schema(ForgotPasswordSchema)
def reset_password(params):
    return {"message": params}
