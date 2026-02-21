import logging

from yasem import SpladeEmbedder

from app.config import settings

logger = logging.getLogger(__name__)

_encoder: SpladeEmbedder | None = None


def get_encoder() -> SpladeEmbedder:
    """Get or create the SPLADE encoder singleton."""
    global _encoder
    if _encoder is None:
        logger.info(f"Loading SPLADE model: {settings.splade_model}")
        _encoder = SpladeEmbedder(settings.splade_model)
        logger.info("SPLADE model loaded successfully")
    return _encoder


def encode_text(text: str) -> dict[str, float]:
    """Encode text into a sparse vector using japanese-splade.

    Returns:
        A dictionary mapping token strings to their weights.
    """
    encoder = get_encoder()
    # encode() expects a list of strings and returns a matrix
    embeddings = encoder.encode([text])
    # get_token_values() converts the matrix/array to a list of dicts or a single dict
    result = encoder.get_token_values(embeddings)
    
    # If a single string was passed, it returns a single dict
    if isinstance(result, list):
        return result[0]
    return result
