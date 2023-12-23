from flask import Flask

from app.shared.utils import AppUtils
from app.core.application.credentials import Credentials
from app.core.application import create_app


def main() -> None:
    """Starting point of the flask application."""

    AppUtils.set_application_path(__file__)

    credentials: Credentials = Credentials()
    app: Flask = create_app(credentials) # dependency injection
    app.run()
    

if __name__ == "__main__":
    main()
