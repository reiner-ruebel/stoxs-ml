import typing as t

from flask import Flask, Response


Extension = tuple[str, object, t.Callable[[Flask], None], dict[str, object]]
Api_Response = t.Union[dict, Response, tuple[t.Union[dict, Response], int]]
