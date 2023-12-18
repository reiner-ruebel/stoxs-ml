"""
Configurations for Flask, DB, ...
"""

import os
from datetime import timedelta
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
    # explicit password requirements
    CUSTOM_REQUIRE_UPPERCASE: bool = True
    CUSTOM_REQUIRE_LOWERCASE: bool = True
    CUSTOM_REQUIRE_DIGITS: bool = True
    CUSTOM_SPECIAL_CHARS: Optional[str] = '!@#%^&*()_+{}:"<>?[]\;\',./|`~' # Note: char '$' not in list
    # seed database
    CUSTOM_SEED_EMAIL: str = os.environ.get('CUSTOM_SEED_EMAIL', 'not-a-valid-email-address') # Need to be overwritten to avoid to have a valid mail address in the code / source control
    CUSTOM_SEED_ROLE: str = os.environ.get('CUSTOM_SEED_ROLE', '')
    CUSTOM_RESET_CODE: str = os.environ.get('CUSTOM_RESET_CODE', '1234567890') # needed to reset and seed the DB. Only possible in dev env. Not a "secure" pw, intended to avoid accidental resets.
    # other
    CUSTOM_USERNAME_NOT_DIFFERENT_FROM_MAIL: bool = True # if the username is a mail address it must be the same as the user's mail address
    CUSTOM_MIGRATION: str = os.environ.get('CUSTOM_MIGRATION', 'false') # Set to 'true' to indicate that a DB migration is happening.
    CUSTOM_BASE_URL = os.environ.get('CUSTOM_BASE_URL', 'http://localhost:5000')
    

class SecurityConfig:
    """ flask-security-too settings. This is for API-only (no CSRF setting). """
    SECURITY_PASSWORD_SALT: str = os.environ.get('SECURITY_PASSWORD_SALT', 'some_salt')
    SECURITY_PASSWORD_LENGTH_MIN: str = os.environ.get('SECURITY_PASSWORD_LENGTH_MIN', '12')
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[str] = 'zxcvbn' # as of version 5.3.2, only zxcvbn is supported
    SECURITY_ZXCVBN_MINIMUM_SCORE: int = 4
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[str] = 'best-effort'
    SECURITY_USERNAME_ENABLE: bool = True # Docu: when set to True, will add support for the user to register a username in addition to an email.
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS: bool = True
    SECURITY_FRESHNESS = timedelta(seconds=-1)


class MailConfig:
    """ SMTP settings """
    # backend
    MAIL_BACKEND: str = 'smtp' # 'smtp' (default), 'sendmail', 'file', 'locmem', 'console', 'dummy'. If TESTING=True, the default is 'locmem'
    MAIL_PORT: int = 587 # (Usually) the SSL / TLS settings convert to the following ports: False / False => 25, True / False => 465, False / True => 587 (True / True => not possible)
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    # account
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp-host-server')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '********')
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME', 'smtp-user-name')
    MAIL_DEFAULT_SENDER: str = os.environ.get('MAIL_DEFAULT_SENDER', 'support@company.com')


class DbConfig:
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False    
    

class JwtConfig:
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', 'set-the-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class RestxConfig:
    RESTX_ERROR_404_HELP: str = 'false'


#
# base configuration
#

class BaseConfig(CustomConfig, SecurityConfig, MailConfig, DbConfig, JwtConfig, RestxConfig):
    """ Default configuration options. This should never be used! """
    SITE_NAME: str = os.environ.get('APP_NAME', 'app')
    SECRET_KEY: str = 'not set in base'
    ENVIRONMENT = os.environ.get('FLASK_ENV', 'development')
    DEBUG: bool = False



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
