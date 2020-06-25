import os.path
import uuid
import math
from flask import g
from sqlalchemy import and_, or_, and_, func
from datetime import datetime
from backend.common import s3
from backend import config
from backend.db.models.document import Document
from backend.db.models.purchase import Purchase
from backend.common.parsers import pdf
from backend.common.errors import Http404Error, Http410Error
from backend.common.logger import logger


def get_document(document_id):
    try:
        return g.session.query(Document).get(document_id)
    except Exception:
        raise Http404Error('Document not found')


def create_document(
    name,
    organization,
    department,
    description,
    uploaded_file_url,
    excerpt_text,
    excerpt_title=None,
):
    document = Document()
    document.title = name
    document.organization = organization
    document.department = department
    document.description = description
    document.text = '\n'.join(excerpt_text)
    document.url = uploaded_file_url

    g.session.add(document)
    g.session.commit()

    return document


def update_document(document, **kwargs):
    if kwargs.get('title'):
        document.title = kwargs.get('title')

    if kwargs.get('organization'):
        document.organization = kwargs.get('organization')

    if kwargs.get('department'):
        document.department = kwargs.get('department')

    if kwargs.get('description'):
        document.description = kwargs.get('description')

    if kwargs.get('text'):
        document.text = kwargs.get('text')

    g.session.commit()

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
        purchase = g.session.query(Purchase).filter_by(
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
    return g.session.query(Document).order_by(
        Document.rank.desc()
    ).limit(page_size).offset(page * page_size).all()


def list_past_user_documents(user, page=0, page_size=10):
    now = datetime.now()

    pairs = g.session.query(Document, Purchase).filter(
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

    pairs = g.session.query(Document, Purchase).filter(
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
        or_filters = [
            Document.title.ilike(f'%{query}%'),
            Document.text.ilike(f'%{query}%')
        ]

        and_filters = []

        if organization:
            and_filters.append(Document.organization.ilike(f'%{organization}%'))
        else:
            or_filters.append(Document.organization.ilike(f'%{query}%'))

        if department:
            and_filters.append(Document.department.ilike(f'%{department}%'))
        else:
            or_filters.append(Document.department.ilike(f'%{query}%'))

        and_filters.append(or_(*or_filters))
        filter_clause = and_(and_filters)

        count = (
            g.session
            .query(func.count(Document.id))
            .filter(filter_clause)
            .scalar()
        )

        documents = (
            g.session
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
    try:
        return g.session.query(Document).order_by(Document.rank.desc()).limit(count).all()
    except Exception as ex:
        logger.exception(f'get_popular_documents error: {ex}')

    return []


def delete_document(document):
    g.session.query(Document).filter_by(id=document.id).delete()
