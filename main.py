from flask import Flask

from app.shared.utils import AppUtils
from app.core.application.app_components import AppComponents


def create_app() -> Flask:
    """Creates the Flask application."""

    app = Flask(__name__)
    AppComponents.init_app(app)

    return app


def main() -> None:
    """Starting point of the flask application."""

    AppUtils.set_application_path(__file__)
    AppComponents.initialize() # Prepare dependency injection for the Flask application.

    app = create_app()
    app.run()
    

if __name__ == "__main__":
    main()
