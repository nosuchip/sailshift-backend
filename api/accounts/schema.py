from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)
    confirmation = fields.Str(required=True)


class ForgotPasswordSchema(Schema):
    email = fields.Str(required=True)


class ResetPasswordSchema(Schema):
    password = fields.Str(required=True)
    confirmation = fields.Str(required=True)
    token = fields.Str(required=True)
