from typing import Annotated

from collections.abc import Sequence

from fastapi import APIRouter, Depends, Request, status

from schemas.url import (
    UrlCreate,
    URLOriginalGet,
    URLOriginalResponse,
    UrlResponse,
    UrlStatsInfo,
    UrlStatsReq,
    UrlStatsResponse,
    UrlVisibilityUpdate,
)
from services import UrlService, get_url_service

router = APIRouter(prefix="/url", tags=["url"])


@router.post("/create", summary="Create URL", description="Create a new URL", status_code=status.HTTP_201_CREATED)
async def create_url(
    request: Request, data: UrlCreate, service: Annotated[UrlService, Depends(get_url_service)]
) -> UrlResponse:
    data.user_id = request.state.user_id
    return await service.create_url(url_data=data)


@router.get("", summary="Get original URL", description="Get original URL", status_code=status.HTTP_200_OK)
async def get_url(
    request: Request, short_id: str, service: Annotated[UrlService, Depends(get_url_service)]
) -> URLOriginalResponse:
    data = URLOriginalGet(short_id=short_id)
    return await service.get_url(url_data=data, request=request)


@router.get("/list", summary="Get user URLs", description="Get user URLs", status_code=status.HTTP_200_OK)
async def get_urls(request: Request, service: Annotated[UrlService, Depends(get_url_service)]) -> Sequence[UrlResponse]:
    return await service.get_user_urls(user_id=request.state.user_id)


@router.post(
    "/visibility", summary="Update URL visibility", description="Update URL visibility", status_code=status.HTTP_200_OK
)
async def update_visibility(
    data: UrlVisibilityUpdate, service: Annotated[UrlService, Depends(get_url_service)]
) -> UrlResponse:
    return await service.update_visibility(url_data=data)


@router.get("/stats", summary="Get URL stats", description="Get URL stats", status_code=status.HTTP_200_OK)
async def get_url_stats(
    short_id: str,
    service: Annotated[UrlService, Depends(get_url_service)],
    full_info: UrlStatsInfo = UrlStatsInfo.short,
    max_results: int = 10,
    offset: int = 0,
) -> UrlStatsResponse:
    data = UrlStatsReq(short_id=short_id, full_info=full_info, max_results=max_results, offset=offset)
    return await service.get_url_stats(url_data=data)
