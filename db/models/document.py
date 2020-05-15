import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import TEXT
from backend.db import Base
from backend.db.types import GUID


class Document(Base):
    __tablename__ = 'documents'

    id = Column(GUID, primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    organization = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    text = Column(TEXT(2048))
    url = Column(String(500), nullable=False, unique=True)
    rank = Column(Integer, nullable=False, default=0)

    def __str__(self):
        return f'<Document {self.title}>'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'organization': self.organization,
            'description': self.description,
            'text': self.text,
            'url': self.url,
        }
