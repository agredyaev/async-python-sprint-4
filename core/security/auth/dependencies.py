from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from core.security.auth.middleware import AuthMiddleware
from core.security.auth.permissions import PermissionChecker, PermissionsCheck
from core.security.auth.service import AuthService


def setup_auth_middleware(
    app: FastAPI,
    auth_jwt: AuthJWT,
    exempt_endpoints: list[str],
    api_version: str = "/v1",
    permissions_enabled: PermissionsCheck = PermissionsCheck.ENABLED,
) -> None:
    auth_service = AuthService(auth_jwt)
    permission_checker = PermissionChecker(lambda: exempt_endpoints, permissions_enabled)

    app.add_middleware(
        AuthMiddleware, auth_service=auth_service, permission_checker=permission_checker, api_version=api_version
    )
