from sqlalchemy import Column, Integer, String
from backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    name = Column(String(256))
    role = Column(String(20), nullable=False, default='user')

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __str__(self):
        return f'<User {self.name} ({self.email})>'
