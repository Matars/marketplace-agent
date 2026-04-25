"""eBay vendor plugin for marketplace-agent.

Uses HTTP scraping with regex extraction. No browser required.
Based on browser-harness domain-skills/ebay/scraping.md reference.
"""
from __future__ import annotations

import re
from urllib.parse import quote_plus

import requests

from marketplace_agent.models import Item, VendorCapability
from marketplace_agent.vendors.base import Vendor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}


def _parse_price(val: str | None) -> int | None:
    if not val:
        return None
    cleaned = re.sub(r"[^\d]", "", val)
    return int(cleaned) if cleaned else None


def _is_blocked(html: str) -> bool:
    return "Pardon Our Interruption" in html or len(html) < 20_000


def _extract_items(html: str, query: str, category: str | None) -> list[Item]:
    """Parse eBay search results HTML into Item objects."""
    if _is_blocked(html):
        return []

    cards = re.split(r"(?=<li[^>]+data-listingid=)", html)
    items: list[Item] = []
    seen_ids: set[str] = set()

    for card in cards[1:]:  # skip preamble before first card
        lid_m = re.search(r"data-listingid=(\d+)", card)
        if not lid_m:
            continue
        listing_id = lid_m.group(1)
        if listing_id in seen_ids:
            continue
        seen_ids.add(listing_id)

        url_m = re.search(r"href=(https://(?:www\.)?ebay\.com/itm/(\d+))", card)
        item_url = url_m.group(1).split("?")[0] if url_m else None

        title_m = re.search(r"s-card__title[^>]*>.*?primary[^>]*>([^<]+)", card, re.DOTALL)
        title = title_m.group(1).strip() if title_m else None

        if not title or title == "Shop on eBay":
            continue

        price_m = re.search(r"class=(?:[\"'])?price[\"']?>?\$([0-9,\.]+)<", card)
        if not price_m:
            price_m = re.search(r"price\">\$([0-9,\.]+)<", card)
        price_str = price_m.group(1) if price_m else None
        price = _parse_price(price_str)

        orig_m = re.search(r"strikethrough[^>]*>\$([0-9,\.]+)", card)
        original_price = _parse_price(orig_m.group(1)) if orig_m else None

        items.append(
            Item(
                title=title,
                url=item_url,
                source="ebay",
                category=category,
                price=price,
                currency="USD",
                metadata={
                    "query": query,
                    "original_price": original_price,
                    "listing_id": listing_id,
                },
            )
        )

    return items


class EBayVendor(Vendor):
    """eBay vendor using HTTP scraping."""

    name = "ebay"
    capabilities = frozenset({VendorCapability.SEARCH, VendorCapability.PRICE_RESEARCH})

    def search(self, query: str, category: str | None = None) -> list[Item]:
        encoded_query = quote_plus(query)
        url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_query}&LH_BIN=1&_sop=15"

        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
        except Exception:
            return []

        return _extract_items(resp.text, query=query, category=category)

    def price_research(self, product: "ProductFacts") -> list[Item]:
        from marketplace_agent.models import ProductFacts

        return self.search(product.title, category="comps")
