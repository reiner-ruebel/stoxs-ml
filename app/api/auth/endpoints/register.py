"""
Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import cast, Any, Optional

from marshmallow import ValidationError
from flask import Blueprint, request
from flask_security import password_complexity_validator, hash_password, send_mail

from app.core.application.blueprints import get_blueprint
from app.core.application.extensions import security
from app.core.security.user import User
from app.core.security.security_service import user_policy_checker
from app.api.shared.utils import Response_c, create_response_c
from app.api.auth.models.register import RegisterModel, RegisterSchema


_blueprint: Blueprint = get_blueprint(__name__)

@_blueprint.post("/register")
def register() -> Response_c:
    """ Registers a new user. """

    try:
        json_data = request.json

        if json_data is None:
            return create_response_c("No data provided", ok = False)

        register_raw_data: dict[str, Any] = cast(dict[str, Any], json_data)
        register_model: RegisterModel = RegisterSchema().load(register_raw_data)

        if security.datastore.find_user(username = register_model.username, email = register_model.email):
            return create_response_c("Username or user mail already exists", ok = False)
        
        validation_msgs: Optional[list[str]] = user_policy_checker(register_model.password, register_model.username, register_model.email)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        validation_msgs = password_complexity_validator(register_model.password, is_register = True)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        register_raw_data["password"] = cast(str, hash_password(register_model.password))
        register_raw_data["active"] = False # user needs to confirm email address first
        
        user: User = security.datastore.create_user(**register_raw_data)
        user.save() # default is to commit
        
        send_mail(
            subject = "Confirm registration",
            recipients = [user.email],
            template = "security/email/welcome",
            user = user,
            confirmation_link = security._ctx.confirm_register_link(user.registration_token),
        ) # type: ignore # pylint: disable=protected-access #)
        

        return create_response_c("Registration mail sent. Please confirm to finish your registration.")

    except ValidationError as err:
        return create_response_c(err.messages, ok = False)
