from flask import Flask

def create_app(config_object):
    app = Flask(__name__)
    
    app.config.from_object(config_object)
    
    # Initialize services like databases, mail etc.
    # Equivalent to ConfigureServices in ASP.NET
    # from .services import init_services
    # init_services(app)

    # Register middleware and routes
    # from . import routes, middleware
    # routes.init_app(app)
    # middleware.init_app(app)
    
    return app
