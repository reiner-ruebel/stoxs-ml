from typing import Optional
from importlib import import_module

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy

from app.core.application.config import Config, BaseConfig
from app.core.application.blueprints import Blueprints
from app.core.application.database import AppSql
from app.core.application.apis import Apis
from app.core.application.extensions import Extension, Extensions
from app.core.application.middleware import Middleware
from app.core.application.error_handlers import ErrorHandlers
from app.core.database.seed_db import DbSeeder
from app.core.shared.error_handler_protocol import ErrorHandlerProtocol


class AppComponents:
    """Dependency injection credentials for the Flask application"""
    
    config_object: BaseConfig
    db: SQLAlchemy
    blueprints: list[Blueprint]
    extensions: list[Extension]
    middleware_modules: list[str]
    error_handlers: list[tuple[int, ErrorHandlerProtocol]]
    
    _apis_created: bool = False
    _init_ok = False

    #
    # Public methods
    #

    @classmethod
    def initialize(cls) -> None:
        """
        Dependency Injection: Initializes the components.
        
        Change to test the application with different components, like an in-memory DB or less blueprints.
        """
        
        cls.config_object = Config.get_config_object()
        cls.db = AppSql.create_db()
        cls.blueprints = Blueprints.get_blueprints()
        cls._apis_created = Apis.create_apis() # Create the APIs after the blueprints are created and before the blueprints are registered.
        cls.extensions = Extensions.get_extensions()
        cls.middleware_modules = Middleware.get_modules()
        cls.error_handlers = ErrorHandlers.get_handlers()

        cls._check_components()

        cls._init_ok = True
    
    
    @classmethod
    def init_app(cls, app: Flask) -> None:
        """Initializes the Flask application with the components."""
        
        if (cls._init_ok == False):
            raise Exception("The components have not been initialized.") # We could initialize here but not is not the established contract with the users of this class.
        
        app.config.from_object(cls.config_object)

        cls.db.init_app(app) # type: ignore
        
        for blueprint in cls.blueprints: # type: ignore
            app.register_blueprint(blueprint)

        for _, init, kwargs in cls.extensions: # type: ignore
            init(app, **kwargs)
        
        for middleware in cls.middleware_modules:
            with app.app_context():
                import_module(middleware)
        
        for error_code, handler in cls.error_handlers:
            app.register_error_handler(error_code, handler.handle_error)
        
        if cls.config_object.CUSTOM_MIGRATION.lower() != 'true':
            with app.app_context():
                db_seeder = DbSeeder(cls.db)
                if db_seeder.seed_needed():
                    db_seeder.seed_db()
                    

    #
    # Private methods
    #

    @classmethod
    def _check_components(cls):
        """Checks if the components have been initialized."""
        
        if cls.config_object is None:
            raise Exception("The config object has not been initialized.")

        if cls.db is None:
            raise Exception("The database has not been initialized.")

        if cls.blueprints is None:
            raise Exception("The blueprints have not been initialized.")

        if cls._apis_created is None:
            raise Exception("The APIs have not been created.")

        if cls.extensions is None:
            raise Exception("The extensions have not been initialized.")

        if cls.middleware_modules is None:
            raise Exception("The middleware modules have not been initialized.")

        if cls.error_handlers is None:
            raise Exception("The error handlers have not been initialized.")
        