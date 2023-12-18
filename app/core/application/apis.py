from importlib import import_module

from flask import Blueprint
from flask_restx import Api, Namespace # type: ignore
from app.core.application.blueprints import get_blueprint

from app.core.shared.utils import get_containers, create_version
from app.api.shared.utils import endpoints, module_import_name


def _create_api(container: str) -> Api:
    """
    Creates an API object out of a container (directory which represents an API).
    The arguments for the API object are taken from the container module or set to defaults if they are not present.
    """
    bp: Blueprint = get_blueprint(container)
    api_module = module_import_name(container)

    # Default values for API configuration
    api_defaults = {
        'version': create_version(1),
        'title': container,
        'description': 'tbd',
        'doc': '/docs',
        'default': 'default'
    }

    # Update defaults with any attributes found in the module
    kwargs = {attr: getattr(api_module, attr, default) for attr, default in api_defaults.items()}

    return Api(bp, **kwargs)


def create_apis() -> None:
    """Creates all APIs and the corresponding namespaces."""

    for container in get_containers():
        api: Api = _create_api(container)

        for endpoint in endpoints(container):
            endpoint_module = import_module(endpoint)
            ns: Namespace = getattr(endpoint_module, "ns", None)
            if ns is not None:
                api.add_namespace(ns)
