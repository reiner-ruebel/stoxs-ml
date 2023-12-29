from importlib import import_module

from flask import Flask

from app.core.application.config import config_object
from app.core.application.blueprints import blueprints
from app.core.application.database import db
from app.core.application.extensions import extensions
from app.core.application.middleware import middleware_modules
from app.core.application.error_handlers import error_handlers


def create_app() -> Flask:
    """Creates and inits the Flask application."""
        
    app = Flask(__name__)
    
    app.config.from_object(config_object)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    db.init_app(app)
        
    for _, _, init, kwargs in extensions:
        init(app, **kwargs)
        
    for middleware in middleware_modules:
        with app.app_context():
            import_module(middleware)
        
    for error_code, handler in error_handlers:
        app.register_error_handler(error_code, handler.handle_error)
        
    return app
