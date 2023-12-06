from typing import Protocol, Tuple
from flask import Response
from werkzeug.exceptions import HTTPException


class ErrorHandlerProtocol(Protocol):
    def handle_error(self, error: HTTPException) -> Tuple[Response, int]:
        pass

