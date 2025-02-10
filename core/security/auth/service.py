from typing import Annotated, Any

from functools import lru_cache

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, Request


class AuthService:
    def __init__(self, authjwt: AuthJWT):
        self.authjwt = authjwt

    async def authenticate(self, request: Request) -> dict[str, Any]:
        await self.authjwt.jwt_required()
        return await self.authjwt.get_raw_jwt()


@lru_cache
def get_auth_service(authjwt: Annotated[AuthJWT, Depends()]) -> AuthService:
    return AuthService(authjwt)
