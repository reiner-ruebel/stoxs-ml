from __future__ import annotations

from typing import TypeVar, Generic, Optional
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


def _create_db() -> SQLAlchemy:
    """ Creates the database """
    db: SQLAlchemy = SQLAlchemy()
    fsqla.FsModels.set_db_info(db)
    return db


db: SQLAlchemy = _create_db()


def _db_commit_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            # Log the error or re-raise
            # logger.error(f"Database error occurred: {e}")
            raise
    return wrapper


T = TypeVar('T', bound='db.Model') # type: ignore

class CRUDMixin(Generic[T]):

    @classmethod
    def get_by_id(cls: type[T], id: int) -> Optional[T]:
        return db.session.query(cls).get(id)

    @classmethod
    def create(cls: type[T], **kwargs) -> T:
        instance: T = cls(**kwargs)
        return instance.save()

    @_db_commit_decorator
    def update(self: T, commit: bool=True, **kwargs) -> T:
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            self.save()
        return self

    @_db_commit_decorator
    def save(self: T, commit: bool=True) -> T:
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    @_db_commit_decorator
    def delete(self, commit: bool=True) -> None:
        db.session.delete(self)
        if commit:
            db.session.commit()
    