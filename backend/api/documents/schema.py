from marshmallow import Schema, fields


class DocumentCreateSchema(Schema):
    price = fields.Number(required=False, allow_none=True)
    title = fields.Str(required=True)
    organization = fields.Str(required=False, allow_none=True)
    department = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)


class DocumentUpdateSchema(Schema):
    id = fields.Str(required=True)
    price = fields.Number(required=True)
    url = fields.Str(required=False, allow_none=True)
    title = fields.Str(required=False, allow_none=True)
    organization = fields.Str(required=False, allow_none=True)
    department = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    text = fields.Str(required=False, allow_none=True)


class DocumentGrantSchema(Schema):
    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    expires_in = fields.Int(required=True)
    notify_user = fields.Boolean(required=False, allow_none=True)


class DocumentSearchSchema(Schema):
    query = fields.Str(required=True)
    title = fields.Str(required=False, allow_none=True)
    organization = fields.Str(required=False, allow_none=True)
    department = fields.Str(required=False, allow_none=True)
    text = fields.Str(required=False, allow_none=True)
    page = fields.Int(required=False, allow_none=True, default=0)
    page_size = fields.Int(required=False, allow_none=True, default=10)
