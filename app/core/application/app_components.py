from importlib import import_module

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy

# In order to test the application with different components, like an in-memory DB or less blueprints, change the imports below.
from app.core.application.config import Config, BaseConfig
from app.core.application.blueprints import Blueprints
from app.core.application.database import AppSql
from app.core.application.apis import Apis
from app.core.application.extensions import Extensions
from app.core.application.middleware import Middleware
from app.core.application.error_handlers import ErrorHandlers

from app.shared.AppTypes import Extension
from app.core.shared.error_handler_protocol import ErrorHandlerProtocol


class AppComponents:
    """
    Dependency injection-like components for the Flask application.
    
    Classes and methods which needs access to the db and other components should import them from here, not from the modules where they are defined.
    """
    
    config_object: BaseConfig
    db: SQLAlchemy
    blueprints: list[Blueprint]
    _extensions: list[Extension]
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
        cls._apis_created = Apis.create_apis()  # Create the APIs after the blueprints are created and before the blueprints are registered.
        cls._extensions = Extensions.get_extensions(cls.db)  # Some extensions need the db for their initialization.
        cls.middleware_modules = Middleware.get_modules()
        cls.error_handlers = ErrorHandlers.get_handlers()

        cls._init_ok = True
    
    
    @classmethod
    def init_app(cls, app: Flask) -> None:
        """Initializes the Flask application with the components."""
        
        if (cls._init_ok == False):
            # We could initialize here, but that is not the established contract with the users of this class.
            raise Exception("The components have not been initialized.")
        
        app.config.from_object(cls.config_object)

        cls.db.init_app(app)
        
        for blueprint in cls.blueprints:
            app.register_blueprint(blueprint)

        for _, _, init, kwargs in cls._extensions:
            init(app, **kwargs)
        
        for middleware in cls.middleware_modules:
            with app.app_context():
                import_module(middleware)
        
        for error_code, handler in cls.error_handlers:
            app.register_error_handler(error_code, handler.handle_error)
            

    @classmethod
    def get_extension(cls, extension_name: str) -> object:
        """Returns an extension by its name."""

        for name, ext_object, _, _ in cls._extensions:
            if name == extension_name:
                return ext_object

        raise ValueError(f"Extension '{extension_name}' not found")
