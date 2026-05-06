"""Scraper registry — maps source type names to scraper classes."""
from scrapers.base import Scraper

_REGISTRY: dict[str, type[Scraper]] = {}


def register(name: str):
    """Decorator to register a scraper class."""
    def wrapper(cls):
        _REGISTRY[name] = cls
        return cls
    return wrapper


def get_scraper(name: str) -> Scraper:
    """Get a scraper instance by source type name."""
    if name not in _REGISTRY:
        raise KeyError(f"Unknown scraper type: {name!r}. Available: {list(_REGISTRY)}")
    return _REGISTRY[name]()


# Import all scrapers to trigger registration
from scrapers import carbonite, shopify, evetech  # noqa: E402, F401
