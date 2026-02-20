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
    result = encoder.embed(text)
    sparse_dict: dict[str, float] = {}
    for token, weight in result:
        if weight > 0:
            sparse_dict[token] = float(weight)
    return sparse_dict
