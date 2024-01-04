from .iweb_host_builder import IWebHostBuilder
from .web_host_builder import WebHostBuilder


class Program:
    """The entry point of the application."""

    @classmethod
    def main(cls):
        """We want to try to maintain a certain abstraction of the web host so that we do not depend on the web framework."""

        web_host_builder = cls._create_web_host_builder()
        web_host = web_host_builder.build()
        web_host.run()


    @staticmethod
    def _create_web_host_builder() -> IWebHostBuilder:
        return WebHostBuilder().configure()
    