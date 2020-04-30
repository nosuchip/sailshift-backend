from datetime import datetime, timedelta
from backend.db import session
from backend import config
from backend.db.models.purchase import Purchase
from backend.db.models.document import Document

from backend.common import s3
from backend.common.errors import Http404Error


def create_purchase(document_id, user_id, expires_in=config.DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC):

    document = session.query(Document).get(document_id)

    if not document:
        raise Http404Error('Document not found')

    purchase = Purchase()
    purchase.download_url = s3.generate_presigned_url(document.url, expires_in)

    now = datetime.now()

    purchase.payment_status = 'create_by_admin'
    purchase.purchased_at = now
    purchase.valid_until = now + timedelta(seconds=expires_in)
    purchase.document_id = document_id
    purchase.user_id = user_id

    session.add(purchase)
    session.commit()

    return purchase
