from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plaintext password against a stored hash."""
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""

    now = datetime.now(UTC)

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.jwt_expiration_minutes
        )

    expire = now + expires_delta

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""

    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )