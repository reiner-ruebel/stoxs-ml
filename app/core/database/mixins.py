from typing import TypeVar, Generic, Optional, Callable, Any, cast
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


from app.core.application.database import AppSql

T = TypeVar('T', bound='AppSql.db.Model') # type: ignore
F = TypeVar('F', bound=Callable[..., Any])  # Generic type for functions


class CrudMixin(Generic[T]):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    
    @staticmethod
    def _db_commit_decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                return result
            except SQLAlchemyError as e:
                AppSql.db.session.rollback()
                raise

        return cast(F, wrapper)  # Cast to maintain the return type


    @classmethod
    def get_by_id(cls: type[T], id: int) -> Optional[T]:
        return AppSql.db.session.query(cls).get(id)


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
        AppSql.db.session.add(self)
        if commit:
            AppSql.db.session.commit()
        return self


    @_db_commit_decorator
    def delete(self, commit: bool=True) -> None:
        AppSql.db.session.delete(self)
        if commit:
            AppSql.db.session.commit()
