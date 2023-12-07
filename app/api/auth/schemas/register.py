from app.shared.consts import Consts

from marshmallow import Schema, fields, validate, ValidationError

from app.shared.utils import valid_mail_address


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    sur_name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    user_name = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    email_address = fields.Email(required=True, validate=validate.Length(max=Consts.MAX_EMAIL_LENGTH))
    password = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH))

    @staticmethod
    def check_username_vs_mailaddress(data: dict[str, str]) -> None:
        if valid_mail_address(data['user_name'] and data['user_name'].lower() != data['email_address'].lower()):
            raise ValidationError("Username cannot be an email address unless it matches your email address.")
