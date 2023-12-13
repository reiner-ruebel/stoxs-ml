"""
Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import cast, Any, Optional

from marshmallow import ValidationError
from flask import Blueprint, request, current_app
from flask_security import password_complexity_validator, hash_password
from flask_security.confirmable import generate_confirmation_link
from flask_mailman import EmailMessage # type: ignore

from app.core.application.config import config
from app.core.application.blueprints import get_blueprint
from app.core.application.extensions import security
from app.core.security.user import User
from app.core.security.security_service import user_policy_checker
from app.api.shared.utils import Response_c, create_data, create_response_c
from app.api.auth.models.register import PreRegisterModel, RegisterModel, RegisterSchema


_blueprint: Blueprint = get_blueprint(__name__)

@_blueprint.post("/register")
def register() -> Response_c:
    """ Registers a new user. """

    try:
        register_raw_data: Optional[dict[str, Any]] = create_data(request)

        if register_raw_data is None:
            return create_response_c("No data provided", ok = False)

        register_model: RegisterModel = RegisterSchema().load(register_raw_data)

        if not PreRegisterModel.query.get(register_model.email):
            return create_response_c("User not pre-registered", ok = False)

        if security.datastore.find_user(username = register_model.username, email = register_model.email):
            return create_response_c("Username or user mail already exists", ok = False)
        
        validation_msgs: Optional[list[str]] = user_policy_checker(register_model.password, register_model.email, register_model.username)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        validation_msgs = password_complexity_validator(register_model.password, is_register = True)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        register_raw_data["password"] = cast(str, hash_password(register_model.password))
        register_raw_data["active"] = False # user needs to confirm email address first
        
        user: User = security.datastore.create_user(**register_raw_data)
        user.username = user.username or user.calc_username()
        user.save() # default is to commit
        
        confirmation_link, token = generate_confirmation_link(user) # requires that the user is saved first

        # with current_app.app_context():
        #     msg = EmailMessage(
        #         subject=f"Confirm your registration at {config.SITE_NAME}",
        #         body=f'This is a test email sent from the Flask application using Google Workspace SMTP Relay. and here is the URL',
        #         to=[user.email],
        #         from_email=config.MAIL_DEFAULT_SENDER
        #         )
        #     msg.send()

        return create_response_c(f"Registration mail sent. Please confirm to finish your registration.{confirmation_link}, {token}")

    except ValidationError as err:
        return create_response_c(err.messages, ok = False)
