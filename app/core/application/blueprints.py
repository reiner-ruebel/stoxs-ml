from typing import cast, Optional
from importlib import import_module

from flask import Blueprint, abort, current_app

from app.core.shared.utils import get_container, get_containers, create_version
from app.api.shared.utils import module_import_name


#
# blueprints that are not used but are required by flask-security-too.
#

@not_used_blueprint.route('/logout')

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


def create_blueprints() -> None:
    pass

class Blueprints:
    """A class that provides access to the blueprints of the application."""
    
    def __init__(self):
        """
        Creates a list of all the applications's blueprints
        
        The blueprints are created based on the available containers.
        The blueprints are not registered with the application.
        Note: In addition, the login and logout views for the flask-security-too extension are overwritten to return a 404.
        """

        not_used_blueprint = Blueprint('not_used_blueprint', __name__)
        not_used_blueprint.add_url_rule('/logout', 'logout', self._abort)
        not_used_blueprint.add_url_rule('/login', 'logout', self._abort)

         # A map of all blueprints (to be registered) by their container name
        self._blueprints_map: dict[str, Blueprint] = {'not_used_blueprint': not_used_blueprint}

        # Create other blueprints based on the available containers
        for container in get_containers():
            bp: Blueprint = self._create_blueprint(container)
            self._blueprints_map[container] = bp


    def get_blueprints(self) -> list[Blueprint]:
        """Return the list of all Blueprint instances"""

        return list(self._blueprints_map.values())


    def get_blueprint(self, container: str) -> Blueprint:
        """Returns a blueprint by its container name, e.g. 'auth', 'stoxs', ..."""

        bp = self._blueprints_map.get(container)
        if bp is None:
            raise ValueError(f"Blueprint for container '{container}' not found.")

        return bp


    def _create_blueprint(self, container: str) -> Blueprint:
        """Creates a blueprint from a container name."""
    
        bp_module = import_module(module_import_name(container))

        version = cast(Optional[str], getattr(bp_module, "version", None))

        url_prefix = f"/{version or create_version(1)}/{container}"

        return Blueprint(container, module_import_name(container), url_prefix=url_prefix)
        

    @staticmethod
    def _abort():
        """We map the logout endpoint to 404. This is because we do not want to use the flask-security-too extension to logout."""
        abort(404)
