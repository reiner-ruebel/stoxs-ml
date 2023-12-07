import os
from typing import Optional

from flask import Response, jsonify

from app.shared.utils import get_application_path, get_module_names
from app.shared.consts import Consts


Response_c = tuple[Response, int]

_bp_dot_root = Consts.BP_ROOT.replace('/', '.')

def endpoints(container: str) -> list[str]:
    """ Returns a list of all endpoints within a blueprint container """
    modules: list[str] = get_module_names(os.path.join(get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS))
    return [f"{_bp_dot_root}.{container}.{Consts.ENDPOINTS}.{module}" for module in modules]


def container_import_name(container: str) -> str:
    """ Returns the import name of a blueprint container """
    return f"{Consts.BP_ROOT.replace('/', '.')}.{container}"


def container_url_prefix(container: str) -> str:
    """ Returns the container url prefix of a blueprint container """
    return f"/{Consts.BP_ROOT}/{container}"


def get_container(module: str) -> Optional[str]:
    """ Retrieves the container name from a module name """

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


def create_response_c(input: dict | str, status_code: int | None=None, ok: bool=True) -> Response_c:
    """
    Creates a tuple of a response and a status code.
    If the input is a string, it will be converted to a dictionary with the key 'message' or 'error' depending on the status code.
    If the status code is not provided, it will be set to 200 if ok is True, otherwise it will be set to 400.
    """

    if status_code is None:
        status_code = 200 if ok else 400

    json_input: dict = input if isinstance(input, dict) else {'message' if status_code == 200 else "error": input}
    response: Response = jsonify(json_input)

    return (response, status_code)
