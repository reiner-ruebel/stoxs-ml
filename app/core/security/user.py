from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy import Column, String

from app.core.application.database import db
from app.shared.consts import Consts


class User(db.Model, fsqla.FsUserMixin): # type: ignore
    firstname = Column(String(Consts.MAX_NAME_LENGTH), nullable=False)
    middlename = Column(String(Consts.MAX_NAME_LENGTH))
    surname = Column(String(Consts.MAX_NAME_LENGTH), nullable=False)
    title = Column(String(Consts.MAX_NAME_LENGTH))
