import logging
from flask import Flask, g
from flask_cors import CORS

from backend.api import accounts
from backend.api import documents
from backend.api import payments
from backend.api import non_api
from backend.api import service
from backend.db import init_db, get_session

from backend.common.logger import logger

from backend import config


def create_app():
    init_db()

    app = Flask(config.APP_NAME,
                template_folder='backend/templates',
                static_folder='backend/static')
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    logging.getLogger('flask_cors').level = logging.DEBUG

    app.register_blueprint(accounts.blueprint)
    app.register_blueprint(documents.blueprint)
    app.register_blueprint(payments.blueprint)
    app.register_blueprint(service.blueprint)

    # Use last
    app.register_blueprint(non_api.blueprint)

    @app.errorhandler(Exception)
    def handle_exception(e):
        code = getattr(e, 'code', None)

        if not code:
            code = getattr(e, 'status', None)

        if code == 500:
            logger.exception(e)

        return {'success': False, 'error': f'{e}'}, 404

    @app.before_request
    def before_request():
        print(">> Request initialization")
        g.session = get_session()

    @app.teardown_request
    def end_request(ex=None):
        print(">> Request finallization")

        if g.session:
            if ex:
                print(f">> rollback session due exception: {ex}")
                g.session.rollback()
            else:
                print(f">> commit session")
                g.session.commit()

            g.session.close()
            g.session = None

    return app
