"""Generic message."""

from pydantic import BaseModel, Field


class Message(BaseModel):
    detail: str
    data: str | None = Field(default=None)
