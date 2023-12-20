from importlib import import_module

from flask import Blueprint
from flask_restx import Api, Namespace # type: ignore
from app.core.application.blueprints import get_blueprint

from app.core.shared.utils import get_containers, create_version
from app.api.shared.utils import endpoints, get_container, module_import_name
from app.api.shared.documentation import descriptions


_api_map: dict[str, Api] = {}


def get_api(module_name: str) -> Api:
    """ Returns the API object for the given container. """

    container = get_container(module_name)
    return _api_map[container]


def _create_api(container: str) -> Api:
    """
    Creates an API object out of a container (directory which represents an API).
    The arguments for the API object are taken from the container module or set to defaults if they are not present.
    """
    bp: Blueprint = get_blueprint(container)
    api_module = import_module(module_import_name(container))

    # Default values for API configuration
    api_defaults = {
        'version': create_version(1),
        'title': container.capitalize(),
        'description': descriptions.get(container, 'detailed description tbd'),
        'doc': '/swagger',
    }

    # Update defaults with any attributes found in the module
    kwargs = {attr: getattr(api_module, attr, default) for attr, default in api_defaults.items()}
    
    api = Api(bp, **kwargs)

    _api_map[container] = api

    return api


def create_apis() -> None:
    """Creates all APIs and the corresponding namespaces."""

    for container in get_containers():
        api: Api = _create_api(container)

        for endpoint in endpoints(container):
            endpoint_module = import_module(endpoint)
            ns: Namespace = getattr(endpoint_module, "ns", None)
            if ns is not None:
                api.add_namespace(ns)
