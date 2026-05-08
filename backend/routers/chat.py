"""
routers/chat.py
---------------
Core chat endpoints:
  POST /chat/ask      — send a question, receive an AI answer
  GET  /chat/history  — retrieve past messages for a session
"""

import uuid

from fastapi import APIRouter, Depends, Request

from middleware.auth import require_auth
from models.schemas import AskRequest, AskResponse, HistoryResponse
from services.ai_gateway import get_ai_response
from services.history import get_history, save_turn

router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask ESA a Business Central question",
    dependencies=[Depends(require_auth)],
)
async def ask(request: Request, body: AskRequest):
    """
    Main chat endpoint.
    1. Resolve or create a session.
    2. Load conversation history.
    3. Call the AI gateway (prompt engine + AI provider).
    4. Persist the new turn.
    5. Return the answer + sources.
    """
    session_id = body.session_id or str(uuid.uuid4())

    # Load existing history for this session
    history = await get_history(session_id)

    # Get answer from AI (prompt engine + provider abstraction)
    answer, sources = await get_ai_response(
        question=body.question,
        history=history,
    )

    # Persist the new user/assistant turn
    await save_turn(session_id, user_msg=body.question, assistant_msg=answer)

    return AskResponse(
        answer=answer,
        session_id=session_id,
        sources=sources,
    )


@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Retrieve chat history for a session",
    dependencies=[Depends(require_auth)],
)
async def history(session_id: str):
    """Return all stored messages for the given session_id."""
    messages = await get_history(session_id)
    return HistoryResponse(session_id=session_id, messages=messages)
