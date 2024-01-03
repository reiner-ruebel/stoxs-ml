from typing import Optional
from dataclasses import dataclass

from marshmallow import Schema
from marshmallow_dataclass import class_schema

from app.core import SwaggerFields


@dataclass
class RegisterPayload:
    """ Register payload model """

    firstname: str = SwaggerFields.FIRSTNAME
    surname: str = SwaggerFields.SURNAME
    email: str = SwaggerFields.EMAIL
    password: str = SwaggerFields.PASSWORD
    username: Optional[str] = SwaggerFields.USERNAME
    middlename: Optional[str] = SwaggerFields.MIDDLENAME
    title: Optional[str] = SwaggerFields.TITLE


    def create_schema(self) -> type[Schema]:
        """ Creates a marshmallow schema for this dataclass. """
        return class_schema(RegisterPayload)
