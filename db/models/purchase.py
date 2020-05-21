from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from backend.db import Base
from backend.db.types import GUID


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, nullable=False)
    purchased_at = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    download_url = Column(String(300), nullable=True)

    document_id = Column(GUID, ForeignKey('documents.id'))
    document = relationship('Document', backref="purchases")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref="purchases")

    payment_id = Column(String(100), nullable=True)
    payment_status = Column(String(50), nullable=True)
    payment_data = Column(JSON, nullable=True)

    def __str__(self):
        return f'<Purchase {self.document_id} by {self.user_id}, valid until {self.valid_until}>'

    def to_json(self, short=True):
        data = {
            'id': self.id,
            'purchased_at': self.purchased_at,
            'valid_until': self.valid_until,
            'download_url': self.download_url,
            'document_id': self.document_id,
            'user_id': self.user_id,
        }

        if not short:
            data['payment_id'] = self.payment_id,
            data['payment_status'] = self.payment_status,
            data['payment_data'] = self.payment_data

        return data
