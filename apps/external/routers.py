#apps/external/routers.py

from fastapi import APIRouter, Depends
from apps.external.posts_service import ExternalPostsService

ex_router = APIRouter(prefix="/external", tags=["External"])


def get_external_posts_service():
    return ExternalPostsService()


@ex_router.get("/posts")
async def get_external_posts(
        service: ExternalPostsService = Depends(get_external_posts_service)
                             ):
    return await service.fetch_posts()
