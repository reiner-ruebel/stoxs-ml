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
    

class DevConfig(BaseConfig):
    """ Development setup """
    SECRET_KEY: str = os.environ.get('SECRET_DEV_KEY', 'dev secret key')
