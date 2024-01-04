from abc import ABC, abstractmethod

from app.web.startup.iweb_host import IWebHost

class IWebHostBuilder(ABC):
    
    @abstractmethod
    def build(self) -> IWebHost:
        pass
    

    @abstractmethod
    def configure(self) -> None:
        pass
    