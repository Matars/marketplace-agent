"""Amazon vendor plugin for marketplace-agent.

Attempts HTTP scraping first. Amazon is heavily JS-rendered so results may be
limited. If HTTP scraping fails or returns empty results, the plugin notes that
browser-harness integration would provide better results.

Based on browser-harness domain-skills/amazon/product-search.md reference.
"""
from __future__ import annotations

import re
from urllib.parse import quote_plus

import requests

from marketplace_agent.models import Item, VendorCapability
from marketplace_agent.vendors.base import Vendor
from marketplace_agent.vendors.browser_harness import fetch_html as _browser_fetch

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://www.amazon.com/",
}


def _fetch_html(url: str) -> str | None:
    """Fetch Amazon search page using a session for cookie persistence. Falls back to browser-harness."""
    session = requests.Session()
    try:
        # Prime the session with a visit to the homepage to establish cookies
        session.get("https://www.amazon.com/", headers=HEADERS, timeout=15)
        resp = session.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception:
        pass

    # Fallback to browser-harness
    return _browser_fetch(url)


def _parse_price(val: str | None) -> int | None:
    if not val:
        return None
    cleaned = re.sub(r"[^\d]", "", val)
    return int(cleaned) if cleaned else None


def _extract_items(html: str, query: str, category: str | None) -> list[Item]:
    """Parse Amazon search results HTML into Item objects.

    Amazon is heavily JS-rendered, so HTTP scraping may yield limited results.
    This extracts what's available in the server-rendered HTML.
    """
    items: list[Item] = []
    seen_asins: set[str] = set()

    # Try to find search result containers with data-asin attribute
    # Pattern: <div data-asin="B08Z6X4NK3" ...>
    asin_pattern = r'data-asin="([A-Z0-9]{10})"'
    asin_matches = list(re.finditer(asin_pattern, html))

    for asin_match in asin_matches:
        asin = asin_match.group(1)
        if asin in seen_asins or not asin:
            continue
        seen_asins.add(asin)

        # Extract a chunk around this ASIN for field extraction
        start = max(0, asin_match.start() - 1000)
        end = min(len(html), asin_match.end() + 5000)
        chunk = html[start:end]

        # Try to extract title - look for h2 with span inside
        title_m = re.search(
            r'<h2[^>]*>.*?<span[^>]*>([^<]+)</span>.*?</h2>',
            chunk,
            re.DOTALL,
        )
        title = title_m.group(1).strip() if title_m else None

        # Try to extract price from .a-price .a-offscreen
        price_m = re.search(
            r'class="a-price"[^>]*>.*?<span class="a-offscreen">\$([0-9,\.]+)</span>',
            chunk,
            re.DOTALL,
        )
        price_str = price_m.group(1) if price_m else None
        price = _parse_price(price_str)

        # If no price found, try alternative pattern
        if not price:
            price_m = re.search(r'\$([0-9,\.]+)', chunk)
            price_str = price_m.group(1) if price_m else None
            price = _parse_price(price_str)

        # Construct item URL
        item_url = f"https://www.amazon.com/dp/{asin}"

        if title:
            items.append(
                Item(
                    title=title,
                    url=item_url,
                    source="amazon",
                    category=category,
                    price=price,
                    currency="USD",
                    metadata={
                        "query": query,
                        "asin": asin,
                    },
                )
            )

    return items


class AmazonVendor(Vendor):
    """Amazon vendor using HTTP scraping.

    Amazon is heavily JS-rendered, so HTTP scraping may yield limited results.
    For better results, use browser-harness integration.
    """

    name = "amazon"
    capabilities = frozenset({VendorCapability.SEARCH, VendorCapability.PRICE_RESEARCH})

    def search(self, query: str, category: str | None = None) -> list[Item]:
        encoded_query = quote_plus(query)
        url = f"https://www.amazon.com/s?k={encoded_query}"

        html = _fetch_html(url)
        if html is None:
            return []

        items = _extract_items(html, query=query, category=category)

        # If HTTP scraping returns empty, note that browser-harness would help
        if not items:
            return []

        return items

    def price_research(self, product: "ProductFacts") -> list[Item]:
        from marketplace_agent.models import ProductFacts

        return self.search(product.title, category="comps")
