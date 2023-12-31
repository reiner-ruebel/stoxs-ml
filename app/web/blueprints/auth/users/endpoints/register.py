from typing import cast, Any, Optional
from flask_security.core import Security

from marshmallow import ValidationError
from sqlalchemy import Column
from flask import current_app
from flask_security import hash_password
from flask_mailman import EmailMultiAlternatives # type: ignore
from flask_restx import Resource, marshal_with # type: ignore

from app.shared.consts import Consts
from app.shared.AppTypes import Api_Response
from app.core.application.config import config_object
from app.core.application.extensions import get_extension
from app.core.security.security_service import SecurityService
from app.core.security.user import User
from app.core.mail.mail import AppMail
from app.core.application.apis import Apis
from app.api.shared.utils import ApiUtils

from ..models.register import PayloadModel, PayloadSchema, response_model
from ..models.pre_register import PreRegisterModel


ns, swagger_model = Apis.endpoint_package(__name__, PayloadModel)

@ns.route("/")
class Register(Resource):
    @ns.expect(swagger_model)
    @ApiUtils.validate_request(PayloadModel)
    @marshal_with(response_model, code=201)
    def post(self, payload: PayloadModel) -> Api_Response:
        """ Registers a new user. """

        security: Security = cast(Security, get_extension(Consts.EXTENSION_SECURITY))

        try:
            if not PreRegisterModel.query.get(payload.email):
                return ApiUtils.create_api_response("Use of this API is by invitation only.", ok = False)

            if security.datastore.find_user(username = payload.username, email = payload.email):
                return ApiUtils.create_api_response("Username or user email already exists.", ok = False)
        
            validation_msgs: Optional[list[str]] = SecurityService.user_policy_checker(payload.password, payload.email, payload.username)

            if validation_msgs:
                return ApiUtils.create_api_response(validation_msgs, ok = False)

            # create user
            payload.password = cast(str, hash_password(payload.password))
        
            user_raw_data: dict[str, Any] = PayloadSchema().dump(payload)
            user_raw_data['active'] = True

            user: User = security.datastore.create_user(**user_raw_data)
            if not user.username:
                user.username = cast(Column[str], user.calc_username())
            user.save() # default is to commit
        
            # send welcome mail and return response
            title: str = f"Welcome to {config_object.SITE_NAME}!"

            kwargs: dict[str, str] = {
                "TITLE": title
                }

            html, text = AppMail.render_template("welcome", **kwargs)

            with current_app.app_context():
                msg = EmailMultiAlternatives(title, text, config_object.MAIL_DEFAULT_SENDER, [user.email])
                msg.attach_alternative(html, "text/html")
                msg.send()

            return ApiUtils.create_api_response(f"Your welcome to {config_object.SITE_NAME}! An email has been sent to you. Once you receive it, you are ready to start working with the API.")

        except ValidationError as err:
            return ApiUtils.create_api_response(err.messages, ok = False)
