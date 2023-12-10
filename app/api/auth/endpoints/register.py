"""
Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import cast, Any, Optional

from flask import Blueprint, request
from flask_security import password_complexity_validator, hash_password
from marshmallow import ValidationError

from app.core.application.extensions import security
from app.core.application.blueprints import get_blueprint
from app.api.auth.schemas.register import RegisterModel, RegisterSchema
from app.api.shared.utils import Response_c, create_response_c
from app.core.security.security_service import user_exist, user_policy_checker


blueprint: Blueprint = get_blueprint(__name__)

@blueprint.post("/register")
def register() -> Response_c:
    """ Registers a new user. """

    try:
        json_data = request.json

        if json_data is None:
            return create_response_c("No data provided", ok = False)

        data: dict[str, Any] = cast(dict[str, Any], json_data)
        register_data: RegisterModel = RegisterSchema().load(data)

        if user_exist(register_data.username, register_data.email):
            return create_response_c("Username or user mail already exists", ok = False)
        
        # https://flask-security-too.readthedocs.io/en/stable/api.html#flask_security.password_complexity_validator usage not 100% clear
        password: Optional[str] = data.get('password')
        if (password is None):
            return create_response_c("No password provided", ok = False)

        data_password_removed: dict = data.copy()
        data_password_removed.pop('password', None)

        validation_msgs: Optional[list[str]] = user_policy_checker(password, register_data.username, register_data.email)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        validation_msgs = password_complexity_validator(password, is_register = True, **data_password_removed)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        password = cast(str, hash_password(password))
        data["password"] = password
        del data_password_removed # Now, we are in control that the original pw is not accessible any more (by standard code)
        
        data["active"] = False # user needs to confirm email address first
        
        user = security.datastore.create_user(**data)
        user.save()

        return create_response_c("Registration mail sent. Please confirm to finish your registration.")

    except ValidationError as err:
        return create_response_c(err.messages, ok = False)
