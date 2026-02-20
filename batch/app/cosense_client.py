import logging
from dataclasses import dataclass

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://scrapbox.io"


@dataclass
class CosensePage:
    """Represents a page from Cosense."""

    title: str
    content: str
    updated: int
    source_url: str


class CosenseClient:
    """Client for fetching pages from the Cosense (Scrapbox) API."""

    def __init__(self, project: str | None = None, sid: str | None = None) -> None:
        self.project = project or settings.cosense_project
        self.sid = sid or settings.cosense_sid
        self._client = httpx.Client(
            base_url=BASE_URL,
            cookies={"connect.sid": self.sid} if self.sid else None,
            timeout=30.0,
        )

    def list_page_titles(self) -> list[str]:
        """Fetch all page titles from the project using pagination."""
        titles: list[str] = []
        skip = 0
        limit = 1000

        while True:
            url = f"/api/pages/{self.project}?limit={limit}&skip={skip}"
            response = self._client.get(url)
            response.raise_for_status()
            data = response.json()
            pages = data.get("pages", [])

            if not pages:
                break

            titles.extend(page["title"] for page in pages)
            logger.info(f"Fetched {len(titles)} page titles so far...")

            if len(pages) < limit:
                break
            skip += limit

        return titles

    def get_page_text(self, title: str) -> str:
        """Fetch the plain text content of a page."""
        url = f"/api/pages/{self.project}/{title}/text"
        response = self._client.get(url)
        response.raise_for_status()
        return response.text

    def fetch_all_pages(self) -> list[CosensePage]:
        """Fetch all pages with their content."""
        titles = self.list_page_titles()
        pages: list[CosensePage] = []

        for i, title in enumerate(titles):
            try:
                content = self.get_page_text(title)
                page = CosensePage(
                    title=title,
                    content=content,
                    updated=0,
                    source_url=f"{BASE_URL}/{self.project}/{title}",
                )
                pages.append(page)
                logger.info(f"[{i + 1}/{len(titles)}] Fetched: {title}")
            except httpx.HTTPStatusError as e:
                logger.warning(f"Failed to fetch '{title}': {e}")
                continue

        return pages

    def close(self) -> None:
        self._client.close()
