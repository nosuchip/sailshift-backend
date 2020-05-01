from marshmallow import Schema, fields
from backend.db import enums


class CreatePaymentIntentSchema(Schema):
    document_id = fields.Str(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True, default=enums.Currencies.USD)
    payment_method = fields.Str(required=True, default='card')
