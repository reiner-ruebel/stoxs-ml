from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


class AppSql:
    """Database component for the Flask application."""
    
    @staticmethod
    def create_db() -> SQLAlchemy:
        """Creates the database"""

        db = SQLAlchemy()
        fsqla.FsModels.set_db_info(db)
        return db
   