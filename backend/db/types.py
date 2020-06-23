from sqlalchemy.types import TypeDecorator, CHAR
import uuid


def to_uuid(value):
    UUID_LENGTH = 32

    if isinstance(value, uuid.UUID):
        return value
    elif len(value) > UUID_LENGTH:
        value = value[:UUID_LENGTH]
    elif len(value) < UUID_LENGTH:
        value = value.zfill(UUID_LENGTH)

    return uuid.UUID(value)


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            return to_uuid(value).hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = to_uuid(value)
            return value
