from __future__ import annotations

from typing import Protocol, TypeVar

from collections.abc import Sequence

from sqlalchemy import SelectBase

In_contra = TypeVar("In_contra", contravariant=True)
Out_co = TypeVar("Out_co", covariant=True)


class RepositoryProtocol(Protocol[In_contra, Out_co]):
    """Base CRUD repository interface"""

    async def upsert(self, obj: In_contra) -> Out_co: ...
    async def get(self, obj: In_contra) -> Out_co | None: ...
    async def update(self, obj: In_contra) -> Out_co: ...
    async def delete(self, obj: In_contra) -> None: ...


class PostgresRepositoryProtocol(RepositoryProtocol[In_contra, Out_co]):
    """Postgres repository protocol CRUD operations."""

    async def bulk_create(self, objects: Sequence[Out_co]) -> None: ...
    async def exists(self, obj: In_contra) -> bool: ...
    async def get_all(self, statement: SelectBase | None) -> Sequence[Out_co]: ...
    async def get_by_statement(self, statement: SelectBase) -> Out_co: ...
