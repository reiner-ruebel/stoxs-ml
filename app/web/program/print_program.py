from .iprogram import IProgram


class PrintProgram(IProgram):
    """Implementation of the IProgram interface to demo DI."""

    def __init__(self) -> None:
        """Init the app"""
        
        self._message = "Well, hello out there."


    def run(self) -> None:
        """Run the application."""

        print(self._message)
