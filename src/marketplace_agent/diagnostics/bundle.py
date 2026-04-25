from __future__ import annotations

from pathlib import Path


class DiagnosticBundle:
    def __init__(self, root: Path) -> None:
        self.root = root

    def path_for(self, vendor: str) -> Path:
        path = self.root / vendor
        path.mkdir(parents=True, exist_ok=True)
        return path
