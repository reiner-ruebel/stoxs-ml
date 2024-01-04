from typing import Any, Optional, Type, get_type_hints, get_args
from dataclasses import is_dataclass, fields as get_fields

from flask_restx import Namespace, Model as SwaggerModel, fields as restx_fields

from .inamespace_manager import INamespaceManager
from app import AppUtils, Consts
from app.core import SwaggerStrings
from .namespace_docu import NamespaceDocu


class NamespaceManager(INamespaceManager):
    """Namespace manager."""
    
    def __init__(self, module_name: str, payload_model: Optional[Type[Any]] = None, codes: Optional[list[int]] = None) -> None:
        self._module_name = module_name
        self._payload_model = payload_model
        self.codes = codes


    @classmethod
    def create_docu(cls, module_name: str, payload_model: Type[Any]) -> NamespaceDocu:
        """Creates the docu to decorate a resource with the route and swagger documentation."""

        namespace = cls._create_namespace(module_name)

        container = CoreUtils.get_container(module_name)
        swagger_model: SwaggerModel = cls._create_swagger_model(payload_model)
        api.models[container+"_"+swagger_model.name] = swagger_model # register the model with the api

        return (namespace, swagger_model)


    @classmethod
    def _create_namespace(cls, module_name: str) -> Namespace:
        """ Creates a new namespace with the given name and description. """

        lookup_name, name = cls._create_namespace_name(module_name)
        description = SwaggerStrings.DESCRIPTIONS.get(lookup_name, "tbd")

        return Namespace(name, description=description)


    @staticmethod
    def _create_namespace_name(module_name: str) -> tuple[str, str]:
        """Creates a namespace name from a module name."""

        parts = module_name.split('.')

        try:
            index = parts.index(Consts.ENDPOINTS)
        except ValueError:
            raise ValueError(f"The module '{module_name}' does not contain an '{Consts.ENDPOINTS}' directory")

        namespace = parts[index - 1]
        filename = parts[-1]

        return f"{namespace}.{filename}", filename


    @staticmethod
    def _create_swagger_model(payload_model: Type[Any]) -> SwaggerModel:
        """ Converts a payload model (dataclass) to a SwaggerModel (restx.Model) to support Swagger. """

        if not is_dataclass(payload_model):
            raise TypeError("Provided model must be a dataclass")

        model_fields = {}
        type_hints = get_type_hints(payload_model)

        for field in get_fields(payload_model):
            field_name = field.name
            field_type = type_hints[field_name]
            kwargs = {
                "title": field.metadata.get("title", None),
                "example": field.metadata.get("example", None),
                "description": field.metadata.get("description", None),
                "required": not AppUtils.flat_field_is_optional(field_type),
                }

            # Map Python types to Flask-RESTx fields
            type_to_field = {
                str: restx_fields.String,
                int: restx_fields.Integer,
                bool: restx_fields.Boolean
            }

            for lookup_type, lookup_method in type_to_field.items():
                if lookup_type == field_type or (AppUtils.flat_field_is_optional(field_type) and lookup_type in get_args(field_type)):
                    model_fields[field_name] = lookup_method(**kwargs)
                    break
         
        return SwaggerModel(payload_model.__name__, model_fields)
