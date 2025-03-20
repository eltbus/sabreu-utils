import pytest
import asyncio
from sabreu_utils.aio.decorators import timeout_fallback


@pytest.mark.asyncio
async def test_function_completes_within_timeout():
    @timeout_fallback(fallback_value="fallback", delay=0.5)
    async def quick_function():
        await asyncio.sleep(0.2)
        return "success"

    result = await quick_function()
    assert result == "success"


@pytest.mark.asyncio
async def test_function_times_out():
    @timeout_fallback(fallback_value="fallback", delay=0.2)
    async def slow_function():
        await asyncio.sleep(0.5)
        return "success"

    result = await slow_function()
    assert result == "fallback"


@pytest.mark.asyncio
async def test_no_timeout():
    @timeout_fallback(fallback_value="fallback", delay=None)
    async def slow_function():
        await asyncio.sleep(0.5)
        return "success"

    result = await slow_function()
    assert result == "success"


@pytest.mark.asyncio
async def test_exception_propagates():
    @timeout_fallback(fallback_value="fallback", delay=0.5)
    async def error_function():
        await asyncio.sleep(0.2)
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError, match="Something went wrong"):
        await error_function()


@pytest.mark.asyncio
async def test_nested_decorators():
    def simple_logger(func):
        async def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            return await func(*args, **kwargs)
        return wrapper

    @simple_logger
    @timeout_fallback(fallback_value="fallback", delay=0.2)
    async def slow_function():
        await asyncio.sleep(0.5)
        return "success"

    result = await slow_function()
    assert result == "fallback"
