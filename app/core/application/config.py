import os

from app.core.config.config_v1 import BaseConfig, DevConfig, ProdConfig


class Config():
    """ Configuration class """

    _config_object: BaseConfig

    @classmethod
    def get_config_object(cls) -> BaseConfig:
        """ Returns the config object """
        
        cls._config_object = DevConfig() if cls.is_development() else ProdConfig()

        return cls._config_object


    @classmethod
    def is_development(cls) -> bool:
        """ returns True if this is a development environment """

        env = os.getenv('FLASK_ENV', 'development') # Safety-net: make sure this is explicitly set to 'development' or 'production'
        if env == 'development':
            return True
        elif env == 'production':
            return False
        else:
            raise ValueError("Invalid 'FLASK_ENV' setting")


    @classmethod
    def is_production(cls) -> bool:
        """ returns True if this is a production environment """

        return not cls.is_development()
    

    @classmethod
    def is_migration(cls) -> bool:
        """ returns True if this is a migration environment """

        return cls._config_object.CUSTOM_MIGRATION.lower() == 'true'
    
config_object = Config.get_config_object()
    