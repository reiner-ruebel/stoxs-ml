"""
Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import cast

from flask import Blueprint, request, jsonify, Response
from flask_security import password_complexity_validator
from marshmallow import ValidationError

from app.core.application.extensions import security
from app.core.application.blueprints import get_blueprint
from app.api.auth.schemas.register import RegisterSchema
from app.api.shared.utils import Response_c, create_response_c


blueprint: Blueprint = get_blueprint(__name__)

@blueprint.post("/register")
def register() -> Response_c:
    """ Registers a new user. """

    try:
        json_data = request.json

        if json_data is None:
            return create_response_c("No data provided", ok = False)

        data: dict[str, str] = cast(dict[str, str], json_data)
        register_schema = RegisterSchema()
        register_data: RegisterSchema = register_schema.load(data)
        
        # https://flask-security-too.readthedocs.io/en/stable/api.html#flask_security.password_complexity_validator usage not 100% clear
        password: str | None = data.get('password')
        if (password is None):
            return create_response_c("No password provided", ok = False)

        data_password_removed: dict = data.copy()
        data_password_removed.pop('password', None)
        validation_msgs: list[str] | None = password_complexity_validator(password, is_register = True, **data_password_removed)
        
        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        RegisterSchema.check_username_vs_mailaddress(data)
        
        user = security.datastore.create_user(**register_data)
        return create_response_c("Registration successful")

    except ValidationError as err:
        return create_response_c(err.messages, ok = False)
