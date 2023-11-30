from flask_security import Security
from flask import Blueprint, current_app, request, jsonify
from marshmallow import ValidationError

from app.core.flaskenv.blueprints import get_blueprint
from app.api.auth.schemas.register import RegisterSchema
from app.shared.http_status_codes import HttpStatusCodes


blueprint:Blueprint = get_blueprint(__name__)

@blueprint.post("/register")
def register():
    try:
        data: dict = request.json
        password: str = data.get('password')
       
        # schema: RegisterSchema = RegisterSchema.load(data)
        # security: Security = current_app.extensions['security']
        
        # validation_msgs, normalized_password = security.validate(password, is_register = True, **data)
        
        # if validation_msgs:
        #     return jsonify(validation_msgs), HttpStatusCodes.HTTP_400_BAD_REQUEST

        # RegisterSchema.validate(schema)
        
        return jsonify({"message": "Registration successful"}), HttpStatusCodes.HTTP_200_OK

    except ValidationError as err:
        return jsonify(err.messages), HttpStatusCodes.HTTP_400_BAD_REQUEST
