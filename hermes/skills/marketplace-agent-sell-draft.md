---
name: marketplace-agent-sell-draft
category: marketplace-agent
description: Create safe marketplace listing drafts from product photos/details. Produces JSON placeholder drafts and never auto-posts without explicit approval.
---

# marketplace-agent sell draft

Use this skill when a user wants to sell a product through marketplace-agent.

## Safety rule

Default mode is draft-only.

Do not auto-post listings, message buyers, accept offers, or submit forms unless the user explicitly requests it and confirms the exact action.

## Draft workflow

1. Collect product inputs:
   - image paths or uploaded photos
   - product type
   - brand/model if known
   - condition
   - included accessories
   - defects/damage
   - pickup/shipping preference
   - minimum acceptable price
2. Use vision if images are available.
3. Ask only the missing high-impact questions.
4. Research comparable listings if find vendors are available.
5. Produce a JSON draft.

## Draft JSON placeholder schema

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

## Tone for listing copy

Be accurate and not spammy. Mention visible defects. Avoid fake urgency. Prefer honest descriptions that reduce buyer back-and-forth.

## Verification

Before finalizing, confirm:

- draft says `requires_approval: true`
- no posting action was taken
- price estimate includes uncertainty/evidence when available
- user can edit title/description before posting
