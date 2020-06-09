from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from backend.db import Base, enums


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    name = Column(String(256), nullable=True)
    role = Column(Enum(enums.UserRoles), nullable=False, default=enums.UserRoles.User)
    active = Column(Boolean(), nullable=False, default=True)
    activated_at = Column(DateTime(), nullable=True)

    def __str__(self):
        return f'<User {self.name} ({self.email})>'

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'activated_at': self.activated_at,
            'active': self.active,
            'role': self.role.value if self.role else ''
        }
