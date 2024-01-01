from dependency_injector import containers, providers
from flask import Flask
from flask_restx import Api  # type: ignore

from .config import Config
from app.core import CoreUtils, Strings


class Container(containers.DeclarativeContainer):
    """
    Web Application container.
    
    Creates the flask app and the config object.
    The config object contains all the config values for the app and the extensions.

    Example of how to access an entry for mail: mail_server = container.config.mail.server
    """

    # config
    config_dict = Config.create_container_config()  # contains all the config values for the app and the extensions.

    config = providers.Configuration()
    config.from_dict(config_dict)
    
    # name
    flask_name = __name__
    try :
        flask_name = config.custom.flask_name
    except:
        pass
    
    # flask app
    flask_app = providers.Singleton(
        Flask,
        flask_name,
        instance_relative_config=True,  # *)
    )
    
    version = config.custom.version
    if not isinstance(version, int):
        version = 1
    
    # API
    flask_api = providers.Singleton(
        Api,
        flask_app,
        title=Strings.TITLE,
        version=CoreUtils.create_version(version),
        description=Strings.DESCRIPTION,
        )


# *) if set to True relative filenames for loading the config are assumed to be relative to the instance path instead of the application root.
