from dependency_injector import containers, providers
from flask import Flask

from .config import Config


class HostingServices(containers.DeclarativeContainer):
    """
    Web Application container.
    
    Creates the web app and the config object.
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
    
    # host (flask app is currently the only option)
    host = providers.Singleton(
        Flask,
        flask_name,
        instance_relative_config=True,  # *)
    )
    

# *) if set to True relative filenames for loading the config are assumed to be relative to the instance path instead of the application root.
