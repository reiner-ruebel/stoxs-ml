from typing import Protocol

from flask import Response
from werkzeug.exceptions import HTTPException


class ErrorHandlerProtocol(Protocol):
    def handle_error(self, error: HTTPException) -> tuple[Response, int]:
        pass
