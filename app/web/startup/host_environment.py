from .ihost_environment import IHostEnvironment


class HostEnvironment(IHostEnvironment):
   def __init__(self, path: str, name: str) -> None:
      self._path = path
      self._name = name
      

   @property
   def web_root_path(self) -> str:
            return self._path
   
   @property
   def application_name(self) -> str:
            return self._name
