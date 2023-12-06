"""
The Flask application creation factory.
""" 

from importlib import import_module

from flask import Flask

from app.core.application.credentials import Credentials


def create_app(credentials: Credentials) -> Flask:
    """
    Flask application factory. Initializes and returns the Flask application.

    The credentials such as blueprints, error handlers, ... are injected and initialized.
    """

    app = Flask(__name__) # create

    app.config.from_object(credentials.config) # config

    credentials.db.init_app(app) # database

    for blueprint in credentials.blueprints: # blueprints
        app.register_blueprint(blueprint)
        
    for model in credentials.models: # models (migration). Mind the order: after db, before extensions
        import_module(model)
        
    for _, init, kwargs in credentials.extensions: # extensions
        init(app, **kwargs)
        
    for error_code, handler in credentials.error_handlers: # error handlers
        app.register_error_handler(error_code, handler.handle_error)

    return app
 