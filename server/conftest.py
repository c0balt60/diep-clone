import pytest
import httpx
from server.app.main import app

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test-server"
    ) as await_client:
        yield await_client
