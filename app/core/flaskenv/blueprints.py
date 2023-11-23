"""
All blueprints are listed in this module
"""

from flask import Blueprint

# list of blueprints (module name, url)
# The default url is the same as the module location. 
_credentials: list[tuple[str, str | None]] = [
    ("account.login", None),
    ("account.register", None),
    ("stoxs/provider", "api")
    ]


def _create_one(credential: tuple[str, str]) -> Blueprint:
    module_name: str = credential[0]
    package_name: str = f"app.api.{module_name}"
    url_prefix:str = "/" + (credential[1] if credential[1] is not None else module_name.replace(".", "/"))

    blueprint: Blueprint = Blueprint(name=module_name, import_name=package_name, url_prefix=url_prefix)
    return blueprint
        

def _create_all() -> list[Blueprint]:
    blueprints: list[Blueprint] = []

    for credential in _credentials:
        blueprint: Blueprint = _create_one(credential)
        blueprints.append(blueprint)

    return blueprints


# all blueprints which want to be registered
all_blueprints: list[Blueprint] = _create_all()
