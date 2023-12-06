"""
Configurations for Flask, DB, ...
"""

import os

from dotenv import load_dotenv


load_dotenv()

class BaseConfig:
    """ Default configuration options. This should never be used! """
    SITE_NAME: str = os.environ.get('APP_NAME', 'stoxs')
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'base secret key')
    ENVIRONMENT = property(lambda self: self.__class__.__name__)
    DEBUG: bool = False

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False    


class DevConfig(BaseConfig):
    """ Development setup """
    DEBUG: bool = True
    SECRET_KEY: str = os.environ.get('SECRET_DEV_KEY', 'dev secret key')


class ProdConfig(BaseConfig):
    """ Production setup """
    SECRET_KEY: str = os.environ.get('SECRET_DEV_KEY', 'dev secret key')


def _get_config() -> BaseConfig:
    """ Returns the config object """
    return DevConfig() if os.environ.get('FLASK_ENV') == 'development' else ProdConfig()

config: BaseConfig = _get_config()
