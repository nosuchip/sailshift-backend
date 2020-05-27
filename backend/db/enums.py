import enum


class UserRoles(enum.Enum):
    User = 'user'
    Admin = 'admin'


class Currencies(enum.Enum):
    USD = 'usd'


class PaymentMethods(enum.Enum):
    Card = 'card'
