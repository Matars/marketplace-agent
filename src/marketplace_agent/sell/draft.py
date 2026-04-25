from __future__ import annotations

from marketplace_agent.models import ListingDraft, ProductFacts


class DraftListingService:
    """Create safe listing drafts from product facts.

    Later this will use vision + price comps. For now it preserves the safety
    contract: drafts require approval and are not posted automatically.
    """

    def create_draft(self, product: ProductFacts, price: int, currency: str) -> ListingDraft:
        return ListingDraft.from_product(product, price=price, currency=currency)
