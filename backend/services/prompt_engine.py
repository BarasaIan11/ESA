"""
services/prompt_engine.py
--------------------------
Three-layer prompt assembly (Identity → Context → History+Query).
This is the anti-hallucination core of ESA.
"""

from models.schemas import Message

# ── Layer 1: Identity & hard boundary ────────────────────────────────────────
SYSTEM_CORE = """
You are ESA, an ERP Support Assistant specialised exclusively in
Microsoft Dynamics 365 Business Central (BC).

RULES — never break these:
1. Only answer questions about BC: setup, configuration, modules
   (Finance, Sales, Purchase, Inventory, Manufacturing, Projects),
   AL/API development, integrations, and troubleshooting.
2. If a question is outside BC or general ERP, respond exactly:
   "I can only assist with Microsoft Dynamics 365 Business Central.
    Please rephrase your question within that scope."
3. Never invent menu paths, field names, or BC behaviour. If you are
   not certain, say "I don't have verified information on this —
   please check the official Microsoft Learn documentation."
4. Always cite the BC module or feature area you are drawing from.
5. Do not discuss competitors (SAP, Oracle, Odoo, etc.).
""".strip()


# ── Layer 2: Retrieved context (RAG) ─────────────────────────────────────────
def build_context_block(chunks: list[str]) -> str:
    """
    Wrap retrieved document chunks in a clearly labelled context block.
    An empty list returns an empty string (no noise when RAG is not yet wired).
    """
    if not chunks:
        return ""

    joined = "\n---\n".join(chunks)
    return f"""

VERIFIED KNOWLEDGE — use this as your primary source:
{joined}

If the answer is not present in the above context, say so explicitly
before attempting to answer from general knowledge.
""".strip()


# ── Layer 3: Conversation history + user query ───────────────────────────────
def build_messages(
    history: list[Message],
    context_block: str,
    user_query: str,
) -> list[dict]:
    """
    Assemble the full message list for the AI provider.

    Structure:
      [system]  SYSTEM_CORE + context_block
      [user/assistant] ... last 6 messages (3 turns)
      [user]    current question
    """
    system_content = SYSTEM_CORE
    if context_block:
        system_content += "\n\n" + context_block

    messages = [{"role": "system", "content": system_content}]

    # Include the last 3 turns (6 messages) for context window efficiency
    for msg in history[-6:]:
        messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": user_query})
    return messages
