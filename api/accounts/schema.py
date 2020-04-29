from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    confirmation = fields.Str(required=True)
    name = fields.Str(required=False)


class ForgotPasswordSchema(Schema):
    email = fields.Str(required=True)


class ResetPasswordSchema(Schema):
    password = fields.Str(required=True)
    confirmation = fields.Str(required=True)
    token = fields.Str(required=True)
