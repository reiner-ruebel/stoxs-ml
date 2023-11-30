"""
Starting point for the machine learning part of the Stoxs application.

The Stoxs class contains the functionality of the application which is embedded in a Flask environment.

Pre-registered users can register and then log in. Registered users can use the REST API to call the Stoxs functionality.
"""

from typing import Type

from app.core.config import BaseConfig, DevConfig
from app.core.flaskenv.flaskenv import FlaskEnv
from app.core.flaskenv.blueprints import blueprints


def main() -> None:
    config: Type[BaseConfig] = DevConfig # Select Dev, Test, Prod

    flask: FlaskEnv = FlaskEnv(config, blueprints)
    flask.register()
    flask.run()


if __name__ == "__main__":
    main()
