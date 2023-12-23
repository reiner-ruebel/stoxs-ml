import typing as t
from types import UnionType
import os
from pathlib import Path


class AppUtils:
    """Support functions that are independent from the application."""

    application_path = None  # Class-level attribute to store the application path

    @classmethod
    def set_application_path(cls, file_path: Path) -> None:
        """
        Set the application path to the directory containing the file.
        
        This should be called from main (AppUtils.set_application_path(__file__)) in order to have access to the root path.
        """

        cls.application_path = Path(file_path).parent


    @classmethod
    def get_application_path(cls) -> Path:
        """Returns the root path of the application."""

        if cls.application_path is None:
            raise ValueError("Application path has not been set.")
        return cls.application_path


    @staticmethod
    def get_module_names(folder: str) -> list[str]:
        """Creates a list of module names without the extension within a folder."""

        return [module[:-3] for module in os.listdir(folder) if module.endswith('.py') and module != '__init__.py']


    @staticmethod
    def flat_field_is_optional(field_type: t.Optional[t.Type]) -> bool:
        """
        Returns True if a (dataclass) field is optional, otherwise False.

        A field is optional if it has a Union type with a NoneType alternative.
        Note that Optional[] is a special form that is converted to a Union with a NoneType option.
        This works for flat unions, not for nested unions.
        
        Examples:
            No annotation => False
            int => False
            Optional[str] => True
            str | None => True
        """

#        field_type = t.get_type_hints(cls).get(field_name, None)
        if field_type is None:
            return False

        origin = t.get_origin(field_type)

        if origin is t.Union or origin is UnionType: # supports Optional[str] and str | None
            return type(None) in t.get_args(field_type)

        return False
    