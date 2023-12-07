"""
The properties of the Credentials class are accessed by the application to initialize itself.
Therefore, the init module and this module are in the same folder.
It is also assumed that the modules with the individual credentials are in the same folder.
"""

from typing import Callable

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy

from .config import BaseConfig
from app.core.shared.error_handler_protocol import ErrorHandlerProtocol


class Credentials:
    """ The credentials we need to create the flask app """
    def __init__(
            self,
            config: BaseConfig,
            db: SQLAlchemy,
            blueprints: list[Blueprint],
            extensions: list[tuple[object, Callable[[Flask], None], dict[str, object]]],
            models: list[str],
            middlewares: list[str],
            error_handlers: list[tuple[int, ErrorHandlerProtocol]],
    ) -> None:
        self.config = config
        self.db = db
        self.blueprints = blueprints
        self.extensions = extensions
        self.models = models
        self.middlewares = middlewares
        self.error_handlers = error_handlers
        