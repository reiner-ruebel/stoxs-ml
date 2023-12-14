"""
Flask and other extensions instantiated here.

To avoid circular imports with views and create_app(), extensions are instantiated here. They will be initialized
(calling init_app()) in application.py.
"""

from typing import Callable

from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from flask_mailman import Mail # type: ignore
from flask_jwt_extended import JWTManager

from app.core.application.database import db
from app.core.security import user_datastore


migrate = Migrate()
security = Security()
mail = Mail()
jwt = JWTManager()

extensions: list[tuple[object, Callable[[Flask], None], dict[str, object]]] = [
    (migrate, migrate.init_app, {'db': db}),
    (security, security.init_app, {'datastore': user_datastore}),
    (mail, mail.init_app, {}),
    (jwt, jwt.init_app, {}),
]
