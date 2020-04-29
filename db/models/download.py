import uuid
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db import Base


class Download(Base):
    __tablename__ = 'downloads'

    uuid = Column(BINARY(16), primary_key=True, nullable=False, default=uuid.uuid4)
    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Document', backref="downloads")
    expires_at = Column(DateTime, nullable=False)

    def __str__(self):
        return f'<Download {self.uuid} {self.document_id} {self.expires_at}>'
