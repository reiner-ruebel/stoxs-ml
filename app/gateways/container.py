from dependency_injector import containers, providers
from flask_sqlalchemy import SQLAlchemy


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    config.from_dict({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        # Add any additional configuration as needed
    })

    db = providers.Singleton(
        SQLAlchemy,
        engine_options={'connect_args': {'check_same_thread': False}}
    )