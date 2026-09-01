import inspect
from typing import Any


async def maybe_await(val: Any) -> Any:
    if inspect.isawaitable(val):
        return await val
    return val
