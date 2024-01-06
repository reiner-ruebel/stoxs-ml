from importlib import import_module
from typing import cast

from dependency_injector.providers import Configuration
from dependency_injector.wiring import Provide, inject
from flask import Flask, request

from app.web.resources import BaseConfig, WsgiServices


class Program:
    """The entry point of the application."""

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
        self._app.config.from_object(self._config_object)
        import_module('app.web.controllers.test')
        

    def run(self) -> None:
        """Run the application."""

        debug: bool = cast(bool, self._config['development'])
        self._app.run(debug=debug)


    def stop(self):
        """Stop the application."""
        self._shutdown_server()


    #
    # private methods
    #

    def _shutdown_server(self) -> None:
        """
        Stops the flask server.
        
        https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
        """

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Could not shutdown the server')
        func()


WsgiServices().wire([__name__])
