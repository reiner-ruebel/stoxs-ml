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
from app.shared.http_status_codes import HttpStatusCodes


blueprint:Blueprint = get_blueprint(__name__)

@blueprint.post("/register")
def register() -> tuple[Response, int]:
    try:
        json_data = request.json

        if json_data is None:
            return jsonify({'error': 'Invalid JSON data'}), HttpStatusCodes.HTTP_400_BAD_REQUEST

        data: dict[str, str] = cast(dict[str, str], json_data)
        register_schema = RegisterSchema()
        register_data: RegisterSchema = register_schema.load(data)
        
        # https://flask-security-too.readthedocs.io/en/stable/api.html#flask_security.password_complexity_validator usage not 100% clear
        password: str | None = data.get('password')
        if (password is None):
            return jsonify({'error': 'Password is required'}), HttpStatusCodes.HTTP_400_BAD_REQUEST

        data_password_removed: dict = data.copy()
        data_password_removed.pop('password', None)
        validation_msgs: list[str] | None = password_complexity_validator(password, is_register = True, **data_password_removed)
        
        if validation_msgs:
            return jsonify(validation_msgs), HttpStatusCodes.HTTP_400_BAD_REQUEST

        RegisterSchema.check_username_vs_mailaddress(data)
        
        return jsonify({"message": "Registration successful"}), HttpStatusCodes.HTTP_200_OK

    except ValidationError as err:
        return jsonify(err.messages), HttpStatusCodes.HTTP_400_BAD_REQUEST
