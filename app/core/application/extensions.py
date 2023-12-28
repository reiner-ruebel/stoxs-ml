from flask_migrate import Migrate
from flask_security import Security
from flask_mailman import Mail # type: ignore
from flask_jwt_extended import JWTManager

from app.shared.consts import Consts
from app.shared.AppTypes import Extension
from app.core.application.database import db
from app.core.security.user_datastore import user_datastore

       
_migrate = Migrate()
_security = Security()
_mail = Mail()
_jwt = JWTManager()

extensions: list[Extension] = [
    (Consts.EXTENSION_MIGRATE, _migrate, _migrate.init_app, {'db': db}),
    (Consts.EXTENSION_SECURITY, _security, _security.init_app, {'datastore': user_datastore}),
    (Consts.EXTENSION_MAIL, _mail, _mail.init_app, {}),
    (Consts.EXTENSION_JWT, _jwt, _jwt.init_app, {}),
]
