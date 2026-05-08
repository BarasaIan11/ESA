"""
middleware/auth.py
------------------
JWT creation and validation.
`require_auth` is a FastAPI dependency — inject it into any route that needs protection.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config import settings

_bearer = HTTPBearer(auto_error=True)


def create_access_token(data: dict) -> str:
    """Create a signed JWT with an expiry."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """
    FastAPI dependency — validates the Bearer JWT.
    Returns the `sub` claim (API key / user id) on success.
    Raises 401 on any failure.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        subject: str | None = payload.get("sub")
        if subject is None:
            raise JWTError("missing sub")
        return subject
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )
