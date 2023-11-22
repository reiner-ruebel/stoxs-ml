"""
Starting point for the machine learning part of the Stoxs application.

The Stoxs class contains the functionality of the application which is embedded in a Flask environment.

Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import Type

from app.core.config import BaseConfig, DevConfig
from app.core.flaskenv.flaskenv import FlaskEnv


def main(config: Type[BaseConfig]) -> None:
    flask: FlaskEnv = FlaskEnv(config)
    flask.blueprints()
    flask.run()


if __name__ == "__main__":
    config: Type[BaseConfig] = DevConfig # Select Dev, Test, Prod
    main(config)
