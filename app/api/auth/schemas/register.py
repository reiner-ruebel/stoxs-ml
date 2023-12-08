from app.shared.consts import Consts

from marshmallow import Schema, fields, validate, ValidationError

from app.shared.utils import valid_mail_address


class RegisterSchema(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    middlename = fields.Str(max=Consts.MAX_NAME_LENGTH)
    surname = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    title = fields.Str(max=Consts.MAX_NAME_LENGTH)
    username = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_NAME_LENGTH, min=1))
    email = fields.Email(required=True, validate=validate.Length(max=Consts.MAX_EMAIL_LENGTH))
    password = fields.Str(required=True, validate=validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH))

    @staticmethod
    def check_username_vs_mailaddress(data: dict[str, str]) -> None:
        if valid_mail_address(data['username']) and data['username'].lower() != data['email'].lower():
            raise ValidationError("Username cannot be an email address unless it matches your email address.")
