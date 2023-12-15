from typing import cast, Optional
import os
from importlib import import_module

from flask import Blueprint
from flask_restx import Api # type: ignore

from app.shared.consts import Consts
from app.shared.utils import get_application_path
from app.api.shared.utils import container_import_name


def get_containers() -> list[str]:
    """
    Returns a list of blueprint containers.
    Potential blueprint containers must be in the api directory.
    All these directories will be scanned.
    If the scanned directory contains a directory named endpoints, then that directory is considered a blueprint container.
    """

    containers: list[str] = []

    for container in os.listdir(os.path.join(get_application_path(), Consts.BP_ROOT)):
        if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container)):
            if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS)):
                containers.append(container)

    return containers


def get_middlewares() -> list[str]:
    """
    Returns a list of middlewares.
    All middleware modules must be in the middlware directory.
    The middleware directory must be a sibling of the shared directory.
    """

    middlewares: list[str] = []

    for middleware in os.listdir(os.path.join(get_application_path(), Consts.MIDDLEWARE)):
        if os.path.isfile(os.path.join(get_application_path(), Consts.MIDDLEWARE, middleware)):
            if middleware.endswith(".py") and (middleware != "__init__.py"):    
                middlewares.append(Consts.MIDDLEWARE.replace("/", ".") + "." + middleware[:-3])

    return middlewares
    

def create_bp_from_container(container: str) -> Blueprint:
    """Creates a blueprint from a container name."""
    
    bp_module = import_module(container_import_name(container))

    version = cast(Optional[str], getattr(bp_module, "version", None))

    url_prefix = f"/{version or create_version(1)}/{container}"

    return Blueprint(container, container_import_name(container), url_prefix=url_prefix)


def create_api_from_bp(bp: Blueprint) -> Api:
    """Creates an Api object for a blueprint."""
    
    container = bp.import_name
    bp_module = import_module(container)

    # Default values for API configuration
    api_defaults = {
        'doc': '/docs',
        'title': container,
        'version': create_version(1),
        'description': 'tbd',
        'default': 'default'
    }

    # Update defaults with any attributes found in the module
    kwargs = {attr: getattr(bp_module, attr, default) for attr, default in api_defaults.items()}

    return Api(bp, **kwargs)


def create_version(version: int):
    """Creates a version string from an integer."""
    return 'v' + str(version) if version > 0 else 'default'
