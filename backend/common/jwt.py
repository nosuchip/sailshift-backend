from jwcrypto import jwt, jwk
from jwcrypto.common import json_decode

from backend import config

key = jwk.JWK(**json_decode(config.JWT_KEY))


def serialize(payload):
    signed_token = jwt.JWT(header={"alg": "HS256"}, claims=payload)
    signed_token.make_signed_token(key)
    encrypted_token = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=signed_token.serialize())
    encrypted_token.make_encrypted_token(key)
    return encrypted_token.serialize()


def deserialize(token):
    encrypted_token = jwt.JWT(key=key, jwt=token)
    signed_token = jwt.JWT(key=key, jwt=encrypted_token.claims)
    return json_decode(signed_token.claims)
