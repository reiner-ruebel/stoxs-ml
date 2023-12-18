from typing import cast

from marshmallow import ValidationError
from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource # type: ignore
from sqlalchemy import and_

from app.shared.http_status_codes import HttpStatusCodes as c
from app.core.security.user import User
from app.api.shared.utils import Api_Response, create_data, create_response_c
from app.api.auth.models.authenticate import AuthenticateModel, AuthenticateSchema


ns = Namespace("authenticate", description="pre-register a user who is allowed to register himself")


@ns.route('/')
class authenticate(Resource):
    def post(self) -> Api_Response:
        USER_NOT_FOUND: str = "Credentials do not match."

        try:
            data = create_data(request)

            if data is None:
                return create_response_c("No authentication data provided.", c.HTTP_401_UNAUTHORIZED)
        
            authenticate_model: AuthenticateModel = AuthenticateSchema().load(data)
        
            if not authenticate_model.email and not authenticate_model.username or not authenticate_model.password:
                return create_response_c("Either email or username and password are required.", c.HTTP_401_UNAUTHORIZED)

            query_conditions = []
            if authenticate_model.username:
                query_conditions.append(User.username == authenticate_model.username)
            if authenticate_model.email:
                query_conditions.append(User.email == authenticate_model.email)
         
            user = User.query.filter(and_(*query_conditions)).first() # if both, username and email are provided they both need to match.

            if user is None or not user.verify_password(authenticate_model.password):
                return create_response_c(USER_NOT_FOUND, c.HTTP_401_UNAUTHORIZED)

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            return create_response_c({
                "message": "Authentication successful.",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expire_in_seconds": cast(int, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
                "refresh_token_expire_in_seconds": cast(int, current_app.config['JWT_REFRESH_TOKEN_EXPIRES'].total_seconds()),
                })

        except ValidationError as err:
            return create_response_c(err.messages, ok = False)
