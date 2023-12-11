"""
Configurations for Flask, DB, ...
"""

import os
from typing import Optional

from dotenv import load_dotenv


# One way of setting the environment variables is to create a .flaskenv file in the root directory of the project.
# If a different file name or options is used, the load_dotenv() call must be adjusted accordingly.
load_dotenv('.flaskenv')


#
# individual configuration settings
#

class CustomConfig:
    """ Customer configuration settings to support specific password policies etc. """
    CUSTOM_REQUIRE_UPPERCASE: bool = True
    CUSTOM_REQUIRE_LOWERCASE: bool = True
    CUSTOM_REQUIRE_DIGITS: bool = True
    CUSTOM_SPECIAL_CHARS: Optional[str] = '!@#%^&*()_+{}:"<>?[]\;\',./|`~' # Note: char '$' not in list
    CUSTOM_USERNAME_NOT_DIFFERENT_FROM_MAIL: bool = True # if the username is a mail address it must be the same as the user's mail address
    CUSTOM_SEED_EMAIL: str = os.environ.get('CUSTOM_SEED_EMAIL', 'admin.user@appmanager.com')
    

class SecurityConfig:
    """ flask-security-too settings """
    SECURITY_PASSWORD_SALT: str = os.environ.get('SECURITY_PASSWORD_SALT', 'some_salt')
    SECURITY_PASSWORD_LENGTH_MIN: str = os.environ.get('SECURITY_PASSWORD_LENGTH_MIN', '12')
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[str] = 'zxcvbn' # as of version 5.3.2, only zxcvbn is supported
    SECURITY_ZXCVBN_MINIMUM_SCORE: int = 4
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[str] = 'best-effort'
    SECURITY_TRACKABLE: bool = True


class MailConfig:
    """ SMTP settings """
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'my.smtp.server')
    MAIL_BACKEND: str = 'smtp'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME', 'username')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '********')
    MAIL_DEFAULT_SENDER: str = os.environ.get('MAIL_DEFAULT_SENDER', 'username@company.com')


#
# base configuration
#
class BaseConfig(CustomConfig, SecurityConfig, MailConfig):
    """ Default configuration options. This should never be used! """
    SITE_NAME: str = os.environ.get('APP_NAME', 'stoxs')
    SECRET_KEY: str = 'not set in base'
    ENVIRONMENT = property(lambda self: self.__class__.__name__)
    DEBUG: bool = False

    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False    


#
# development and production configurations
#

class DevConfig(BaseConfig):
    """ Development setup """
    DEBUG: bool = True
    SECRET_KEY: str = os.environ.get('SECRET_DEV_KEY', 'dev secret key')


class ProdConfig(BaseConfig):
    """ Production setup """
    SECRET_KEY: str = os.environ.get('SECRET_PROD_KEY', 'prod secret key')


#
# config object
#

def _get_config() -> BaseConfig:
    """ Returns the config object """
    return DevConfig() if os.environ.get('FLASK_ENV') == 'development' else ProdConfig()

config: BaseConfig = _get_config()
