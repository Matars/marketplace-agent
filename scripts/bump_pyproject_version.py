#!/usr/bin/env python3
"""Bump the patch version in pyproject.toml and stage it for commit.

Used by git-hooks/pre-commit. This project intentionally releases by
pyproject.toml version bumps only — no git tags.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
VERSION_RE = re.compile(r'(?m)^(version\s*=\s*")([0-9]+)\.([0-9]+)\.([0-9]+)(")\s*$')


def main() -> int:
    text = PYPROJECT.read_text()
    match = VERSION_RE.search(text)
    if not match:
        print("[version-bump] Could not find project version in pyproject.toml", file=sys.stderr)
        return 1

    major, minor, patch = map(int, match.group(2, 3, 4))
    old_version = f"{major}.{minor}.{patch}"
    new_version = f"{major}.{minor}.{patch + 1}"

    new_text = VERSION_RE.sub(rf"\g<1>{new_version}\g<5>", text, count=1)
    PYPROJECT.write_text(new_text)

    subprocess.run(["git", "add", str(PYPROJECT.relative_to(ROOT))], cwd=ROOT, check=True)
    print(f"[version-bump] pyproject.toml: {old_version} -> {new_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
