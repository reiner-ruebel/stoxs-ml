from typing import Optional
from dataclasses import dataclass

from marshmallow_dataclass import class_schema
from flask_restx import fields, Model # type: ignore

from app.api.shared.utils import create_restx_model_names
from app.api.shared.documentation import common_fields


@dataclass
class PayloadModel:
    """ Register payload model """
    
    firstname: str = common_fields['firstname']
    surname: str = common_fields['surname']
    email: str = common_fields['email']
    password: str = common_fields['password']
    username: Optional[str] = common_fields['username']
    middlename: Optional[str] = common_fields['middlename']
    title: Optional[str] = common_fields['title']
    
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
