import os.path
from flask import Blueprint, send_file
from backend.common.errors import Http404Error
from backend.common.logger import logger


blueprint = Blueprint('non_api', __name__)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def catch_all(path):
    logger.warn(f"Static fallback file handler for path {path}")

    if 'img' not in path and 'favicon' not in path:
        static_html_path = os.path.join(os.path.dirname(__file__), '../../static/index.html')

        return send_file(static_html_path)

    raise Http404Error(f"Resource {path} doesn't served by static handler")
