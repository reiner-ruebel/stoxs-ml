from typing import Any, Callable, Optional, Type, TypeVar, Union

from flask import Flask, Response


F = TypeVar('F', bound=Callable[..., Any])   # Generic type for functions


Extension = tuple[str, object, Callable[[Flask], None], dict[str, object]]


_StrOrStrDict = Union[str, dict[str, str]]
_ResponseDict = Union[dict[str, str], dict[str, _StrOrStrDict]]

ApiResponse = Union[
    _ResponseDict,
    Response,
    tuple[Union[_ResponseDict, Response], int]
    ]


NamespaceResponse = dict[int, tuple[str, Optional[Type[Any]]]]
