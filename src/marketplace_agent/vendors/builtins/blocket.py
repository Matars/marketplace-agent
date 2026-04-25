"""Blocket vendor plugin for marketplace-agent.

Scrapes Blocket search results by fetching the search page and extracting
dehydrated React Query state from embedded base64 JSON scripts.

Based on browser-harness inspection of blocket.se.
"""
from __future__ import annotations

import base64
import json
import re
from urllib.parse import quote_plus

import requests

from marketplace_agent.models import Item, VendorCapability
from marketplace_agent.vendors.base import Vendor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def _extract_search_docs(html: str) -> list[dict]:
    """Parse Blocket search page HTML and return search result docs."""
    scripts = re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.DOTALL)
    for raw in scripts:
        raw = raw.strip()
        data = None
        try:
            data = json.loads(raw)
        except Exception:
            try:
                data = json.loads(base64.b64decode(raw))
            except Exception:
                continue
        if not isinstance(data, dict) or "queries" not in data:
            continue
        for query in data["queries"]:
            qk = query.get("queryKey")
            if (
                isinstance(qk, list)
                and len(qk) > 0
                and isinstance(qk[0], dict)
                and qk[0].get("scope") == "search"
            ):
                return query.get("state", {}).get("data", {}).get("docs", [])
    return []


def _docs_to_items(docs: list[dict], query: str, category: str | None) -> list[Item]:
    items: list[Item] = []
    seen_urls: set[str] = set()
    for doc in docs:
        url = doc.get("canonical_url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        price_info = doc.get("price") or {}
        amount = price_info.get("amount")
        currency = price_info.get("currency_code")
        items.append(
            Item(
                title=doc.get("heading", ""),
                url=url,
                source="blocket",
                category=category,
                price=amount,
                currency=currency,
                metadata={
                    "query": query,
                    "location": doc.get("location"),
                    "ad_id": doc.get("ad_id"),
                    "trade_type": doc.get("trade_type"),
                },
            )
        )
    return items


class BlocketVendor(Vendor):
    """Blocket (Sweden) vendor using dehydrated-state HTML scraping."""

    name = "blocket"
    capabilities = frozenset({VendorCapability.SEARCH, VendorCapability.PRICE_RESEARCH})

    def search(self, query: str, category: str | None = None) -> list[Item]:
        encoded = quote_plus(query)
        url = f"https://www.blocket.se/recommerce/forsale/search?q={encoded}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
        except Exception:
            return []

        docs = _extract_search_docs(resp.text)
        if not docs:
            return []

        return _docs_to_items(docs, query=query, category=category)

    def price_research(self, product: "ProductFacts") -> list[Item]:
        return self.search(product.title, category="comps")
