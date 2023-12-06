from flask_security.models import fsqla_v3 as fsqla

from app.core.application.database import db

class User(db.Model, fsqla.FsUserMixin): # type: ignore
    pass
