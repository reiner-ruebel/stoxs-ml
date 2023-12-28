from typing import cast, Any, Optional
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource # type: ignore

from flask import Blueprint, request, current_app
from flask_security import hash_password
from flask_mailman import EmailMultiAlternatives # type: ignore

from app.api.shared.utils import ApiUtils
from app.shared.AppTypes import Api_Response


ns = Namespace("refresh", description="Refresh token.")

@ns.route("/")
#@jwt_required(refresh=True)
class refresh(Resource):
    def post(self) -> Api_Response:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return ApiUtils.create_api_response({
                "message": "Refresh successful.",
                "access_token": access_token,
                "access_token_expire_in_seconds": cast(int, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
                })
