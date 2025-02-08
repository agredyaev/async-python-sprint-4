from typing import Any

import ipaddress

from collections.abc import Callable

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.security.auth.exceptions import AuthJWTError, BlacklistError, InternalServerError, PermissionDeniedError
from core.security.auth.permissions import PermissionChecker
from core.security.auth.service import AuthService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: FastAPI,
            auth_service: AuthService,
            permission_checker: PermissionChecker,
            blacklist: list[ipaddress.IPv4Network],
            api_version: str = "/v1"
    ):
        super().__init__(app)
        self.auth_service = auth_service
        self.permission_checker = permission_checker
        self.api_version = api_version
        self.blacklist = blacklist

    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> JSONResponse:
        path = request.url.path.split(self.api_version)[-1]
        client_ip = request.client.host

        if client_ip in self.blacklist:
            return self.handle_error(exc=BlacklistError())

        if not self.permission_checker.is_exempt(path):
            try:
                current_user = await self.auth_service.authenticate(request)
                if not current_user:
                    self.handle_error(exc=AuthJWTError())

                if self.permission_checker.permissions_enabled:
                    user_perms = current_user.get("permissions", [])
                    if not self.permission_checker.has_permission(user_perms, path):
                        self.handle_error(exc=PermissionDeniedError())

                request.state.user = current_user

            except Exception:
                return self.handle_error(exc=InternalServerError())

        return await call_next(request)

    @staticmethod
    def handle_error(exc: AuthJWTError | PermissionDeniedError | InternalServerError | BlacklistError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

