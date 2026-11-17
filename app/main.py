from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.engine import create_db_engine, create_session_factory
from app.modules.health.router import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = create_db_engine()

    try:
        app.state.session_factory = create_session_factory(engine)
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="Notification Platform",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Notification Platform is running"}

app.include_router(health_router)