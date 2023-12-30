import typing as t
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import DeclarativeBase

from app.core.application.containers import Container


Base = DeclarativeBase()  # type: ignore

T = t.TypeVar('T', bound='Base')  # type: ignore
F = t.TypeVar('F', bound=t.Callable[..., t.Any])   # Generic type for functions


class CrudMixin(t.Generic[T]):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    
    @staticmethod
    @inject
    def _db_commit_decorator(func: F, db: SQLAlchemy = Provide[Container.db]) -> F:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            try:
                result = func(*args, **kwargs)
                return result
            except SQLAlchemyError as e:
                db.session.rollback()
                raise

        return t.cast(F, wrapper)  # Cast to maintain the return type


    @classmethod
    @inject
    def get_by_id(cls: type[T], id: int, db: SQLAlchemy = Provide[Container.db]) -> t.Optional[T]:
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
