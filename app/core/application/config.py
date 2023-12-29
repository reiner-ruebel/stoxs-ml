import os

from app.core.config.config_v1 import BaseConfig, DevConfig, ProdConfig


def is_development() -> bool:
    """ returns True if this is a development environment """

    env = os.getenv('FLASK_ENV', 'development') # Safety-net: make sure this is explicitly set to 'development' or 'production'
    if env == 'development':
        return True
    elif env == 'production':
        return False
    else:
        raise ValueError("Invalid 'FLASK_ENV' setting")


def is_production() -> bool:
    """ returns True if this is a production environment """

    return not is_development()
    

config_object: BaseConfig = DevConfig() if is_development() else ProdConfig()


def is_migration() -> bool:
    """Returns True if this is a migration environment."""

    return config_object.CUSTOM_MIGRATION.lower() == 'true'
        