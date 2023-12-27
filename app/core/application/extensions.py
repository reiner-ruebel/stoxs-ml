"""
Flask and other extensions instantiated here.

To avoid circular imports with blueprints and create_app(), extensions are instantiated here. They will be initialized
(calling init_app()) in application.py.
"""

from typing import Callable

from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from flask_mailman import Mail # type: ignore
from flask_jwt_extended import JWTManager

from app.core.application.database import AppSql
from app.core.security import user_datastore

Extension = tuple[object, Callable[[Flask], None], dict[str, object]]

class Extensions:
    _migrate = Migrate()
    _security = Security()
    _mail = Mail()
    _jwt = JWTManager()

    @classmethod
    def get_extensions(cls) -> list[Extension]:
        return [
            (cls._migrate, cls._migrate.init_app, {'db': AppSql.db}),
            (cls._security, cls._security.init_app, {'datastore': user_datastore}),
            (cls._mail, cls._mail.init_app, {}),
            (cls._jwt, cls._jwt.init_app, {}),
        ]
