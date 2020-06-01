from datetime import datetime, timedelta
from backend.db import session
from backend import config
from backend.common.errors import Http400Error, Http404Error
from backend.db.models.purchase import Purchase
from backend.db.models.document import Document
from backend.common import s3
from backend.common.logger import logger


def get_purchase(purchase_id=None, payment_id=None):
    if not purchase_id and not payment_id:
        raise Http400Error('Either purchase ID or payment Id must be provided')

    query = session.query(Purchase)

    if purchase_id:
        query = query.filter_by(id=purchase_id)
    else:
        query = query.filter_by(payment_id=payment_id)

    try:
        return query.one()
    except Exception:
        raise Http404Error(f'Purchase not found')


def create_purchase(
    document_id,
    user_id,
    expires_in=config.DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC,
    payment_status=None,
    payment_id=None,
    payment_data=None
):

    document = session.query(Document).get(document_id)

    if not document:
        raise Http404Error('Document not found')

    purchase = Purchase()
    purchase.download_url = s3.generate_presigned_url(document.url, expires_in)

    now = datetime.now()

    purchase.document_id = document_id
    purchase.user_id = user_id

    if expires_in:
        purchase.purchased_at = now
        purchase.valid_until = now + timedelta(seconds=expires_in)

    purchase.payment_status = payment_status or 'create_by_admin'
    purchase.payment_id = payment_id
    purchase.payment_data = payment_data

    session.add(purchase)
    session.commit()

    return purchase


def activate_purchase(purchase_id, expires_in=config.DOCUMENT_DOWNLOAD_EXPIRATION_TIME_SEC, payment_status=None):
    purchase = get_purchase(purchase_id=purchase_id)

    if purchase.purchased_at and purchase.valid_until:
        logger.warn(f"Purchase {purchase_id} already activated, skip")
        return purchase

    document = session.query(Document).get(purchase.document_id)

    purchase.download_url = s3.generate_presigned_url(document.url, expires_in)
    now = datetime.now()

    purchase.purchased_at = now
    purchase.valid_until = now + timedelta(seconds=expires_in)

    if payment_status:
        purchase.payment_status = payment_status

    session.commit()

    return purchase


def fail_purchase(purchase_id):
    purchase = get_purchase(purchase_id=purchase_id)

    if purchase.purchased_at and purchase.valid_until:
        logger.warn(f"Purchase {purchase_id} already activated, skip")
        return purchase

    purchase.payment_status = 'failed'
    session.commit()

    return False
