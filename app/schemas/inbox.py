from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


InboxCategory = Literal[
    "information",
    "task",
    "deadline",
    "promise",
    "schedule_change",
    "reminder",
    "decision",
    "other",
]

InboxStatus = Literal[
    "new",
    "pending",
    "completed",
    "dismissed",
]

Priority = Literal[
    "low",
    "medium",
    "high",
]


class InboxItemCreate(BaseModel):
    source: str = Field(
        description="Where the information came from, such as manual, email, calendar, or message."
    )

    content: str = Field(
        min_length=1,
        description="Original unprocessed information."
    )


class InboxAnalysis(BaseModel):
    """AI-generated understanding of incoming information."""

    summary: str

    category: InboxCategory

    priority: Priority

    requires_action: bool

    due_date: date | None = None

    people: list[str] = Field(default_factory=list)

    status: InboxStatus = "new"


class InboxItem(BaseModel):
    """Persisted Life Inbox item."""

    id: str

    source: str

    content: str

    summary: str

    category: InboxCategory

    priority: Priority

    requires_action: bool

    due_date: date | None = None

    people: list[str] = Field(default_factory=list)

    status: InboxStatus = "new"

    created_at: datetime