from fastapi import APIRouter

from app.core.deps import CurrentUserDep
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: CurrentUserDep):
    """
    Get current user.
    """
    return current_user
