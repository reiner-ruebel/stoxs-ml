from dataclasses import dataclass, field

from marshmallow import validate

from app.shared.consts import Consts


@dataclass
class ResetInput:
    """ Reset input model """

    password: str = field(metadata={"validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH)})

