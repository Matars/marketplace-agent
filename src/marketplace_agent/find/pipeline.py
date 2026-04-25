from __future__ import annotations

from marketplace_agent.models import Item
from marketplace_agent.vendors.base import Vendor


class SearchPipeline:
    def __init__(self, vendors: list[Vendor]) -> None:
        self.vendors = vendors

    def search(self, query: str, category: str | None = None) -> list[Item]:
        items: list[Item] = []
        for vendor in self.vendors:
            items.extend(vendor.search(query, category=category))
        return items
