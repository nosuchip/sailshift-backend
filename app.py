from flask import Flask
from flask_cors import CORS

from backend.api import accounts
from backend.api import documents
from backend.api import payments
from backend.db import init_db


def create_app():
    init_db()

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(accounts.blueprint)
    app.register_blueprint(documents.blueprint)
    app.register_blueprint(payments.blueprint)

    return app
