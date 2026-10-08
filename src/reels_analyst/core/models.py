from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReelRecord(BaseModel):
    """Normalized source record accepted by the ingestion layer."""

    model_config = ConfigDict(str_strip_whitespace=True)

    reel_id: str = Field(min_length=1)
    published_at: datetime
    caption: str = ""
    format: str = "reel"
    duration_seconds: float = Field(gt=0, le=900)
    plays: int = Field(ge=0)
    reach: int = Field(ge=0)
    likes: int = Field(ge=0)
    comments: int = Field(ge=0)
    saves: int = Field(ge=0)
    shares: int = Field(ge=0)
    profile_visits: int = Field(ge=0)
    follows: int = Field(ge=0)
    avg_watch_seconds: float = Field(ge=0)
    completion_rate: float = Field(ge=0, le=1)
    audio_name: str = "Original audio"
    topic: str = "Uncategorized"
    cover_url: str | None = None

    @field_validator("completion_rate", mode="before")
    @classmethod
    def convert_percentage(cls, value: object) -> float:
        number = float(value)
        return number / 100 if number > 1 else number
