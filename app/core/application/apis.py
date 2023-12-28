from typing import Type, get_type_hints, get_args
from dataclasses import fields as get_fields, is_dataclass
from importlib import import_module

from flask import Blueprint
from flask_restx import Api, Namespace, Model as SwaggerModel, fields as restx_fields # type: ignore

from app.shared.consts import Consts
from app.shared.utils import AppUtils
from app.core.shared.utils import CoreUtils
from app.api.shared.documentation import ApiStrings
from app.api.shared.utils import ApiUtils
from app.core.application.blueprints import Blueprints


class Apis:
    
    _api_map: dict[str, Api] = {}

    #
    # Public methods
    #

    @classmethod
    def create_apis(cls) -> None:
        """
        Creates all APIs and the corresponding namespaces.
        
        The method always returns True, because:
            - We never access the (flask-restx) APIs directly.
            - The namespaces are created and inside the modules the routes are added to the namespaces.
        """

        for container in CoreUtils.get_containers():
            api: Api = cls._create_api(container)

            for endpoint in ApiUtils.endpoints(container):
                endpoint_module = import_module(endpoint)
                ns: Namespace = getattr(endpoint_module, "ns", None)
                if ns is not None:
                    api.add_namespace(ns)


    @classmethod
    def endpoint_package(cls, module_name: str, payload_model: Type) -> tuple[Namespace, SwaggerModel]:
        """ Creates a tuple of a namespace, ... and swagger model for a given module name. """

        container = CoreUtils.get_container(module_name)
        namespace = cls._create_namespace(module_name)
        api = cls._get_api(module_name)
        swagger_model: SwaggerModel = cls._create_swagger_model(payload_model)
        api.models[container+"_"+swagger_model.name] = swagger_model # register the model with the api

        return (namespace, swagger_model)


    #
    # Private methods
    #

    @classmethod
    def _get_api(cls, module_name: str) -> Api:
        """ Returns the API object for the given container. """

        container = CoreUtils.get_container(module_name)
        return cls._api_map[container]


    @classmethod
    def _create_api(cls, container: str) -> Api:
        """
        Creates an API object out of a container (directory which represents an API).
        The arguments for the API object are taken from the container module or set to defaults if they are not present.
        """
        bp: Blueprint = Blueprints.get_blueprint(container)
        api_module = import_module(ApiUtils.module_import_name(container))

        # Default values for API configuration
        api_defaults = {
            'version': CoreUtils.create_version(1),
            'title': container.capitalize(),
            'description': ApiStrings.DESCRIPTIONS.get(container, 'detailed description tbd'),
            'doc': '/swagger',
        }

        # Update defaults with any attributes found in the module
        kwargs = {attr: getattr(api_module, attr, default) for attr, default in api_defaults.items()}
    
        api = Api(bp, **kwargs)

        cls._api_map[container] = api

        return api


    @classmethod
    def _create_namespace(cls, module_name: str) -> Namespace:
        """ Creates a new namespace with the given name and description. """

        lookup_name, name = cls._create_namespace_name(module_name)
        description = ApiStrings.DESCRIPTIONS.get(lookup_name, "tbd")

        return Namespace(name, description=description)


    @staticmethod
    def _create_namespace_name(module_name: str) -> tuple[str, str]:
        parts = module_name.split('.')

        try:
            index = parts.index(Consts.ENDPOINTS)
        except ValueError:
            raise ValueError(f"The module '{module_name}' does not contain an '{Consts.ENDPOINTS}' directory")

        namespace = parts[index - 1]
        filename = parts[-1]

        # Return the concatenated string
        return f"{namespace}.{filename}", filename


    @staticmethod
    def _create_swagger_model(payload_model: Type) -> SwaggerModel:
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
