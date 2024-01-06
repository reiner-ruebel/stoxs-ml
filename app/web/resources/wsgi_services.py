from typing import Any, Optional, cast

from dependency_injector import containers, providers

from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_restx import Api
from flask_mailman import Mail
from flask_jwt_extended import JWTManager

from .config import Config


class WsgiServices(containers.DeclarativeContainer):
    """
    Web Application container.
    
    Creates the web app and the config object.
    The config object contains all the config values for the app and the extensions.

    Example of how to access an entry for mail: mail_server = container.config.mail.server
    """
    
    # Dependency injection config: https://python-dependency-injector.ets-labs.org/index.html

    config_dict = Config.create_container_config()  # contains all the config values for the app and the extensions.

    config = providers.Configuration(strict=True)  # In strict mode configuration provider raises an error on access to any undefined option.
    config.from_dict(config_dict)
    config.development.from_value(Config.is_development())
    config.production.from_value(Config.is_production())
    config.migration.from_value(Config.is_migration())

    config_object = Config.get_config_object()  # for flask only


    # Flask: https://flask.palletsprojects.com/en/latest/

    flask_name = __name__
    try :
        flask_name = config.custom.flask_name
    except:
        pass
    
    app = providers.Singleton(
        Flask,
        flask_name,
        instance_relative_config=True,  # if set to True relative filenames for loading the config are assumed to be relative to the instance path instead of the application root.
    )
    

    # Database: https://flask-sqlalchemy.palletsprojects.com/en/latest/

    db = providers.Singleton(
        SQLAlchemy,
        app
        )


    # Babel: https://python-babel.github.io/flask-babel/

    def _get_locale(self) -> Optional[str]:
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.
        return request.accept_languages.best_match(['de', 'fr', 'en'])

    def _get_timezone(self) -> Any:
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone
        
    babel = providers.Singleton(
        Babel,
        app,
        locale_selector=_get_locale,
        timezone_selector=_get_timezone,
        )
    

    # Restx: https://flask-restx.readthedocs.io/en/latest/

    api = providers.Singleton(
        Api,
        app = app,
        version = config.api.version,
        title = config.api.title,
        description = config.api.description,
        )
    

    # Mail: https://pythonhosted.org/Flask-Mail/

    mail = providers.Singleton(
        Mail,
        app
        )
    

    # JWT: https://pythonhosted.org/Flask-JWT/

    jwt = providers.Singleton(
        JWTManager,
        app
        )

