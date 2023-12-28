from flask_migrate import Migrate
from flask_security import Security
from flask_mailman import Mail # type: ignore
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.shared.consts import Consts
from app.shared.AppTypes import Extension
from app.core.security import user_datastore


class Extensions:
    """Extensions to be initialized in the Flask application."""

    @staticmethod
    def get_extensions(db: SQLAlchemy) -> list[Extension]:
        """Returns a list of extensions to be initialized."""
        
        migrate = Migrate()
        security = Security()
        mail = Mail()
        jwt = JWTManager()

        return [
            (Consts.EXTENSION_MIGRATE, migrate, migrate.init_app, {'db': db}),
            (Consts.EXTENSION_SECURITY, security, security.init_app, {'datastore': user_datastore}),
            (Consts.EXTENSION_MAIL, mail, mail.init_app, {}),
            (Consts.EXTENSION_JWT, jwt, jwt.init_app, {}),
        ]
