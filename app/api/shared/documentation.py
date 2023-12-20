from dataclasses import field

from marshmallow import validate

from app.shared.consts import Consts


descriptions: dict[str, str] = {
    "admin": "Admin related functionality. Required role is admin.",
    "auth": "Authentication related functionality.",
    "userstore": "Userstore related functionality. Required role is admin.",
    "userstore.reset": "Reset the database to default values. This is only available in development mode.",
    "auth.register": "To register a user who has already been pre-registered",
}


common_fields: dict[str, field] = {
    "id": field(description="The unique identifier of the user."),

    "firstname": field(metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1),
        'description': f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'First Name',
        'example': 'Peter'
        }),

    "surname": field(metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1),
        "description": f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'Last Name',
        'example': 'Pan'
        }),

   "email": field(metadata={
        "validate": [validate.Email(), validate.Length(max=Consts.MAX_EMAIL_LENGTH)],
        "description": f"Max {Consts.MAX_EMAIL_LENGTH} chars",
        'title': 'Email Address',
        'example': 'peter.pan@neverland.eu'
        }),

    "password": field(metadata={
        "validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH),
        "description": f"Between {Consts.MIN_PASSWORD_LENGTH} and {Consts.MAX_PASSWORD_LENGTH} chars",
        'title': 'Password',
        'example': 'kogpwF!18&ei6%'
        }),

    "username": field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        "description": f"Max {Consts.MAX_NAME_LENGTH} chars",
        'title': 'Username',
        'example': 'PeterPan'
        }),

    "middlename": field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        'title': 'Middle Name',
        'example': 'T.'
        }),

    "title": field(default=None, metadata={
        "validate": validate.Length(max=Consts.MAX_NAME_LENGTH),
        'title': 'Title',
        'example': 'Prof.'
        }),
    } 