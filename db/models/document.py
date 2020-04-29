from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TEXT
from backend.db import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    organization = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    text = Column(TEXT(2048))
    url = Column(String(500), nullable=False, unique=True)

    def __str__(self):
        return f'<Document {self.title}>'
