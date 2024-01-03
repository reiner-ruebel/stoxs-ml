from dependency_injector.wiring import inject, Provide
from flask import Flask

from .container import Container
from .config import Config
from .shared.namespace_factory import NamespaceFactory
from .shared.namespace_docu import NamespaceDocu
from shared.utils import Utils as WebUtils


@inject
def create_app(app: Flask = Provide[Container.flask_app]) -> Flask:
    return app

Container().wire(modules=[__name__])

__all__ = ['create_app', 'Config', 'NamespaceFactory', 'NamespaceDocu', 'WebUtils']
