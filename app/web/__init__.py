from dependency_injector.wiring import inject, Provide
from flask import Flask

from .container import Container
from .config import Config

@inject
def create_app(app: Flask = Provide[Container.flask_app]) -> Flask:
    return app

Container().wire(modules=[__name__])

__all__ = ['create_app', 'Config']
