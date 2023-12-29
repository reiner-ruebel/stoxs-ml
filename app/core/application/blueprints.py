from typing import cast, Optional
from importlib import import_module

from flask import Blueprint, abort, current_app

from app.core.shared.utils import CoreUtils
from app.api.shared.utils import ApiUtils


#
# Static blueprints to void the flask-security-too login and logout views and to show the routes in dev mode.
#

def _abort():
    """Overwrites the login and logout views of the flask-security-too extension to return a 404."""

    abort(404)


def _show_routes():
    """Quick overview of the routes of the application (dev mode only)"""

    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = f"{rule.endpoint}: {methods} {rule.rule}"
        output.append(line)

    return '<br>'.join(output)


#
# Internal blueprint handling
#

_blueprints_map: dict[str, Blueprint] = {}


def _create_blueprint(container: str) -> Blueprint:
    """Creates a blueprint from a container name."""
    
    bp_module = import_module(ApiUtils.module_import_name(container))

    version = cast(Optional[str], getattr(bp_module, "version", None))

    url_prefix = f"/{version or CoreUtils.create_version(1)}/{container}"

    return Blueprint(container, ApiUtils.module_import_name(container), url_prefix=url_prefix)
        

def _get_blueprints() -> list[Blueprint]:
    """
    First, creates a list of all the applications's blueprints
        
    The blueprints are created based on the available containers.
    Note: In addition, the login and logout views for the flask-security-too extension are overwritten to return a 404.
    """

    not_used_name = '_not_used_blueprint'

    not_used_blueprint = Blueprint(not_used_name, __name__)
    not_used_blueprint.add_url_rule('/logout', 'logout', _abort)
    not_used_blueprint.add_url_rule('/login', 'logout', _abort)
    not_used_blueprint.add_url_rule('/show-routes', 'show-routes', _show_routes)

    _blueprints_map[not_used_name] = not_used_blueprint

    # Create other blueprints based on the available containers
    for container in CoreUtils.get_containers():
        bp: Blueprint = _create_blueprint(container)
        _blueprints_map[container] = bp
        
    return list(_blueprints_map.values())
    

#
# External
#

def get_blueprint(container: str) -> Blueprint:
    """Returns a blueprint by its container name like 'auth', 'stoxs'."""

    bp = _blueprints_map.get(container)
    if bp is None:
        raise ValueError(f"Blueprint for container '{container}' not found.")

    return bp


blueprints = _get_blueprints()
