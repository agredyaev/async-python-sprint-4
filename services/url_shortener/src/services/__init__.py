from typing import Annotated

from functools import lru_cache

from fastapi import Depends

from core.database.uow import AsyncUnitOfWork
from repositories import UrlRepository, UrlStatsRepository, UserRepository, get_uow, get_url_repo, get_url_stats_repo
from services.url import UrlService
from services.user import UserService


@lru_cache
def get_user_service(
    uow: Annotated[AsyncUnitOfWork, Depends(get_uow)], user_repo: Annotated[UserRepository, Depends(get_uow)]
) -> UserService:
    return UserService(user_repo=user_repo, uow=uow)


@lru_cache
def get_url_service(
    uow: Annotated[AsyncUnitOfWork, Depends(get_uow)],
    url_repo: Annotated[UrlRepository, Depends(get_url_repo)],
    stats_repo: Annotated[UrlStatsRepository, Depends(get_url_stats_repo)],
) -> UrlService:
    return UrlService(url_repo=url_repo, stats_repo=stats_repo, uow=uow)
