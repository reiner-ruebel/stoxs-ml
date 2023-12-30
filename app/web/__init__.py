from .container import Container


class WebApp:
    """
    The WebApp class is the entry point for the web application.

        It creates the container and runs the app.
    """

    def __init__(self):
        self._container = Container()


    def run(self):
        app = self._container.create_app()
        app.run()
