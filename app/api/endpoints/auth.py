# app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlmodel import select

from app.core.deps import CurrentUserDep
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)
from app.db.dependencies import get_session
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    path="/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, session=Depends(get_session)):
    statement = select(User).where(
        (User.email == user_in.email) | (User.username == user_in.username)
    )
    result = await session.exec(statement)
    if result.first():
        raise HTTPException(
            status_code=400, detail="Username or Email already registered"
        )

    user_data = user_in.model_dump()
    hashed_pw = hash_password(user_data.pop("password"))
    new_user = User(hashed_password=hashed_pw, **user_data)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


<<<<<<< HEAD
router = APIRouter(prefix="/auth", tags=["Authentication"])


=======
>>>>>>> f1a903f (feat(auth): complete JWT auth system with refresh tokens, logout)
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    statement = select(User).where(User.username == form_data.username)
    result = await session.exec(statement)
    user = result.first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    user.hashed_refresh_token = hash_password(refresh_token)
    session.add(user)
    await session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, session=Depends(get_session)):
    try:
        payload = decode_jwt_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    statement = select(User).where(User.id == int(user_id))
    result = await session.exec(statement)
    user = result.first()

    if not user or not verify_password(refresh_token, user.hashed_refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)

    user.hashed_refresh_token = hash_password(new_refresh_token)
    session.add(user)
    await session.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: CurrentUserDep, session=Depends(get_session)):
    current_user.hashed_refresh_token = None
    session.add(current_user)
    await session.commit()
