import logging

import ollama

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """あなたは質問応答アシスタントです。
ユーザーの質問に対して、提供されたコンテキスト情報をもとに正確に回答してください。

ルール:
- コンテキストに含まれる情報のみを使って回答してください。
- コンテキストに回答に十分な情報がない場合は、その旨を伝えてください。
- 回答は日本語で、簡潔かつ分かりやすくしてください。
- 参照元のページがある場合はタイトルを明記してください。
"""


def generate_answer(query: str, contexts: list[dict]) -> str:
    """Generate an answer using Ollama Gemma3 with retrieved contexts.

    Args:
        query: The user's question.
        contexts: List of search results, each with 'title', 'content', 'source_url'.

    Returns:
        The generated answer string.
    """
    context_text = _build_context(contexts)

    user_message = f"""## 質問
{query}

## 参照情報
{context_text}
"""

    client = ollama.Client(host=settings.ollama_base_url)

    try:
        response = client.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise


def _build_context(contexts: list[dict]) -> str:
    """Build a formatted context string from search results."""
    parts: list[str] = []
    for i, ctx in enumerate(contexts, 1):
        title = ctx.get("title", "Unknown")
        content = ctx.get("content", "")
        # Truncate very long content to fit in context window
        if len(content) > 2000:
            content = content[:2000] + "..."
        parts.append(f"### [{i}] {title}\n{content}")
    return "\n\n".join(parts)
