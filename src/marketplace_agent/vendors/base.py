from __future__ import annotations

from abc import ABC

from marketplace_agent.models import Item, ListingDraft, ProductFacts, VendorCapability


class Vendor(ABC):
    """Base class for marketplace integrations.

    Vendors advertise capabilities because not every marketplace supports every
    workflow. Searching can be safe and public; posting and buyer messaging may
    require authenticated browser automation and explicit user approval.
    """

    name: str
    capabilities: frozenset[VendorCapability] = frozenset()

    def supports(self, capability: VendorCapability) -> bool:
        return capability in self.capabilities

    def search(self, query: str, category: str | None = None) -> list[Item]:
        raise NotImplementedError(f"{self.name} does not implement search")

    def price_research(self, product: ProductFacts) -> list[Item]:
        raise NotImplementedError(f"{self.name} does not implement price research")

    def draft_listing(self, product: ProductFacts) -> ListingDraft:
        raise NotImplementedError(f"{self.name} does not implement listing drafts")

    def post_listing(self, draft: ListingDraft) -> str:
        raise NotImplementedError(f"{self.name} does not implement posting")
