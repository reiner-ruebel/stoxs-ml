"""
All blueprints are listed in this module
This is the central point of the application where we have a list of all endpoints available in the application.
"""

from importlib import import_module
from typing import Optional

from flask import Blueprint

from app.api.common import endpoints, container_import_name, container_url_prefix, containers, get_container


# A map of all blueprints (to be registered) by their container name
_blueprints_map: dict[str, Blueprint] = {}


def get_blueprint(module_name: str) -> Optional[Blueprint]:
    """ Returns a blueprint by its container name """
    container: Optional[str] = get_container(module_name)
    return None if container is None else _blueprints_map.get(container, None)


def _create_all() -> list[Blueprint]:
    for container in containers:
        blueprint: Blueprint = Blueprint(container, container_import_name(container), url_prefix=container_url_prefix(container))
        _blueprints_map[container] = blueprint
        for endpoint in endpoints(container):
            import_module(endpoint)

    return list(_blueprints_map.values())


# A list of all blueprints (which want to be registered)
blueprints: list[Blueprint] = _create_all()
