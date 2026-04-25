from __future__ import annotations

from pydantic import BaseModel, Field


class UserConfig(BaseModel):
    country: str = "SE"
    currency: str = "SEK"
    language: str = "en"


class ScheduleConfig(BaseModel):
    cron: str | None = None
    timezone: str = "Europe/Stockholm"


class MarketplaceConfig(BaseModel):
    name: str = "My Marketplace Agent"
    user: UserConfig = Field(default_factory=UserConfig)
    schedule: ScheduleConfig = Field(default_factory=ScheduleConfig)
