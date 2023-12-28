from typing import cast, Type

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from flask_security.core import Security
from flask_security.datastore import UserDatastore

from app.shared.consts import Consts
from app.core.application.app_components import Config, AppComponents as C
from app.core.security.roles import roles
from app.api.auth.models.pre_register import PreRegisterModel

Base = declarative_base()


class DbSeeder:
    """Class for seeding the database with predefined data."""

    _security: Security = cast(Security, C.get_extension(Consts.EXTENSION_SECURITY))

    @classmethod
    def reset(cls) -> None:
        """ Resets the DB. The user datastore and the pre-register are truncated. Then the DB is seeded again. """

        if not Config.is_development():
            raise RuntimeError("Reset operation is not allowed in this environment")
        
        if not cls._userstore_available():
            raise RuntimeError("Userstore is not available")

        try:
            # Start a transaction
            C.db.session.begin()

            # Reset tables
            cls._reset_users_and_roles()
            cls._empty_table(PreRegisterModel)

            # Commit the transaction
            C.db.session.commit()

        except Exception as e:
            C.db.session.rollback()
            raise e

        cls.seed_db()
        

    @classmethod
    def seed_db(cls) -> None:
        """Seed the database with defined roles, permissions and the pre_register table."""

        if not cls.seed_needed():
            return

        if not PreRegisterModel.query.get(C.config_object.CUSTOM_SEED_EMAIL):
            pre_register = PreRegisterModel(email=C.config_object.CUSTOM_SEED_EMAIL, role=C.config_object.CUSTOM_SEED_ROLE)
            C.db.session.add(pre_register)

        us: UserDatastore = cls._security.datastore

        for role_data in roles:
            role = us.find_role(role_data['name'])
            if not role:
                # Create the role if it doesn't exist
                us.create_role(**role_data)

        C.db.session.commit()


    @classmethod
    def seed_needed(cls) -> bool:
        """Check if the 'user' and 'pre_register' tables exist and make sure that no migration is taking place."""
        
        if Config.is_migration():
            return False

        # If we do not have any tables yet, we do not need to seed any data. In fact, we would not be able to do this.
        if not cls._userstore_available():
            return False

        # If the pre_register table is empty we need to seed the tables.
        seed_mail = PreRegisterModel.query.get(C.config_object.CUSTOM_SEED_EMAIL)
        return seed_mail is None


    @classmethod
    def _userstore_available(cls) -> bool:
        engine: Engine = C.db.engine
        inspector = inspect(engine)

        # if either of the tables does not exist we are not able to operate
        return True if 'user' in inspector.get_table_names() and Consts.DB_PRE_REGISTER in inspector.get_table_names() else False

        
    @classmethod
    def _reset_users_and_roles(cls) -> None:
        """ Use datastore's methods to first delete users and then safely empty the roles table. """

        for user in cls._security.datastore.user_model.query.all():
            cls._security.datastore.delete_user(user)

        cls._empty_table(cls._security.datastore.role_model)
        

    @classmethod
    def _empty_table(cls, model: Type[Base]) -> None: # type: ignore
        """ Delete all records in the table """

        C.db.session.query(model).delete()
        C.db.session.commit()
