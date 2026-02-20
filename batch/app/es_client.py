import logging
from typing import Any

from elasticsearch import Elasticsearch

from app.config import settings

logger = logging.getLogger(__name__)

INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "kuromoji"},
            "content": {"type": "text", "analyzer": "kuromoji"},
            "content_vector": {"type": "sparse_vector"},
            "source_url": {"type": "keyword"},
            "updated_at": {"type": "date"},
        }
    }
}


class ESClient:
    """Elasticsearch client for indexing documents."""

    def __init__(self, url: str | None = None, index: str | None = None) -> None:
        self.url = url or settings.elasticsearch_url
        self.index = index or settings.elasticsearch_index
        self._client = Elasticsearch(self.url)

    def create_index(self) -> None:
        """Create the index with sparse_vector mapping if it doesn't exist."""
        if self._client.indices.exists(index=self.index):
            logger.info(f"Index '{self.index}' already exists, skipping creation.")
            return
        self._client.indices.create(index=self.index, body=INDEX_MAPPING)
        logger.info(f"Index '{self.index}' created successfully.")

    def delete_index(self) -> None:
        """Delete the index if it exists."""
        if self._client.indices.exists(index=self.index):
            self._client.indices.delete(index=self.index)
            logger.info(f"Index '{self.index}' deleted.")

    def bulk_index(self, documents: list[dict[str, Any]]) -> None:
        """Bulk index documents."""
        actions: list[dict[str, Any]] = []
        for doc in documents:
            actions.append({"index": {"_index": self.index}})
            actions.append(doc)
        if actions:
            self._client.bulk(body=actions)
            logger.info(f"Bulk indexed {len(documents)} documents.")

    def count(self) -> int:
        """Return the number of documents in the index."""
        result = self._client.count(index=self.index)
        return result["count"]

    def close(self) -> None:
        self._client.close()
