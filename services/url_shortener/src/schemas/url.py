from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

import shortuuid

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class UrlVisibility(StrEnum):
    public = auto()
    private = auto()


class UserIdMixIn(BaseModel):
    user_id: UUID | None = Field(None, description="User ID")


class VisibilityMixIn(BaseModel):
    visibility: UrlVisibility


class ShortUrlIdMixIn(BaseModel):
    short_id: str = Field(..., description="Short URL ID")


class OriginalUrlMixIn(BaseModel):
    original_url: HttpUrl = Field(..., pattern="^https?://", description="Original URL to shorten")


class UrlCreate(VisibilityMixIn, OriginalUrlMixIn, UserIdMixIn):
    short_id: str | None = Field(None, max_length=8, description="Generated short URL ID")

    @field_validator("short_id", mode="before")
    @classmethod
    def generate_short_id(cls, value: str | None) -> str:
        if not value:
            return shortuuid.ShortUUID().random(length=8)
        return value


class UrlResponse(VisibilityMixIn, ShortUrlIdMixIn, OriginalUrlMixIn):
    short_url: str = Field(..., description="Shortened URL")

    model_config = ConfigDict(from_attributes=True)


class UrlStatsResponse(BaseModel):
    total_clicks: int
    access_time: list[datetime]
    client_info: list[str] | None

    model_config = ConfigDict(from_attributes=True)


class URLOriginalGet(ShortUrlIdMixIn, UserIdMixIn): ...


class URLOriginalResponse(OriginalUrlMixIn): ...


class UrlStatsParams(BaseModel):
    full_info: bool = False
    max_results: int = 10
    offset: int = 0


class UrlStatsReq(UrlStatsParams, ShortUrlIdMixIn): ...


class UrlVisibilityUpdate(ShortUrlIdMixIn, VisibilityMixIn): ...
