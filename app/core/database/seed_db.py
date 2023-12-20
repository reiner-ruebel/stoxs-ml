from typing import Type

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from flask_security.datastore import UserDatastore

from app.shared.consts import Consts
from app.shared.utils import is_development
from app.core.application.extensions import security
from app.core.application.config import CustomConfig
from app.core.security.roles import roles
from app.api.auth.models.pre_register import PreRegisterModel

Base = declarative_base()


class DbSeeder:
    """ Seed the database with defined roles, permissions and the pre_register table. """

    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db


    def seed_needed(self) -> bool:
        """ Check if the 'user' and 'pre_register' tables exist """
        
        # If we do not have any tables yet, we do not need to seed any data. In fact, we would not be able to do this.
        if not self._userstore_available():
            return False

        # If the pre_register table is empty we need to seed the tables.
        seed_mail = PreRegisterModel.query.get(CustomConfig.CUSTOM_SEED_EMAIL)
        return seed_mail is None


    def seed_db(self) -> None:
        """ Seed the database with defined roles, permissions and the pre_register table. """

        if not PreRegisterModel.query.get(CustomConfig.CUSTOM_SEED_EMAIL):
            pre_register = PreRegisterModel(email=CustomConfig.CUSTOM_SEED_EMAIL, role=CustomConfig.CUSTOM_SEED_ROLE)
            self.db.session.add(pre_register)

        us: UserDatastore = security.datastore

        for role_data in roles:
            role = us.find_role(role_data['name'])
            if not role:
                # Create the role if it doesn't exist
                us.create_role(**role_data)

        self.db.session.commit()


    def reset(self) -> None:
        """ Resets the DB. The user datastore and the pre-register are truncated. Then the DB is seeded again. """

        if not is_development():
            raise RuntimeError("Reset operation is not allowed in this environment")
        
        if not self._userstore_available():
            raise RuntimeError("Userstore is not available")

        try:
            # Start a transaction
            self.db.session.begin()

            # Reset tables
            self._reset_users_and_roles()
            self._empty_table(PreRegisterModel)

            # Commit the transaction
            self.db.session.commit()

        except Exception as e:
            self.db.session.rollback()
            raise e

        self.seed_db()
        

    def _userstore_available(self) -> bool:
        engine: Engine = self.db.engine
        inspector = inspect(engine)

        # if either of the tables does not exist we are not able to operate
        return True if 'user' in inspector.get_table_names() and Consts.DB_PRE_REGISTER in inspector.get_table_names() else False

        
    def _reset_users_and_roles(self) -> None:
        """ Use datastore's methods to first delete users and then safely empty the roles table. """
        for user in security.datastore.user_model.query.all():
            security.datastore.delete_user(user)

        self._empty_table(security.datastore.role_model)
        

    def _empty_table(self, model: Type[Base]) -> None: # type: ignore
        """ Delete all records in the table """
        self.db.session.query(model).delete()
        self.db.session.commit()
