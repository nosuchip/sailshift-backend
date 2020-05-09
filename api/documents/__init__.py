import os
from flask import Blueprint, request, g
from backend.common.decorators import validate_schema, admin_required, login_required
from backend.api.documents.schema import DocumentCreateSchema, DocumentUpdateSchema, DocumentGrantSchema
from backend.api.documents import document_controller
from backend.api.payments import purchase_controller
from backend.api.accounts import user_controller
from backend.common.errors import Http404Error
from backend.common import s3
from backend.db.models.document import Document
from backend.db import session
from backend.common import mailer


blueprint = Blueprint('documents', __name__, url_prefix='/api/documents')


@blueprint.route('/admin/upload', methods=['POST'])
@admin_required
@validate_schema(DocumentCreateSchema, lambda req: req.form)
def admin_upload_document(params):
    temp_file_path, uploaded_file_url = document_controller.upload_file_to_s3(request.files['file'])
    excerpt_title, excerpt_text = document_controller.make_document_excerpt(temp_file_path)
    document = document_controller.create_document(
        params['title'],
        params['organization'],
        params['description'],
        uploaded_file_url,
        excerpt_text,
        excerpt_title
    )

    os.unlink(temp_file_path)

    return {
        'document': {
            'id': document.id,
            'title': document.title,
            'organization': document.organization,
            'description': document.description,
            'text': document.text,
            'url': document.url,
        }
    }


@blueprint.route('/admin/<document_id>', methods=['PUT'])
@admin_required
@validate_schema(DocumentUpdateSchema)
def admin_update_documents(document_id, params):
    document = document_controller.get_document(document_id)

    if not document:
        raise Http404Error('Document not found')

    document = document_controller.update_document(document, **params)

    return {
        'document': {
            'id': document.id,
            'title': document.title,
            'organization': document.organization,
            'description': document.description,
            'text': document.text,
            'url': document.url,
        }
    }


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


@blueprint.route('/admin/download/<document_id>', methods=['GET'])
@admin_required
def admin_download(document_id):
    url = document_controller.generate_expireable_document_url(document_id=document_id, expires_in=60)
    return {'url': url}, 302


@blueprint.route('/admin/grant', methods=['POST'])
@admin_required
@validate_schema(DocumentGrantSchema)
def admin_grant_document_download(params):
    user = user_controller.get_user_by_id(params['user_id'])
    document = document_controller.get_document(params['document_id'])
    purchase = purchase_controller.create_purchase(params['document_id'], params['user_id'], params['expires_in'])

    if params.get('notify_user'):
        try:
            mailer.send(
                user.email,
                'email/document_granted',
                {
                    'document': document,
                    'purchase': purchase
                },
                'Document access granted'
            )
        except Exception as ex:
            print(f'Unable to send email to user {user.email}:', ex)

    return {
        'document': {
            'id': document.id,
            'title': document.title,
            'organization': document.organization,
            'description': document.description,
            'text': document.text
        },
        'purchase': {
            'purchased_at': purchase.purchased_at,
            'valid_until': purchase.valid_until,
            'download_url': purchase.download_url
        },
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'activated_at': user.activated_at
        }
    }


@blueprint.route('/', methods=['GET'])
def list_documents():
    page = int(request.args.get('page', 0))
    documents = document_controller.list_documents(page)

    return {
        'documents': [{
            'id': document.id,
            'title': document.title,
            'organization': document.organization,
            'description': document.description,
            'text': document.text,
            'url': document.url
        } for document in documents]
    }


@blueprint.route('/<document_id>', methods=['GET'])
@login_required
def get_documents(document_id):
    document = document_controller.get_document(document_id)

    result = {
        'document': {
            'id': document.id,
            'title': document.title,
            'organization': document.organization,
            'description': document.description,
            'text': document.text
        }
    }

    user_purchase = document_controller.get_user_document_purchase(g.user, document, False)

    if user_purchase:
        result['purchase'] = {
            'purchased_at': user_purchase.purchased_at,
            'valid_until': user_purchase.valid_until,
            'download_url': user_purchase.download_url
        }

    return result


@blueprint.route('/my', methods=['GET'])
@login_required
def get_my_documents():
    documents = document_controller.list_actual_user_documents(g.user)
    return {'documents': documents}
    # document = document_controller.get_document(document_id)

    # result = {
    #     'document': {
    #         'id': document.id,
    #         'title': document.title,
    #         'organization': document.organization,
    #         'description': document.description,
    #         'text': document.text
    #     }
    # }

    # user_purchase = document_controller.get_user_document_purchase(g.user, document, False)

    # if user_purchase:
    #     result['purchase'] = {
    #         'purchased_at': user_purchase.purchased_at,
    #         'valid_until': user_purchase.valid_until,
    #         'download_url': user_purchase.download_url
    #     }

    # return result


@blueprint.route('/past', methods=['GET'])
@login_required
def get_my_past_documents():
    documents = document_controller.list_past_user_documents(g.user)
    return {'documents': documents}
    # document = document_controller.get_document(document_id)

    # result = {
    #     'document': {
    #         'id': document.id,
    #         'title': document.title,
    #         'organization': document.organization,
    #         'description': document.description,
    #         'text': document.text
    #     }
    # }

    # user_purchase = document_controller.get_user_document_purchase(g.user, document, False)

    # if user_purchase:
    #     result['purchase'] = {
    #         'purchased_at': user_purchase.purchased_at,
    #         'valid_until': user_purchase.valid_until,
    #         'download_url': user_purchase.download_url
    #     }

    # return result
