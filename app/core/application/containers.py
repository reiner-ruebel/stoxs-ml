from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        SQLAlchemy
    )


