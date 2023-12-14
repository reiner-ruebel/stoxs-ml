"""
Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import cast, Any, Optional

from marshmallow import ValidationError
from sqlalchemy import Column
from flask import Blueprint, request, current_app
from flask_security import hash_password
from flask_mailman import EmailMultiAlternatives # type: ignore

from app.core.application.config import config
from app.core.application.blueprints import get_blueprint
from app.core.application.extensions import security
from app.core.security.user import User
from app.core.security.security_service import user_policy_checker
from app.core.mail.mail import render_template
from app.api.shared.utils import Response_c, create_data, create_response_c
from app.api.auth.models.register import PreRegisterModel, RegisterModel, RegisterSchema


_blueprint: Blueprint = get_blueprint(__name__)

@_blueprint.post("/register")
def register() -> Response_c:
    """ Registers a new user. """

    try:
        # validate data
        register_raw_data: Optional[dict[str, Any]] = create_data(request)

        if register_raw_data is None:
            return create_response_c("No registration data provided.", ok = False)

        register_model: RegisterModel = RegisterSchema().load(register_raw_data)

        if not PreRegisterModel.query.get(register_model.email):
            return create_response_c("Use of this API is by invitation only.", ok = False)

        if security.datastore.find_user(username = register_model.username, email = register_model.email):
            return create_response_c("Username or user email already exists.", ok = False)
        
        validation_msgs: Optional[list[str]] = user_policy_checker(register_model.password, register_model.email, register_model.username)

        if validation_msgs:
            return create_response_c(validation_msgs, ok = False)

        # create user
        register_raw_data["password"] = cast(str, hash_password(register_model.password))
        register_raw_data["active"] = True # no confirmation needed, since the user is pre-registered
        
        user: User = security.datastore.create_user(**register_raw_data)
        if not user.username:
            user.username = cast(Column[str], user.calc_username())
        user.save() # default is to commit
        
        # send welcome mail and return response
        title: str = f"Welcome to {config.SITE_NAME}!"

        kwargs: dict[str, str] = {
            "TITLE": title
            }

        html, text = render_template("welcome", **kwargs)

        with current_app.app_context():
            msg = EmailMultiAlternatives(title, text, config.MAIL_DEFAULT_SENDER, [user.email])
            msg.attach_alternative(html, "text/html")
            msg.send()

        return create_response_c(f"Your welcome to {config.SITE_NAME}! An email has been sent to you. Once you receive it, you are ready to start working with the API.")

    except ValidationError as err:
        return create_response_c(err.messages, ok = False)
