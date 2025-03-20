import pytest
import asyncio
from sabreu_utils.aio.decorators import timeout_fallback


@pytest.mark.asyncio
async def test_function_completes_within_timeout():
    @timeout_fallback(fallback_value="fallback", delay=1.0)
    async def quick_function():
        await asyncio.sleep(0.5)  # Takes 0.5 seconds
        return "success"

    result = await quick_function()
    assert result == "success"
