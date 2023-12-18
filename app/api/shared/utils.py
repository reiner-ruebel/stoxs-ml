from typing import Optional, Union, Any, cast
import os
from functools import wraps

from marshmallow import ValidationError
from flask import Response, request, Request
from flask_restx import Namespace

from app.core.application import config
from app.shared.utils import get_application_path, get_module_names
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
    """ Returns the import name of the module of a blueprint container """
    return f"{Consts.BP_ROOT.replace('/', '.')}.{container}"


def get_container(module: str) -> Optional[str]:
    """Retrieves the container name (like 'auth') from an endpoint module, typically called like get_container(__name__)"""

    segments = module.split(".")

    try:
        endpoints_index = segments.index(Consts.ENDPOINTS)
    except ValueError:
        return None

    if endpoints_index >= 1:
        parent_directory = segments[endpoints_index - 1]
        return parent_directory
    else:
        return None


def create_api_response(message: dict | list[str] | str, status_code: int | None=None, ok: bool=True) -> Api_Response:
    """
    Creates a tuple of a response dict and a status code.
    If the input is a string, it will be converted to a dictionary with the key 'message' or 'error' depending on the status code.
    If the status code is not provided, it will be set to 200 if ok is True, otherwise it will be set to 400.
    """

    if status_code is None:
        status_code = HttpStatusCodes.HTTP_200_OK if ok else HttpStatusCodes.HTTP_400_BAD_REQUEST

    json: dict = message if isinstance(message, dict) else {'message' if is_success(status_code) else _create_error(message)}

    return (json, status_code)


def _create_error(code_or_message: str) -> dict:
    """ Creates an error dictionary with the given message. """

    message = error_map.get(code_or_message, code_or_message) # get the corresponding message if we have a code, else the massage has been provided
    code = None if message == code_or_message else code_or_message
    documentation_url = f"{config.CUSTOM_BASE_URL}/{Consts.ERROR}s#{code}" if code is not None else None

    inner = {
        Consts.MESSAGE: message,
    }
    
    if code is not None:
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


def create_namespace(file: str) -> Namespace:
    """ Creates a new namespace with the given name and description. """

    lookup_name, name = create_namespace_name(file)
    description = descriptions.get(lookup_name, "tbd")

    return Namespace(name, description=description)


def create_namespace_name(file: str) -> tuple[str, str]:
    # Split the path into its components
    path_parts = file.split(os.sep)

    # Find the index of 'endpoints'
    try:
        index = path_parts.index('endpoints')
    except ValueError:
        raise ValueError("The path does not contain an 'endpoints' directory")

    # Extract the directory name just above 'endpoints' and the filename without extension
    namespace = path_parts[index - 1]
    filename = os.path.splitext(os.path.basename(file))[0]

    # Return the concatenated string
    return f"{namespace}.{filename}", filename
