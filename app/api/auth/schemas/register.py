from app.shared.consts import Consts

from typing import Dict, Any

from marshmallow import Schema, fields, validate, ValidationError

from app.shared.lib import valid_mail_address


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH))
    sur_name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH))
    user_name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH))
    email_address = fields.Email(required=True, validate=validate.Length(max=Consts.MAX_EMAIL_LENGTH))
    password = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH))

    @staticmethod
    def validate(data: Dict[str, Any]) -> None:
        if data['user_name'].lower() == data['email_address'].lower() and valid_mail_address(data['user_name']):
            raise ValidationError("Username cannot be an email address unless it's the same with your email address!")

