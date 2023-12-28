from dataclasses import dataclass

from app.shared.consts import Consts
from app.core.application.app_components import AppComponents as C


@dataclass
class PreRegisterModel(C.db.Model): # type: ignore
    """ Users who register themselves must be pre-registered. """

    __tablename__ = Consts.DB_PRE_REGISTER

    email = C.db.Column(C.db.String(Consts.MAX_EMAIL_LENGTH), primary_key=True)
    role = C.db.Column(C.db.String(Consts.MAX_NAME_LENGTH), nullable=True)  # Separate multiple roles with a comma
