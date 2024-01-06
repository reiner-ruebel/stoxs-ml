from abc import ABC, abstractmethod

class ITestService(ABC):
    
    @abstractmethod
    def hello(self) -> str:
        pass

