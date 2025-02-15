import types

from typing import Protocol

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.logging.logger import CoreLogger

logger = CoreLogger.get_logger("unit_of_database_work")


class UnitOfWorkProtocol(Protocol):
    async def __aenter__(self) -> "AsyncUnitOfWork": ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None
    ) -> bool | None: ...


class AsyncUnitOfWork(UnitOfWorkProtocol):
    """Unit of work for async database operations."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "AsyncUnitOfWork":
        self.session = self.session_factory()
        await self.session.begin()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None
    ) -> bool | None:
        result = False
        if self.session is None:
            return result
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
            result = True
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.exception("Database error: %s", exc_info=e)
            result = False
        finally:
            await self.session.close()

        return result
