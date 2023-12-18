from typing import Callable, Any

import bleach
import werkzeug
from flask import Flask, current_app
from werkzeug.wrappers import Request


class SanitizeMiddleware:
    def __init__(self, wsgi_app: Callable[[dict[Any, Any], Callable[..., Any]], Any]) -> None:
        self.app = wsgi_app

    def __call__(self, environ: dict, start_response: Callable) -> werkzeug.wrappers.ResponseStream:
        request = Request(environ)

        # Sanitize query parameters
        for key, values in request.args.items(multi=True):
            sanitized_values = [bleach.clean(value) for value in values]
            request.args.setlist(key, sanitized_values)

        # Sanitize form data
        if request.method == "POST":
            for key, values in request.form.items(multi=True):
                sanitized_values = [bleach.clean(value) for value in values]
                request.form.setlist(key, sanitized_values)

        # Continue processing the request
        return self.app(environ, start_response)


SanitizeMiddleware(current_app.wsgi_app)
