from dependency_injector.wiring import inject, Provide

from app.web.program import IProgram, ProgramServices


@inject
def main(program: IProgram = Provide[ProgramServices.program]) -> None:
    """
    Application entry point.
    
    We use the `inject` decorator to inject the program instance (rather than create an instance locally).
    If we want to test a different implementation of the `IProgram` interface, we make the adjustments in the app.web.program package.
    
    Dependency injection: https://python-dependency-injector.ets-labs.org/index.html
    """
    
    _program = program
    _program.run()


if __name__ == '__main__':
    ProgramServices().wire(modules=[__name__])
    main()
