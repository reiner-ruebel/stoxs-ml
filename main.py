"""
Starting point for the machine learning part of the Stoxs application.

The Stoxs class contains the functionality of the application which is embedded in a Flask environment.

Credentials are required to create an instance of the application. These are defined in the Credentials class.

To maintain a dependency injection, the credentials are created independently of the application. The application is then created with the credentials.

Each part can be dynamically replaced by importing it from another module, e.g. for testing purposes.
"""

from flask import Flask

from app.core.application.config import config
from app.core.application.database import db
from app.core.application.blueprints import blueprints
from app.core.application.extensions import extensions
from app.core.application.models import models
from app.core.application.exceptions import error_handlers

from app.core.application.credentials import Credentials
from app.core.application import create_app


_credentials: Credentials = Credentials(config, db, blueprints, extensions, models, error_handlers)

app: Flask = create_app(_credentials)

if __name__ == "__main__":
    app.run()
