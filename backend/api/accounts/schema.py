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


class UpdateUserSchema(Schema):
    password = fields.Str(required=False)
    confirmation = fields.Str(required=False)
    name = fields.Str(required=False, allow_none=True)
    email = fields.Str(required=False)
    active = fields.Bool(required=False)
    activated_at = fields.Str(required=False)
    id = fields.Number(required=False)
    role = fields.Str(required=False)


class ContactSchema(Schema):
    email = fields.Str(required=True)
    message = fields.Str(required=True)
    subject = fields.Str(required=True)
