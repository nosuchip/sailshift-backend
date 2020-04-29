import os.path
import uuid
from backend.common import s3
from backend import config
from backend.db.models.document import Document
from backend.db import session
from backend.common.parsers import pdf


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


def update_document():
    pass


def upload_file_to_s3(file):
    file_ext = os.path.splitext(file.filename)
    file_name = uuid.uuid4().hex + file_ext[1]
    file_path = os.path.join('/tmp', file_name)
    file.save(file_path)

    file_url = s3.upload_file(file_path, config.AWS_S3_BUCKET, file_name)

    return file_path, file_url


def make_document_excerpt(file_path):
    lines = pdf.parse(file_path, lines_to_return=config.EXCERPTS_LINES_COUNT)

    return '', lines
