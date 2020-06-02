import os.path
import uuid
import math
from sqlalchemy import and_, or_, func
from datetime import datetime
from backend.common import s3
from backend import config
from backend.db.models.document import Document
from backend.db.models.purchase import Purchase
from backend.db import session
from backend.common.parsers import pdf
from backend.common.errors import Http404Error, Http410Error


def get_document(document_id):
    try:
        return session.query(Document).get(document_id)
    except Exception:
        raise Http404Error('Document not found')


def create_document(
    name,
    organization,
    description,
    uploaded_file_url,
    excerpt_text,
    excerpt_title=None,
):
    document = Document()
    document.title = name
    document.organization = organization
    document.description = description
    document.text = '\n'.join(excerpt_text)
    document.url = uploaded_file_url

    session.add(document)
    session.commit()

    return document


def update_document(document, **kwargs):
    if kwargs.get('title'):
        document.title = kwargs.get('title')

    if kwargs.get('organization'):
        document.organization = kwargs.get('organization')

    if kwargs.get('description'):
        document.description = kwargs.get('description')

    if kwargs.get('text'):
        document.text = kwargs.get('text')

    session.commit()

    return document


def upload_file_to_s3(file):
    file_ext = os.path.splitext(file.filename)
    file_name = uuid.uuid4().hex + file_ext[1]
    file_path = os.path.join('/tmp', file_name)
    file.save(file_path)

    file_url = s3.upload_file(file_path, file_name)

    return file_path, file_url


def make_document_excerpt(file_path):
    lines = pdf.parse(file_path, lines_to_return=config.EXCERPTS_LINES_COUNT)

    return '', lines


def generate_expireable_document_url(document_id=None, document=None, expires_in=None):
    if not document:
        document = get_document(document_id)

        if not document:
            raise Http404Error('Document not found')

    return s3.generate_presigned_url(document.url, expires_in)


def get_user_document_purchase(user, document, raise_on_missing=True):
    try:
        purchase = session.query(Purchase).filter_by(
            user_id=user.id,
            document_id=document.id
        ).one()
    except Exception:
        if raise_on_missing:
            raise Http404Error('Document not found in user\'s purchase')
        else:
            return None

    if not purchase or not purchase.valid_until:
        if raise_on_missing:
            raise Http404Error('Document not found in user\'s purchase')
        else:
            return None

    if purchase.valid_until < datetime.now():
        if raise_on_missing:
            raise Http410Error('Purchased document expired. Please purchase again.')
        else:
            return None

    return purchase


def list_documents(page=0, page_size=10):
    documents = session.query(Document).order_by(Document.rank.desc()).limit(page_size).offset(page*page_size).all()
    return documents


def list_past_user_documents(user, page=0, page_size=10):
    now = datetime.now()

    pairs = session.query(Document, Purchase).filter(
        Document.purchases.any(and_(Purchase.user_id == user.id, Purchase.valid_until < now))
    ).filter(
        Purchase.document_id == Document.id
    ).filter(
        Purchase.payment_status == 'success'
    ).limit(page_size).offset(page*page_size).all()

    results = []

    for doc, purchase in pairs:
        data = purchase.to_json()
        data['document'] = doc.to_json(short=True)

        results.append(data)

    return results


def list_actual_user_documents(user, page=0, page_size=10):
    now = datetime.now()

    pairs = session.query(Document, Purchase).filter(
        Document.purchases.any(and_(Purchase.user_id == user.id, Purchase.valid_until >= now))
    ).filter(
        Purchase.document_id == Document.id
    ).filter(
        Purchase.payment_status == 'success'
    ).limit(page_size).offset(page*page_size).all()

    results = []

    for doc, purchase in pairs:
        data = purchase.to_json()
        data['document'] = doc.to_json(short=True)

        results.append(data)

    return results


def search_documents(query, title=None, organization=None, department=None, text=None, page=None, page_size=None):
    page = page or 0
    page_size = page_size or 10
    count = 0
    documents = []

    if query:
        filter_clause = or_(
            Document.title.ilike(f'%{query}%'),
            Document.organization.ilike(f'%{query}%'),
            Document.text.ilike(f'%{query}%')
        )

        count = (
            session
            .query(func.count(Document.id))
            .filter(filter_clause)
            .scalar()
        )

        documents = (
            session
            .query(Document)
            .filter(filter_clause)
            .order_by(Document.rank.desc())
            .limit(page_size)
            .offset(page*page_size)
            .all()
        )

    pagination = {
        'total': count,
        'pages': math.ceil(count / page_size),
        'page': page
    }

    return documents, pagination


def get_popular_documents(count=5):
    documents = session.query(Document).order_by(Document.rank.desc()).limit(count).all()
    return documents


def delete_document(document):
    session.delete(document)
    session.commit()
