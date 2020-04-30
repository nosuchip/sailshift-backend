from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db import Base
from backend.db.types import GUID


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, nullable=False)
    payment_status = Column(String(50), nullable=True)
    purchased_at = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    download_url = Column(String(300), nullable=True)

    document_id = Column(GUID, ForeignKey('documents.id'))
    document = relationship('Document', backref="purchases")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref="purchases")

    def __str__(self):
        return f'<Purchase {self.document_id} by {self.user_id}, valid until {self.valid_until}>'
