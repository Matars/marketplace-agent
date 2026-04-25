---
name: marketplace-agent-browser-harness
category: marketplace-agent
description: Use the bundled browser-use/browser-harness submodule as the preferred browser exploration layer for building marketplace-agent vendor scrapers.
---

# marketplace-agent browser-harness integration

Use this skill when Hermes needs to inspect a marketplace website or build/repair a vendor scraper.

## Purpose

browser-harness gives Hermes direct CDP control over a real or remote browser. For marketplace-agent, use it to discover stable search URLs, selectors, embedded JSON, network APIs, pagination, and anti-bot behavior.

## Full upstream repo included as submodule

browser-harness is not represented by a few copied snippets. The full upstream repo is included at:

```text
third_party/browser-harness/
```

Before using it, read:

- `third_party/browser-harness/SKILL.md`
- `third_party/browser-harness/install.md`
- `third_party/browser-harness/domain-skills/amazon/product-search.md`
- `third_party/browser-harness/domain-skills/ebay/scraping.md`

## Setup expectation

If `third_party/browser-harness` is empty or missing, initialize the repo submodules from the engine repo.

Use the browser-harness install instructions from its own `install.md`. Use `uv`, not pip directly.

## Usage pattern

Prefer browser-harness for vendor discovery, not as the production scraper runtime unless necessary.

1. Use browser-harness to inspect the site.
2. Extract stable URL/API/selector knowledge.
3. Implement that knowledge in marketplace-agent vendor Python code.
4. Run marketplace-agent tests and `marketplace-agent find <workspace>`.

This keeps production find runs deterministic and avoids requiring live browser control for every scrape unless a site truly needs it.

## Vendor priority

For default providers:

1. eBay: first try HTTP scraping using the bundled eBay browser-harness domain skill. It often works without Chrome but can trigger bot detection after repeated requests.
2. Amazon: use browser-harness discovery first because Amazon is heavily dynamic and region/session dependent.

## Safety

- Do not bypass CAPTCHA/login/anti-bot systems without explicit user approval.
- If the site blocks scraping, report it and propose an alternative.
- Respect marketplaces' terms and rate limits.
- Do not use browser automation to post listings or message users unless explicitly approved.
