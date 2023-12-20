from typing import Optional
from dataclasses import dataclass, field
from flask_restx.reqparse import Argument
from flask_restx.swagger import RequestParser

from marshmallow import validate
from marshmallow_dataclass import class_schema
from flask_restx import fields, Model # type: ignore

from app.shared.consts import Consts
from app.api.shared.utils import create_restx_model_names


@dataclass
class PayloadModel:
    """Register payload model"""
#    firstname: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1), "help": f"First Name, max {Consts.MAX_NAME_LENGTH} long"}),
    firstname: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1), 'description': f"First Name, max {Consts.MAX_NAME_LENGTH} long", 'title': 'First Name', 'example': 'Peter'})
    surname: str = field(metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH, min=1)})
    email: str = field(metadata={"validate": validate.Email(), "validate": validate.Length(max=Consts.MAX_EMAIL_LENGTH)})
    password: str = field(metadata={"validate": validate.Length(max=Consts.MAX_PASSWORD_LENGTH, min=Consts.MIN_PASSWORD_LENGTH)})
    username: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})
    middlename: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})
    title: Optional[str] = field(default=None, metadata={"validate": validate.Length(max=Consts.MAX_NAME_LENGTH)})
    number: Optional[int] = field(default=19, metadata={"validate": validate.Range(min=0, max=100), 'help': 'this is the help'})

PayloadSchema = class_schema(PayloadModel)


class HugoName(fields.Raw):
    def format(self, value):
        return value + 'hugo'

s_model, r_model = create_restx_model_names(__name__)

_base_model = Model('RegisterBaseModel', {
    'firstname': fields.String(required=True, description='First name'),
    'surname': fields.String(required=True, description='Surname'),
    'email': fields.String(required=True, description='Email address'),
    'username': fields.String(description='Username', required=False),
    'middlename': fields.String(description='Middle Name', required=False),
    'title': fields.String(description='Title', required=False)
})


response_model = _base_model.clone(r_model, {
    'hugoed_name': HugoName(attribute='surname'),
})