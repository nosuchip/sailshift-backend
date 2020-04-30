from marshmallow import Schema, fields


class DocumentCreateSchema(Schema):
    title = fields.Str(required=True)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)


class DocumentUpdateSchema(Schema):
    title = fields.Str(required=False)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)
    text = fields.Str(required=False)


class DocumentGrantSchema(Schema):
    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    expires_in = fields.Int(required=True)
    notify_user = fields.Boolean(required=False)
