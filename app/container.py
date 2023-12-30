from dependency_injector import containers, providers
import json

from flask import Flask

from .config import Config


class Container(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()

    config.from_dict(Config.create_container_config())
    
    # keep the name 'create_app' as it is used in the wsgi.py file
    create_app = providers.Singleton(
        Flask,
#        __name__,
        config.custom.flask_name,
        instance_relative_config=True  # *)
    )


# *) if set to True relative filenames for loading the config are assumed to be relative to the instance path instead of the application root.    
