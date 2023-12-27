from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


class AppSql:
    """A class that provides access to the database of the application."""
    
    db: SQLAlchemy

    @classmethod
    def create_db(cls) -> SQLAlchemy:
        """Creates the database"""

        cls.db = SQLAlchemy()
        fsqla.FsModels.set_db_info(cls.db)
        return cls.db
   