"""
services/history.py
--------------------
In-memory conversation history store.

⚠️  This is intentionally simple for Phase 1 — it keeps history in a
    Python dict so you can test the full chat loop without a database.
    Phase 2 will replace this with async SQLAlchemy / Redis persistence.
"""

from models.schemas import Message

# session_id → list of Message objects
_store: dict[str, list[Message]] = {}


async def get_history(session_id: str) -> list[Message]:
    """Return the stored messages for a session (empty list if new)."""
    return _store.get(session_id, [])


async def save_turn(
    session_id: str,
    user_msg: str,
    assistant_msg: str,
) -> None:
    """Append a user/assistant pair to the session history."""
    if session_id not in _store:
        _store[session_id] = []

    _store[session_id].extend([
        Message(role="user", content=user_msg),
        Message(role="assistant", content=assistant_msg),
    ])

    # Keep only the last 20 messages (10 turns) to cap memory usage
    _store[session_id] = _store[session_id][-20:]
