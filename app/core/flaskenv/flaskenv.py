"""
Flask environment
""" 

from importlib import import_module
from typing import Type

from flask import Flask

from app.core.flaskenv.blueprints import all_blueprints
from app.core.config import BaseConfig


class FlaskEnv:
    """ The app's Flask environment """

    def __init__(self, config: Type[BaseConfig]) -> None:
        """ Create the app. """
        self.config = config
        self._app: Flask = Flask(__name__)
        self._app.config.from_object(self.config)
        

    def blueprints(self) -> None:
        """ Loads all modules and registers all blueprints """
        for blueprint in all_blueprints:
            import_module(blueprint.import_name)
            self._app.register_blueprint(blueprint)
     

    def run(self) -> None:
        """ Run the app """
        self._app.run()
