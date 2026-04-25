from __future__ import annotations

from collections.abc import Iterable

from marketplace_agent.models import VendorCapability
from marketplace_agent.vendors.base import Vendor


class VendorRegistry:
    def __init__(self) -> None:
        self._vendors: dict[str, type[Vendor]] = {}

    def register(self, vendor_cls: type[Vendor]) -> None:
        name = getattr(vendor_cls, "name", None)
        if not name:
            raise ValueError("vendor class must define a non-empty name")
        self._vendors[name] = vendor_cls

    def names(self) -> list[str]:
        return sorted(self._vendors)

    def get(self, name: str) -> type[Vendor]:
        try:
            return self._vendors[name]
        except KeyError as exc:
            raise KeyError(f"unknown vendor: {name}") from exc

    def for_capability(self, capability: VendorCapability) -> list[type[Vendor]]:
        return [
            vendor_cls
            for vendor_cls in self._vendors.values()
            if capability in getattr(vendor_cls, "capabilities", frozenset())
        ]

    def register_many(self, vendors: Iterable[type[Vendor]]) -> None:
        for vendor in vendors:
            self.register(vendor)
