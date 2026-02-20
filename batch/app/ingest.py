"""Batch ingestion script: Fetch Cosense pages and index into Elasticsearch.

Usage:
    python -m app.ingest
"""

import logging
import sys
import time

from app.config import settings
from app.cosense_client import CosenseClient
from app.encoder_client import EncoderClient
from app.es_client import ESClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 20


def main() -> None:
    logger.info("=== Cosense → Elasticsearch Ingestion ===")
    logger.info(f"Project: {settings.cosense_project}")
    logger.info(f"Encoder: {settings.encoder_url}")
    logger.info(f"Elasticsearch: {settings.elasticsearch_url}/{settings.elasticsearch_index}")

    cosense = CosenseClient()
    encoder = EncoderClient()
    es = ESClient()

    # Check encoder health
    if not encoder.health_check():
        logger.error("Encoder service is not available. Start it first.")
        sys.exit(1)

    try:
        # 1. Create index
        logger.info("Creating Elasticsearch index...")
        es.create_index()

        # 2. Fetch pages from Cosense
        logger.info("Fetching pages from Cosense...")
        pages = cosense.fetch_all_pages()
        logger.info(f"Fetched {len(pages)} pages total.")

        if not pages:
            logger.warning("No pages found. Exiting.")
            return

        # 3. Encode and index pages in batches
        logger.info("Encoding and indexing pages...")
        batch: list[dict] = []
        indexed_count = 0
        start_time = time.time()

        for i, page in enumerate(pages):
            try:
                if not page.content.strip():
                    logger.info(f"[{i + 1}/{len(pages)}] Skipping empty page: {page.title}")
                    continue

                # Call encoder API
                sparse_vector = encoder.encode(page.content)

                doc = {
                    "title": page.title,
                    "content": page.content,
                    "content_vector": sparse_vector,
                    "source_url": page.source_url,
                }
                batch.append(doc)

                if len(batch) >= BATCH_SIZE:
                    es.bulk_index(batch)
                    indexed_count += len(batch)
                    elapsed = time.time() - start_time
                    logger.info(
                        f"[{i + 1}/{len(pages)}] Indexed {indexed_count} docs "
                        f"({elapsed:.1f}s elapsed)"
                    )
                    batch = []

            except Exception as e:
                logger.error(f"Failed to process '{page.title}': {e}")
                continue

        # Index remaining batch
        if batch:
            es.bulk_index(batch)
            indexed_count += len(batch)

        elapsed = time.time() - start_time
        logger.info("=== Ingestion complete ===")
        logger.info(f"Total indexed: {indexed_count} documents in {elapsed:.1f}s")
        logger.info(f"Index document count: {es.count()}")

    finally:
        cosense.close()
        encoder.close()
        es.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)
