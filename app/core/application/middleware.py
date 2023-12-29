import os

from app.shared.consts import Consts
from app.shared.utils import AppUtils


_middleware_modules: list[str] = []

def _get_modules() -> list[str]:
    """
    Returns a list of middleware modules.

    The list will look like this: ['app.core.middleware.sanitize', 'app.core.middleware.authenticate', ...]
    """
        
    application_path = AppUtils.get_application_path()

    for middleware in os.listdir(os.path.join(application_path, Consts.MIDDLEWARE)):
        if os.path.isfile(os.path.join(application_path, Consts.MIDDLEWARE, middleware)):
            if middleware.endswith(".py") and (middleware != "__init__.py"):    
                _middleware_modules.append(Consts.MIDDLEWARE.replace("/", ".") + "." + middleware[:-3])

    return _middleware_modules

middleware_modules = _get_modules()
