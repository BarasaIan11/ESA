"""
schemas.py
----------
Pydantic models for all API request and response payloads.
"""

from pydantic import BaseModel, Field
from typing import Literal


# ── Chat ──────────────────────────────────────────────────────────────────────

class Message(BaseModel):
    """A single message in a conversation turn."""
    role: Literal["user", "assistant", "system"]
    content: str


class AskRequest(BaseModel):
    """POST /chat/ask  — body sent by the frontend."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's Business Central question.",
        examples=["How do I set up payment terms in BC?"],
    )
    session_id: str | None = Field(
        None,
        description="Opaque session identifier for conversation continuity.",
    )


class AskResponse(BaseModel):
    """POST /chat/ask  — body returned to the frontend."""
    answer: str
    session_id: str
    sources: list[str] = Field(
        default_factory=list,
        description="Document chunks or page references used to build the answer.",
    )


class HistoryResponse(BaseModel):
    """GET /chat/history  — list of past messages for a session."""
    session_id: str
    messages: list[Message]


# ── Auth ──────────────────────────────────────────────────────────────────────

class TokenRequest(BaseModel):
    api_key: str = Field(..., description="The user's raw API key.")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
