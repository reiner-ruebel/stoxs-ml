import os
from typing import Optional

from app.shared.consts import Consts
from app.shared.utils import AppUtils


class Middleware:
    """A class that provides access to the middleware of the application."""

    _middleware_modules: Optional[list[str]] = None

    @classmethod
    def get_modules(cls) -> list[str]:
        """
        Returns a list of middleware modules.

        The list will look like this: ['app.core.middleware.sanitize', 'app.core.middleware.authenticate', ...]
        """
        
        if cls._middleware_modules is not None:
            return cls._middleware_modules
        
        cls._middleware_modules = []
        application_path = AppUtils.get_application_path()

        for middleware in os.listdir(os.path.join(application_path, Consts.MIDDLEWARE)):
            if os.path.isfile(os.path.join(application_path, Consts.MIDDLEWARE, middleware)):
                if middleware.endswith(".py") and (middleware != "__init__.py"):    
                    cls._middleware_modules.append(Consts.MIDDLEWARE.replace("/", ".") + "." + middleware[:-3])

        return cls._middleware_modules
