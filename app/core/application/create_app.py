from flask import Flask

from app.core.application.app_components import AppComponents


def create_app() -> Flask:
    """Creates the Flask application."""

    app = Flask(__name__)
    AppComponents.init_app(app)

    return app
