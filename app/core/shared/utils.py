import os

from app.shared.consts import Consts
from app.shared.utils import AppUtils


class CoreUtils:
    """A class that provides access to the core utilities of the application."""

    @staticmethod
    def get_container(module: str) -> str:
        """ Retrieves the blueprint container name (like 'auth') from an endpoint module (app.api.auth.endpoints.register), typically called like get_container(__name__) """

        segments = module.split(".")

        try:
            endpoints_index = segments.index(Consts.ENDPOINTS)
        except ValueError: 
            raise Exception(f"Could not detect a blueprint container for the module '{module}'.")

        if endpoints_index >= 1:
            parent_directory = segments[endpoints_index - 1]
            return parent_directory
        else:
            raise Exception(f"The module '{module}' is in an '{Consts.ENDPOINTS}' folder that does not follow the standard naming conventions.")


    @staticmethod
    def get_containers() -> list[str]:
        """
        Returns a list of blueprint containers.

        The list will look like this: ['auth', 'admin', ...]
        Potential blueprint containers must be located in the api root directory.
        All these directories are scanned.
        If the scanned directory contains a directory named endpoints, then that directory is considered a blueprint container.
        """

        containers: list[str] = []
        application_path = AppUtils.get_application_path()

        for container in os.listdir(os.path.join(application_path, Consts.BP_ROOT)):
            if os.path.isdir(os.path.join(application_path, Consts.BP_ROOT, container)):
                if os.path.isdir(os.path.join(application_path, Consts.BP_ROOT, container, Consts.ENDPOINTS)):
                    containers.append(container)

        return containers


    @staticmethod
    def create_version(version: int):
        """Creates a version string from an integer."""
        return 'v' + str(version) if version > 0 else 'default'
