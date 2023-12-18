import os
from typing import Optional, Any, cast, Union

from flask import Response, jsonify, Request

from app.shared.utils import get_application_path, get_module_names
from app.shared.consts import Consts
from app.shared.http_status_codes import HttpStatusCodes, is_success


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


def create_response_c(input: dict | list[str] | str, status_code: int | None=None, ok: bool=True) -> Api_Response:
    """
    Creates a tuple of a response and a status code.
    If the input is a string, it will be converted to a dictionary with the key 'message' or 'error' depending on the status code.
    If the status code is not provided, it will be set to 200 if ok is True, otherwise it will be set to 400.
    """

    if status_code is None:
        status_code = HttpStatusCodes.HTTP_200_OK if ok else HttpStatusCodes.HTTP_400_BAD_REQUEST

    json_input: dict = input if isinstance(input, dict) else {'message' if is_success(status_code) else "error": input}
    response: Response = jsonify(json_input)

    return (response, status_code)


def create_data(request: Request) -> Optional[dict[str, Any]]:
    """ Returns the json data of a request casted to a dicr or None if no data was provided """
    json_data = request.json
    return None if json_data is None else cast(dict[str, Any], json_data)
