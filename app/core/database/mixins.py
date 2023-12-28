import typing as t
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from app.core.application.database import db


# Developer note: Could not get mypy to recognize the bound part of the type variable, so I had to use type: ignore.
T = t.TypeVar('T', bound='AppSql.db.Model')  # type: ignore
F = t.TypeVar('F', bound=t.Callable[..., t.Any])   # Generic type for functions


class CrudMixin(t.Generic[T]):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    
    @staticmethod
    def _db_commit_decorator(func: F) -> F:
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
    def get_by_id(cls: type[T], id: int) -> t.Optional[T]:
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
