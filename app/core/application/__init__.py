from importlib import import_module

from flask import Flask

# Dependency Injection
from .config import config
from .database import db
from .blueprints import blueprints
from .extensions import extensions
from .models import models
from .middlewares import middlewares
from .exceptions import error_handlers

from app.core.database.seed_db import DbSeeder


def create_app() -> Flask:
    """ Flask application factory. Initializes and returns the Flask application. """

    app = Flask(__name__) # create

    app.config.from_object(config) # config

    db.init_app(app) # database

    for blueprint in blueprints: # blueprints
        app.register_blueprint(blueprint)
        
    for model in models: # models (migration). Mind the order: after db, before extensions
        import_module(model)
        
    for _, init, kwargs in extensions: # extensions
        init(app, **kwargs)
        
    for middleware in middlewares: # middlewares
        with app.app_context():
            import_module(middleware)
        
    for error_code, handler in error_handlers: # error handlers
        app.register_error_handler(error_code, handler.handle_error)
        
    with app.app_context():
        db_seeder = DbSeeder(db)
        if db_seeder.seed_needed():
            db_seeder.seed_db()

    return app
 