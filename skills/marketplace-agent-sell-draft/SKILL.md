---
name: marketplace-agent-sell-draft
description: Create a safe marketplace listing draft from product details/photos. Produces JSON drafts only and never posts/messages without explicit approval.
version: 0.0.2
metadata:
  hermes:
    tags: [marketplace-agent, selling, listing, draft, marketplace]
---

# marketplace-agent sell draft

Use this skill when the user wants to prepare a listing for something they want to sell.

## Safety rule

Default mode is draft-only.

Do not auto-post listings, message buyers, accept offers, submit forms, or bypass login/captcha unless the user explicitly requests it and confirms the exact action.

## Default paths

- repo: user-provided path if given; otherwise locate the clone before assuming the current directory is the repo root
- workspace: `workspaces/default` relative to the repo
- outputs: inside the gitignored workspace

## Draft workflow

1. Locate the repo and workspace. Do not assume Hermes was started from the repo root.
2. Collect product inputs:
   - item type
   - brand/model if known
   - condition
   - included accessories
   - defects/damage
   - pickup/shipping preference
   - minimum acceptable price or target price
   - image paths/photos if available
3. Use vision if images are available.
4. Ask only missing high-impact questions.
5. Research comparable listings if configured find vendors can help.
6. Produce a JSON draft inside the workspace.
7. Show the draft path and summarize what still needs user approval.

## Draft JSON shape

```json
{
  "status": "draft",
  "requires_approval": true,
  "product": {
    "title": "Sony WH-1000XM4",
    "brand": "Sony",
    "model": "WH-1000XM4",
    "condition": "used",
    "image_paths": []
  },
  "listing": {
    "title": "Sony WH-1000XM4 noise cancelling headphones",
    "description": "...",
    "price": 1200,
    "currency": "SEK",
    "category": "electronics",
    "tags": ["headphones", "sony", "bluetooth"]
  },
  "pricing": {
    "fast_sale": 1000,
    "fair": 1200,
    "optimistic": 1500,
    "evidence": []
  },
  "posting": {
    "auto_post": false,
    "target_vendors": []
  }
}
```

## Listing copy style

Be accurate and not spammy. Mention visible defects. Avoid fake urgency. Prefer honest descriptions that reduce buyer back-and-forth.

## Verification

Before finalizing, confirm:

- draft says `requires_approval: true`
- no posting action was taken
- price estimate includes uncertainty/evidence when available
- user can edit title/description before posting
