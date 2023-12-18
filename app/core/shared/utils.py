import os

from app.shared.consts import Consts
from app.shared.utils import get_application_path


def get_containers() -> list[str]:
    """
    Returns a list of blueprint containers.
    The list will look like this: ['auth', 'admin', ...]
    Potential blueprint containers must be located in the api root directory.
    All these directories are scanned.
    If the scanned directory contains a directory named endpoints, then that directory is considered a blueprint container.
    """

    containers: list[str] = []

    for container in os.listdir(os.path.join(get_application_path(), Consts.BP_ROOT)):
        if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container)):
            if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS)):
                containers.append(container)

    return containers


def get_middleware_modules() -> list[str]:
    """
    Returns a list of middleware modules.
    The list will look like this: ['app.core.middleware.sanitize', 'app.core.middleware.authenticate', ...]
    All middleware modules must be in the middleware directory.
    The middleware directory must be a sibling of the app/core/shared directory.
    """

    middleware_modules: list[str] = []

    for middleware in os.listdir(os.path.join(get_application_path(), Consts.MIDDLEWARE)):
        if os.path.isfile(os.path.join(get_application_path(), Consts.MIDDLEWARE, middleware)):
            if middleware.endswith(".py") and (middleware != "__init__.py"):    
                middleware_modules.append(Consts.MIDDLEWARE.replace("/", ".") + "." + middleware[:-3])

    return middleware_modules
    

def create_version(version: int):
    """Creates a version string from an integer."""
    return 'v' + str(version) if version > 0 else 'default'
