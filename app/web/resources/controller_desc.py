from typing import Any, Callable
from .base_controller import BaseController

class ControllerDesc:

    def __init__(self, controller: BaseController) -> None:
        self.name = controller.__class__.__name__
        self.methods: list[Callable[..., Any]] = controller.methods
        
    def _is_controller(self, obj: Any) -> bool:
        return isinstance(obj, BaseController)
