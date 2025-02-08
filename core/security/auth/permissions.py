from collections.abc import Callable
from enum import IntEnum


class PermissionsCheck(IntEnum):
    ENABLED = 1
    DISABLED = 0

class PermissionChecker:
    def __init__(
        self,
        exempt_endpoints_provider: Callable[[], list[str]],
        permissions_check: PermissionsCheck = PermissionsCheck.ENABLED
    ):
        self.exempt_endpoints_provider = exempt_endpoints_provider
        self.permissions_enabled = permissions_check

    def is_exempt(self, path: str) -> bool:
        return path in self.exempt_endpoints_provider()

    @staticmethod
    def has_permission(user_permissions: list[str], path: str) -> bool:
        return any(
            path.startswith(permission)
            for permission in user_permissions
        )
