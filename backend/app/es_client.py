import logging
from typing import Any

from elasticsearch import Elasticsearch

from app.config import settings

logger = logging.getLogger(__name__)


class ESClient:
    """Elasticsearch client for searching documents."""

    def __init__(self, url: str | None = None, index: str | None = None) -> None:
        self.url = url or settings.elasticsearch_url
        self.index = index or settings.elasticsearch_index
        self._client = Elasticsearch(self.url)

    def search(
        self, sparse_vector: dict[str, float], top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Search documents using sparse vector similarity."""
        query = {
            "query": {
                "sparse_vector": {
                    "field": "content_vector",
                    "query_vector": sparse_vector,
                }
            },
            "size": top_k,
            "_source": ["title", "content", "source_url"],
        }

        response = self._client.search(index=self.index, body=query)
        hits = response["hits"]["hits"]

        results = []
        for hit in hits:
            results.append(
                {
                    "title": hit["_source"]["title"],
                    "content": hit["_source"]["content"],
                    "source_url": hit["_source"]["source_url"],
                    "score": hit["_score"],
                }
            )

        return results

    def close(self) -> None:
        self._client.close()
