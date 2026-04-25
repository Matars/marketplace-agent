from marketplace_agent.models import Item, ListingDraft, ProductFacts, VendorCapability
from marketplace_agent.vendors.base import Vendor
from marketplace_agent.vendors.registry import VendorRegistry


class ExampleVendor(Vendor):
    name = "example"
    capabilities = frozenset({VendorCapability.SEARCH, VendorCapability.PRICE_RESEARCH})

    def search(self, query: str, category: str | None = None) -> list[Item]:
        return [Item(title=f"{query} item", url="https://example.com/1", source=self.name, category=category)]


def test_vendor_registry_finds_vendors_by_capability():
    registry = VendorRegistry()
    registry.register(ExampleVendor)

    assert registry.names() == ["example"]
    assert registry.for_capability(VendorCapability.SEARCH) == [ExampleVendor]
    assert registry.for_capability(VendorCapability.POST_LISTING) == []


def test_vendor_search_returns_normalized_items():
    vendor = ExampleVendor()

    items = vendor.search("rtx 3060", category="gpu")

    assert items[0].title == "rtx 3060 item"
    assert items[0].source == "example"
    assert items[0].category == "gpu"


def test_listing_draft_requires_user_approval_by_default():
    product = ProductFacts(title="Sony WH-1000XM4", condition="used")

    draft = ListingDraft.from_product(product, price=1200, currency="SEK")

    assert draft.title == "Sony WH-1000XM4"
    assert draft.price == 1200
    assert draft.currency == "SEK"
    assert draft.requires_approval is True
