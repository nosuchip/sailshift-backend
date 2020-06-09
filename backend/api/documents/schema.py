from marshmallow import Schema, fields


class DocumentCreateSchema(Schema):
    price = fields.Number(required=False)
    title = fields.Str(required=True)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)


class DocumentUpdateSchema(Schema):
    id = fields.Str(required=True)
    price = fields.Number(required=True)
    url = fields.Str(required=False)
    title = fields.Str(required=False)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)
    text = fields.Str(required=False)


class DocumentGrantSchema(Schema):
    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    expires_in = fields.Int(required=True)
    notify_user = fields.Boolean(required=False)


class DocumentSearchSchema(Schema):
    query = fields.Str(required=True)
    title = fields.Str(required=False)
    organization = fields.Str(required=False)
    department = fields.Str(required=False)
    text = fields.Str(required=False)
    page = fields.Int(required=False, default=0)
    page_size = fields.Int(required=False, default=10)
