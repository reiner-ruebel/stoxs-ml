from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy import Column, String

from app.shared.consts import Consts
from app.core.application.app_components import AppComponents as C
from app.core.database.mixins import CrudMixin


class User(CrudMixin['User'], C.db.Model, fsqla.FsUserMixin):  # type: ignore
    """User model for the Flask application."""

    firstname = Column(String(Consts.MAX_NAME_LENGTH), nullable=False)
    middlename = Column(String(Consts.MAX_NAME_LENGTH))
    surname = Column(String(Consts.MAX_NAME_LENGTH), nullable=False)
    title = Column(String(Consts.MAX_NAME_LENGTH))
