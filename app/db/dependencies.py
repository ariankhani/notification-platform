from collections.abc import AsyncGenerator

from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request, ) -> AsyncGenerator[AsyncSession, None]:
    ssesion_factory = request.app.state.session_factory

    async with ssesion_factory() as session:
        yield session