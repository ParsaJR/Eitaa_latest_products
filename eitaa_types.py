from typing import TypedDict

from attr import dataclass


@dataclass
class Message(TypedDict):
    """Represents a single eitaa message."""

    text: str | None
    image_url: str | None
    iso_time: str
    message_number: int
    views: int | None


@dataclass
class Channel:
    """Represents a single eitaa channel, And its latest messages"""

    id: str
    messages: list[Message]
