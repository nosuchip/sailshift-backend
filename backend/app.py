import logging
from flask import Flask
from flask_cors import CORS

from backend.api import accounts
from backend.api import documents
from backend.api import payments
from backend.api import non_api
from backend.api import service
from backend.db import init_db


def create_app():
    init_db()

    app = Flask(__name__)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    logging.getLogger('flask_cors').level = logging.DEBUG

    app.register_blueprint(accounts.blueprint)
    app.register_blueprint(documents.blueprint)
    app.register_blueprint(payments.blueprint)
    app.register_blueprint(service.blueprint)

    # Use last
    app.register_blueprint(non_api.blueprint)

    return app
