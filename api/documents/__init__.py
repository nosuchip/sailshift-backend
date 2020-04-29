import os
from flask import Blueprint, request
from backend.common.decorators import validate_schema, admin_required, login_required
from backend.api.documents.schema import DocumentCreateSchema, DocumentUpdateSchema
from backend.api.documents import document_controller as controller
from backend.common.errors import Http404Error
from backend.common import s3
from backend.db.models.download import Document
from backend.db import session

blueprint = Blueprint('documents', __name__, url_prefix='/documents')


@blueprint.route('/admin/upload', methods=['POST'])
@admin_required
@validate_schema(DocumentCreateSchema, lambda req: req.form)
def admin_upload_document(params):
    print("Form:", request.form)
    print("Files:", request.files)
    print("Params:", params)

    temp_file_path, uploaded_file_url = controller.upload_file_to_s3(request.files['file'])
    excerpt_title, excerpt_text = controller.make_document_excerpt(temp_file_path)
    document = controller.create_document(
        params['name'],
        params['organization'],
        params['description'],
        uploaded_file_url,
        excerpt_text,
        excerpt_title
    )

    os.unlink(temp_file_path)

    return {'document': {
        'title': document.title,
        'organization': document.organization,
        'description': document.description,
        'text': document.text,
        'url': document.url,
    }}


@blueprint.route('/admin/<document_id>', methods=['PUT'])
@validate_schema(DocumentUpdateSchema)
def admin_update_documents(document_id, params):
    document = Document.query.get(document_id)

    if not document:
        raise Http404Error('Document not found')

    if params.get('name'):
        document.name = params.get('name')

    if params.get('organization'):
        document.organization = params.get('organization')

    if params.get('description'):
        document.description = params.get('description')

    if params.get('text'):
        document.text = params.get('text')

    session.commit()

    return document


@blueprint.route('/admin/<document_id>', methods=['DELETE'])
def admin_delete_documents(document_id):
    document = Document.query.get(document_id)

    if not document:
        raise Http404Error('Document not found')

    try:
        s3.delete_file(document.url)
        document.delete()
    finally:
        session.commit()

    return {}


@blueprint.route('/admin/download/<document_id', methods=['GET'])
@admin_required
def admin_download(params):
    pass


@blueprint.route('/admin/grant', methods=['POST'])
@admin_required
def admin_grant_document_download(params):
    pass


@blueprint.route('/dowload/<download_token>', methods=['GET'])
@login_required
def donwload(download_token):
    pass


@blueprint.route('/', methods=['GET'])
def list_documents():
    # pageNo
    pass
