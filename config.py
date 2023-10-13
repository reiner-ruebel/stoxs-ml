import os

class BaseConfig:
    """ Base configuration. There is a xls helper available to create the code"""
    SECURITY_STATIC_FOLDER = os.environ.get('SECURITY_STATIC_FOLDER', 'static')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')
    
    # Added manually
    DEBUG = False


class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    DEBUG = True
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
