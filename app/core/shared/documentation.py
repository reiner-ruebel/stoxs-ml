from typing import Optional
from dataclasses import field

from marshmallow import validate

from app.shared.consts import Consts


class SwaggerFields:
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


class ErrorMap:
    ERRORS: dict[str, str] = {
    "No_data_provided": "No data provided",
    "user_not_found": "User not found.",
    "user_already_exists": "User already exists.",
    "user_not_active": "User is not active.",
    "user_not_authenticated": "User is not authenticated.",
    "invalid_password": "Invalid password.",
    "invalid_token": "Invalid token.",
    "invalid_reset_code": "Invalid reset code.",
    "invalid_email": "Invalid email.",
    "invalid_username": "Invalid username.",
    }
    

class Strings:
    TITLE = "Corvendor stoxs"
    DESCRIPTION = "Corvendor stoxs is a stock management system for mega large businesses."


class SwaggerStrings:
    """Strings used in the API."""

    DESCRIPTIONS: dict[str, str] = {
        "admin": "Admin related functionality. Required role is admin.",
        "auth": "Authentication related functionality.",
        "userstore": "Userstore related functionality. Required role is admin.",
        "userstore.reset": "Reset the database to default values. This is only available in development mode.",
        "auth.register": "To register a user who has already been pre-registered",
    }
