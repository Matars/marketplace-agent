---
name: marketplace-agent-vendor-repair
description: Add or repair a marketplace-agent vendor/provider using browser-harness discovery, stable API/HTML extraction, tests/validation, and safe anti-bot handling.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, vendor, scraper, browser-harness]
---

# marketplace-agent vendor repair

Use this skill when a marketplace/vendor is missing, broken, returning zero unexpectedly, or needs scraper updates.

## Default paths

- repo: user-provided path if given; otherwise locate the clone before assuming the current directory is the repo root
- workspace: `workspaces/default` relative to the repo
- browser-harness: `third_party/browser-harness/`

## First checks

If the vendor/site is missing, ask the user for it instead of requiring them to edit the copied prompt.

1. Locate the repo and workspace. Do not assume Hermes was started from the repo root.
2. Identify the vendor/site and representative search query.
3. Check whether the provider should be:
   - reusable built-in: `src/marketplace_agent/vendors/builtins/<name>.py`
   - user/workspace-specific: `<workspace>/vendors/<name>.py` once plugin loading exists
4. Read relevant repo skill/docs if present:
   - `hermes/skills/marketplace-agent-vendor-builder.md`
   - `hermes/skills/marketplace-agent-browser-harness.md`
   - `third_party/browser-harness/SKILL.md`
   - `third_party/browser-harness/install.md`

## Discovery workflow

1. Open the vendor search page with a representative query.
2. Determine whether results come from:
   - server-rendered HTML
   - embedded JSON (`__NEXT_DATA__`, JSON-LD, hydration state)
   - public/client XHR API
   - login/captcha/anti-bot flow
3. Prefer stable structured sources in this order:
   - public JSON/API endpoint
   - embedded Next.js/hydration data
   - JSON-LD
   - semantic HTML/CSS selectors as fallback
4. Extract normalized item fields:
   - title
   - url
   - price integer if available
   - currency
   - location
   - source/vendor
   - category/query metadata
5. Implement or repair the provider.
6. Add tests or small fixtures when practical.
7. Run targeted validation and then the workspace find workflow.

## Safety

If the vendor requires login, captcha, or aggressive anti-bot bypass, stop and explain options. Do not evade protections without explicit user approval and a legitimate account/session.

## Output expectations

Summarize:

- root cause of the provider issue
- files changed
- validation/tests run
- item count after repair
- remaining limitations
