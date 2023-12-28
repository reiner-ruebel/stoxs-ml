from flask_security.datastore import SQLAlchemyUserDatastore

from app.core.application.database import db
from .user import User
from .role import Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
