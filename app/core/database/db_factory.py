from app.core.application.config import config_object

from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


class DbFactory:
    """Database component for the Flask application."""
    
    @staticmethod
    def create_db() -> SQLAlchemy:
        """Creates the database"""
        
        if config_object.CUSTOM_DB_TYPE != 'strange':
            db = SQLAlchemy()
            fsqla.FsModels.set_db_info(db)

        return db
   