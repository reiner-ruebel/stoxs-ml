from ast import Str
from typing import Union, TypedDict

from .permissions import Permissions


class Roles:
    """ Available roles. """

    APP_ADMIN: str = "app_admin"
    STOXS_ALL: str = "stoxs_all"
    STOXS_BASE: str = "stoxs_base"
    STOXS_PRO: str = "stoxs_pro"


class _RoleDict(TypedDict):
    name: str
    description: str
    permissions: Union[str, list[str]]


roles: list[_RoleDict] = [
    {
        'name': Roles.APP_ADMIN,
        'description': 'Administrator',
        'permissions': Permissions.APP_ADMIN
    },
    {
        'name': Roles.STOXS_ALL,
        'description': 'stoxs admin and stoxs api',
        'permissions': Permissions.STOXS_ADMIN
    },
    {
        'name': Roles.STOXS_BASE,
        'description': 'Machine learning stoxs',
        'permissions': [Permissions.STOXS_GET, Permissions.STOXS_ML]
    },
    {
        'name': Roles.STOXS_PRO,
        'description': 'stoxs get data',
        'permissions': [Permissions.STOXS_GET,]
    },
]
