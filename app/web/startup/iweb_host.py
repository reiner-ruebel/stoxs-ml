from abc import ABC, abstractmethod

class IWebHost(ABC):
    """Abstract interface for a web host."""

    @abstractmethod
    def run(self) -> None:
        """Run the web host."""
        pass
    

    @abstractmethod
    def stop(self) -> None:
        """Stop the web host."""
        pass
    