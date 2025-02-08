from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkProtocol(Protocol):
    async def __aenter__(self) -> "AsyncUnitOfWork": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...


class AsyncUnitOfWork(UnitOfWorkProtocol):
    """Unit of work for async database operations."""
    def __init__(self, session_factory=AsyncSession):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
