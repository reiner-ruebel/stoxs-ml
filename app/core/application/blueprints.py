from typing import cast, Optional
from importlib import import_module

from flask import Blueprint, abort, current_app

from app.core.shared.utils import get_containers, create_version
from app.api.shared.utils import endpoints, get_container, module_import_name


#
# blueprints that are not used but are required by flask-security-too.
#

not_used_blueprint = Blueprint('not_used_blueprint', __name__)

@not_used_blueprint.route('/logout')
def logout():
    """We map the logout endpoint to 404. This is because we do not want to use the flask-security-too extension to logout."""
    abort(404)


@not_used_blueprint.route('/login')
def login():
    """We map the logout endpoint to 404. This is because we do not want to use the flask-security-too extension to login."""
    abort(404)


@not_used_blueprint.route("/show_routes")
def show_routes():
    """Quick overview of the routes of the application."""

    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = f"{rule.endpoint}: {methods} {rule.rule}"
        output.append(line)

    return '<br>'.join(output)


#
# Automated blueprint scanning and creation
#

_blueprints_map: dict[str, Blueprint] = {'not_used_blueprint': not_used_blueprint} # A map of all blueprints (to be registered) by their container name


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


def get_blueprints() -> list[Blueprint]:
    """Returns all blueprints of the application."""

    return list(_blueprints_map.values())
