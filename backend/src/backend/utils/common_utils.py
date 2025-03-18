from inspect import BoundArguments, signature
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from pydantic import AnyUrl


def get_bound_arguments(func, *args, **kwargs) -> BoundArguments:
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


def path_to_dotted_string(api_path: str | Path) -> str:
    if isinstance(api_path, Path):
        return str(api_path).strip("/").replace("/", ".")
    elif isinstance(api_path, str):
        return api_path.strip("/").replace("/", ".")
