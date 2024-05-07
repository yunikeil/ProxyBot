from httpx import AsyncClient


async def test_google(async_client: AsyncClient):
    response = await async_client.get("https://www.google.com/")
    assert response.status_code == 200
