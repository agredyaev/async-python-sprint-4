from typing import Annotated

from fastapi import Depends, FastAPI

from core.security.auth.middleware import AuthMiddleware
from core.security.auth.permissions import PermissionChecker, PermissionsCheck
from core.security.auth.service import AuthService, get_auth_service


def setup_auth_middleware(
    app: FastAPI,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    exempt_endpoints: list[str],
    blacklist: list[str],
    api_version: str,
    permissions_enabled: PermissionsCheck = PermissionsCheck.DISABLED,
) -> None:
    permission_checker = PermissionChecker(exempt_endpoints, permissions_enabled)

    app.add_middleware(
        AuthMiddleware,
        auth_service=auth_service,
        permission_checker=permission_checker,
        api_version=api_version,
        blacklist=blacklist,
    )
