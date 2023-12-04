"""Flask and other extensions instantiated here.

To avoid circular imports with views and create_app(), extensions are instantiated here. They will be initialized
(calling init_app()) in application.py.
"""

from typing import Callable

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security


security = Security()


extensions: list[tuple[object, Callable[[Flask], None]]] = [
    (security, security.init_app),
]
