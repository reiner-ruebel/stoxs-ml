from typing import Optional
from dataclasses import dataclass, field

from marshmallow import validate

from app.shared.consts import Consts


@dataclass
class CommonFields:
    """Common fields for all models."""

    ID: str = field(metadata={
        "description": "The unique identifier of the user."
        })

    FIRSTNAME: str = field(metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1),
        'description': f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'First Name',
        'example': 'Peter'
        })

    SURNAME: str = field(metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1),
        "description": f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'Last Name',
        'example': 'Pan'
        })

    EMAIL: str = field(metadata={
        "validate": [validate.Email(), validate.Length(max=Consts.MAX_EMAIL_LENGTH)],
        "description": f"Max {Consts.MAX_EMAIL_LENGTH} chars",
        'title': 'Email Address',
        'example': 'peter.pan@neverland.eu'
        })

    PASSWORD: str = field(metadata={
        "validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH),
        "description": f"Between {Consts.MIN_PASSWORD_LENGTH} and {Consts.MAX_PASSWORD_LENGTH} chars",
        'title': 'Password',
        'example': 'kogpwF!18&ei6%'
        })

    USERNAME: Optional[str] = field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        "description": f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'Username',
        'example': 'PeterPan'
        })

    MIDDLENAME: Optional[str] = field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        'title': 'Middle Name',
        'example': 'T.'
        })

    TITLE: Optional[str] = field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        'title': 'Title',
        'example': 'Prof.'
        })


class ApiStrings:
    """Strings used in the API."""

    DESCRIPTIONS: dict[str, str] = {
        "admin": "Admin related functionality. Required role is admin.",
        "auth": "Authentication related functionality.",
        "userstore": "Userstore related functionality. Required role is admin.",
        "userstore.reset": "Reset the database to default values. This is only available in development mode.",
        "auth.register": "To register a user who has already been pre-registered",
    }
