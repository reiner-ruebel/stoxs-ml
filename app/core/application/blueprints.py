from typing import cast, Optional
from importlib import import_module

from flask import Blueprint

from app.core.shared.utils import get_containers, create_version
from app.api.shared.utils import endpoints, get_container, module_import_name


# A map of all blueprints (to be registered) by their container name
_blueprints_map: dict[str, Blueprint] = {}


def _create_blueprint(container: str) -> Blueprint:
    """Creates a blueprint from a container name."""
    
    bp_module = import_module(module_import_name(container))

    version = cast(Optional[str], getattr(bp_module, "version", None))

    url_prefix = f"/{version or create_version(1)}/{container}"

    return Blueprint(container, module_import_name(container), url_prefix=url_prefix)


def get_blueprint(container: str) -> Blueprint:
    """Returns a blueprint by its container name, e.g. 'auth', 'stoxs', ..."""

    bp = _blueprints_map.get(container)
    if bp is None:
        raise ValueError(f"Blueprint for container '{container}' not found.")
    return bp


def create_blueprints() -> None:
    """Creates and returns a list of all blueprints of the application and imports the modules of the corresponding endpoints."""

    for container in get_containers(): # Here you can find the definition of a container.
        bp: Blueprint = _create_blueprint(container)
        _blueprints_map[container] = bp

        for endpoint in endpoints(container):
            import_module(endpoint) # The module has access to its blueprint through the module name so it can define routes, etc.


def get_blueprints() -> list[Blueprint]:
    """Returns all blueprints of the application."""

    return list(_blueprints_map.values())
