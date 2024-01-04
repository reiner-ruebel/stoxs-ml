from .iweb_host_builder import IWebHostBuilder
from .iweb_host import IWebHost
from .web_host import WebHost


class WebHostBuilder(IWebHostBuilder):

    def build(self) -> IWebHost:
        return WebHost()
    
    def use_startup(self, startup) -> IWebHostBuilder:
        providers = startup.get_providers()
        return self
    