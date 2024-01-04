from abc import ABC, abstractmethod

class IHostEnvironment(ABC):
    """Minimum required attributes of the host environment."""

    @property
    @abstractmethod
    def web_root_path(self) -> str:
        pass

    @property
    @abstractmethod
    def application_name(self) -> str:
        pass
