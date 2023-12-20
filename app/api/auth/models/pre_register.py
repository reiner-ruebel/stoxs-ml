from dataclasses import dataclass

from app.shared.consts import Consts
from app.core.application.database import db


@dataclass
class PreRegisterModel(db.Model): # type: ignore
    """ Users who register themselves must be pre-registered. """

    __tablename__ = Consts.DB_PRE_REGISTER

    email = db.Column(db.String(Consts.MAX_EMAIL_LENGTH), primary_key=True)
    role = db.Column(db.String(Consts.MAX_NAME_LENGTH), nullable=True) # Separate multiple roles with a comma
