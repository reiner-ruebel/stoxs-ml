import traceback

from flask import jsonify, current_app
from app.core.shared.error_handler_protocol import ErrorHandlerProtocol


class BaseErrorHandler:
    def __init__(self, status_code: int):
        self.status_code = status_code

    def handle_error(self, error: Exception) -> tuple:
        """Log the error and return a JSON response."""
        current_app.logger.error(f'Error {self.status_code}: {str(error)}')
        traceback_str = ''.join(traceback.format_exception(type(error), value=error, tb=error.__traceback__))
        current_app.logger.debug(traceback_str)

        response = jsonify({"error": f"An error occurred: {str(error)}"})
        return response, self.status_code


class InternalServerErrorHandler(BaseErrorHandler):
    def __init__(self):
        super().__init__(500)

    # You can override handle_error here if needed


class NeedApplicationJsoneErrorHandler(BaseErrorHandler):
    def __init__(self):
        super().__init__(415)


error_handlers: list[tuple[int, ErrorHandlerProtocol]] = [
    (500, InternalServerErrorHandler()),
    (415, NeedApplicationJsoneErrorHandler()),
]
