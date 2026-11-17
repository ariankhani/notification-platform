
import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

logger = logging.getLogger(__name__)

DATABASE_CHECK_TIMEOUT = 3.0


async def check_database(
    session_factory: async_sessionmaker[AsyncSession],
) -> bool:
    async def run_check() -> None:
        async with session_factory() as session:
            await session.execute(text("SELECT 1"))

    try:
        await asyncio.wait_for(
            run_check(),
            timeout=DATABASE_CHECK_TIMEOUT,
        )
    except (SQLAlchemyError, OSError, TimeoutError):
        logger.warning(
            "Database readiness check failed",
            exc_info=True,
        )
        return False

    return True
