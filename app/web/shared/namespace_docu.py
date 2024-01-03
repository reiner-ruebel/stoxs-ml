from typing import Optional
from dataclasses import InitVar, dataclass, field

from app import NamespaceResponse


@dataclass
class NamespaceDocu:
    """ Namespace documentation """

    name: InitVar[str]
    body: str
    description: str = 'tbd'
    route: str = field(init=False)
    responses: Optional[list[NamespaceResponse]] = None

    # does not understand that name is a str...
    def __post_init__(self) -> None:  # type: ignore
        self.route = '/' + self.name.lower()  # type: ignore
        