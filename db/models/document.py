from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TEXT
from backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    organization = Column(String(500), unique=True, nullable=False)
    text = Column(TEXT(2048))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __str__(self):
        return f'<User {self.name} ({self.email})>'
