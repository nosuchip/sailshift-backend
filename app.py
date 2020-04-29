from flask import Flask

from backend.api import accounts
from backend.db import init_db


def create_app():
    init_db()

    app = Flask(__name__)

    app.register_blueprint(accounts.blueprint)

    return app
