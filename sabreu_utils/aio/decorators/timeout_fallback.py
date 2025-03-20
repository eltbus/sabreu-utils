from typing import Callable, TypeVar, Awaitable
import asyncio


T = TypeVar("T")
AsyncFunc = Callable[..., Awaitable[T]]


def timeout_fallback(
    fallback_value: T, delay: float | None = None
) -> Callable[[AsyncFunc[T]], AsyncFunc[T]]:
    """Applies an asynchronous timeout to an asynchronous function.
    If the function does not complete before the timeout, it returns the fallback_value.
    Args:
        fallback_value (T): Value returned if the function times out.
        delay (float | None): Timeout duration in seconds. If None, no timeout is applied.
    Returns:
        Callable: The decorated function with timeout functionality.
    """

    def actual_decorator(fun: AsyncFunc[T]) -> AsyncFunc[T]:
        async def wrapper(*args, **kwargs) -> T:
            try:
                async with asyncio.timeout(delay=delay):
                    return await fun(*args, **kwargs)
            except asyncio.TimeoutError:
                return fallback_value

        return wrapper

    return actual_decorator
