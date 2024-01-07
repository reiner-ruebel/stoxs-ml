from abc import ABC, abstractmethod

class IProgram(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
    