"""
routers/auth.py
---------------
Authentication endpoints.
Currently issues a JWT when a valid API key is supplied.
Full user/password auth can be layered on later.
"""

from fastapi import APIRouter, HTTPException, status

from models.schemas import TokenRequest, TokenResponse
from middleware.auth import create_access_token

router = APIRouter()


@router.post("/token", response_model=TokenResponse, summary="Exchange API key for JWT")
async def get_token(body: TokenRequest):
    """
    Supply your ESA API key → receive a short-lived JWT.
    Include the JWT as `Authorization: Bearer <token>` on every /chat request.
    """
    # TODO: validate body.api_key against a database of registered keys.
    # For now we accept any non-empty key so development can proceed.
    if not body.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    token = create_access_token(data={"sub": body.api_key})
    return TokenResponse(access_token=token)
