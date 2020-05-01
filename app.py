from flask import Flask

from backend.api import accounts
from backend.api import documents
from backend.api import payments
from backend.db import init_db


def create_app():
    init_db()

    app = Flask(__name__)

    app.register_blueprint(accounts.blueprint)
    app.register_blueprint(documents.blueprint)
    app.register_blueprint(payments.blueprint)

    return app
