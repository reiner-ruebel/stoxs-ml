from abc import ABC, abstractmethod

from .register_payload import RegisterPayload
from .register_result import RegisterResult


class IAccountService(ABC):
    
    @abstractmethod
    def register(self, payload: RegisterPayload) -> RegisterResult:
        pass
