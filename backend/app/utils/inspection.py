import inspect
from inspect import BoundArguments


def func_inspect(func, *args, **kwargs) -> BoundArguments:
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args
