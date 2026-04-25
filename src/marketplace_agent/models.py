from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class VendorCapability(StrEnum):
    SEARCH = "search"
    PRICE_RESEARCH = "price_research"
    DRAFT_LISTING = "draft_listing"
    POST_LISTING = "post_listing"
    MESSAGE_BUYERS = "message_buyers"


class Item(BaseModel):
    title: str
    url: str | None = None
    source: str
    category: str | None = None
    price: int | None = None
    currency: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProductFacts(BaseModel):
    title: str
    condition: str | None = None
    brand: str | None = None
    model: str | None = None
    description: str | None = None
    image_paths: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ListingDraft(BaseModel):
    title: str
    description: str = ""
    price: int
    currency: str
    condition: str | None = None
    requires_approval: bool = True
    product: ProductFacts

    @classmethod
    def from_product(cls, product: ProductFacts, price: int, currency: str) -> "ListingDraft":
        return cls(
            title=product.title,
            description=product.description or "",
            price=price,
            currency=currency,
            condition=product.condition,
            product=product,
            requires_approval=True,
        )
