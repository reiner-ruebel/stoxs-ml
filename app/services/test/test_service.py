from .itest_service import ITestService

class TestService(ITestService):
    def __init__(self) -> None:
        pass

    def hello(self) -> str:
        return "Hello from TestService"
