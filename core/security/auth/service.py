from typing import Any

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Request


class AuthService:
    def __init__(self, authjwt: AuthJWT):
        self.authjwt = authjwt

    async def authenticate(self, request: Request) -> dict[str, Any]:
        await self.authjwt.jwt_required()
        return await self.authjwt.get_raw_jwt()
