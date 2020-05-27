from flask import Blueprint, request

blueprint = Blueprint('service', __name__, url_prefix='/api/service')


@blueprint.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {'status': 'healthy'}

@blueprint.route('/headers', methods=['GET'])
def headers():
    return {'headers': request.headers}
