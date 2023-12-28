from flask_security.datastore import SQLAlchemyUserDatastore

from app.core.application.app_components import AppComponents as C
from .user import User
from .role import Role


user_datastore = SQLAlchemyUserDatastore(C.db, User, Role)
