from flask import Flask

from .container import Container


class WebApp:
    """
    The WebApp class is the entry point for the web application.

    It creates the container and runs the app.
    """

    def __init__(self) -> None:
        self._container = Container()


    def create_app(self) -> Flask:
        app: Flask = self._container.create_app()
        return app
