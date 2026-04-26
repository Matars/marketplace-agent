#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _to_int_price(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        s = value.strip().replace(" ", "")
        if not s:
            return None
        s = s.replace(",", ".")
        out = []
        for ch in s:
            if ch.isdigit() or ch in ".-":
                out.append(ch)
        if not out:
            return None
        try:
            return int(float("".join(out)))
        except ValueError:
            return None
    return None


def normalize_item(item: dict[str, Any], idx: int) -> dict[str, Any]:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    price = _to_int_price(item.get("price"))
    currency = item.get("currency") or metadata.get("currency") or "SEK"
    title = str(item.get("title") or "(untitled)")
    url = str(item.get("url") or "")
    source = str(item.get("source") or "unknown")
    category = str(item.get("category") or "uncategorized")

    location = metadata.get("location")
    condition = metadata.get("condition")

    return {
        "id": metadata.get("ad_id") or f"item-{idx}",
        "title": title,
        "url": url,
        "source": source,
        "category": category,
        "price": price,
        "currency": str(currency),
        "location": str(location) if location else "",
        "condition": str(condition) if condition else "",
        "query": str(metadata.get("query") or ""),
        "raw_metadata": metadata,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize marketplace-agent latest.json for frontend rendering.")
    parser.add_argument("--input", default="workspaces/default/output/latest.json", help="Path to latest.json")
    parser.add_argument("--output", default="frontend/data/items-normalized.json", help="Path to normalized output json")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    src = json.loads(in_path.read_text(encoding="utf-8"))
    raw_items = src.get("items", []) if isinstance(src, dict) else []
    if not isinstance(raw_items, list):
        raw_items = []

    items = [normalize_item(item if isinstance(item, dict) else {}, i) for i, item in enumerate(raw_items, start=1)]

    payload = {
        "workspace": src.get("workspace") if isinstance(src, dict) else None,
        "generated_at": src.get("generated_at") if isinstance(src, dict) else None,
        "normalized_at": datetime.now(timezone.utc).isoformat(),
        "count": len(items),
        "items": items,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out_path} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
