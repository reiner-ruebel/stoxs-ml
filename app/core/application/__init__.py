from importlib import import_module

from flask import Flask

# Dependency injection: For testing purposes, etc., create replacement modules, such as extensions_test.
from .config import config
from .database import db
from .blueprints import create_blueprints, get_blueprints
from .apis import create_apis
from .extensions import extensions
from .middleware import middleware_modules
from .exceptions import error_handlers

from app.core.database.seed_db import DbSeeder


def create_app() -> Flask:
    """Flask application factory. Initializes and returns the Flask application."""

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    create_blueprints()
        
    create_apis()
        
    for blueprint in get_blueprints():
        app.register_blueprint(blueprint)

    for _, init, kwargs in extensions:
        init(app, **kwargs)
        
    for middleware in middleware_modules:
        with app.app_context():
            import_module(middleware)
        
    for error_code, handler in error_handlers:
        app.register_error_handler(error_code, handler.handle_error)
        
    if config.CUSTOM_MIGRATION != 'true':
        with app.app_context():
            db_seeder = DbSeeder(db)
            if db_seeder.seed_needed():
                db_seeder.seed_db()
                
    return app
 