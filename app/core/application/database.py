from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla

def _create_db() -> SQLAlchemy:
    """ Creates the database """
    db: SQLAlchemy = SQLAlchemy()
    fsqla.FsModels.set_db_info(db)
    return db


db: SQLAlchemy = _create_db()
