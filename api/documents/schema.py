from marshmallow import Schema, fields


class DocumentCreateSchema(Schema):
    name = fields.Str(required=True)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)


class DocumentUpdateSchema(Schema):
    name = fields.Str(required=False)
    organization = fields.Str(required=False)
    description = fields.Str(required=False)
    text = fields.Str(required=False)
