from dataclasses import fields as get_fields, is_dataclass
from typing import Collection, Optional, Type, Union, Any, cast, get_type_hints, _GenericAlias
import os
from functools import wraps

from flask_restx.reqparse import RequestParser
from marshmallow import ValidationError
from flask import Response, request, Request
from flask_restx import Model as SwaggerModel, Namespace, fields

from app.core.application.config import config
from app.shared.utils import get_application_path, get_module_names, is_optional
from app.shared.consts import Consts
from app.shared.http_status_codes import HttpStatusCodes, is_success
from app.api.shared.errors import error_map
from app.api.shared.documentation import descriptions


Api_Response = Union[dict, Response, tuple[Union[dict, Response], int]]

_bp_dot_root = Consts.BP_ROOT.replace('/', '.')

def endpoints(container: str) -> list[str]:
    """Returns a list of all endpoints within a blueprint container"""

    modules: list[str] = get_module_names(os.path.join(get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS))
    return [f"{_bp_dot_root}.{container}.{Consts.ENDPOINTS}.{module}" for module in modules]


def module_import_name(container: str) -> str:
    """Returns the import name of the module of a blueprint container. Example: 'auth' => 'app.api.auth'"""
    return f"{Consts.BP_ROOT.replace('/', '.')}.{container}"


def get_container(module: str) -> str:
    """Retrieves the container name (like 'auth') from an endpoint module, typically called like get_container(__name__)"""

    segments = module.split(".")

    endpoints_index = segments.index(Consts.ENDPOINTS)

    if endpoints_index >= 1:
        parent_directory = segments[endpoints_index - 1]
        return parent_directory
    else:
        raise Exception("no endpoint")


def create_api_response(message: dict | list[str] | str, status_code: int | None=None, ok: bool=True) -> Api_Response:
    """
    Creates a tuple of a response dict and a status code.
    If the input is a string, it will be converted to a dictionary with the key 'message' or 'error' depending on the status code.
    If the status code is not provided, it will be set to 200 if ok is True, otherwise it will be set to 400.
    """

    if status_code is None:
        status_code = HttpStatusCodes.HTTP_200_OK if ok else HttpStatusCodes.HTTP_400_BAD_REQUEST

    str_message: str = cast(str, message) if isinstance(message, str) else ", ".join(cast(list[str], message)) if isinstance(message, list) else ""
    json: Collection[Any] = message if isinstance(message, dict) else {'message' if is_success(status_code) else _create_error(str_message)}

    return (json, status_code) # type: ignore


def _create_error(code_or_message: str) -> dict:
    """ Creates an error dictionary with the given message. """

    message = error_map.get(code_or_message, code_or_message) # get the corresponding message if we have a code, else the massage has been provided
    code = None if message == code_or_message else code_or_message
    documentation_url = f"{config.CUSTOM_BASE_URL}/{Consts.ERROR}s#{code}" if code is not None else None

    inner = {
        Consts.MESSAGE: message,
    }
    
    if code is not None and documentation_url is not None:
        inner["documentation_url"] = documentation_url
        inner[Consts.ERROR] = code


    return {
        Consts.ERROR: inner
    }


def validate_request(schema_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request_data = create_data(request)
                if request_data is None:
                    return create_api_response("No_data_provided", HttpStatusCodes.HTTP_400_BAD_REQUEST)

                schema = schema_class()
                model = schema.load(request_data)
                return func(*args, **kwargs, model=model)
            except ValidationError as err:
                return create_api_response(err.messages, ok = False)
        return wrapper
    return decorator


def create_data(request: Request) -> Optional[dict[str, Any]]:
    """ Returns the json data of a request casted to a dicr or None if no data was provided """

    json_data = request.json
    return None if json_data is None else cast(dict[str, Any], json_data)


def create_namespace(module_name: str) -> Namespace:
    """ Creates a new namespace with the given name and description. """

    lookup_name, name = create_namespace_name(module_name)
    description = descriptions.get(lookup_name, "tbd")

    return Namespace(name, description=description)


def create_namespace_name(module_name: str) -> tuple[str, str]:
    parts = module_name.split('.')

    try:
        index = parts.index(Consts.ENDPOINTS)
    except ValueError:
        raise ValueError(f"The module '{module_name}' does not contain an '{Consts.ENDPOINTS}' directory")

    namespace = parts[index - 1]
    filename = parts[-1]

    # Return the concatenated string
    return f"{namespace}.{filename}", filename


def get_leaf(module_name: str) -> str:
    """ Returns the leaf of a module, e.g. 'app.api.auth.endpoints.authenticate' => 'authenticate' """
    return module_name.split('.')[-1]


def create_restx_model_names(module_name: str) -> tuple[str, str]:
    """
    Creates a tuple of a swagger model name and a response model name.
    This method is typically called with __name__ as argument, e.g. create_restx_model_names(__name__)
    """
    
    name: str = get_leaf(module_name).capitalize()

    return Consts.SWAGGER_MODEL + name, Consts.RESPONSE_MODEL + name


def create_parser(payload_model: Type) -> RequestParser:
    """ Converts a payload model (dataclass) to a RequestParser to support Swagger. """

    if not is_dataclass(payload_model):
        raise TypeError("payload_model must be a dataclass")

    parser = RequestParser()
    type_hints = get_type_hints(payload_model)
    
    for field in get_fields(payload_model):
        # Extract metadata
        help_text = field.metadata.get("help", "")
        field_name = field.name
        field_type = type_hints[field_name]
        this_type: Type = int
        if field_type == str or (isinstance(field_type, _GenericAlias) and str in field_type.__args__):
            this_type = str
        required = not is_optional(field_type)

        # Add argument to parser
        parser.add_argument(
            name=field.name, 
            type=this_type, 
            help=help_text, 
            required=True, 
            location='json' # Use 'json' for body parameters
        )

    return parser


def create_swagger_model(payload_model: Type) -> SwaggerModel:
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
            "description": field.metadata.get("description", ""),
            "required": not is_optional(type_hints[field_name]),
            }

        # Map Python types to Flask-RESTx fields
        if field_type == str or (isinstance(field_type, _GenericAlias) and str in field_type.__args__):
            model_fields[field_name] = fields.String(**kwargs)
        elif field_type == int or (isinstance(field_type, _GenericAlias) and int in field_type.__args__):
            model_fields[field_name] = fields.Integer(**kwargs)
         
    return SwaggerModel(payload_model.__name__, model_fields)
