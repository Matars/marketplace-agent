from __future__ import annotations

from marketplace_agent.models import Item, ProductFacts, VendorCapability
from marketplace_agent.vendors.base import Vendor


class DemoVendor(Vendor):
    """Offline demo vendor used to prove the find pipeline without scraping yet."""

    name = "demo"
    capabilities = frozenset({VendorCapability.SEARCH, VendorCapability.PRICE_RESEARCH})

    def search(self, query: str, category: str | None = None) -> list[Item]:
        slug = query.lower().replace(" ", "-")
        return [
            Item(
                title=f"Demo listing for {query}",
                url=f"https://example.com/{slug}",
                source=self.name,
                category=category,
                price=1000,
                currency="SEK",
                metadata={"demo": True, "query": query},
            )
        ]

    def price_research(self, product: ProductFacts) -> list[Item]:
        return self.search(product.title, category="comps")
