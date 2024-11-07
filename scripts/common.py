from typing import (Any, Callable, Concatenate, Coroutine, ParamSpec, Protocol,
                    TypeVar)

from aiohttp import ClientSession, ClientTimeout

P = ParamSpec("P")
R = TypeVar("R")


def aio_wrpper(
    func: Callable[Concatenate[ClientSession, P], Coroutine[Any, Any, R]]
) -> Callable[P, Coroutine[Any, Any, R]]:
    async def wrapper(*args, **kwargs):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            return await func(session, *args, **kwargs)
    return wrapper
