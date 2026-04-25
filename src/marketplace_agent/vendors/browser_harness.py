"""Browser-harness fallback for vendor plugins when HTTP scraping is blocked.

Requires browser-harness to be installed and Chrome to have remote debugging enabled.
The bundled submodule is at third_party/browser-harness/.
"""
from __future__ import annotations

import shutil
import subprocess


def fetch_html(url: str, timeout: int = 45) -> str | None:
    """Fetch page HTML via browser-harness if available.

    Returns None if browser-harness is not installed or Chrome is not accessible.
    """
    if not shutil.which("browser-harness"):
        return None

    script = f'''new_tab("{url}")
wait_for_load()
print(document.documentElement.outerHTML)'''

    try:
        result = subprocess.run(
            ["browser-harness", "-c", script],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass

    return None
