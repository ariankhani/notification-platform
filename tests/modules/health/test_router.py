
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.health.router import router


@asynccontextmanager
async def lifespan_for_tests(app: FastAPI):
    app.state.session_factory = object()
    yield


def make_client():
    app = FastAPI(lifespan=lifespan_for_tests)
    app.include_router(router)
    return TestClient(app)


def test_liveness():
    with make_client() as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_legacy_health():
    with make_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_success():
    with patch(
        "app.modules.health.router.check_database",
        new_callable=AsyncMock,
        return_value=True,
    ) as check, make_client() as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
    check.assert_awaited_once()


def test_readiness_failure():
    with patch(
        "app.modules.health.router.check_database",
        new_callable=AsyncMock,
        return_value=False,
    ), make_client() as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database unavailable",
    }
