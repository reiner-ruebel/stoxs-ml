import os
from importlib import import_module
from typing import cast

from dependency_injector.providers import Configuration
from dependency_injector.wiring import Provide, inject
from flask import Flask, request

from .iprogram import IProgram
from app import Consts
from app.web.resources import BaseConfig, WsgiServices


class FlaskProgram(IProgram):
    """Implementation of the IProgram interface to init and run the app."""

    @inject
    def __init__(self,
                 app: Flask = Provide[WsgiServices.app],
                 config: Configuration = Provide[WsgiServices.config],
                 config_object: BaseConfig = Provide[WsgiServices.config_object]
                 ) -> None:
        """Create and init the flask app"""

        self._config = config
        self._app = app
        self._config_object = config_object
        
        self._setup()

        with self._app.app_context():
            import_module('app.web.controllers.test1')
        

    def run(self) -> None:
        """Run the application."""

        self._app.run(debug=self._development)


    def stop(self):
        """Stop the application."""
        self._shutdown_server()


    #
    # private methods
    #

    def _setup(self) -> None:
        """Setup the application."""

        self._app.config.from_object(self._config_object)
        self._development = cast(bool, self._config['development'])
            
    def _create_rules(self):
        """Create the routes of the application."""

        if self._development:
            self._app.add_url_rule(rule='/show', endpoint='show_my_routes', view_func=self._show_routes)


    def _shutdown_server(self) -> None:
        """
        Stops the flask server.
        
        https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
        """

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Could not shutdown the server')
        func()


    def _show_routes(self):
        """Quick overview of the routes of the application (dev mode only)"""

        output: list[str] = []

        for rule in self._app.url_map.iter_rules():
            if rule.methods is None:
                continue
            methods = ','.join(sorted(rule.methods))
            line = f"{rule.rule} => {methods} => {rule.endpoint}"
            output.append(line)

        return '<br>'.join(output)
    

    @staticmethod
    def _find_controllers() -> list[str]:
        controllers: list[str] = []

        for entry in os.listdir(Consts.CONTROLLER_ROOT):
            full_path = os.path.join(Consts.CONTROLLER_ROOT, entry)
            if os.path.isfile(full_path) and entry.endswith('.py'):
                module_path = full_path.replace(os.path.sep, '.')
                module, _ = os.path.splitext(module_path)

        return controllers


WsgiServices().wire([__name__])
