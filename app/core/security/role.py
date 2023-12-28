from flask_security.models import fsqla_v3 as fsqla

from app.core.application.app_components import AppComponents as C

class Role(C.db.Model, fsqla.FsRoleMixin): # type: ignore
    pass
