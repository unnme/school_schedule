import inspect
from inspect import BoundArguments
from typing import Any

from pydantic import AnyUrl


def func_inspect(func, *args, **kwargs) -> BoundArguments:
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args


def parse_cors(v: Any) -> list[AnyUrl] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [AnyUrl(i.strip()) for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(f"Invalid CORS value: {v}")
