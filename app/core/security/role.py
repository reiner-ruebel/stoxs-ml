from flask_security.models import fsqla_v3 as fsqla

from app.core.application.database import db

class Role(db.Model, fsqla.FsRoleMixin): # type: ignore
    pass
