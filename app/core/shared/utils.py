import os

from app.shared.consts import Consts
from app.shared.utils import get_application_path


def get_containers() -> list[str]:
    """ Returns a list of blueprint containers.
        Potential blueprint containers must be in the api directory.
        All these directories will be scanned.
        If the scanned directory contains a directory named endpoints, then that directory is considered a blueprint container. """

    containers: list[str] = []

    for container in os.listdir(os.path.join(get_application_path(), Consts.BP_ROOT)):
        if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container)):
            if os.path.isdir(os.path.join(get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS)):
                containers.append(container)

    return containers
    