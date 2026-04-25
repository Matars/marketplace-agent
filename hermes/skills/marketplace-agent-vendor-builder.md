---
name: marketplace-agent-vendor-builder
category: marketplace-agent
description: Build and repair marketplace-agent vendor plugins using browser inspection/browser-harness style DOM analysis. Use for custom vendors and real marketplace scrapers.
---

# marketplace-agent vendor builder

Use this skill when a user wants marketplace-agent to search a vendor that is not implemented yet.

## Goal

Create or repair a vendor plugin under the user's workspace or the engine repo, depending on intent:

- reusable built-in vendor: engine repo `src/marketplace_agent/vendors/builtins/<name>.py`
- user-specific vendor: workspace `vendors/<name>.py` once plugin loading exists

For now, built-ins are supported first.

## Vendor capability model

Every vendor should subclass `marketplace_agent.vendors.base.Vendor` and declare capabilities:

```python
class BlocketVendor(Vendor):
    name = "blocket"
    capabilities = frozenset({VendorCapability.SEARCH})
```

Implement `search(query: str, category: str | None = None) -> list[Item]` first. Do not implement posting/message automation unless explicitly requested and safety-reviewed.

## Browser analysis workflow

1. Open the vendor search page with a representative query.
2. Identify whether results are:
   - server-rendered HTML
   - embedded JSON (`__NEXT_DATA__`, JSON-LD, hydration state)
   - client-side API/XHR
   - blocked / login-only
3. Prefer stable structured sources over CSS selectors:
   - public JSON API
   - embedded Next.js data
   - JSON-LD
   - then CSS selectors as fallback
4. Extract normalized fields:
   - title
   - url
   - price integer if available
   - currency
   - location if available
   - source/vendor name
   - category
5. Add tests with saved minimal HTML/JSON fixtures when practical.
6. Run:

```bash
uv run pytest -q
uv run marketplace-agent find <workspace>
```

## Error handling

Do not silently return zero items when the DOM/API shape changed. Raise or record clear diagnostics:

- URL tested
- HTTP status
- page length
- selector/API that failed
- sample HTML/JSON path if captured

## Anti-bot/login safety

If the vendor requires login, captcha, or aggressive anti-bot bypass, stop and explain options. Do not evade protections without explicit user approval and a legitimate account/session.

## Output contract

Return normalized `Item` objects:

```python
Item(
    title="RTX 3090 Founders Edition",
    url="https://...",
    source="blocket",
    category="local_ai_gpu",
    price=8500,
    currency="SEK",
    metadata={"query": query},
)
```
