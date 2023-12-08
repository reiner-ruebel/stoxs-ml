"""
Configurations for Flask, DB, ...
"""

import os

from dotenv import load_dotenv


load_dotenv()

class MailConfig:
    """ SMTP settings """
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'my.smtp.server')
    MAIL_BACKEND = 'smtp'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'username')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '********')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'username@company.com')


class BaseConfig(MailConfig):
    """ Default configuration options. This should never be used! """
    SITE_NAME: str = os.environ.get('APP_NAME', 'stoxs')
    SECURITY_PASSWORD_SALT: str = os.environ.get('SECURITY_PASSWORD_SALT', 'stoxs')
    SECRET_KEY: str = 'not set in base'
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
    SECRET_KEY: str = os.environ.get('SECRET_PROD_KEY', 'prod secret key')


def _get_config() -> BaseConfig:
    """ Returns the config object """
    return DevConfig() if os.environ.get('FLASK_ENV') == 'development' else ProdConfig()

config: BaseConfig = _get_config()
