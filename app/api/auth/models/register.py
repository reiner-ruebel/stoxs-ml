from dataclasses import dataclass, field
from typing import Optional

from marshmallow import validate
from marshmallow_dataclass import class_schema

from app.shared.consts import Consts
from app.core.application.database import db


@dataclass
class PreRegisterModel(db.Model): # type: ignore
    """ Users who register themselves must be pre-registered. """
    __tablename__ = Consts.DB_PRE_REGISTER
    email = db.Column(db.String(Consts.MAX_EMAIL_LENGTH), primary_key=True)


@dataclass
class RegisterModel:
    """ Register model """
    firstname: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1)})
    surname: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1)})
    username: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1)})
    email: str = field(metadata={"validate": validate.Email(), "validate": validate.Length(max=Consts.MAX_EMAIL_LENGTH)})
    password: str = field(metadata={"validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH)})
    middlename: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})
    title: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})

RegisterSchema = class_schema(RegisterModel)
