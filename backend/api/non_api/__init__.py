import os.path
from flask import Blueprint, send_file, make_response
from backend.common.errors import Http404Error
from backend.common.logger import logger, config
from backend.api.prerender import prerender_controller
from backend.common.decorators import async_action

blueprint = Blueprint('non_api', __name__)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
@async_action
async def catch_all(path):
    logger.warn(f"Static fallback file handler for path {path}")

    # Prerender

    if prerender_controller.should_prerender(path):
        html = await prerender_controller.render_url(f"{config.SITE_URL}/{path}")
        resp = make_response(html)
        resp.mimetype = 'text/plain'
        return resp

    # Some special handlers

    if path.endswith('manifest.json'):
        special_static_path = os.path.join(os.path.dirname(__file__),
                                           '../../static/manifest.json')

        return send_file(special_static_path)

    if path.endswith('service-worker.js'):
        special_static_path = os.path.join(os.path.dirname(__file__),
                                           '../../static/service-worker.js')

        return send_file(special_static_path)

    if 'precache-manifest' in path:
        special_static_path = os.path.join(os.path.dirname(__file__),
                                           '../../static/',
                                           path)

        return send_file(special_static_path)

    if 'img' not in path and 'favicon' not in path:
        static_html_path = os.path.join(os.path.dirname(__file__),
                                        '../../static/index.html')

        return send_file(static_html_path)

    raise Http404Error(f"Resource {path} doesn't served by static handler")
