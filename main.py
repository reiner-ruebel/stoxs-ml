"""
Starting point for the machine learning part of the Stoxs application.

The Stoxs class contains the functionality of the application which is embedded in a Flask environment.

Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from flask import Flask

from app.core.application.config import config
from app.core.application.blueprints import blueprints
from app.core.application.database import db
from app.core.application.extensions import extensions
from app.core.application import create_app


if __name__ == "__main__":
    """ We obtain the configuration, blueprints, database and extensions from the corresponding modules in a dependency injection style. """

    app: Flask = create_app(config, blueprints, db, extensions)
    app.run()
