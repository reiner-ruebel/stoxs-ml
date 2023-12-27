from typing import cast, Optional
from importlib import import_module

from flask import Blueprint, abort, current_app

from app.core.shared.utils import CoreUtils
from app.api.shared.utils import ApiUtils


class Blueprints:
    """A class that provides access to the blueprints of the application."""
    
    _blueprints_map: Optional[dict[str, Blueprint]] = None

    #
    # Public methods
    #

    @classmethod
    def get_blueprints(cls) -> list[Blueprint]:
        """Returns the list of all Blueprint instances."""
        
        bp_map: dict[str, Blueprint] = cls._get_map()
        return list(bp_map.values())
    

    @classmethod
    def get_blueprint(cls, container: str) -> Blueprint:
        """Returns a blueprint by its container name, e.g. 'auth', 'stoxs', ..."""

        if cls._blueprints_map is None:
            raise ValueError("Blueprints not initialized.")

        bp = cls._blueprints_map.get(container)
        if bp is None:
            raise ValueError(f"Blueprint for container '{container}' not found.")

        return bp


    #
    # Static methods to create the blueprints
    #

    @classmethod
    def _get_map(cls) -> dict[str, Blueprint]:
        """
        First, creates a list of all the applications's blueprints
        
        The blueprints are created based on the available containers.
        The blueprints are not registered with the application.
        Note: In addition, the login and logout views for the flask-security-too extension are overwritten to return a 404.
        """

        if cls._blueprints_map is not None:
            return cls._blueprints_map

        not_used_blueprint = Blueprint('not_used_blueprint', __name__)
        not_used_blueprint.add_url_rule('/logout', 'logout', cls._abort)
        not_used_blueprint.add_url_rule('/login', 'logout', cls._abort)
        not_used_blueprint.add_url_rule('/show-routes', 'show-routes', cls._show_routes)

         # A map of all blueprints (to be registered) by their container name
        cls._blueprints_map = {'not_used_blueprint': not_used_blueprint}

        # Create other blueprints based on the available containers
        for container in CoreUtils.get_containers():
            bp: Blueprint = cls._create_blueprint(container)
            cls._blueprints_map[container] = bp
            
        return cls._blueprints_map


    @classmethod
    def _create_blueprint(cls, container: str) -> Blueprint:
        """Creates a blueprint from a container name."""
    
        bp_module = import_module(ApiUtils.module_import_name(container))

        version = cast(Optional[str], getattr(bp_module, "version", None))

        url_prefix = f"/{version or CoreUtils.create_version(1)}/{container}"

        return Blueprint(container, ApiUtils.module_import_name(container), url_prefix=url_prefix)
        

    #
    # Static blueprints to void the flask-security-too login and logout views and to show the routes in dev mode.
    #

    @staticmethod
    def _abort():
        """Overwrites the login and logout views of the flask-security-too extension to return a 404."""

        abort(404)


    @staticmethod
    def _show_routes():
        """Quick overview of the routes of the application (dev mode only)"""

        output = []
        for rule in current_app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            line = f"{rule.endpoint}: {methods} {rule.rule}"
            output.append(line)

        return '<br>'.join(output)
    