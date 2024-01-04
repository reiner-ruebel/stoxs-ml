from dependency_injector.wiring import Provide, inject
from flask import Flask, request

from .iweb_host import IWebHost
from.hosting_services import HostingServices


class WebHost(IWebHost):
    """
    Creates a flask host.
    
    Adjust here to use a different web framework.
    """

    @inject
    def __init__(self, app: Flask = Provide[HostingServices.host]) -> None:
        self._app = app

    #
    # public methods
    #  
  
    def run(self) -> None:
        self._app.run()
        

    def stop(self):
        self._shutdown_server()


    #
    # private methods
    #

    def _shutdown_server(self) -> None:
        """
        Stops the flask server.
        
        https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
        """

        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Could not shutdown the server')
        func()
    