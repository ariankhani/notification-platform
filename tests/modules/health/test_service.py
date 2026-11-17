
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.health.service import check_database


def make_session_factory(
    execute_side_effect=None,
):
    session = MagicMock()
    session.execute = AsyncMock(
        side_effect=execute_side_effect,
    )

    factory = MagicMock()
    context = factory.return_value
    context.__aenter__ = AsyncMock(return_value=session)
    context.__aexit__ = AsyncMock(return_value=False)

    return factory, session


@pytest.mark.asyncio
async def test_database_check_success():
    factory, session = make_session_factory()

    result = await check_database(factory)

    assert result is True
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_database_check_failure():
    factory, _ = make_session_factory(
        execute_side_effect=OSError("Connection failed"),
    )

    result = await check_database(factory)

    assert result is False


@pytest.mark.asyncio
async def test_database_check_timeout(monkeypatch):
    from app.modules.health import service

    monkeypatch.setattr(
        service,
        "DATABASE_CHECK_TIMEOUT",
        0.01,
    )

    async def slow_execute(*args, **kwargs):
        import asyncio

        await asyncio.sleep(1)

    factory, _ = make_session_factory(
        execute_side_effect=slow_execute,
    )

    result = await check_database(factory)

    assert result is False
