"""
All blueprints are listed in this module
This is the central point of the application where we have a list of all endpoints available in the application.
"""

from typing import cast
from importlib import import_module

from flask import Blueprint

from app.core.shared.utils import create_api_from_bp, create_bp_from_container, get_containers
from app.api.shared.utils import endpoints, get_container


# A map of all blueprints (to be registered) by their container name
_blueprints_map: dict[str, Blueprint] = {}


def get_blueprint(module_name: str) -> Blueprint:
    """Returns a blueprint by its container name"""

    container = cast(str, get_container(module_name))
    bp = _blueprints_map.get(container)
    if bp is None:
        raise ValueError(f"Blueprint for container '{container}' not found.")
    return bp


def _create_all() -> list[Blueprint]:
    """Creates and returns a list of all blueprints of the application and imports the modules of the corresponding endpoints."""

    for container in get_containers(): # Here you can find the definition of a container.
        bp = create_bp_from_container(container)
        _blueprints_map[container] = bp
        api = create_api_from_bp(bp)

        for endpoint in endpoints(container):
            endpoint_module = import_module(endpoint) # The module has access to its blueprint through the module name so it can define routes, etc.
            ns = getattr(endpoint_module, "ns", None)
            if ns is not None:
                api.add_namespace(ns)

    return list(_blueprints_map.values())


# A list of all blueprints (which want to be registered)
blueprints: list[Blueprint] = _create_all()
