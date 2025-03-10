from typing import Any
from inspect import BoundArguments, signature

from fastapi import HTTPException
from pydantic import AnyUrl


def func_inspect(func, *args, **kwargs) -> BoundArguments:
    sig = signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args


def parse_cors(v: Any) -> list[AnyUrl] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [AnyUrl(i.strip()) for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise HTTPException(status_code=400, detail=f"Invalid CORS value: {v}")
