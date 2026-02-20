import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class EncoderClient:
    """Client for the Sparse Encoder API service."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.encoder_url
        self._client = httpx.Client(base_url=self.base_url, timeout=60.0)

    def encode(self, text: str) -> dict[str, float]:
        """Encode text to a sparse vector via the encoder API."""
        response = self._client.post(
            "/api/encode",
            json={"text": text},
        )
        response.raise_for_status()
        return response.json()["vector"]

    def health_check(self) -> bool:
        """Check if the encoder service is healthy."""
        try:
            response = self._client.get("/api/health")
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def close(self) -> None:
        self._client.close()
