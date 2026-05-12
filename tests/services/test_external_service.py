# tests/services/test_external_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from apps.external.posts_service import ExternalPostsService


@pytest.mark.services
@pytest.mark.asyncio
async def test_fetch_posts_success():
    fake_response = [{"id": 1, "title": "test", "body": "body"}]

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = AsyncMock(return_value=fake_response)

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch(
        "apps.external.posts_service.httpx.AsyncClient"
    ) as client_mock:
        client_mock.return_value.__aenter__.return_value = mock_client

        service = ExternalPostsService()
        result = await service.fetch_posts()
        result = await result

    assert result == fake_response


@pytest.mark.services
@pytest.mark.asyncio
async def test_fetch_posts_empty_list():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = AsyncMock(return_value=[])

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch(
        "apps.external.posts_service.httpx.AsyncClient"
    ) as client_mock:
        client_mock.return_value.__aenter__.return_value = mock_client

        service = ExternalPostsService()
        result = await service.fetch_posts()
        result = await result

    assert result == []


@pytest.mark.services
@pytest.mark.asyncio
async def test_fetch_posts_http_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server error",
        request=MagicMock(),
        response=MagicMock(status_code=500),
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch(
        "apps.external.posts_service.httpx.AsyncClient"
    ) as client_mock:
        client_mock.return_value.__aenter__.return_value = mock_client

        service = ExternalPostsService()

        with pytest.raises(httpx.HTTPStatusError):
            await service.fetch_posts()


@pytest.mark.services
@pytest.mark.asyncio
async def test_fetch_posts_timeout():
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.ConnectTimeout("Timeout")

    with patch(
        "apps.external.posts_service.httpx.AsyncClient"
    ) as client_mock:
        client_mock.return_value.__aenter__.return_value = mock_client

        service = ExternalPostsService()

        with pytest.raises(httpx.ConnectTimeout):
            await service.fetch_posts()
