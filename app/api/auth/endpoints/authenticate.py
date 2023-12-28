from typing import cast

from marshmallow import ValidationError
from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource # type: ignore
from sqlalchemy import and_

from app.shared.http_status_codes import HttpStatusCodes as c
from app.core.security.user import User
from app.api.shared.utils import Api_Response, ApiUtils
from app.api.auth.models.authenticate import AuthenticateModel, AuthenticateSchema


ns = Namespace("authenticate", description="pre-register a user who is allowed to register himself")


@ns.route('/')
class authenticate(Resource):
    def post(self) -> Api_Response:
        try:
            data: dict[str, str] = {} # ApiUtils.create_data(request)

            if data is None:
                return ApiUtils.create_api_response("No authentication data provided.", c.HTTP_401_UNAUTHORIZED)
        
            authenticate_model: AuthenticateModel = AuthenticateSchema().load(data)
        
            if not authenticate_model.email and not authenticate_model.username or not authenticate_model.password:
                return ApiUtils.create_api_response("Either email or username and password are required.", c.HTTP_401_UNAUTHORIZED)

            query_conditions = []
            if authenticate_model.username:
                query_conditions.append(User.username == authenticate_model.username)
            if authenticate_model.email:
                query_conditions.append(User.email == authenticate_model.email)
         
            user = User.query.filter(and_(*query_conditions)).first() # if both, username and email are provided they both need to match.

            if user is None or not user.verify_password(authenticate_model.password):
                return ApiUtils.create_api_response("Credentials do not match.", c.HTTP_401_UNAUTHORIZED)

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            return ApiUtils.create_api_response({
                "message": "Authentication successful.",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expire_in_seconds": cast(int, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
                "refresh_token_expire_in_seconds": cast(int, current_app.config['JWT_REFRESH_TOKEN_EXPIRES'].total_seconds()),
                })

        except ValidationError as err:
            return ApiUtils.create_api_response(err.messages, ok = False)
