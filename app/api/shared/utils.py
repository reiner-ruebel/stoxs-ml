from typing import Collection, Optional, Union, Any, cast # type: ignore
import os
from functools import wraps

from marshmallow import ValidationError
from flask import Response, request, Request

from app.shared.AppTypes import Api_Response
from app.shared.utils import AppUtils
from app.shared.consts import Consts
from app.shared.http_status_codes import HttpStatusCodes, is_success
from app.api.shared.errors import error_map


class ApiUtils:
    """A class that provides access to the APIs of the application."""
    
    _bp_dot_root = Consts.BP_ROOT.replace('/', '.')

    @classmethod
    def endpoints(cls, container: str) -> list[str]:
        """Returns a list of all endpoints within a blueprint container"""

        modules: list[str] = AppUtils.get_module_names(os.path.join(AppUtils.get_application_path(), Consts.BP_ROOT, container, Consts.ENDPOINTS))
        return [f"{cls._bp_dot_root}.{container}.{Consts.ENDPOINTS}.{module}" for module in modules]


    @staticmethod
    def module_import_name(container: str) -> str:
        """Returns the import name of the module of a blueprint container. Example: 'auth' => 'app.api.auth'"""
        return f"{Consts.BP_ROOT.replace('/', '.')}.{container}"


    @classmethod
    def create_api_response(cls, message: dict | list[str] | str, status_code: int | None=None, ok: bool=True) -> Api_Response:
        """
        Creates a tuple of a response dict and a status code.

        If the input is a string, it will be converted to a dictionary with the key 'message' or 'error' depending on the status code.
        If the status code is not provided, it will be set to 200 if ok is True, otherwise it will be set to 400.
        """

        if status_code is None:
            status_code = HttpStatusCodes.HTTP_200_OK if ok else HttpStatusCodes.HTTP_400_BAD_REQUEST

        str_message: str = cast(str, message) if isinstance(message, str) else ", ".join(cast(list[str], message)) if isinstance(message, list) else ""
        json: Collection[Any] = message if isinstance(message, dict) else {'message' if is_success(status_code) else cls._create_error(str_message)}

        return (json, status_code) # type: ignore


    @classmethod
    def _create_error(cls, code_or_message: str) -> dict:
        """ Creates an error dictionary with the given message. """

        message = error_map.get(code_or_message, code_or_message) # get the corresponding message if we have a code, else the massage has been provided
        code = None if message == code_or_message else code_or_message
        documentation_url = f"{AppUtils.get_base_url()}.ERRORs#{code}" if code is not None else None

        inner = {
            Consts.MESSAGE: message,
        }
    
        if code is not None and documentation_url is not None:
            inner["documentation_url"] = documentation_url
            inner[Consts.ERROR] = code


        return {
            Consts.ERROR: inner
        }


    @classmethod
    def validate_request(cls, schema_class):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    request_data = cls.create_data(request)
                    if request_data is None:
                        return cls.create_api_response("No_data_provided", HttpStatusCodes.HTTP_400_BAD_REQUEST)

                    schema = schema_class()
                    model = schema.load(request_data)
                    return func(*args, **kwargs, model=model)
                except ValidationError as err:
                    return cls.create_api_response(err.messages, ok = False)
            return wrapper
        return decorator


    @classmethod
    def _create_data(cls, request: Request) -> Optional[dict[str, Any]]:
        """ Returns the json data of a request casted to a dict or None if no data was provided """

        json_data = request.json
        return None if json_data is None else cast(dict[str, Any], json_data)


    @staticmethod
    def create_restx_model_names(module_name: str) -> tuple[str, str]:
        """
        Creates a tuple of a swagger model name and a response model name.
        This method is typically called with __name__ as argument, e.g. create_restx_model_names(__name__)
        """
    
        name: str = AppUtils.get_leaf(module_name).capitalize()

        return Consts.SWAGGER_MODEL + name, Consts.RESPONSE_MODEL + name
