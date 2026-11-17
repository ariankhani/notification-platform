
from fastapi import APIRouter, HTTPException, Request, status

from app.modules.health.service import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
@router.get("/health/live")
async def liveness_check():
    return {"status": "healthy"}


@router.get("/health/ready")
async def readiness_check(request: Request):
    session_factory = request.app.state.session_factory

    if not await check_database(session_factory):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

    return {"status": "ready"}
