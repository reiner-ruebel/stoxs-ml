from typing import Optional
import os
from datetime import timedelta

from dotenv import load_dotenv

from app.shared.utils import AppUtils


# One way of setting the environment variables is to create a .flaskenv file in the root directory of the project.
# If a different filename is used, the load_dotenv() call must be adjusted accordingly.
# If such a file does not exist, the line below has no effect and the environment must be set by some other means.
load_dotenv('.flaskenv')


#
# Individual configuration settings
#

class _CustomConfig:
    """ Customer configuration settings to support specific password policies, etc. """

    # Explicit password requirements
    CUSTOM_REQUIRE_UPPERCASE = True
    CUSTOM_REQUIRE_LOWERCASE = True
    CUSTOM_REQUIRE_DIGITS = True
    CUSTOM_SPECIAL_CHARS: Optional[str] = '!@#%^&*()_+{}:"<>?[]\;\',./|`~'

    # Seed Database
    CUSTOM_DB_TYPE = os.environ.get('CUSTOM_DB_TYPE', 'sqlite') # 'sqlite' (default), 'postgres', 'mysql', 'mssql'
    CUSTOM_SEED_EMAIL = os.environ.get('CUSTOM_SEED_EMAIL', 'not-a-valid-email-address') # Must be overridden to avoid having a valid mail address in source control.
    CUSTOM_SEED_ROLE = os.environ.get('CUSTOM_SEED_ROLE', '')
    CUSTOM_RESET_CODE = os.environ.get('CUSTOM_RESET_CODE', '1234567890') # to reset and seed the DB. Only possible in dev env.

    # Other
    CUSTOM_USERNAME_NOT_DIFFERENT_FROM_MAIL = True # If the username is an email address, it must match the user's email address.
    CUSTOM_MIGRATION = os.environ.get('CUSTOM_MIGRATION', 'False') # Set to 'True' by flask-migrate to indicate that a DB migration is taking place.
    CUSTOM_BASE_URL = AppUtils.get_base_url()
    

class _SecurityConfig:
    """ flask-security-too settings. This is for REST API only (no CSRF setting). """

    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'some_salt')
    SECURITY_PASSWORD_LENGTH_MIN = os.environ.get('SECURITY_PASSWORD_LENGTH_MIN', '12')
    SECURITY_PASSWORD_COMPLEXITY_CHECKER: Optional[str] = 'zxcvbn' # As of version 5.3.2, only zxcvbn is supported.
    SECURITY_ZXCVBN_MINIMUM_SCORE = 4
    SECURITY_PASSWORD_CHECK_BREACHED: Optional[str] = 'best-effort'
    SECURITY_USERNAME_ENABLE = True # Docu: when set to True, will add support for the user to register a username in addition to an email.
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    SECURITY_FRESHNESS = timedelta(seconds=-1)


class _MailConfig:
    """ SMTP settings """

    # backend
    MAIL_BACKEND = 'smtp' # 'smtp' (default), 'sendmail', 'file', 'locmem', 'console', 'dummy'. If TESTING=True, the default is 'locmem'
    MAIL_PORT = 587 # (Usually) the SSL / TLS settings convert to the following ports: False / False => 25, True / False => 465, False / True => 587 (True / True => not possible)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # account
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp-host-server')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '********')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'smtp-user-name')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'support@company.com')


class _DbConfig:
    """ Database settings """

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class _JwtConfig:
    """ JWT settings """

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'set-the-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class _RestxConfig:
    """ RESTX settings """

    RESTX_ERROR_404_HELP = 'false'
    RESTX_INCLUDE_ALL_MODELS = True


#
# Base Configuration
#

class BaseConfig(_CustomConfig, _SecurityConfig, _MailConfig, _DbConfig, _JwtConfig, _RestxConfig):
    """ Default configuration options. This should never be used! """

    SITE_NAME = os.environ.get('APP_NAME', 'app')
    SECRET_KEY = 'not set in base'
    ENVIRONMENT = os.environ.get('FLASK_ENV', 'development')
    DEBUG = False


#
# Development and Production Configurations
#

class DevConfig(BaseConfig):
    """ Development setup """

    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_DEV_KEY', 'dev secret key')


class ProdConfig(BaseConfig):
    """ Production setup """

    SECRET_KEY = os.environ.get('SECRET_PROD_KEY', 'prod secret key')
