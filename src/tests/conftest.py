from typing import AsyncGenerator

import pytest
from httpx import AsyncClient


@pytest.fixture()
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as async_client:
        yield async_client
