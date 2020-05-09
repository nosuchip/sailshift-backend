import os.path
from flask import Blueprint, send_file


blueprint = Blueprint('non_api', __name__)

@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def catch_all(path):
    print(f"Static fallback file handler for path {path}")
    static_html_path = os.path.join(os.path.dirname(__file__), '../../static/dist/index.html')

    return send_file(static_html_path)
