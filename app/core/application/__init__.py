"""
Flask environment
""" 

from typing import Callable

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy

from app.core.application.config import BaseConfig


def create_app(
    config: BaseConfig,
    blueprints: list[Blueprint],
    db: SQLAlchemy,
    extensions: list[tuple[object, Callable[[Flask], None]]]
) -> Flask:
    """
    Flask application factory. Initializes and returns the Flask application.

    Blueprints are registered in here.
    """

    app = Flask(__name__)
    app.config.from_object(config)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
    db.init_app(app)

    for _, init in extensions:
        init(app)

    return app
 