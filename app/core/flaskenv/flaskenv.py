"""
Flask environment
""" 

from typing import Type

from flask import Blueprint, Flask

from app.core.config import BaseConfig


class FlaskEnv:
    """ The app's Flask environment """

    def __init__(self, config: Type[BaseConfig], blueprints:list[Blueprint]) -> None:
        """ Create the app. """
        self.config = config
        self.blueprints = blueprints
        self._app: Flask = Flask(__name__)
        self._app.config.from_object(self.config)
        self._app.config['DEBUG'] = True
        

    def register(self) -> None:
        """ Loads all modules and registers all blueprints """
        for blueprint in self.blueprints:
            self._app.register_blueprint(blueprint)
     

    def run(self) -> None:
        """ Run the app """
        self._app.run()
