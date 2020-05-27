from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import TEXT
from backend.db import Base


class Prerender(Base):
    __tablename__ = 'prerenders'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False, unique=True, index=True)
    path = Column(String(500), nullable=False, unique=True, index=True)
    html = Column(TEXT(2048))

    def __str__(self):
        return f'<Prerender {self.title}>'
