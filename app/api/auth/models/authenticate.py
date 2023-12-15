from dataclasses import dataclass, field
from typing import Optional

from marshmallow import validate
from marshmallow_dataclass import class_schema

from app.shared.consts import Consts


@dataclass
class AuthenticateModel:
    """ Login model """
    password: str = field(metadata={"validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH)})
    email: Optional[str] = field(metadata={"validate": validate.Email(), "validate": validate.Length(max=Consts.MAX_EMAIL_LENGTH)})
    username: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})

AuthenticateSchema = class_schema(AuthenticateModel)
