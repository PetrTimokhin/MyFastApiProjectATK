#apps/external/services/posts_service.py
# for services tests
import httpx


class ExternalPostsService:
    POSTS_URL = "https://jsonplaceholder.typicode.com/posts"

    async def fetch_posts(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.POSTS_URL, timeout=10)

        response.raise_for_status()
        return response.json()
