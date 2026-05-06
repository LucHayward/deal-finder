"""Base scraper interface for all site implementations."""
from abc import ABC, abstractmethod


class Scraper(ABC):
    """Common interface for all site scrapers."""

    @abstractmethod
    def discover(self, url: str, **kwargs) -> list[dict]:
        """Discover products/listings from a category or listing page.

        Returns list of dicts with at minimum: url, title, price, source.
        """

    @abstractmethod
    def fetch(self, url: str) -> dict:
        """Fetch full details from a single product/listing page.

        Returns dict with: url, title, price, status, source, fetched_at,
        plus any site-specific fields.
        """
