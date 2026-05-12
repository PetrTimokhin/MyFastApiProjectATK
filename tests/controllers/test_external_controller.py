#tests/controllers/test_external_controller.py

import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from main import app
from apps.external.routers import get_external_posts_service


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_external_posts():
    mock_service = AsyncMock()
    mock_service.fetch_posts.return_value = [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"},
    ]

    app.dependency_overrides[get_external_posts_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/external/posts")

    assert response.status_code == 200
    assert len(response.json()) == 2

    app.dependency_overrides.clear()

