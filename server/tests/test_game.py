import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_score_route(client: AsyncClient):
    response = await client.get("/game/score")
    assert response.status_code == 200
    assert response.json() == {"score": 50}
