from __future__ import annotations

from pydantic import BaseModel, Field


class UserConfig(BaseModel):
    country: str = "SE"
    currency: str = "SEK"
    language: str = "en"


class ScheduleConfig(BaseModel):
    cron: str | None = None
    timezone: str = "Europe/Stockholm"


class CategoryConfig(BaseModel):
    name: str
    queries: list[str] = Field(default_factory=list)


class VendorConfig(BaseModel):
    name: str
    type: str = "demo"
    enabled: bool = True


class MarketplaceConfig(BaseModel):
    name: str = "My Marketplace Agent"
    user: UserConfig = Field(default_factory=UserConfig)
    schedule: ScheduleConfig = Field(default_factory=ScheduleConfig)
    categories: list[CategoryConfig] = Field(default_factory=list)
    vendors: list[VendorConfig] = Field(default_factory=list)
