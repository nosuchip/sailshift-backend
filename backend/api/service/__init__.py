from flask import Blueprint

blueprint = Blueprint('service', __name__, url_prefix='/api/service')


@blueprint.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {'status': 'healthy'}
