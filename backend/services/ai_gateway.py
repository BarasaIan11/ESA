"""
services/ai_gateway.py
-----------------------
Provider-agnostic AI abstraction.

  - Reads ACTIVE_AI_PROVIDER from config to decide which client to use.
  - Supports OpenAI and Google Gemini.
  - Handles retry + basic fallback logging.
  - Returns (answer: str, sources: list[str]).

Phase 2 will wire retriever.py here to inject RAG context.
"""

import logging

from config import settings
from models.schemas import Message
from services.prompt_engine import build_context_block, build_messages

logger = logging.getLogger(__name__)


# ── OpenAI client (lazy init) ─────────────────────────────────────────────────
def _openai_client():
    from openai import AsyncOpenAI
    return AsyncOpenAI(api_key=settings.openai_api_key)


# ── Gemini client (lazy init) ─────────────────────────────────────────────────
def _gemini_client():
    from google import genai
    return genai.Client(api_key=settings.gemini_api_key)


# ── Main entry point ──────────────────────────────────────────────────────────
async def get_ai_response(
    question: str,
    history: list[Message],
    rag_chunks: list[str] | None = None,
) -> tuple[str, list[str]]:
    """
    Build the prompt and call the active AI provider.

    Args:
        question:   The user's raw question.
        history:    Prior conversation messages for this session.
        rag_chunks: Retrieved document chunks (empty until Phase 2 RAG is live).

    Returns:
        (answer, sources) — answer text and list of source references.
    """
    chunks = rag_chunks or []
    context_block = build_context_block(chunks)
    messages = build_messages(history, context_block, question)

    provider = settings.active_ai_provider.lower()

    try:
        if provider == "openai":
            answer = await _call_openai(messages)
        elif provider == "gemini":
            answer = await _call_gemini(messages)
        else:
            raise ValueError(f"Unknown AI provider: '{provider}'")
    except Exception as exc:
        logger.error("AI provider error (%s): %s", provider, exc, exc_info=True)
        answer = (
            "I'm currently unable to process your request. "
            "Please try again in a moment."
        )

    # Sources will be populated by retriever.py in Phase 2
    sources: list[str] = [c[:120] + "…" for c in chunks] if chunks else []
    return answer, sources


# ── Provider implementations ──────────────────────────────────────────────────

async def _call_openai(messages: list[dict]) -> str:
    client = _openai_client()
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,  # type: ignore[arg-type]
        temperature=0.2,    # lower = more deterministic, fewer hallucinations
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def _call_gemini(messages: list[dict]) -> str:
    """
    New Google GenAI SDK implementation.
    """
    import asyncio
    client = _gemini_client()

    system_instruction = next(
        (m["content"] for m in messages if m["role"] == "system"), ""
    )

    # Convert OpenAI-style history to Google-style history
    contents = []
    non_system = [m for m in messages if m["role"] != "system"]

    for msg in non_system[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    user_query = non_system[-1]["content"]

    # Use the more reliable 'gemini-1.5-flash' for testing, or 'gemini-1.5-pro'
    model_id = settings.gemini_model

    # Run the sync SDK call in a thread pool
    def _do_generate():
        return client.models.generate_content(
            model=model_id,
            contents=[*contents, {"role": "user", "parts": [{"text": user_query}]}],
            config={
                "system_instruction": system_instruction,
                "temperature": 0.2,
            }
        )

    response = await asyncio.to_thread(_do_generate)
    return response.text
