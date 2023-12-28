from flask import Blueprint

# To test the application with different components, such as an in-memory DB or fewer blueprints, change the imports below.
# These modules should not be imported anywhere else in the application.
# Components should be used from the AppComponents class.
from app.core.application.blueprints import Blueprints
from app.core.application.apis import Apis
from app.core.application.extensions import extensions
from app.core.application.middleware import Middleware
from app.core.application.error_handlers import ErrorHandlers

from app.shared.AppTypes import Extension
from app.core.shared.error_handler_protocol import ErrorHandlerProtocol


class AppComponents:
    """
    Dependency injection-like components for the Flask application.
    
    Classes and methods which needs access to the db and other components should import them from here, not from the modules where they are defined.
    """
    
    blueprints: list[Blueprint]
    extensions: list[Extension]
    middleware_modules: list[str]
    error_handlers: list[tuple[int, ErrorHandlerProtocol]]
    

    @classmethod
    def initialize(cls) -> None:
        """
        Dependency Injection: Initializes the components.
        
        Change to test the application with different components, like an in-memory DB or less blueprints.
        """
        
        cls.blueprints = Blueprints.get_blueprints()
        Apis.create_apis()  # Create the APIs after the blueprints are created and before the blueprints are registered.
        cls.extensions = extensions
        cls.middleware_modules = Middleware.get_modules()
        cls.error_handlers = ErrorHandlers.get_handlers()
    
    
    @classmethod
    def get_extension(cls, extension_name: str) -> object:
        """Returns an extension by its name."""

        for name, ext_object, _, _ in cls.extensions:
            if name == extension_name:
                return ext_object

        raise ValueError(f"Extension '{extension_name}' not found")
